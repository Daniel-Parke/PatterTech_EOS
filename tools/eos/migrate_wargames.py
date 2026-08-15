"""Migrate the frozen 114 decision procedures to semantic Wargames.

The source is the immutable pre-migration tree at ``BASELINE_COMMIT``.  A
rerun therefore renders the same bytes instead of trying to reinterpret its
own output.  The frozen identity/path digest is independent of the Doctrine
migration and makes a move, rename or silent loss a hard failure.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Iterable, Mapping, Sequence

from tools.eos.frontmatter import parse as parse_frontmatter
from tools.eos.knowledge_migration import BASELINE_COMMIT


FROZEN_COUNT = 114
FROZEN_INVENTORY_SHA256 = (
    "2d532914db4bc3ce91459f055656e54da31b69cfc54fe8fd269726d766052dda"
)
DOCTRINE_LEDGER = "org/migration/DOCTRINE_MIGRATION.json"
WARGAME_LEDGER = "org/migration/WARGAME_MIGRATION.json"
GENERATOR = "tools.eos.migrate_wargames"

WARGAME_HEADINGS = (
    "Decision question and stakes",
    "Doctrines or coverage gap under pressure",
    "Preconditions and engagement triggers",
    "Options",
    "Failure premises",
    "Decision rule",
    "Safe default",
    "Cheapest discriminating test",
    "Fallback, exit and revisit",
    "Counter-evidence and transfer limits",
)

_PROCEDURE_PATH = re.compile(
    r"^(?:packs/[^/]+/guides|inception/wargames)/"
    r"((?:GD|WG)-[A-Z0-9]+-[0-9]{3})-[^/]+\.md$"
)
_LEGACY_LABEL = re.compile(
    r"(?<![A-Z0-9-])(?:B[0-9]+|D[0-9]+|BR-[0-9]+|H[0-9]+)"
    r"(?![A-Z0-9-])"
)
_H2 = re.compile(r"(?m)^## (.+?)\s*$")
_OPTION = re.compile(r"(?ms)^### (.+?)\s*$\n(.*?)(?=^### |\Z)")


class WargameMigrationError(RuntimeError):
    """The reviewed Wargame migration cannot be reproduced safely."""


@dataclass(frozen=True)
class Doctrine:
    identifier: str
    statement: str
    authority: str
    applies_when: tuple[str, ...]
    path: str


@dataclass(frozen=True)
class Procedure:
    identifier: str
    path: str
    text: str
    metadata: Mapping[str, object]
    body: str

    @property
    def pack(self) -> str | None:
        parts = PurePosixPath(self.path).parts
        return parts[1] if parts and parts[0] == "packs" else None


# These procedures did not cite a legacy B/D/BR/H label.  The mappings were
# reviewed against the final Doctrine ledger, rather than guessed at runtime.
# Explicit legacy labels always take precedence over this table.
DOC_OVERRIDES: dict[str, tuple[str, ...]] = {
    "GD-AGENT-002": ("DOC-AGENT-010", "DOC-AGENT-012"),
    "GD-SWARM-001": (
        "DOC-AGENT-008", "DOC-SWARM-012", "DOC-SWARM-013", "DOC-SWARM-024",
    ),
    "GD-SWARM-003": ("DOC-SWARM-025",),
    "GD-AIML-002": ("DOC-AIML-008",),
    "GD-AIML-003": (
        "DOC-AIML-004", "DOC-AIML-006", "DOC-AGENT-003", "DOC-COD-001",
    ),
    "GD-AIML-004": ("DOC-AIML-016",),
    "GD-AIML-005": ("DOC-AIML-003", "DOC-AIML-017"),
    "GD-API-004": ("DOC-API-013",),
    "GD-API-005": ("DOC-API-006",),
    "GD-ARCH-001": ("DOC-ARCH-001", "DOC-ARCH-004", "DOC-ARCH-005"),
    "GD-BLM-001": ("DOC-BLM-003",),
    "GD-BLM-002": ("DOC-BLM-008",),
    "GD-BMP-001": ("DOC-BMP-005",),
    "GD-BMP-002": ("DOC-BMP-009",),
    "GD-BMP-003": ("DOC-BMP-007",),
    "GD-BMP-004": ("DOC-BMP-012",),
    "GD-COD-002": ("DOC-COD-006", "DOC-COD-007"),
    "GD-COD-005": ("DOC-COD-009", "DOC-COD-010"),
    "GD-DATA-004": ("DOC-DATA-008",),
    "GD-DATAENG-002": ("DOC-DATAENG-002",),
    "WG-DEL-005": ("DOC-DEL-002", "DOC-DEL-006", "DOC-COD-001"),
    "WG-DEL-006": ("DOC-DEL-002", "DOC-DEL-006", "DOC-COD-001"),
    "WG-DEL-007": ("DOC-DISC-009", "DOC-DISC-013", "DOC-DEL-008"),
    "GD-DEVOPS-001": ("DOC-DEVOPS-001",),
    "GD-DEVOPS-002": ("DOC-DEVOPS-008",),
    "GD-DEVOPS-003": ("DOC-DEVOPS-009",),
    "GD-DEVOPS-004": ("DOC-DEVOPS-004",),
    "WG-OPS-003": ("DOC-DEVOPS-005",),
    "GD-DOCS-001": ("DOC-DOCS-004",),
    "GD-DOCS-003": ("DOC-DOCS-009",),
    "GD-DOCS-005": ("DOC-DOCS-001", "DOC-DOCS-011"),
    "GD-IDENT-002": ("DOC-IDENT-015",),
    "GD-NAT-001": ("DOC-NAT-008",),
    "GD-NAT-003": ("DOC-NAT-004", "DOC-NAT-010"),
    "GD-HOUSE-001": ("DOC-HOUSE-010",),
    "GD-HOUSE-002": ("DOC-HOUSE-001",),
    "GD-HOUSE-004": ("DOC-HOUSE-007", "DOC-HOUSE-008"),
    "GD-RESEARCH-001": ("DOC-RESEARCH-010", "DOC-RESEARCH-015"),
    "GD-RESEARCH-002": ("DOC-RESEARCH-020",),
    "GD-SEC-001": ("DOC-SEC-003",),
    "GD-SEC-002": ("DOC-SEC-018",),
    "GD-SEC-003": ("DOC-SEC-011",),
    "GD-SEC-004": ("DOC-SEC-006",),
    "GD-SUPPLY-001": (
        "DOC-SUPPLY-002", "DOC-SUPPLY-003", "DOC-SEC-014",
    ),
    "GD-SUPPLY-003": (
        "DOC-SUPPLY-005", "DOC-DEVOPS-005", "DOC-DEVOPS-008",
    ),
    "GD-SUPPLY-004": ("DOC-SUPPLY-011",),
    "GD-UIUX-002": ("DOC-UIUX-003", "DOC-UIUX-010"),
}


# Only cases admitted as an existing refresh or relation-covered case in the
# 2026-08-15 research packet receive pressure predicates here.  The admitted
# new Wargames own the other pressure rows.
PRESSURE_MAP: dict[str, tuple[str, ...]] = {
    "GD-AGENT-001": ("agent_coordination_cost_is_material",),
    "GD-SWARM-001": ("agent_coordination_cost_is_material",),
    "GD-AIML-003": ("evaluation_oracle_is_undecided",),
    "GD-ARCH-001": ("requires_independent_deployability",),
    "WG-ARCH-001": ("requires_independent_deployability",),
    "WG-DEL-005": ("test_fidelity_changes_outcome",),
    "WG-DEL-006": (
        "test_fidelity_changes_outcome",
        "evaluation_oracle_is_undecided",
    ),
    "WG-DEL-007": ("riskiest_assumption_is_unproved",),
    "GD-SUPPLY-001": ("producer_trust_is_unproved",),
    "GD-SUPPLY-003": ("dependency_update_changes_known_good",),
    "GD-DEVOPS-002": ("dependency_update_changes_known_good",),
    "GD-UIUX-001": (
        "serves_novice_and_expert_users",
        "house_style_costs_access_or_performance",
    ),
    "GD-UIUX-003": ("house_style_costs_access_or_performance",),
}


# Pressure-specific Doctrines supplement an explicitly cited legacy label.
# This is needed where the new pressure crosses pack boundaries.
PRESSURE_DOC_ADDITIONS: dict[str, tuple[str, ...]] = {
    "GD-AGENT-001": (
        "DOC-AGENT-008", "DOC-SWARM-012", "DOC-SWARM-013", "DOC-SWARM-024",
    ),
    "GD-UIUX-001": (
        "DOC-UIUX-009", "DOC-DISC-016", "DOC-HOUSE-004", "DOC-HOUSE-015",
        "DOC-UIUX-011", "DOC-UIUX-014",
    ),
    "GD-UIUX-003": (
        "DOC-HOUSE-004", "DOC-HOUSE-015", "DOC-UIUX-011", "DOC-UIUX-014",
    ),
    "WG-ARCH-001": ("DOC-ARCH-004", "DOC-ARCH-005"),
    "GD-DEVOPS-002": ("DOC-SUPPLY-005",),
}


CONSEQUENCE_OVERRIDES = {
    "GD-AIML-003",
    "GD-ARCH-001",
    "WG-ARCH-001",
    "GD-DEVOPS-002",
    "GD-SUPPLY-001",
    "GD-SUPPLY-003",
    "GD-UIUX-001",
    "GD-UIUX-003",
    "WG-DEL-005",
    "WG-DEL-006",
}


RELATION_CANDIDATES: dict[str, tuple[str, ...]] = {
    "GD-AGENT-001": ("DREL-AGENT-001",),
    "GD-SWARM-001": ("DREL-AGENT-001",),
    "GD-AIML-003": ("DREL-AIML-002",),
    "GD-ARCH-001": ("DREL-ARCH-003",),
    "WG-ARCH-001": ("DREL-ARCH-003",),
    "WG-DEL-005": ("DREL-DEL-002",),
    "WG-DEL-006": ("DREL-DEL-002", "DREL-AIML-002"),
    "GD-SUPPLY-001": ("DREL-SUPPLY-001",),
    "GD-SUPPLY-003": ("DREL-SUPPLY-002",),
    "GD-DEVOPS-002": ("DREL-SUPPLY-002",),
    "GD-UIUX-001": ("DREL-UIUX-001", "DREL-HOUSE-002"),
    "GD-UIUX-003": ("DREL-HOUSE-001",),
}


CONFLICT_WHEN_RELATED = {
    "GD-DEVOPS-002", "GD-SUPPLY-003", "GD-UIUX-001", "GD-UIUX-003",
}


SOURCE_ADDITIONS: dict[str, tuple[str, ...]] = {
    "GD-AGENT-001": ("EV-0452",),
    "GD-SWARM-001": ("EV-0452",),
    "GD-ARCH-001": ("EV-0564",),
    "WG-ARCH-001": ("EV-0564",),
    "WG-DEL-007": ("EV-0579",),
    "GD-DISC-001": ("EV-0579",),
    "GD-SUPPLY-001": ("EV-0549", "EV-0582"),
}


RESEARCH_NOTES: dict[str, str] = {
    "GD-AGENT-001": (
        "EV-0452 is benchmark evidence across stated models, harnesses and task "
        "graphs. It supports decomposability, tool load and verifier placement as "
        "pressures, not a universal topology ranking or cut-off."
    ),
    "GD-SWARM-001": (
        "EV-0452 reports gains on decomposable work and losses on sequential, "
        "tool-heavy work. Transfer the direction only: coordination cost, baseline "
        "capability and central verification still need measurement on this task."
    ),
    "GD-ARCH-001": (
        "EV-0564 contributes quality-attribute scenarios, sensitivity points and "
        "trade-off points. Its multi-day facilitated method does not transfer as "
        "mandatory ceremony for a small venture."
    ),
    "WG-DEL-007": (
        "EV-0579 separates exploratory code from software that reaches users. It "
        "does not make every small change reversible: a spike still needs a named "
        "deletion or hardening boundary."
    ),
    "GD-DISC-001": (
        "EV-0579 supports a narrow exploratory path only while its deletion or "
        "promotion boundary remains explicit. Copying or retaining the result "
        "moves it back through the normal evidence gate."
    ),
    "GD-SUPPLY-001": (
        "EV-0582 says what provenance can establish about where, when and how an "
        "artefact was produced. EV-0549 preserves the hard limit: accurate "
        "provenance can still describe a malicious or flawed producer, so producer "
        "trust and safe use remain separate admission questions."
    ),
}


CHEAPEST_TEST_OVERRIDES = {
    "GD-ARCH-001": (
        "Map change coupling, deployment cadence, isolation, ownership and "
        "capacity from recent work. Test one proposed seam without splitting "
        "deployment, then ask whether the measured pressure still requires an "
        "independently deployable boundary."
    ),
    "WG-DEL-007": (
        "Build the narrowest end-to-end path. List the deletion or hardening "
        "work required before any artefact reaches users, then use that list "
        "to decide whether the slice remains a spike or enters the normal gate."
    ),
    "WG-DEL-005": (
        "Run the same contract against the proposed double and the nearest "
        "available real boundary. Seed one representative mismatch and require "
        "the independent oracle to catch it."
    ),
    "WG-DEL-006": (
        "Run the same representative case through the proposed oracle and an "
        "independently authored reference. Seed one plausible shared mistake; "
        "the test discriminates only if the independent path rejects it."
    ),
    "GD-SUPPLY-001": (
        "Verify a correctly attested artefact whose source or selected "
        "dependency is deliberately policy-bad. Record what provenance proves, "
        "what the admission verifier rejects, and which trust claim remains open."
    ),
    "GD-SUPPLY-003": (
        "Take one representative security update through the cooldown exception, "
        "suite, staged release, rollback and incident reconstruction path. Compare "
        "that proof with the known-good deployment it would replace."
    ),
    "GD-AGENT-001": (
        "Compare one bounded single-agent baseline with the smallest justified "
        "decomposition under the same task set, model budget and external "
        "verifier. Measure useful accepted work and coordination cost separately."
    ),
    "GD-SWARM-001": (
        "Compare one bounded single-agent baseline with the smallest justified "
        "lane split under the same task set, model budget and external verifier. "
        "Include merge and verification time in the result."
    ),
    "GD-AIML-003": (
        "Calibrate each proposed judge against the same human-labelled sample. "
        "Report agreement, disagreement, order effects, abstention and cost before "
        "allowing any judge to decide the claimed behaviour."
    ),
    "GD-UIUX-001": (
        "Run the same representative task with novice and frequent users. Record "
        "completion, error and search time, then repeat on the lowest supported "
        "device if house treatment or density changes performance."
    ),
    "GD-DISC-001": (
        "Build the narrowest representative path and list the assumptions it can "
        "actually test. Name its deletion or promotion boundary, then list the "
        "hardening evidence required before any retained artefact reaches users."
    ),
    "GD-UIUX-003": (
        "Exercise the hardest representative journey with reduced motion and on "
        "the lowest supported device, then inspect the accessibility tree and "
        "named assistive-technology path for the claimed criteria."
    ),
    "GD-HOUSE-001": (
        "Test one representative task with the intended audience under reduced "
        "motion and on the lowest supported device. Measure loading and frame "
        "behaviour before spending the optional house treatment."
    ),
}


RETIRED_SUCCESSORS: dict[str, tuple[str, ...]] = {
    "WG-VOX-001": ("GD-WRIT-003",),
    "WG-WEB-001": ("GD-UIUX-001",),
    "WG-WEB-003": ("GD-HOUSE-002",),
    "WG-WEB-005": ("GD-HOUSE-001",),
    "WG-WEB-006": ("GD-UIUX-001",),
    "WG-WEB-011": ("GD-HOUSE-001",),
    "WG-WEB-012": ("GD-HOUSE-004",),
    "WG-WEB-013": ("GD-UIUX-002", "GD-UIUX-004"),
    "WG-WEB-014": ("GD-HOUSE-004",),
}


RETIRED_PROSE = {
    "WG-WEB-001": "the retired historical web surface-register scenario",
    "WG-WEB-003": "the retired historical web container-choice scenario",
    "WG-WEB-005": "the retired historical web ornament-budget scenario",
    "WG-WEB-006": "the retired historical web density-and-audience scenario",
}


def _git(root: Path, *args: str) -> str:
    process = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="strict",
        timeout=60,
    )
    if process.returncode:
        detail = process.stderr.strip() or "unknown git failure"
        raise WargameMigrationError(
            "git %s failed: %s" % (" ".join(args), detail)
        )
    return process.stdout


def _normalise(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _inventory_hash(rows: Mapping[str, str]) -> str:
    payload = "".join(
        f"{identifier}\t{rows[identifier]}\n" for identifier in sorted(rows)
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def frozen_procedures(root: Path) -> dict[str, str]:
    """Reconstruct and verify the independent 114-item identity freeze."""

    root = Path(root).resolve()
    resolved = _git(root, "rev-parse", "--verify", f"{BASELINE_COMMIT}^{{commit}}").strip()
    if resolved != BASELINE_COMMIT:
        raise WargameMigrationError(
            f"baseline resolved to {resolved}, expected {BASELINE_COMMIT}"
        )
    rows: dict[str, str] = {}
    paths = _git(root, "ls-tree", "-r", "--name-only", BASELINE_COMMIT).splitlines()
    for path in paths:
        match = _PROCEDURE_PATH.fullmatch(path)
        if not match:
            continue
        identifier = match.group(1)
        if identifier in rows:
            raise WargameMigrationError(f"frozen ID repeats: {identifier}")
        text = _git(root, "show", f"{BASELINE_COMMIT}:{path}")
        parsed = parse_frontmatter(text)
        if not parsed.present or parsed.errors:
            raise WargameMigrationError(f"cannot parse frozen procedure: {path}")
        heading = re.search(
            r"(?m)^# ((?:GD|WG)-[A-Z0-9]+-[0-9]{3})(?::|\s|$)",
            parsed.body,
        )
        if not heading or heading.group(1) != identifier:
            raise WargameMigrationError(f"frozen path and heading disagree: {path}")
        rows[identifier] = path
    digest = _inventory_hash(rows)
    if len(rows) != FROZEN_COUNT or digest != FROZEN_INVENTORY_SHA256:
        raise WargameMigrationError(
            f"frozen inventory drifted: rows={len(rows)}, sha256={digest}"
        )
    return rows


def _read_frozen(root: Path, inventory: Mapping[str, str]) -> dict[str, Procedure]:
    procedures: dict[str, Procedure] = {}
    for identifier, path in sorted(inventory.items()):
        text = _normalise(_git(root, "show", f"{BASELINE_COMMIT}:{path}"))
        parsed = parse_frontmatter(text)
        procedures[identifier] = Procedure(
            identifier=identifier,
            path=path,
            text=text,
            metadata=dict(parsed.data),
            body=parsed.body.strip(),
        )
    return procedures


def _check_live_identity(root: Path, inventory: Mapping[str, str]) -> None:
    seen: dict[str, list[str]] = {}
    candidates = sorted(root.glob("packs/*/guides/*.md"))
    candidates.extend(sorted(root.glob("inception/wargames/*.md")))
    for path in candidates:
        rel = path.relative_to(root).as_posix()
        match = _PROCEDURE_PATH.fullmatch(rel)
        if not match:
            continue
        identifier = match.group(1)
        parsed = parse_frontmatter(path.read_text(encoding="utf-8"))
        declared = str(parsed.data.get("id") or identifier)
        seen.setdefault(declared, []).append(rel)
        if declared != identifier:
            raise WargameMigrationError(
                f"procedure path declares a different ID: {rel}: {declared}"
            )
    for identifier, expected in inventory.items():
        paths = seen.get(identifier, [])
        if paths != [expected]:
            raise WargameMigrationError(
                f"frozen identity/path drift: {identifier}: {paths!r}, "
                f"expected {[expected]!r}"
            )


def _values(value: object) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    if isinstance(value, tuple):
        return [str(item) for item in value if str(item)]
    return [str(value)]


def _load_doctrines(
    root: Path,
) -> tuple[dict[str, Doctrine], dict[tuple[str, str], tuple[str, ...]], dict]:
    ledger_path = root / DOCTRINE_LEDGER
    if not ledger_path.is_file():
        raise WargameMigrationError(f"Doctrine ledger is absent: {DOCTRINE_LEDGER}")
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    if ledger.get("baseline_commit") != BASELINE_COMMIT:
        raise WargameMigrationError("Doctrine ledger is not pinned to the baseline")
    rows = ledger.get("rows") or []
    if len(rows) != 501:
        raise WargameMigrationError(
            f"Doctrine ledger has {len(rows)} rows, expected 501"
        )

    doctrines: dict[str, Doctrine] = {}
    for path in sorted(root.glob("packs/*/doctrines/DOC-*.md")):
        parsed = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not parsed.present or parsed.errors:
            raise WargameMigrationError(f"cannot parse Doctrine: {path}")
        metadata = parsed.data
        identifier = str(metadata.get("id") or "")
        if not identifier:
            raise WargameMigrationError(f"Doctrine has no ID: {path}")
        if identifier in doctrines:
            raise WargameMigrationError(f"Doctrine ID repeats: {identifier}")
        doctrines[identifier] = Doctrine(
            identifier=identifier,
            statement=str(metadata.get("statement") or metadata.get("summary") or ""),
            authority=str(metadata.get("authority") or "default"),
            applies_when=tuple(_values(metadata.get("applies_when"))),
            path=path.relative_to(root).as_posix(),
        )

    labels: dict[tuple[str, str], tuple[str, ...]] = {}
    ledger_targets: set[str] = set()
    for row in rows:
        targets = tuple(str(item) for item in row.get("targets", []))
        ledger_targets.update(targets)
        anchor = row.get("legacy_anchor")
        if not anchor:
            continue
        pack = PurePosixPath(str(row["path"])).parts[1]
        key = (pack, str(anchor))
        if key in labels:
            raise WargameMigrationError(f"Doctrine label repeats: {key!r}")
        labels[key] = targets
    missing = sorted(ledger_targets - set(doctrines))
    if missing:
        raise WargameMigrationError(
            "Doctrine ledger targets do not resolve: " + ", ".join(missing)
        )
    return doctrines, labels, ledger


def _sections(body: str) -> tuple[str, list[tuple[str, str]]]:
    matches = list(_H2.finditer(body))
    prefix = body[: matches[0].start()].strip() if matches else body.strip()
    sections: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        sections.append((match.group(1).strip(), body[match.end() : end].strip()))
    return prefix, sections


def _section(rows: Sequence[tuple[str, str]], *names: str) -> str:
    for name, value in rows:
        if name in names:
            return value.strip()
    return ""


def _frontmatter_value(value: object) -> str:
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(str(item) for item in value) + "]"
    return str(value)


def _replace_retired(text: str) -> str:
    for identifier, replacement in RETIRED_PROSE.items():
        text = text.replace(identifier, replacement)
    return text


def _procedure_targets(
    procedure: Procedure,
    labels: Mapping[tuple[str, str], tuple[str, ...]],
    doctrines: Mapping[str, Doctrine],
) -> tuple[str, ...]:
    if procedure.pack is None:
        return ()
    targets: list[str] = []
    for label in _LEGACY_LABEL.findall(procedure.body):
        for target in labels.get((procedure.pack, label), ()):
            if target not in targets:
                targets.append(target)
    if not targets:
        targets.extend(DOC_OVERRIDES.get(procedure.identifier, ()))
    for target in PRESSURE_DOC_ADDITIONS.get(procedure.identifier, ()):
        if target not in targets:
            targets.append(target)
    if not targets:
        raise WargameMigrationError(
            f"no reviewed Doctrine target for {procedure.identifier}"
        )
    missing = [target for target in targets if target not in doctrines]
    if missing:
        raise WargameMigrationError(
            f"{procedure.identifier} names missing Doctrines: {missing!r}"
        )
    return tuple(targets)


def _option_rows(options: str) -> list[tuple[str, str]]:
    return [(match.group(1).strip(), match.group(2).strip()) for match in _OPTION.finditer(options)]


def _normalise_options(options: str) -> str:
    """Promote the one legacy bold-option form to the common H3 contract."""

    return re.sub(
        r"(?m)^\*\*([A-Z0-9]+)\.\s+(.+?)\.\*\*\s*(.*)$",
        lambda match: (
            f"### {match.group(1)}. {match.group(2)}\n\n{match.group(3)}"
        ),
        options,
    )


def _clean_excerpt(text: str, limit: int = 520) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    clipped = text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:")
    return clipped + "."


def _failure_mechanism(option_body: str) -> str:
    patterns = (
        r"(?is)\*\*Costs?\.\*\*\s*(.*?)(?=\n\s*\n|\Z)",
        r"(?is)(?:^|\n)Costs?:\s*(.*?)(?=\n\s*\n|\Z)",
        r"(?is)\bCosts?\b[:.]?\s*(.*?)(?=\n\s*\n|\Z)",
    )
    for pattern in patterns:
        match = re.search(pattern, option_body)
        if match and match.group(1).strip():
            return _clean_excerpt(match.group(1))
    paragraphs = [part.strip() for part in re.split(r"\n\s*\n", option_body) if part.strip()]
    for paragraph in paragraphs:
        if re.search(r"(?i)\b(cost|risk|fail|cannot|tax|blind|weak|loss)\w*\b", paragraph):
            return _clean_excerpt(paragraph)
    return _clean_excerpt(paragraphs[-1] if paragraphs else option_body)


def _first_question(preconditions: str) -> str:
    lines = preconditions.splitlines()
    for index, line in enumerate(lines):
        if not line.startswith("- "):
            continue
        parts = [line[2:].strip()]
        for continuation in lines[index + 1 :]:
            if continuation.startswith("- ") or not continuation.strip():
                break
            parts.append(continuation.strip())
        return _clean_excerpt(" ".join(parts), 300)
    first = re.split(r"(?<=[?.!])\s+", _clean_excerpt(preconditions, 400))[0]
    return first or "Which option changes the material outcome?"


def _first_risk(options: Sequence[tuple[str, str]]) -> str:
    if not options:
        return "the selected option's stated failure premise appears"
    return _failure_mechanism(options[0][1]).rstrip(".")


def _worked_ruling_note(worked: str) -> str:
    count = len(re.findall(r"(?m)^- ", worked))
    noun = "note" if count == 1 else "notes"
    return (
        f"The baseline file carried {count} worked ruling {noun}. They are not "
        "copied into this live Wargame because they record a selection but do "
        "not carry both a privacy-reviewed harvest and an independently "
        "verifiable execution outcome. The immutable source remains available "
        f"at commit `{BASELINE_COMMIT}` for historical provenance. No `RUL-*` "
        "record was admitted from this procedure."
    )


def _metadata(
    procedure: Procedure,
    doctrines: Mapping[str, Doctrine],
    targets: tuple[str, ...],
    live_relations: set[str],
) -> dict[str, object]:
    source = dict(procedure.metadata)
    sources = _values(source.get("sources"))
    if not sources:
        sources = ["kernel/SCALE_MATRIX.md"]
    for identifier in SOURCE_ADDITIONS.get(procedure.identifier, ()):
        if identifier not in sources:
            sources.append(identifier)
    always_walk = procedure.identifier in {
        "WG-EOS-001", "WG-EOS-002",
        "GD-SEC-001", "GD-SEC-002", "GD-SEC-003", "GD-SEC-004",
    }
    if procedure.pack is None:
        applies_when = ["runs_agents"]
        modes = ["selection", "gap"]
    elif always_walk:
        applies_when = ["runs_agents"]
        modes = ["selection"]
    else:
        same_pack = [
            doctrines[target]
            for target in targets
            if f"packs/{procedure.pack}/" in doctrines[target].path
        ]
        owner = same_pack[0] if same_pack else doctrines[targets[0]]
        applies_when = list(owner.applies_when) or ["always"]
        modes = ["selection"]
        if any(doctrines[target].authority != "binding" for target in targets):
            modes.append("exception")

    result: dict[str, object] = {
        "id": procedure.identifier,
        "summary": str(source.get("summary") or procedure.identifier),
        "kind": "wargame",
        "type": "wargame",
        "tags": sorted(set(_values(source.get("tags"))) | {"eos", "wargame"}),
        "scenario_modes": modes,
    }
    if targets:
        result["applicable_doctrines"] = list(targets)
    else:
        result["gap_domain"] = "inception"
    relations = [
        identifier
        for identifier in RELATION_CANDIDATES.get(procedure.identifier, ())
        if identifier in live_relations
    ]
    if relations and procedure.identifier in CONFLICT_WHEN_RELATED:
        if "conflict" not in modes:
            modes.append("conflict")
    result["scenario_modes"] = modes
    result.update({
        "applies_when": applies_when[:1],
        "engages_when": list(
            PRESSURE_MAP.get(procedure.identifier, ("operator_requests_wargame",))
        ),
        "consequence": (
            "high"
            if always_walk or procedure.identifier in CONSEQUENCE_OVERRIDES
            else "routine"
        ),
        "relations": relations,
    })
    if always_walk:
        result["always_walk"] = "true"
    for key in ("scope", "authority", "basis", "evidence_grade", "volatility"):
        if source.get(key):
            result[key] = source[key]
    result["sources"] = sources
    result["review"] = str(source.get("review") or "2027-08")
    result["lifecycle"] = str(source.get("lifecycle") or source.get("status") or "active")
    result["generated_by"] = GENERATOR
    return result


def _render_frontmatter(metadata: Mapping[str, object]) -> str:
    lines = ["---"]
    for key, value in metadata.items():
        lines.append(f"{key}: {_frontmatter_value(value)}")
    lines.append("---")
    return "\n".join(lines)


def _render_body(
    procedure: Procedure,
    doctrines: Mapping[str, Doctrine],
    targets: tuple[str, ...],
    metadata: Mapping[str, object],
) -> str:
    prefix, rows = _sections(procedure.body)
    question = _section(rows, "The question", "Decision question and stakes")
    preconditions = _section(
        rows, "It depends on", "Preconditions and engagement triggers"
    )
    options = _normalise_options(_section(rows, "Options", "Timing options"))
    decision = _section(rows, "Decision rule")
    default = _section(rows, "Default", "Safe default")
    worked = _section(rows, "Worked rulings")
    if not all((prefix, question, preconditions, options, decision, default)):
        raise WargameMigrationError(
            f"baseline body lacks a required decision organ: {procedure.path}"
        )
    option_rows = _option_rows(options)
    if len(option_rows) < 2:
        raise WargameMigrationError(
            f"baseline has fewer than two options: {procedure.path}"
        )

    if targets:
        doctrine_lines = []
        for target in targets:
            doctrine = doctrines[target]
            doctrine_lines.append(
                f"- `{target}` ({doctrine.authority}): {doctrine.statement}"
            )
        doctrine_lines.append("")
        doctrine_lines.append(
            "The options test how those propositions apply here. A Wargame may "
            "justify departure from a default, advisory rule or preference. It "
            "does not waive a binding Doctrine; contrary evidence opens Doctrine "
            "review or an ADR."
        )
        doctrine_pressure = "\n".join(doctrine_lines)
    else:
        doctrine_pressure = (
            "This inception fork covers a gap before pack Doctrine is activated. "
            "It is always walked because venture scale and repository shape decide "
            "which later rules can be loaded safely."
        )

    engages = ", ".join(f"`{item}`" for item in _values(metadata["engages_when"]))
    applies = ", ".join(f"`{item}`" for item in _values(metadata["applies_when"]))
    trigger_note = (
        f"\n\nApplicability is {applies}. Engagement is {engages}. "
        + (
            "This is an always-walk decision."
            if metadata.get("always_walk") == "true"
            else "If no engagement fact is true, an operator may still request it explicitly."
        )
    )

    failures = []
    for name, body in option_rows:
        failures.append(f"### Premortem for {name}")
        failures.append("")
        failures.append(
            f"Assume `{name}` was selected and the outcome failed. Test this "
            f"option's stated failure mechanism first: {_failure_mechanism(body)}"
        )
        failures.append("")
    failure_text = "\n".join(failures).rstrip()

    discriminator = CHEAPEST_TEST_OVERRIDES.get(procedure.identifier)
    if discriminator is None:
        discriminator = (
            "Settle this question with the smallest representative probe: "
            f"**{_first_question(preconditions)}** Compare only the option branches "
            "that answer changes, using the decision rule above as the oracle. "
            "Stop when the result rules at least one credible option in or out."
        )

    fallback = (
        "**Fallback `safe-default`:** " + _clean_excerpt(default, 600) + "\n\n"
        "**Exit condition:** Stop or roll back the selected branch when "
        + _first_risk(option_rows)
        + ", or when its stated preconditions cease to hold.\n\n"
        "**Revisit trigger:** Run this Wargame again when the answer to this "
        f"question changes: {_first_question(preconditions)}"
    )

    recognised = {
        "The question", "Decision question and stakes",
        "It depends on", "Preconditions and engagement triggers",
        "Options", "Timing options", "Decision rule", "Default", "Safe default",
        "Worked rulings", "Counter-evidence", "Counter-evidence and transfer limits",
        "Evidence boundary",
    }
    counter_parts: list[str] = []
    existing_counter = _section(
        rows, "Counter-evidence", "Counter-evidence and transfer limits"
    )
    evidence_boundary = _section(rows, "Evidence boundary")
    if existing_counter:
        counter_parts.append(existing_counter)
    if evidence_boundary:
        counter_parts.extend(("### Evidence boundary", "", evidence_boundary))
    for name, value in rows:
        if name not in recognised and value:
            counter_parts.extend((f"### Preserved reasoning: {name}", "", value))
    if worked:
        counter_parts.extend((
            "### Historical ruling boundary", "", _worked_ruling_note(worked),
        ))
    research_note = RESEARCH_NOTES.get(procedure.identifier)
    if research_note:
        counter_parts.extend(("### Current research boundary", "", research_note))
    counter_parts.extend((
        "### Transfer limit", "",
        "Use this decision rule only where its applicability holds and the "
        "representative test matches the venture's users, scale and failure cost. "
        "The cited evidence and prior arguments establish decision factors, not a "
        "universal outcome. Revisit on contrary evidence, a changed pressure fact "
        "or a changed Doctrine lifecycle.",
    ))

    rendered_sections = (
        ("Decision question and stakes", question),
        ("Doctrines or coverage gap under pressure", doctrine_pressure),
        (
            "Preconditions and engagement triggers",
            preconditions + trigger_note,
        ),
        ("Options", options),
        ("Failure premises", failure_text),
        ("Decision rule", decision),
        ("Safe default", default),
        ("Cheapest discriminating test", discriminator),
        ("Fallback, exit and revisit", fallback),
        ("Counter-evidence and transfer limits", "\n".join(counter_parts)),
    )
    body = prefix + "\n\n" + "\n\n".join(
        f"## {heading}\n\n{content.strip()}"
        for heading, content in rendered_sections
    )
    return _replace_retired(body).strip() + "\n"


def render_procedure(
    procedure: Procedure,
    doctrines: Mapping[str, Doctrine],
    labels: Mapping[tuple[str, str], tuple[str, ...]],
    live_relations: set[str],
) -> tuple[str, dict]:
    targets = _procedure_targets(procedure, labels, doctrines)
    metadata = _metadata(procedure, doctrines, targets, live_relations)
    body = _render_body(procedure, doctrines, targets, metadata)
    text = _render_frontmatter(metadata) + "\n\n" + body
    return text, {
        "id": procedure.identifier,
        "path": procedure.path,
        "disposition": "live-convert",
        "scenario_modes": metadata["scenario_modes"],
        **(
            {"applicable_doctrines": list(targets)}
            if targets else {"gap_domain": "inception"}
        ),
        "engages_when": metadata["engages_when"],
        "relations": metadata["relations"],
        "ruling_disposition": "not-extracted",
        "ruling_reason": (
            "The baseline worked notes record selections but do not carry both "
            "a privacy-reviewed harvest and an independently verifiable execution "
            "outcome. Historical provenance remains at the pinned baseline."
        ),
    }


def _retired_rows(root: Path) -> list[dict]:
    manifest = json.loads((root / "archive/RETIRED_IDS.json").read_text(encoding="utf-8"))
    identifiers = manifest.get("ids") or {}
    if len(identifiers) != 22:
        raise WargameMigrationError(
            f"retired Wargame inventory has {len(identifiers)} rows, expected 22"
        )
    rows = []
    for identifier, path in sorted(identifiers.items()):
        successors = RETIRED_SUCCESSORS.get(identifier, ())
        row = {
            "id": identifier,
            "historical_path": path,
            "disposition": (
                "semantic-duplicate-retired-superseded"
                if successors else "historical-only"
            ),
            "active_ruling_allowed": False,
            "operational_reference_status": "none-in-claimed-paths",
        }
        if successors:
            row["superseded_by"] = list(successors)
        rows.append(row)
    return rows


def _live_relation_ids(root: Path) -> set[str]:
    identifiers: set[str] = set()
    for path in sorted(root.glob("packs/*/doctrines/relations/DREL-*.json")):
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except ValueError as exc:
            raise WargameMigrationError(f"invalid relation JSON: {path}") from exc
        identifier = str(document.get("id") or "")
        if not identifier:
            raise WargameMigrationError(f"relation has no ID: {path}")
        if identifier in identifiers:
            raise WargameMigrationError(f"relation ID repeats: {identifier}")
        identifiers.add(identifier)
    return identifiers


def build_migration(root: Path) -> tuple[dict[str, str], dict]:
    """Return desired file bytes and the complete reviewed migration ledger."""

    root = Path(root).resolve()
    inventory = frozen_procedures(root)
    _check_live_identity(root, inventory)
    procedures = _read_frozen(root, inventory)
    doctrines, labels, doctrine_ledger = _load_doctrines(root)
    live_relations = _live_relation_ids(root)

    rendered: dict[str, str] = {}
    rows = []
    for identifier in sorted(procedures):
        text, row = render_procedure(
            procedures[identifier], doctrines, labels, live_relations,
        )
        rendered[row["path"]] = text
        rows.append(row)

    retired = _retired_rows(root)
    retired_ids = {row["id"] for row in retired}
    for path, text in rendered.items():
        present = sorted(identifier for identifier in retired_ids if identifier in text)
        if present:
            raise WargameMigrationError(
                f"generated live procedure {path} cites retired IDs: {present!r}"
            )

    ledger = {
        "version": 1,
        "kind": "wargame-migration",
        "baseline_commit": BASELINE_COMMIT,
        "frozen_inventory_sha256": FROZEN_INVENTORY_SHA256,
        "doctrine_inventory_sha256": doctrine_ledger.get("inventory_sha256"),
        "generator": GENERATOR,
        "procedure_count": len(rows),
        "retired_count": len(retired),
        "procedures": rows,
        "retired": retired,
    }
    return rendered, ledger


def _ledger_text(ledger: dict) -> str:
    return json.dumps(ledger, indent=2, ensure_ascii=False) + "\n"


def stale_paths(root: Path) -> list[str]:
    rendered, ledger = build_migration(root)
    desired = dict(rendered)
    desired[WARGAME_LEDGER] = _ledger_text(ledger)
    stale = []
    for rel, text in desired.items():
        path = root / rel
        current = path.read_text(encoding="utf-8") if path.is_file() else None
        if current != text:
            stale.append(rel)
    return sorted(stale)


def apply_migration(root: Path) -> tuple[int, int]:
    root = Path(root).resolve()
    rendered, ledger = build_migration(root)
    changed = 0
    for rel, text in {**rendered, WARGAME_LEDGER: _ledger_text(ledger)}.items():
        path = root / rel
        current = path.read_text(encoding="utf-8") if path.is_file() else None
        if current == text:
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8", newline="\n")
        changed += 1
    return changed, len(rendered)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Apply or check the frozen 114-procedure Wargame migration."
    )
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--apply", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args(argv)
    root = args.repo.resolve()
    if args.check:
        stale = stale_paths(root)
        if stale:
            print("Wargame migration is stale:")
            for path in stale:
                print(f"- {path}")
            return 1
        print(f"Wargame migration is at a fixpoint ({FROZEN_COUNT} procedures)")
        return 0
    changed, total = apply_migration(root)
    print(f"migrated {total} Wargames; changed {changed} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
