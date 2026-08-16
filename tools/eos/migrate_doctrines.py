"""Apply the reviewed 25-pack Doctrine migration for T-0026.

The generator reads the frozen pre-migration tree at ``BASELINE_COMMIT``.
It refuses inventory drift, so re-running it after the migration reaches the
same bytes rather than trying to parse its own output.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Sequence

from tools.eos.frontmatter import parse as parse_frontmatter
from tools.eos.knowledge_migration import (
    BASELINE_COMMIT,
    EXPECTED_INVENTORY_SHA256,
    SourceBlock,
    inventory_sha256,
    read_baseline,
)


INVENTORY_PATH = "org/migration/DOCTRINE_SOURCE_INVENTORY.json"
LEDGER_PATH = "org/migration/DOCTRINE_MIGRATION.json"
ALIASES_PATH = "registry/identifier-aliases.json"
NAMING_BASELINE_PATH = "org/migration/NAMING_BASELINE.json"
GENERATOR_MARKER = "generated_by: tools.eos.migrate_doctrines"
CHALLENGE_TRIGGER = "operator_requests_doctrine_review"

PACK_CODES = {
    "agentic-development": "AGENT",
    "agentic-swarm": "SWARM",
    "ai-ml-llm": "AIML",
    "api-integration": "API",
    "architecture": "ARCH",
    "business-logic-modelling": "BLM",
    "business-model-pricing": "BMP",
    "coding": "COD",
    "data-analytics": "DATA",
    "data-engineering": "DATAENG",
    "delivery-testing": "DEL",
    "devops-reliability": "DEVOPS",
    "docs-dx": "DOCS",
    "identity-access": "IDENT",
    "legal-licensing": "LEGAL",
    "marketing-growth": "MKTG",
    "native-client": "NAT",
    "pattertech-house": "HOUSE",
    "product-discovery": "DISC",
    "research-knowledge": "RESEARCH",
    "security-privacy": "SEC",
    "supply-chain-integrity": "SUPPLY",
    "support-operations": "SUPPORT",
    "ui-ux": "UIUX",
    "writing-content": "WRIT",
}

PACK_DEPENDENCIES = {
    "agentic-development": ["ai-ml-llm", "security-privacy"],
    "agentic-swarm": ["agentic-development", "delivery-testing"],
    "ai-ml-llm": ["data-analytics", "security-privacy"],
    "api-integration": ["architecture", "security-privacy"],
    "architecture": ["business-logic-modelling"],
    "business-logic-modelling": ["product-discovery"],
    "business-model-pricing": ["product-discovery", "legal-licensing"],
    "coding": ["architecture"],
    "data-analytics": ["product-discovery"],
    "data-engineering": ["architecture", "security-privacy"],
    "delivery-testing": ["coding"],
    "devops-reliability": ["delivery-testing", "security-privacy"],
    "docs-dx": ["writing-content", "coding"],
    "identity-access": ["architecture", "security-privacy"],
    "legal-licensing": ["security-privacy"],
    "marketing-growth": [
        "product-discovery", "writing-content", "legal-licensing",
    ],
    "native-client": ["ui-ux", "architecture"],
    "pattertech-house": ["ui-ux", "writing-content"],
    "product-discovery": [],
    "research-knowledge": [],
    "security-privacy": [],
    "supply-chain-integrity": ["security-privacy", "devops-reliability"],
    "support-operations": ["product-discovery", "devops-reliability"],
    "ui-ux": ["product-discovery"],
    "writing-content": ["product-discovery"],
}

# Evidence-led records admitted after the frozen 501-row migration. They stay
# outside the migration ledger, but PACK.md remains the local decision map and
# therefore links them deterministically on every replay.
POST_MIGRATION_ADMISSIONS = {
    "ai-ml-llm": [
        ("WG-AIML-001", "wargames/WG-AIML-001-model-hosting.md", "Wargame"),
    ],
    "architecture": [
        ("WG-ARCH-009", "wargames/WG-ARCH-009-messaging-and-flow.md", "Wargame"),
        ("WG-ARCH-010", "wargames/WG-ARCH-010-storage-engine-selection.md", "Wargame"),
        ("WG-ARCH-011", "wargames/WG-ARCH-011-locality-and-consistency.md", "Wargame"),
        ("WG-ARCH-012", "wargames/WG-ARCH-012-capability-ownership.md", "Wargame"),
    ],
    "data-analytics": [
        ("DOC-DATA-020", "doctrines/DOC-DATA-020-representative-measurement-before-material-compute-claims.md", "default Doctrine"),
        ("DOC-DATA-021", "doctrines/DOC-DATA-021-measured-data-compute-promotion-ladder.md", "default Doctrine"),
        ("WG-DATA-001", "wargames/WG-DATA-001-analytical-engine-selection.md", "Wargame"),
        ("WG-DATA-002", "wargames/WG-DATA-002-representation-boundary.md", "Wargame"),
        ("WG-DATA-003", "wargames/WG-DATA-003-acceleration-ladder.md", "Wargame"),
    ],
    "delivery-testing": [
        ("WG-DEL-008", "wargames/WG-DEL-008-incident-hotfix.md", "Wargame"),
    ],
    "devops-reliability": [
        ("WG-DEVOPS-006", "wargames/WG-DEVOPS-006-honest-degradation.md", "Wargame"),
        ("WG-DEVOPS-007", "wargames/WG-DEVOPS-007-observability-and-privacy.md", "Wargame"),
    ],
    "ui-ux": [
        ("DOC-UIUX-023", "doctrines/DOC-UIUX-023-native-semantics-before-custom-interaction.md", "default Doctrine"),
        ("WG-UIUX-001", "wargames/WG-UIUX-001-web-delivery-shape.md", "Wargame"),
        ("WG-UIUX-002", "wargames/WG-UIUX-002-semantic-or-custom-interaction.md", "Wargame"),
    ],
}


PACK_PROSE_REPLACEMENTS = {
    "identity-access": (
        (
            "Fifteen sources, all fetched on 2026-08-15. This pack was written before\n"
            "the fragment import ran, so there are no evidence ids to cite yet and\n"
            "the front matter says `pending-fragment-import` rather than inventing\n"
            "them. Citations in the body name the source instead, which stays true\n"
            "after the import assigns ids.",
            "Fifteen sources, all fetched on 2026-08-15. The fragment import\n"
            "assigned `EV-0517` through `EV-0531`, and front matter cites those\n"
            "canonical rows. Citations in the body retain readable source names\n"
            "beside the stable evidence identities.",
        ),
    ),
}

FAMILY_TO_LEDGER = {
    "requirements": "requirement",
    "defaults": "default",
    "preferences": "preference",
    "voice-scope": "voice-scope",
}

AUTHORITY_DEFAULT_OVERRIDES = {
    # Reconciled mixed-authority requirement organs.
    "packs/docs-dx/PACK.md:requirements:001",
    "packs/docs-dx/PACK.md:requirements:002",
    "packs/docs-dx/PACK.md:requirements:003",
    "packs/docs-dx/PACK.md:requirements:005",
    "packs/docs-dx/PACK.md:requirements:006",
    "packs/legal-licensing/PACK.md:requirements:001",
    "packs/legal-licensing/PACK.md:requirements:003",
    "packs/legal-licensing/PACK.md:requirements:006",
    "packs/native-client/PACK.md:requirements:001",
    "packs/native-client/PACK.md:requirements:002",
    "packs/native-client/PACK.md:requirements:003",
    "packs/native-client/PACK.md:requirements:007",
    "packs/identity-access/PACK.md:requirements:002",
    "packs/identity-access/PACK.md:requirements:004",
    "packs/research-knowledge/PACK.md:requirements:006",
}

API_WEBHOOK = "packs/api-integration/PACK.md:requirements:002"
ARCH_WEBHOOK = "packs/architecture/PACK.md:requirements:003"
CODING_ORACLE = "packs/coding/PACK.md:requirements:001"
DELIVERY_ORACLE = "packs/delivery-testing/PACK.md:requirements:001"
ARCH_GENERATED = "packs/architecture/PACK.md:requirements:002"
SECURITY_APPROVAL = "packs/security-privacy/PACK.md:requirements:006"
UI_OVERLAY = "packs/ui-ux/PACK.md:requirements:004"
IDENTITY_CREDENTIAL = "packs/identity-access/PACK.md:requirements:003"
NATIVE_PREFERENCE = "packs/native-client/PACK.md:preferences:001"
WRITING_EOS_VOICE = "packs/writing-content/PACK.md:voice-scope:001"
WRITING_VENTURE_VOICE = "packs/writing-content/PACK.md:voice-scope:002"
WRITING_BRAND_VOICE = "packs/writing-content/PACK.md:voice-scope:003"
WRITING_B8 = "packs/writing-content/PACK.md:defaults:005"
WRITING_VENTURE_DEFAULT = "packs/writing-content/PACK.md:defaults:013"


class DoctrineMigrationError(RuntimeError):
    """The reviewed migration cannot be reproduced safely."""


@dataclass(frozen=True)
class PartSpec:
    statement: str
    authority: str | None = None
    basis: str | None = None
    evidence_grade: str | None = None
    scope: str | None = None
    applies_when: tuple[str, ...] = ()


@dataclass
class PackSource:
    slug: str
    path: str
    text: str
    metadata: dict
    blocks: list[SourceBlock]


@dataclass
class DoctrineDefinition:
    identifier: str
    owner_pack: str
    statement: str
    authority: str
    basis: str
    evidence_grade: str
    scope: str
    applies_when: list[str]
    sources: list[str]
    review: str
    verification_refs: list[str]
    accepted_adr: str | None = None
    contributors: list[SourceBlock] = field(default_factory=list)
    filename: str = ""

    @property
    def path(self) -> str:
        return f"packs/{self.owner_pack}/doctrines/{self.filename}"


SPECIAL_PARTS = {
    API_WEBHOOK: (
        PartSpec(
            "Webhook receivers authenticate the exact raw request before "
            "parsing, reject stale deliveries, and process accepted deliveries "
            "idempotently against a pinned payload version.",
            authority="binding",
            basis="standard",
            applies_when=("receives_webhooks",),
        ),
    ),
    CODING_ORACLE: (
        PartSpec(
            "The oracle that judges a change is authored independently of the "
            "implementation under test.",
            authority="binding",
            basis="empirical-evidence",
            evidence_grade="controlled",
            applies_when=("edits_source",),
        ),
        PartSpec(
            "A gate oracle is observed failing before its green result counts "
            "as acceptance evidence.",
            authority="binding",
            basis="empirical-evidence",
            evidence_grade="observational",
            applies_when=("decides_merge",),
        ),
    ),
    ARCH_GENERATED: (
        PartSpec(
            "Generated contract artefacts are produced deterministically from "
            "a committed source and CI fails when they drift.",
            authority="binding",
            basis="standard",
            applies_when=("has_cross_language_contract",),
        ),
        PartSpec(
            "A typed client verifies that a response succeeded before treating "
            "the response body as data.",
            authority="binding",
            basis="standard",
            applies_when=("consumes_external_api",),
        ),
    ),
    SECURITY_APPROVAL: (
        PartSpec(
            "Consequential external actions wait for a harness-recorded operator "
            "approval immediately before execution.",
            authority="binding",
            basis="decision",
            applies_when=("has_external_egress",),
        ),
        PartSpec(
            "An MCP or tool proxy never passes a bearer token through to another "
            "system.",
            authority="binding",
            basis="decision",
            applies_when=("runs_agents",),
        ),
        PartSpec(
            "A session identifier is never accepted as authentication.",
            authority="binding",
            basis="decision",
            applies_when=("runs_agents",),
        ),
        PartSpec(
            "Proxying an external action through a client requires consent for "
            "that client.",
            authority="binding",
            basis="decision",
            applies_when=("has_external_egress",),
        ),
        PartSpec(
            "A local installation shows the exact command before it can run.",
            authority="binding",
            basis="decision",
            applies_when=("runs_agents",),
        ),
    ),
    UI_OVERLAY: (
        PartSpec(
            "Do not add a script that claims to repair accessibility at runtime.",
            authority="default",
            basis="decision",
            applies_when=("has_user_interface",),
        ),
        PartSpec(
            "Do not infer assistive-technology use without the person's consent.",
            authority="binding",
            basis="law",
            applies_when=("handles_personal_data",),
        ),
    ),
    IDENTITY_CREDENTIAL: (
        PartSpec(
            "Validate a token's signature, issuer, audience and expiry on every "
            "request, using an algorithm fixed by the verifier.",
            authority="binding", basis="standard",
            applies_when=("authenticates_people",),
        ),
        PartSpec(
            "An identity token is never accepted as an access token.",
            authority="binding", basis="standard",
            applies_when=("authenticates_people",),
        ),
        PartSpec(
            "A session identifier is never forwarded as a bearer credential.",
            authority="binding", basis="standard",
            applies_when=("authenticates_people",),
        ),
        PartSpec(
            "Session identifiers come from a cryptographic generator.",
            authority="binding", basis="standard",
            applies_when=("authenticates_people",),
        ),
        PartSpec(
            "Reissue the session identifier whenever privilege changes.",
            authority="binding", basis="standard",
            applies_when=("authenticates_people",),
        ),
        PartSpec(
            "Invalidate the server-side session at logout.",
            authority="binding", basis="standard",
            applies_when=("authenticates_people",),
        ),
    ),
    NATIVE_PREFERENCE: (
        PartSpec(
            "Framework family within the selected client architecture is a "
            "venture preference.",
            authority="preference", basis="decision",
            applies_when=("ships_a_binary",), scope="venture",
        ),
        PartSpec(
            "Language for a shared client core is a venture preference.",
            authority="preference", basis="decision",
            applies_when=("ships_a_binary",), scope="venture",
        ),
        PartSpec(
            "The CRDT or synchronisation vendor is a preference after the "
            "conflict policy is fixed.",
            authority="preference", basis="decision",
            applies_when=("has_local_write_store",), scope="venture",
        ),
        PartSpec(
            "Document versus relational local storage is a venture preference.",
            authority="preference", basis="decision",
            applies_when=("has_local_write_store",), scope="venture",
        ),
        PartSpec(
            "Release cadence beyond store constraints is a venture preference.",
            authority="preference", basis="decision",
            applies_when=("distributes_via_app_store",), scope="venture",
        ),
        PartSpec(
            "Whether to ship a companion watch or television surface is a "
            "venture preference.",
            authority="preference", basis="decision",
            applies_when=("ships_a_binary",), scope="venture",
        ),
    ),
}

NO_NEW_DEFINITION = {
    ARCH_WEBHOOK,
    DELIVERY_ORACLE,
    WRITING_EOS_VOICE,
    WRITING_VENTURE_VOICE,
    WRITING_BRAND_VOICE,
}


def _git(root: Path, *args: str) -> str:
    try:
        process = subprocess.run(
            ["git", "-C", str(root), *args], capture_output=True, text=True,
            encoding="utf-8", errors="strict", timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise DoctrineMigrationError(f"git {' '.join(args)} could not run") from exc
    if process.returncode:
        raise DoctrineMigrationError(
            f"git {' '.join(args)} failed: {process.stderr.strip()}"
        )
    return process.stdout.replace("\r\n", "\n").replace("\r", "\n")


def _normalise(value: str) -> str:
    return " ".join(value.replace("\n", " ").split())


def _pack_slug(path: str) -> str:
    return PurePosixPath(path).parts[1]


def _source_title_and_reason(block: SourceBlock) -> tuple[str, str]:
    text = block.text.strip()
    if text.startswith("|"):
        cells = [cell.strip() for cell in text.strip("|").split("|")]
        title = cells[0] if cells else "Recorded default"
        reason = "\n\n".join(cell for cell in cells[1:] if cell)
        return _statement(title), reason or "No separate rationale was recorded."

    candidate = text
    if re.match(r"^\d+\.\s+", candidate):
        candidate = re.sub(r"^\d+\.\s+", "", candidate, count=1)
    elif candidate.startswith("- "):
        candidate = candidate[2:]

    bold = re.match(r"(?s)^\*\*(.+?)\*\*", candidate)
    if bold:
        title = re.sub(r"^(?:B\d+|D\d+|BR-\d+|H\d+)\.\s*", "", bold.group(1))
        reason = candidate[bold.end():].lstrip(" ,:;-\n")
        return _statement(title), reason or "No separate rationale was recorded."

    first = re.split(r"(?<=[.!?])\s+", _normalise(candidate), maxsplit=1)
    title = first[0]
    reason = first[1] if len(first) > 1 else "No separate rationale was recorded."
    return _statement(title), reason


def _statement(value: str) -> str:
    value = _normalise(value)
    value = value.replace("`", "").replace("**", "")
    value = re.sub(r"\s+", " ", value).strip(" -,:;")
    if not value:
        value = "Review the recorded source proposition"
    if value[-1] not in ".!?":
        value += "."
    return value


def _slug(value: str, maximum: int) -> str:
    value = value.lower().replace("'", "")
    value = re.sub(r"[^a-z0-9]+", "-", value).strip("-")
    if len(value) <= maximum:
        return value or "doctrine"
    prefix = value[:maximum + 1]
    if "-" in prefix:
        prefix = prefix.rsplit("-", 1)[0]
    else:
        prefix = value[:maximum]
    return prefix.rstrip("-") or "doctrine"


def _ev_ids(text: str) -> list[str]:
    return sorted(set(re.findall(r"\bEV-\d{4}\b", text)))


def _explicit_basis(text: str) -> str | None:
    pattern = (
        r"(?i)(?:\*\*)?basis(?:\*\*)?(?::|\s+)\s*"
        r"(empirical-evidence|local-observation|decision|law|standard)\b"
    )
    matches = re.findall(pattern, text)
    return matches[-1].lower() if matches else None


def _authority(block: SourceBlock, inventory_row: dict) -> str:
    if block.source_key in AUTHORITY_DEFAULT_OVERRIDES:
        return "default"
    if block.path == "packs/pattertech-house/PACK.md" and block.family == "requirements":
        return "preference"
    if block.path.startswith("packs/security-privacy/") and block.family == "requirements":
        return "binding"
    if block.path.startswith("packs/devops-reliability/") and block.family == "requirements":
        return "binding"
    return str(inventory_row["preliminary_authority"])


def _scope(block: SourceBlock) -> str:
    if block.source_key == WRITING_B8:
        return "eos-internal"
    if block.source_key == WRITING_VENTURE_DEFAULT:
        return "venture"
    return "estate"


def _applies_when(block: SourceBlock, pack: PackSource) -> list[str]:
    declared = list(pack.metadata.get("applies_when") or [])
    if isinstance(pack.metadata.get("applies_when"), str):
        declared = [str(pack.metadata["applies_when"])]
    mentioned = [name for name in declared if re.search(rf"\b{re.escape(name)}\b", block.text)]
    return mentioned[:1] or declared[:1] or ["always"]


def _basis_and_grade(
    block: SourceBlock, pack: PackSource, authority: str,
) -> tuple[str, str, str, str | None]:
    basis = _explicit_basis(block.text) or str(pack.metadata.get("basis") or "decision")
    grade = str(pack.metadata.get("evidence_grade") or "asserted")
    accepted_adr = None

    if block.source_key == "packs/architecture/PACK.md:requirements:001":
        basis, grade = "empirical-evidence", "observational"
    elif block.source_key == ARCH_GENERATED:
        basis = "standard"
    elif block.source_key in {API_WEBHOOK, ARCH_WEBHOOK}:
        basis = "standard"

    if authority == "binding" and basis == "decision":
        exempt = block.path.startswith((
            "packs/security-privacy/", "packs/devops-reliability/",
        ))
        adrs = re.findall(r"\bADR-\d{4}\b", block.text)
        if exempt:
            accepted_adr = "ADR-0012"
        elif adrs:
            accepted_adr = adrs[-1]
    return authority, basis, grade, accepted_adr


def _frontmatter_value(value) -> str:
    if isinstance(value, list):
        return "[" + ", ".join(str(item) for item in value) + "]"
    return str(value)


def _load_sources(root: Path) -> tuple[dict[str, PackSource], dict[str, dict]]:
    inventory = json.loads((root / INVENTORY_PATH).read_text(encoding="utf-8"))
    if inventory.get("baseline_commit") != BASELINE_COMMIT:
        raise DoctrineMigrationError("Doctrine source inventory commit drifted")
    if inventory.get("inventory_sha256") != EXPECTED_INVENTORY_SHA256:
        raise DoctrineMigrationError("Doctrine source inventory hash drifted")
    rows = inventory.get("rows") or []
    if len(rows) != 501:
        raise DoctrineMigrationError(f"Doctrine source inventory has {len(rows)} rows")
    inventory_rows = {row["source_key"]: row for row in rows}
    if len(inventory_rows) != 501:
        raise DoctrineMigrationError("Doctrine source inventory repeats a source_key")

    blocks = read_baseline(root)
    if len(blocks) != 501 or inventory_sha256(blocks) != EXPECTED_INVENTORY_SHA256:
        raise DoctrineMigrationError("Pinned Doctrine source reconstruction drifted")
    block_rows = {block.source_key: block for block in blocks}
    if set(block_rows) != set(inventory_rows):
        raise DoctrineMigrationError("Inventory and pinned source keys differ")
    for key, block in block_rows.items():
        row = inventory_rows[key]
        expected = (
            row["path"], row["family"], row["ordinal"], row["start"],
            row["end"], row["block_sha256"],
        )
        actual = (
            block.path, block.family, block.ordinal, block.start, block.end,
            block.block_sha256,
        )
        if actual != expected:
            raise DoctrineMigrationError(f"Frozen source row drifted: {key}")

    grouped: dict[str, list[SourceBlock]] = defaultdict(list)
    for block in blocks:
        grouped[block.path].append(block)
    packs: dict[str, PackSource] = {}
    for path in sorted(grouped):
        text = _git(root, "show", f"{BASELINE_COMMIT}:{path}")
        parsed = parse_frontmatter(text)
        if not parsed.present or parsed.errors:
            raise DoctrineMigrationError(f"Cannot parse pinned pack metadata: {path}")
        slug = _pack_slug(path)
        packs[slug] = PackSource(
            slug=slug, path=path, text=text, metadata=parsed.data,
            blocks=sorted(grouped[path], key=lambda row: (row.start, row.family)),
        )
    if set(packs) != set(PACK_CODES):
        raise DoctrineMigrationError("Pack-code map does not cover the frozen estate")
    if set(PACK_DEPENDENCIES) != set(PACK_CODES):
        raise DoctrineMigrationError("Pack dependency map does not cover the frozen estate")
    return packs, inventory_rows


def _make_definitions(
    packs: dict[str, PackSource], inventory_rows: dict[str, dict],
) -> tuple[dict[str, DoctrineDefinition], dict[str, list[str]]]:
    definitions: dict[str, DoctrineDefinition] = {}
    row_targets: dict[str, list[str]] = {}
    counters: dict[str, int] = defaultdict(int)

    for pack_name in sorted(packs):
        pack = packs[pack_name]
        for block in pack.blocks:
            if block.source_key in NO_NEW_DEFINITION:
                row_targets[block.source_key] = []
                continue
            title, _ = _source_title_and_reason(block)
            parts = SPECIAL_PARTS.get(block.source_key, (PartSpec(title),))
            targets: list[str] = []
            for part in parts:
                counters[pack_name] += 1
                identifier = (
                    f"DOC-{PACK_CODES[pack_name]}-{counters[pack_name]:03d}"
                )
                authority = part.authority or _authority(
                    block, inventory_rows[block.source_key],
                )
                authority, basis, grade, accepted_adr = _basis_and_grade(
                    block, pack, authority,
                )
                if part.basis:
                    basis = part.basis
                if part.evidence_grade:
                    grade = part.evidence_grade
                if authority == "binding" and basis == "decision":
                    if block.path.startswith((
                        "packs/security-privacy/",
                        "packs/devops-reliability/",
                    )):
                        accepted_adr = "ADR-0012"
                    elif not accepted_adr:
                        authority = "default"
                statement = _statement(part.statement)
                sources = _ev_ids(block.text)
                if not sources:
                    inherited = pack.metadata.get("sources") or []
                    sources = list(inherited) if isinstance(inherited, list) else [str(inherited)]
                definition = DoctrineDefinition(
                    identifier=identifier,
                    owner_pack=pack_name,
                    statement=statement,
                    authority=authority,
                    basis=basis,
                    evidence_grade=grade,
                    scope=part.scope or _scope(block),
                    applies_when=list(part.applies_when) or _applies_when(block, pack),
                    sources=sorted(set(sources)),
                    review=str(pack.metadata.get("review") or "2027-08"),
                    verification_refs=[f"packs/{pack_name}/CHECKS.md"],
                    accepted_adr=accepted_adr,
                    contributors=[block],
                )
                slug_limit = 72 - len(identifier) - 1
                definition.filename = (
                    f"{identifier}-{_slug(definition.statement, slug_limit)}.md"
                )
                definitions[identifier] = definition
                targets.append(identifier)
            row_targets[block.source_key] = targets

    def merge(source_key: str, target: str) -> None:
        block = next(
            block for pack in packs.values() for block in pack.blocks
            if block.source_key == source_key
        )
        row_targets[source_key] = [target]
        definitions[target].contributors.append(block)
        extra = _ev_ids(block.text)
        if not extra:
            inherited = packs[_pack_slug(block.path)].metadata.get("sources") or []
            extra = list(inherited) if isinstance(inherited, list) else [str(inherited)]
        definitions[target].sources = sorted(set(definitions[target].sources + extra))

    merge(ARCH_WEBHOOK, row_targets[API_WEBHOOK][0])
    merge(DELIVERY_ORACLE, row_targets[CODING_ORACLE][0])
    merge(WRITING_EOS_VOICE, row_targets[WRITING_B8][0])
    merge(WRITING_VENTURE_VOICE, row_targets[WRITING_VENTURE_DEFAULT][0])
    row_targets[WRITING_BRAND_VOICE] = []

    normalised: dict[str, str] = {}
    for definition in definitions.values():
        key = _normalise(definition.statement).lower()
        if key in normalised:
            raise DoctrineMigrationError(
                f"Doctrine statement {definition.identifier} duplicates "
                f"{normalised[key]}"
            )
        normalised[key] = definition.identifier
    if set(row_targets) != {
        block.source_key for pack in packs.values() for block in pack.blocks
    }:
        raise DoctrineMigrationError("Not every frozen source row has targets")
    return definitions, row_targets


def _focused_reason(block: SourceBlock, statement: str) -> str:
    _, reason = _source_title_and_reason(block)
    segments = [
        _normalise(part)
        for part in re.split(r"(?<=[.!?])\s+|;\s+", reason)
        if _normalise(part)
    ]
    if len(segments) <= 2:
        return " ".join(segments) or "No separate rationale was recorded."
    stop = {
        "the", "a", "an", "and", "or", "to", "of", "in", "is", "as",
        "at", "for", "from", "with", "that", "this", "it", "be", "before",
    }
    wanted = {
        word for word in re.findall(r"[a-z0-9]+", statement.lower())
        if len(word) > 2 and word not in stop
    }

    def score(segment: str) -> tuple[int, int]:
        words = set(re.findall(r"[a-z0-9]+", segment.lower()))
        overlap = len(wanted & words)
        rationale = 2 if re.search(
            r"(?i)\b(prevents?|basis|scope|reason|evidence|EV-\d{4})\b",
            segment,
        ) else 0
        return overlap * 3 + rationale, -segments.index(segment)

    selected = sorted(segments, key=score, reverse=True)[:3]
    selected_set = set(selected)
    return " ".join(segment for segment in segments if segment in selected_set)


def _render_doctrine(
    definition: DoctrineDefinition, row_targets: dict[str, list[str]],
) -> str:
    lines = [
        "---",
        f"summary: {definition.statement}",
        "type: doctrine",
        "tags: [eos]",
        f"id: {definition.identifier}",
        f"statement: {definition.statement}",
        "kind: doctrine",
        f"authority: {definition.authority}",
        f"basis: {definition.basis}",
        f"evidence_grade: {definition.evidence_grade}",
        f"scope: {definition.scope}",
        f"applies_when: {_frontmatter_value(definition.applies_when)}",
        f"challenge_triggers: [{CHALLENGE_TRIGGER}]",
        f"sources: {_frontmatter_value(definition.sources)}",
        f"review: {definition.review}",
        "lifecycle: active",
        f"verification_refs: {_frontmatter_value(definition.verification_refs)}",
        "migration_sources: " + _frontmatter_value([
            block.source_key for block in definition.contributors
        ]),
        GENERATOR_MARKER,
    ]
    anchors = sorted({
        block.legacy_anchor for block in definition.contributors
        if block.legacy_anchor
    })
    if anchors:
        lines.append(f"legacy_anchors: {_frontmatter_value(anchors)}")
    if definition.accepted_adr:
        lines.append(f"accepted_adr: {definition.accepted_adr}")
    lines.extend([
        "---", "", f"# {definition.identifier}", "",
        "The `statement` field is the canonical standing proposition.", "",
        "## Reasoning and limits", "",
    ])
    for block in definition.contributors:
        if len(definition.contributors) > 1:
            lines.extend([f"### `{block.source_key}`", ""])
        _, full_reason = _source_title_and_reason(block)
        if len(row_targets[block.source_key]) > 1:
            reason = _focused_reason(block, definition.statement)
        else:
            reason = full_reason
        lines.extend([reason.strip(), ""])
    lines.extend([
        "## Migration provenance", "",
        "This Doctrine was reviewed from the following frozen source blocks:", "",
    ])
    for block in definition.contributors:
        lines.append(
            f"- `{block.source_key}`, lines {block.start}-{block.end}, "
            f"SHA-256 `{block.block_sha256}`."
        )
    return "\n".join(lines).rstrip() + "\n"


def _ledger_reason(
    block: SourceBlock, disposition: str, targets: list[str],
    definitions: dict[str, DoctrineDefinition],
) -> str:
    if block.source_key == WRITING_BRAND_VOICE:
        return (
            "The brand scope is intentionally empty until a venture adopts a "
            "named brand voice, so explanatory pack prose remains and no active "
            "Doctrine is manufactured."
        )
    if block.source_key == ARCH_WEBHOOK:
        return (
            f"Merged into {targets[0]} under api-integration because both rows "
            "govern the same raw-byte webhook authentication protocol; the API "
            "pack owns its mechanics and scope."
        )
    if block.source_key == DELIVERY_ORACLE:
        return (
            f"Merged into {targets[0]} because the delivery requirement and the "
            "coding rule state the same independent-oracle proposition with the "
            "same implementation-change scope."
        )
    if block.source_key == WRITING_EOS_VOICE:
        return (
            f"Merged into {targets[0]}, the existing EOS-internal B8 voice "
            "default, rather than retaining a second normative copy in the "
            "voice-scope table."
        )
    if block.source_key == WRITING_VENTURE_VOICE:
        return (
            f"Merged into {targets[0]}, the existing venture-documentation "
            "default, because the voice-scope row adds scope rather than a new "
            "prescription."
        )
    if len(targets) > 1:
        return (
            f"Split {block.source_key} into {len(targets)} independently "
            "challengeable propositions ({', '.join(targets)}) so a departure "
            "from one clause does not silently waive the others."
        )
    definition = definitions[targets[0]]
    note = ""
    if block.source_key == "packs/research-knowledge/PACK.md:requirements:002":
        note = (
            " It remains separate from security B1 because this rule governs a "
            "source's claim about authority, not only embedded instructions."
        )
    elif block.source_key in {
        "packs/docs-dx/PACK.md:requirements:004",
        "packs/ui-ux/PACK.md:requirements:005",
    }:
        note = (
            " It remains scoped to this artefact class rather than merging into "
            "the architecture contract rule, whose applicability is different."
        )
    elif block.source_key == "packs/agentic-swarm/PACK.md:requirements:009":
        note = (
            " It remains distinct from agentic-development B1 because it also "
            "governs worktree isolation and integrator merge order."
        )
    return (
        f"Created {definition.identifier} as the canonical "
        f"{definition.authority} proposition for {block.source_key}; its "
        f"applicability is {', '.join(definition.applies_when)}.{note}"
    )


def _build_ledger(
    packs: dict[str, PackSource], inventory_rows: dict[str, dict],
    definitions: dict[str, DoctrineDefinition], row_targets: dict[str, list[str]],
) -> dict:
    rows = []
    for pack in sorted(packs.values(), key=lambda item: item.path):
        for block in pack.blocks:
            if block.source_key == WRITING_BRAND_VOICE:
                disposition = "retain_explanatory"
                targets: list[str] = []
            elif block.source_key in {
                ARCH_WEBHOOK, DELIVERY_ORACLE,
                WRITING_EOS_VOICE, WRITING_VENTURE_VOICE,
            }:
                disposition = "merge_into"
                targets = row_targets[block.source_key]
            else:
                disposition = "create"
                targets = row_targets[block.source_key]
            row = {
                "source_key": block.source_key,
                "path": block.path,
                "family": FAMILY_TO_LEDGER[block.family],
                "ordinal": block.ordinal,
                "start": block.start,
                "end": block.end,
                "block_sha256": block.block_sha256,
                "disposition": disposition,
                "reason": _ledger_reason(
                    block, disposition, targets, definitions,
                ),
            }
            legacy = inventory_rows[block.source_key].get("legacy_anchor")
            if legacy:
                row["legacy_anchor"] = legacy
            if disposition in {"create", "merge_into"}:
                row["targets"] = targets
            else:
                row["destination"] = "packs/writing-content/PACK.md#voice-scopes"
            rows.append(row)
    return {
        "version": 1,
        "baseline_commit": BASELINE_COMMIT,
        "inventory_sha256": EXPECTED_INVENTORY_SHA256,
        "rows": rows,
    }


def _build_alias_registry(ledger: dict) -> dict:
    """Map every stable pack anchor to one primary canonical Doctrine.

    Five legacy labels were compound rules and now point at several atomic
    Doctrine records. The HTML anchor remains the complete compatibility
    surface in PACK.md; the resolver returns the first atom as the stable
    primary identity and the pack map exposes the remaining atoms.
    """

    aliases: dict[str, str] = {}
    for row in ledger["rows"]:
        anchor = row.get("legacy_anchor")
        targets = row.get("targets") or []
        if not anchor or not targets:
            continue
        path = str(row["path"])
        pack = PurePosixPath(path).parent.name
        primary = str(targets[0])
        aliases[f"{path}#{anchor}"] = primary
        aliases[f"{pack}#{anchor}"] = primary
    return {"version": 1, "aliases": dict(sorted(aliases.items()))}


def _load_naming_contract(root: Path) -> dict:
    path = Path(root) / NAMING_BASELINE_PATH
    try:
        contract = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise DoctrineMigrationError(
            f"Cannot read the frozen naming contract at {NAMING_BASELINE_PATH}: {exc}"
        ) from exc
    packs = contract.get("packs") if isinstance(contract, dict) else None
    aliases = contract.get("identifier_migration") if isinstance(contract, dict) else None
    if not isinstance(packs, dict) or set(packs) != set(PACK_CODES):
        raise DoctrineMigrationError("Naming contract does not cover the 25 packs")
    if not isinstance(aliases, dict) or len(aliases) != 103:
        raise DoctrineMigrationError("Naming contract does not carry 103 Wargame aliases")
    for slug, spec in packs.items():
        if spec.get("id_namespace") != PACK_CODES[slug]:
            raise DoctrineMigrationError(
                f"Naming namespace for {slug} disagrees with its Doctrine allocation"
            )
    return contract


def _build_current_alias_registry(ledger: dict, naming: dict) -> dict:
    document = _build_alias_registry(ledger)
    aliases = dict(document["aliases"])
    aliases.update({
        str(old): str(new)
        for old, new in naming["identifier_migration"].items()
    })
    document["aliases"] = dict(sorted(aliases.items()))
    return document


def _synthetic_anchor(block: SourceBlock, inventory_row: dict) -> str | None:
    legacy = inventory_row.get("legacy_anchor")
    if legacy:
        return str(legacy)
    if block.family == "requirements" and re.match(r"^\d+\.\s+\*\*", block.text):
        return f"B{block.ordinal}"
    return None


def _relative_doc_link(pack_name: str, definition: DoctrineDefinition) -> str:
    source_dir = PurePosixPath("packs") / pack_name
    return os.path.relpath(definition.path, source_dir).replace("\\", "/")


def _render_navigation(
    pack: PackSource, inventory_rows: dict[str, dict],
    ledger_rows: dict[str, dict], definitions: dict[str, DoctrineDefinition],
) -> list[str]:
    lines = [
        "## Doctrine",
        "",
        "Standing rules are atomic Doctrine files. The labels below are stable",
        "compatibility anchors; they do not encode authority.",
        "",
    ]
    for block in pack.blocks:
        row = ledger_rows[block.source_key]
        anchor = _synthetic_anchor(block, inventory_rows[block.source_key])
        if anchor:
            lines.append(f'<a id="{anchor}"></a>')
            label = f"`{anchor}`"
        else:
            label = f"source `{block.family}:{block.ordinal:03d}`"
        if row["disposition"] == "retain_explanatory":
            lines.append(
                f"- {label} remains explanatory at [voice scopes](#voice-scopes) "
                "until a named brand voice is adopted."
            )
            continue
        rendered = []
        for identifier in row["targets"]:
            definition = definitions[identifier]
            link = _relative_doc_link(pack.slug, definition)
            rendered.append(
                f"[{identifier}]({link}) ({definition.authority})"
            )
        lines.append(f"- {label} to " + ", ".join(rendered))
    admissions = POST_MIGRATION_ADMISSIONS.get(pack.slug, [])
    if admissions:
        lines += [
            "",
            "### Later evidence-led admissions",
            "",
            "These records were admitted after the frozen source migration.",
            "Their own metadata is canonical; this map does not restate it.",
            "",
        ]
        for identifier, path, record_type in admissions:
            lines.append(f"- [{identifier}]({path}) ({record_type})")
    return lines + [""]


def _render_voice_scopes(
    pack: PackSource, row_targets: dict[str, list[str]],
    definitions: dict[str, DoctrineDefinition],
) -> list[str]:
    eos = definitions[row_targets[WRITING_EOS_VOICE][0]]
    venture = definitions[row_targets[WRITING_VENTURE_VOICE][0]]
    return [
        "## Voice scopes",
        "",
        "Voice is deliberately scoped rather than inherited as one universal law.",
        "",
        f"- EOS-internal prose resolves through "
        f"[{eos.identifier}]({_relative_doc_link(pack.slug, eos)}).",
        f"- Venture documentation resolves through "
        f"[{venture.identifier}]({_relative_doc_link(pack.slug, venture)}).",
        "- Brand voice remains explanatory and empty until a venture adopts a",
        "  named brand voice. Adoption creates a brand-scoped preference; absence",
        "  is not a breach.",
        "",
    ]


def _render_pack(
    pack: PackSource, inventory_rows: dict[str, dict], ledger: dict,
    definitions: dict[str, DoctrineDefinition], row_targets: dict[str, list[str]],
    naming: dict,
) -> str:
    parsed = parse_frontmatter(pack.text)
    metadata = dict(parsed.data)
    naming_spec = naming["packs"][pack.slug]
    metadata.update({
        "summary": (
            f"Activation, outcomes and decision map for the {pack.slug} "
            "Doctrine and Wargames"
        ),
        "kind": "record",
        "type": "pack",
        "display_name": naming_spec["display_name"],
        "category": naming_spec["category"],
        "id_namespace": naming_spec["id_namespace"],
        "authority": "none",
        "basis": "decision",
        "evidence_grade": "not-applicable",
        "review": "none",
        "depends_on": PACK_DEPENDENCIES[pack.slug],
    })
    front = ["---"]
    for key, value in metadata.items():
        front.append(f"{key}: {_frontmatter_value(value)}")
    front.extend(["---", ""])

    ledger_rows = {row["source_key"]: row for row in ledger["rows"]}
    body = re.sub(
        r"\bdecision guides\b", "Wargames", parsed.body,
        flags=re.IGNORECASE,
    )
    body = re.sub(
        r"\bdecision guide\b", "Wargame", body,
        flags=re.IGNORECASE,
    )
    body = re.sub(
        r"(?m)^# [^\n]+$", f"# {naming_spec['display_name']}", body, count=1,
    )
    for old, new in PACK_PROSE_REPLACEMENTS.get(pack.slug, ()):
        if old not in body:
            raise DoctrineMigrationError(
                f"reviewed PACK prose anchor is absent: {pack.path}: {old[:40]}"
            )
        body = body.replace(old, new)
    body_lines = body.splitlines()
    sections: list[tuple[int, int, str]] = []
    h2 = [
        (index, line[3:].strip())
        for index, line in enumerate(body_lines)
        if line.startswith("## ")
    ]
    for number, (start, heading) in enumerate(h2):
        end = h2[number + 1][0] if number + 1 < len(h2) else len(body_lines)
        sections.append((start, end, heading))
    first_section = sections[0][0] if sections else len(body_lines)
    rendered = body_lines[:first_section]
    navigation_written = False
    normative = {
        "Binding requirements", "Requirements", "House requirements",
        "Defaults", "Preferences",
    }
    for start, end, heading in sections:
        if heading in normative:
            if not navigation_written:
                rendered.extend(_render_navigation(
                    pack, inventory_rows, ledger_rows, definitions,
                ))
                navigation_written = True
            continue
        if pack.slug == "writing-content" and heading == "The three voice scopes":
            rendered.extend(_render_voice_scopes(pack, row_targets, definitions))
            continue
        rendered.extend(body_lines[start:end])
    if not navigation_written:
        raise DoctrineMigrationError(f"No normative organ found in {pack.path}")
    while rendered and rendered[-1] == "":
        rendered.pop()
    return "\n".join(front + rendered).rstrip() + "\n"


def build_migration(root: Path) -> dict[str, str]:
    """Return every generated output path and its deterministic content."""

    root = Path(root).resolve()
    naming = _load_naming_contract(root)
    packs, inventory_rows = _load_sources(root)
    definitions, row_targets = _make_definitions(packs, inventory_rows)
    ledger = _build_ledger(
        packs, inventory_rows, definitions, row_targets,
    )
    if len(ledger["rows"]) != 501:
        raise DoctrineMigrationError("Migration ledger does not cover 501 rows")

    outputs = {
        definition.path: _render_doctrine(definition, row_targets)
        for definition in definitions.values()
    }
    for pack in packs.values():
        outputs[pack.path] = _render_pack(
            pack, inventory_rows, ledger, definitions, row_targets, naming,
        )
    outputs[LEDGER_PATH] = json.dumps(
        ledger, indent=2, ensure_ascii=False,
    ) + "\n"
    outputs[ALIASES_PATH] = json.dumps(
        _build_current_alias_registry(ledger, naming), indent=2, ensure_ascii=False,
    ) + "\n"
    return dict(sorted(outputs.items()))


def apply_migration(root: Path) -> dict[str, int]:
    root = Path(root).resolve()
    outputs = build_migration(root)
    expected_docs = {
        path for path in outputs if "/doctrines/DOC-" in path
    }
    removed = 0
    for path in sorted(root.glob("packs/*/doctrines/DOC-*.md")):
        rel = path.relative_to(root).as_posix()
        if rel in expected_docs:
            continue
        text = path.read_text(encoding="utf-8")
        if GENERATOR_MARKER not in text:
            # The migration owns only atoms descended from the frozen source
            # inventory. Later, independently admitted Doctrine is canonical
            # content and must survive a migration replay untouched.
            continue
        path.unlink()
        removed += 1
    changed = 0
    for rel, content in outputs.items():
        path = root / rel
        current = path.read_text(encoding="utf-8") if path.is_file() else None
        if current == content:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8", newline="\n")
        changed += 1
    return {
        "outputs": len(outputs),
        "doctrines": len(expected_docs),
        "changed": changed,
        "removed": removed,
    }


def check_fixpoint(root: Path) -> list[str]:
    root = Path(root).resolve()
    outputs = build_migration(root)
    changed = []
    for rel, content in outputs.items():
        path = root / rel
        if not path.is_file() or path.read_text(encoding="utf-8") != content:
            changed.append(rel)
    expected_docs = {
        path for path in outputs if "/doctrines/DOC-" in path
    }
    for path in sorted(root.glob("packs/*/doctrines/DOC-*.md")):
        rel = path.relative_to(root).as_posix()
        if rel not in expected_docs and GENERATOR_MARKER in path.read_text(
            encoding="utf-8"
        ):
            changed.append(rel)
    return sorted(set(changed))


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Apply the reviewed Doctrine migration from its frozen source."
    )
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    if args.check:
        drift = check_fixpoint(args.repo)
        if drift:
            print("Doctrine migration is not at a fixpoint:")
            for path in drift:
                print(f"- {path}")
            return 1
        print("Doctrine migration is at a fixpoint")
        return 0
    result = apply_migration(args.repo)
    print(
        "Doctrine migration: "
        f"{result['doctrines']} doctrines, {result['outputs']} outputs, "
        f"{result['changed']} changed, {result['removed']} removed"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
