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
NAMING_BASELINE = "org/migration/NAMING_BASELINE.json"
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
_CANONICAL_PROCEDURE_PATH = re.compile(
    r"^(?:packs/[^/]+/wargames|inception/wargames)/"
    r"(WG-[A-Z0-9]+-[0-9]{3})-[^/]+\.md$"
)
_IDENTIFIER_BOUNDARY = r"[A-Z0-9]"
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
    source_identifier: str
    source_path: str
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
    "WG-AGENT-002": ("DOC-AGENT-010", "DOC-AGENT-012"),
    "WG-SWARM-001": (
        "DOC-AGENT-008", "DOC-SWARM-012", "DOC-SWARM-013", "DOC-SWARM-024",
    ),
    "WG-SWARM-003": ("DOC-SWARM-025",),
    "WG-AIML-003": ("DOC-AIML-008",),
    "WG-AIML-004": (
        "DOC-AIML-004", "DOC-AIML-006", "DOC-AGENT-003", "DOC-COD-001",
    ),
    "WG-AIML-005": ("DOC-AIML-016",),
    "WG-AIML-006": ("DOC-AIML-003", "DOC-AIML-017"),
    "WG-API-004": ("DOC-API-013",),
    "WG-API-005": ("DOC-API-006",),
    "WG-ARCH-013": ("DOC-ARCH-001", "DOC-ARCH-004", "DOC-ARCH-005"),
    "WG-BLM-001": ("DOC-BLM-003",),
    "WG-BLM-002": ("DOC-BLM-008",),
    "WG-BMP-001": ("DOC-BMP-005",),
    "WG-BMP-002": ("DOC-BMP-009",),
    "WG-BMP-003": ("DOC-BMP-007",),
    "WG-BMP-004": ("DOC-BMP-012",),
    "WG-COD-002": ("DOC-COD-006", "DOC-COD-007"),
    "WG-COD-005": ("DOC-COD-009", "DOC-COD-010"),
    "WG-DATA-007": ("DOC-DATA-008",),
    "WG-DATAENG-002": ("DOC-DATAENG-002",),
    "WG-DEL-005": ("DOC-DEL-002", "DOC-DEL-006", "DOC-COD-001"),
    "WG-DEL-006": ("DOC-DEL-002", "DOC-DEL-006", "DOC-COD-001"),
    "WG-DEL-007": ("DOC-DISC-009", "DOC-DISC-013", "DOC-DEL-008"),
    "WG-DEVOPS-001": ("DOC-DEVOPS-001",),
    "WG-DEVOPS-002": ("DOC-DEVOPS-008",),
    "WG-DEVOPS-003": ("DOC-DEVOPS-009",),
    "WG-DEVOPS-004": ("DOC-DEVOPS-004",),
    "WG-DEVOPS-005": ("DOC-DEVOPS-005",),
    "WG-DOCS-001": ("DOC-DOCS-004",),
    "WG-DOCS-003": ("DOC-DOCS-009",),
    "WG-DOCS-005": ("DOC-DOCS-001", "DOC-DOCS-011"),
    "WG-IDENT-002": ("DOC-IDENT-015",),
    "WG-NAT-001": ("DOC-NAT-008",),
    "WG-NAT-003": ("DOC-NAT-004", "DOC-NAT-010"),
    "WG-HOUSE-001": ("DOC-HOUSE-010",),
    "WG-HOUSE-002": ("DOC-HOUSE-001",),
    "WG-HOUSE-004": ("DOC-HOUSE-007", "DOC-HOUSE-008"),
    "WG-RESEARCH-001": ("DOC-RESEARCH-010", "DOC-RESEARCH-015"),
    "WG-RESEARCH-002": ("DOC-RESEARCH-020",),
    "WG-SEC-001": ("DOC-SEC-003",),
    "WG-SEC-002": ("DOC-SEC-018",),
    "WG-SEC-003": ("DOC-SEC-011",),
    "WG-SEC-004": ("DOC-SEC-006",),
    "WG-SUPPLY-001": (
        "DOC-SUPPLY-002", "DOC-SUPPLY-003", "DOC-SEC-014",
    ),
    "WG-SUPPLY-003": (
        "DOC-SUPPLY-005", "DOC-DEVOPS-005", "DOC-DEVOPS-008",
    ),
    "WG-SUPPLY-004": ("DOC-SUPPLY-011",),
    "WG-UIUX-004": ("DOC-UIUX-003", "DOC-UIUX-010"),
}


# Only cases admitted as an existing refresh or relation-covered case in the
# 2026-08-15 research packet receive pressure predicates here.  The admitted
# new Wargames own the other pressure rows.
PRESSURE_MAP: dict[str, tuple[str, ...]] = {
    "WG-AGENT-001": ("agent_coordination_cost_is_material",),
    "WG-SWARM-001": ("agent_coordination_cost_is_material",),
    "WG-AIML-004": ("evaluation_oracle_is_undecided",),
    "WG-ARCH-013": ("requires_independent_deployability",),
    "WG-ARCH-001": ("requires_independent_deployability",),
    "WG-DEL-005": ("test_fidelity_changes_outcome",),
    "WG-DEL-006": (
        "test_fidelity_changes_outcome",
        "evaluation_oracle_is_undecided",
    ),
    "WG-DEL-007": ("riskiest_assumption_is_unproved",),
    "WG-SUPPLY-001": ("producer_trust_is_unproved",),
    "WG-SUPPLY-003": ("dependency_update_changes_known_good",),
    "WG-DEVOPS-002": ("dependency_update_changes_known_good",),
    "WG-UIUX-003": (
        "serves_novice_and_expert_users",
        "house_style_costs_access_or_performance",
    ),
    "WG-UIUX-005": ("house_style_costs_access_or_performance",),
}


# Pressure-specific Doctrines supplement an explicitly cited legacy label.
# This is needed where the new pressure crosses pack boundaries.
PRESSURE_DOC_ADDITIONS: dict[str, tuple[str, ...]] = {
    "WG-AGENT-001": (
        "DOC-AGENT-008", "DOC-SWARM-012", "DOC-SWARM-013", "DOC-SWARM-024",
    ),
    "WG-UIUX-003": (
        "DOC-UIUX-009", "DOC-DISC-016", "DOC-HOUSE-004", "DOC-HOUSE-015",
        "DOC-UIUX-011", "DOC-UIUX-014",
    ),
    "WG-UIUX-005": (
        "DOC-HOUSE-004", "DOC-HOUSE-015", "DOC-UIUX-011", "DOC-UIUX-014",
    ),
    "WG-ARCH-001": ("DOC-ARCH-004", "DOC-ARCH-005"),
    "WG-DEVOPS-002": ("DOC-SUPPLY-005",),
}


CONSEQUENCE_OVERRIDES = {
    "WG-AIML-004",
    "WG-ARCH-013",
    "WG-ARCH-001",
    "WG-DEVOPS-002",
    "WG-SUPPLY-001",
    "WG-SUPPLY-003",
    "WG-UIUX-003",
    "WG-UIUX-005",
    "WG-DEL-005",
    "WG-DEL-006",
}


RELATION_CANDIDATES: dict[str, tuple[str, ...]] = {
    "WG-AGENT-001": ("DREL-AGENT-001",),
    "WG-SWARM-001": ("DREL-AGENT-001",),
    "WG-AIML-004": ("DREL-AIML-002",),
    "WG-ARCH-013": ("DREL-ARCH-003",),
    "WG-ARCH-001": ("DREL-ARCH-003",),
    "WG-DEL-005": ("DREL-DEL-002",),
    "WG-DEL-006": ("DREL-DEL-002", "DREL-AIML-002"),
    "WG-SUPPLY-001": ("DREL-SUPPLY-001",),
    "WG-SUPPLY-003": ("DREL-SUPPLY-002",),
    "WG-DEVOPS-002": ("DREL-SUPPLY-002",),
    "WG-UIUX-003": ("DREL-UIUX-001", "DREL-HOUSE-002"),
    "WG-UIUX-005": ("DREL-HOUSE-001",),
}


CONFLICT_WHEN_RELATED = {
    "WG-DEVOPS-002", "WG-SUPPLY-003", "WG-UIUX-003", "WG-UIUX-005",
}


SOURCE_ADDITIONS: dict[str, tuple[str, ...]] = {
    "WG-AGENT-001": ("EV-0452",),
    "WG-SWARM-001": ("EV-0452",),
    "WG-ARCH-013": ("EV-0564",),
    "WG-ARCH-001": ("EV-0564",),
    "WG-DEL-007": ("EV-0579",),
    "WG-DISC-001": ("EV-0579",),
    "WG-SUPPLY-001": ("EV-0549", "EV-0582"),
}


# The two packs below were authored before their fragment import assigned EV
# identities. These reviewed subsets replace the frozen placeholder with the
# evidence that bears on each decision, rather than citing every source in the
# pack indiscriminately.
SOURCE_OVERRIDES: dict[str, tuple[str, ...]] = {
    "WG-DATAENG-001": ("EV-0505", "EV-0507", "EV-0509", "EV-0510"),
    "WG-DATAENG-002": (
        "EV-0511", "EV-0513", "EV-0514", "EV-0515", "EV-0516",
    ),
    "WG-DATAENG-003": (
        "EV-0506", "EV-0508", "EV-0512", "EV-0513", "EV-0514",
    ),
    "WG-DATAENG-004": ("EV-0506", "EV-0508", "EV-0514"),
    "WG-IDENT-001": (
        "EV-0517", "EV-0518", "EV-0519", "EV-0520", "EV-0521",
        "EV-0522", "EV-0523",
    ),
    "WG-IDENT-002": ("EV-0524", "EV-0525", "EV-0526", "EV-0527"),
    "WG-IDENT-003": (
        "EV-0524", "EV-0525", "EV-0526", "EV-0527", "EV-0531",
    ),
    "WG-IDENT-004": ("EV-0528", "EV-0529", "EV-0530"),
}


RESEARCH_NOTES: dict[str, str] = {
    "WG-AGENT-001": (
        "EV-0452 is benchmark evidence across stated models, harnesses and task "
        "graphs. It supports decomposability, tool load and verifier placement as "
        "pressures, not a universal topology ranking or cut-off."
    ),
    "WG-SWARM-001": (
        "EV-0452 reports gains on decomposable work and losses on sequential, "
        "tool-heavy work. Transfer the direction only: coordination cost, baseline "
        "capability and central verification still need measurement on this task."
    ),
    "WG-ARCH-013": (
        "EV-0564 contributes quality-attribute scenarios, sensitivity points and "
        "trade-off points. Its multi-day facilitated method does not transfer as "
        "mandatory ceremony for a small venture."
    ),
    "WG-DEL-007": (
        "EV-0579 separates exploratory code from software that reaches users. It "
        "does not make every small change reversible: a spike still needs a named "
        "deletion or hardening boundary."
    ),
    "WG-DISC-001": (
        "EV-0579 supports a narrow exploratory path only while its deletion or "
        "promotion boundary remains explicit. Copying or retaining the result "
        "moves it back through the normal evidence gate."
    ),
    "WG-SUPPLY-001": (
        "EV-0582 says what provenance can establish about where, when and how an "
        "artefact was produced. EV-0549 preserves the hard limit: accurate "
        "provenance can still describe a malicious or flawed producer, so producer "
        "trust and safe use remain separate admission questions."
    ),
}


CHEAPEST_TEST_OVERRIDES = {
    "WG-ARCH-013": (
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
    "WG-SUPPLY-001": (
        "Verify a correctly attested artefact whose source or selected "
        "dependency is deliberately policy-bad. Record what provenance proves, "
        "what the admission verifier rejects, and which trust claim remains open."
    ),
    "WG-SUPPLY-003": (
        "Take one representative security update through the cooldown exception, "
        "suite, staged release, rollback and incident reconstruction path. Compare "
        "that proof with the known-good deployment it would replace."
    ),
    "WG-AGENT-001": (
        "Compare one bounded single-agent baseline with the smallest justified "
        "decomposition under the same task set, model budget and external "
        "verifier. Measure useful accepted work and coordination cost separately."
    ),
    "WG-SWARM-001": (
        "Compare one bounded single-agent baseline with the smallest justified "
        "lane split under the same task set, model budget and external verifier. "
        "Include merge and verification time in the result."
    ),
    "WG-AIML-004": (
        "Calibrate each proposed judge against the same human-labelled sample. "
        "Report agreement, disagreement, order effects, abstention and cost before "
        "allowing any judge to decide the claimed behaviour."
    ),
    "WG-UIUX-003": (
        "Run the same representative task with novice and frequent users. Record "
        "completion, error and search time, then repeat on the lowest supported "
        "device if house treatment or density changes performance."
    ),
    "WG-DISC-001": (
        "Build the narrowest representative path and list the assumptions it can "
        "actually test. Name its deletion or promotion boundary, then list the "
        "hardening evidence required before any retained artefact reaches users."
    ),
    "WG-UIUX-005": (
        "Exercise the hardest representative journey with reduced motion and on "
        "the lowest supported device, then inspect the accessibility tree and "
        "named assistive-technology path for the claimed criteria."
    ),
    "WG-HOUSE-001": (
        "Test one representative task with the intended audience under reduced "
        "motion and on the lowest supported device. Measure loading and frame "
        "behaviour before spending the optional house treatment."
    ),
}


RETIRED_SUCCESSORS: dict[str, tuple[str, ...]] = {
    "WG-VOX-001": ("WG-WRIT-003",),
    "WG-WEB-001": ("WG-UIUX-003",),
    "WG-WEB-003": ("WG-HOUSE-002",),
    "WG-WEB-005": ("WG-HOUSE-001",),
    "WG-WEB-006": ("WG-UIUX-003",),
    "WG-WEB-011": ("WG-HOUSE-001",),
    "WG-WEB-012": ("WG-HOUSE-004",),
    "WG-WEB-013": ("WG-UIUX-004", "WG-UIUX-006"),
    "WG-WEB-014": ("WG-HOUSE-004",),
}


RETIRED_PROSE = {
    "WG-WEB-001": "the retired historical web surface-register scenario",
    "WG-WEB-003": "the retired historical web container-choice scenario",
    "WG-WEB-005": "the retired historical web ornament-budget scenario",
    "WG-WEB-006": "the retired historical web density-and-audience scenario",
}


# The frozen inception source predates the structured RULINGS file and its
# resulting scale-matrix growth. Keep the decision semantics while referring to
# the matrix as the canonical file-count surface, so another template addition
# cannot make this generated Wargame stale.
OPTION_REFRESHES: dict[str, str] = {
    "WG-EOS-001": """### S. Small venture shape

The S column in `kernel/SCALE_MATRIX.md` defines the seed and operating
surface. It carries one human and one task surface without organisational
charters or integrator tooling. It costs little to run, but offers no
separation of duties or compliance machinery.

### ORG. Organisational shape

The ORG column in `kernel/SCALE_MATRIX.md` defines the larger seed and
operating surface. It adds the constitution, boot and testing law,
artefact shapes, questions, playbooks, graph build, situational roles,
cadence and claims. Work becomes task records with derived views and can
separate duties where the router requires it. Verification bandwidth
becomes the limiting resource.""",
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


def _string_mapping(value: object, field: str) -> dict[str, str]:
    if not isinstance(value, dict) or not all(
        isinstance(key, str) and isinstance(item, str)
        for key, item in value.items()
    ):
        raise WargameMigrationError(
            f"naming baseline field {field} must be a string mapping"
        )
    return dict(value)


def _string_list(value: object, field: str) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(item, str) for item in value
    ):
        raise WargameMigrationError(
            f"naming baseline field {field} must be a string list"
        )
    return list(value)


def _load_naming_contract(root: Path) -> dict[str, object]:
    path = root / NAMING_BASELINE
    try:
        contract = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValueError) as exc:
        raise WargameMigrationError(
            f"cannot read naming baseline: {NAMING_BASELINE}"
        ) from exc
    if not isinstance(contract, dict):
        raise WargameMigrationError("naming baseline must contain an object")
    if contract.get("schema_version") != 1 or contract.get("task") != "T-0028":
        raise WargameMigrationError("unsupported naming baseline contract")
    identifiers = _string_mapping(
        contract.get("identifier_migration"), "identifier_migration"
    )
    targets = _string_mapping(contract.get("target_wargames"), "target_wargames")
    counts = contract.get("counts")
    if not isinstance(counts, dict):
        raise WargameMigrationError("naming baseline counts must contain an object")
    if len(identifiers) != 103:
        raise WargameMigrationError("naming baseline must contain 103 ID aliases")
    if len(targets) != int(counts.get("wargames", -1)):
        raise WargameMigrationError(
            "naming baseline Wargame count does not match its target paths"
        )
    if len(set(identifiers.values())) != len(identifiers):
        raise WargameMigrationError("naming baseline ID aliases are not one-to-one")
    if set(identifiers.values()) - set(targets):
        raise WargameMigrationError(
            "a naming baseline ID alias has no canonical Wargame target"
        )
    _string_list(contract.get("canonical_collections"), "canonical_collections")
    _string_list(
        contract.get("retired_collection_paths"), "retired_collection_paths"
    )
    _string_list(contract.get("optional_collections"), "optional_collections")
    _string_mapping(
        contract.get("public_file_migration"), "public_file_migration"
    )
    _string_mapping(
        contract.get("lesson_disposition_migration"),
        "lesson_disposition_migration",
    )
    return contract


def canonical_procedures(root: Path) -> dict[str, str]:
    """Map the frozen 114 source identities to their reviewed current targets."""

    root = Path(root).resolve()
    frozen = frozen_procedures(root)
    contract = _load_naming_contract(root)
    return _canonical_inventory(frozen, contract)


def _canonical_inventory(
    frozen: Mapping[str, str], contract: Mapping[str, object]
) -> dict[str, str]:
    identifiers = _string_mapping(
        contract["identifier_migration"], "identifier_migration"
    )
    targets = _string_mapping(contract["target_wargames"], "target_wargames")
    result: dict[str, str] = {}
    for source_identifier, source_path in sorted(frozen.items()):
        identifier = identifiers.get(source_identifier, source_identifier)
        target_path = targets.get(identifier)
        if target_path is None:
            raise WargameMigrationError(
                f"frozen Wargame has no canonical target: {source_identifier}"
            )
        match = _CANONICAL_PROCEDURE_PATH.fullmatch(target_path)
        if not match or match.group(1) != identifier:
            raise WargameMigrationError(
                f"invalid canonical Wargame target: {identifier}: {target_path}"
            )
        source_parts = PurePosixPath(source_path).parts
        target_parts = PurePosixPath(target_path).parts
        if source_parts[0] == "packs" and (
            target_parts[0] != "packs" or target_parts[1] != source_parts[1]
        ):
            raise WargameMigrationError(
                f"Wargame target changes owning pack: {source_path} -> {target_path}"
            )
        if identifier in result:
            raise WargameMigrationError(
                f"two frozen Wargames map to current ID {identifier}"
            )
        result[identifier] = target_path
    if len(result) != FROZEN_COUNT:
        raise WargameMigrationError(
            f"canonical inventory has {len(result)} rows, expected {FROZEN_COUNT}"
        )
    return result


def _source_target_paths(contract: Mapping[str, object]) -> dict[str, str]:
    identifiers = _string_mapping(
        contract["identifier_migration"], "identifier_migration"
    )
    targets = _string_mapping(contract["target_wargames"], "target_wargames")
    inverse = {current: legacy for legacy, current in identifiers.items()}
    paths: dict[str, str] = {}
    for identifier, target in targets.items():
        source_identifier = inverse.get(identifier, identifier)
        pure = PurePosixPath(target)
        if len(pure.parts) >= 4 and pure.parts[0] == "packs":
            parts = list(pure.parts)
            if parts[2] != "wargames":
                raise WargameMigrationError(
                    f"pack Wargame target is outside wargames/: {target}"
                )
            parts[2] = "guides"
            name = parts[-1]
            if not name.startswith(identifier + "-"):
                raise WargameMigrationError(
                    f"Wargame target basename does not begin with its ID: {target}"
                )
            parts[-1] = source_identifier + name[len(identifier) :]
            source = PurePosixPath(*parts).as_posix()
        else:
            source = target
        if source in paths:
            raise WargameMigrationError(
                f"two canonical Wargames share historical path {source}"
            )
        paths[source] = target
    return paths


def _canonicalise_text(text: str, contract: Mapping[str, object]) -> str:
    """Apply the reviewed naming substitutions to generated historical text."""

    for old, new in sorted(
        _source_target_paths(contract).items(),
        key=lambda item: (-len(item[0]), item[0]),
    ):
        text = text.replace(old, new)

    identifiers = _string_mapping(
        contract["identifier_migration"], "identifier_migration"
    )
    for old, new in sorted(identifiers.items()):
        pattern = re.compile(
            rf"(?<!{_IDENTIFIER_BOUNDARY}){re.escape(old)}"
            rf"(?!{_IDENTIFIER_BOUNDARY})"
        )
        text = pattern.sub(new, text)

    retired = _string_list(
        contract["retired_collection_paths"], "retired_collection_paths"
    )
    canonical = _string_list(
        contract["canonical_collections"], "canonical_collections"
    )
    optional = _string_list(
        contract["optional_collections"], "optional_collections"
    )
    if len(retired) != 4 or len(canonical) < 4 or len(optional) != 1:
        raise WargameMigrationError("unsupported collection naming contract")
    collection_pairs = (
        (retired[0], canonical[1]),
        (retired[1], canonical[2]),
        (retired[2], canonical[3]),
        (retired[3], optional[0]),
    )
    packs = contract.get("packs")
    if not isinstance(packs, dict) or not all(isinstance(key, str) for key in packs):
        raise WargameMigrationError("naming baseline packs must contain an object")
    for old, new in collection_pairs:
        for prefix in ("(", "`"):
            text = text.replace(prefix + old + "/", prefix + new + "/")
        for pack in packs:
            text = text.replace(
                f"packs/{pack}/{old}/", f"packs/{pack}/{new}/"
            )

    public = _string_mapping(
        contract["public_file_migration"], "public_file_migration"
    )
    for old, new in public.items():
        text = text.replace(PurePosixPath(old).name, PurePosixPath(new).name)
    text = text.replace("GUIDE" + "_INDEX.md", "WARGAME_INDEX.md")
    dispositions = _string_mapping(
        contract["lesson_disposition_migration"],
        "lesson_disposition_migration",
    )
    for old, new in dispositions.items():
        pattern = re.compile(rf"(?<![a-z-]){re.escape(old)}(?![a-z-])")
        text = pattern.sub(new, text)

    # The frozen procedures predate the public Wargame vocabulary. Preserve
    # genuine qualified documents such as style guides and interview guides,
    # but do not let a live Wargame call itself a guide on replay.
    entity_terms = (
        (r"\bThis\s+guide\b", "This Wargame"),
        (r"\bthis\s+guide\b", "this Wargame"),
        (r"\bThe\s+guide\b", "The Wargame"),
        (r"\bthe\s+guide\b", "the Wargame"),
        (r"\btopology\s+guide\b", "topology Wargame"),
        (r"\boracle-strategy\s+guide\b", "oracle-strategy Wargame"),
        (r"\btransformation-tool\s+guide\b", "transformation-tool Wargame"),
    )
    for pattern, replacement in entity_terms:
        text = re.sub(pattern, replacement, text)
    return text


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


def _read_frozen(
    root: Path,
    inventory: Mapping[str, str],
    canonical: Mapping[str, str],
    contract: Mapping[str, object],
) -> dict[str, Procedure]:
    identifiers = _string_mapping(
        contract["identifier_migration"], "identifier_migration"
    )
    procedures: dict[str, Procedure] = {}
    for source_identifier, source_path in sorted(inventory.items()):
        identifier = identifiers.get(source_identifier, source_identifier)
        path = canonical[identifier]
        text = _normalise(
            _git(root, "show", f"{BASELINE_COMMIT}:{source_path}")
        )
        parsed = parse_frontmatter(text)
        procedures[identifier] = Procedure(
            identifier=identifier,
            path=path,
            source_identifier=source_identifier,
            source_path=source_path,
            text=text,
            metadata=dict(parsed.data),
            body=parsed.body.strip(),
        )
    return procedures


def _check_live_identity(root: Path, inventory: Mapping[str, str]) -> None:
    seen: dict[str, list[str]] = {}
    candidates = sorted(root.glob("packs/*/wargames/*.md"))
    candidates.extend(sorted(root.glob("inception/wargames/*.md")))
    for path in candidates:
        rel = path.relative_to(root).as_posix()
        match = _CANONICAL_PROCEDURE_PATH.fullmatch(rel)
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
    for identifier, expected in sorted(inventory.items()):
        paths = seen.get(identifier, [])
        if paths != [expected]:
            raise WargameMigrationError(
                f"canonical identity/path drift: {identifier}: {paths!r}, "
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


def _challenge_questions(preconditions: str, limit: int = 2) -> list[str]:
    """Return compact legacy engagement questions for a falsification test."""

    questions: list[str] = []
    lines = preconditions.splitlines()
    index = 0
    while index < len(lines) and len(questions) < limit:
        line = lines[index]
        if not line.startswith("- "):
            index += 1
            continue
        parts = [line[2:].strip()]
        index += 1
        while index < len(lines):
            continuation = lines[index]
            if continuation.startswith("- ") or not continuation.strip():
                break
            parts.append(continuation.strip())
            index += 1
        questions.append(_clean_excerpt(" ".join(parts), 260))
    if not questions:
        questions.append(_first_question(preconditions))
    return questions


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
    sources = list(SOURCE_OVERRIDES.get(
        procedure.identifier, tuple(_values(source.get("sources"))),
    ))
    if not sources:
        sources = ["kernel/SCALE_MATRIX.md"]
    for identifier in SOURCE_ADDITIONS.get(procedure.identifier, ()):
        if identifier not in sources:
            sources.append(identifier)
    always_walk = procedure.identifier in {
        "WG-EOS-001", "WG-EOS-002",
        "WG-SEC-001", "WG-SEC-002", "WG-SEC-003", "WG-SEC-004",
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
    options = OPTION_REFRESHES.get(procedure.identifier, options)
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
    research_note = RESEARCH_NOTES.get(procedure.identifier)
    if not counter_parts and not research_note:
        questions = _challenge_questions(preconditions)
        tested = " and ".join(f"**{question}**" for question in questions)
        counter_parts.extend((
            "### Counter-evidence to test", "",
            "Facts that change the engagement answers above can overturn the "
            f"safe default. Test {tested} against the selected option. A "
            "contrary result counts only when it uses the same representative "
            "constraints and changes the decision rule, rather than merely "
            "preferring another style.",
        ))
    if research_note:
        counter_parts.extend(("### Current research boundary", "", research_note))
    if worked:
        counter_parts.extend((
            "### Historical ruling boundary", "", _worked_ruling_note(worked),
        ))
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
    naming_contract: Mapping[str, object],
) -> tuple[str, dict]:
    targets = _procedure_targets(procedure, labels, doctrines)
    metadata = _metadata(procedure, doctrines, targets, live_relations)
    body = _render_body(procedure, doctrines, targets, metadata)
    text = _canonicalise_text(
        _render_frontmatter(metadata) + "\n\n" + body,
        naming_contract,
    )
    return text, {
        "id": procedure.source_identifier,
        "path": procedure.source_path,
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


def _retired_rows(
    root: Path, naming_contract: Mapping[str, object]
) -> list[dict]:
    manifest = json.loads((root / "archive/RETIRED_IDS.json").read_text(encoding="utf-8"))
    identifiers = manifest.get("ids") or {}
    if len(identifiers) != 22:
        raise WargameMigrationError(
            f"retired Wargame inventory has {len(identifiers)} rows, expected 22"
        )
    rows = []
    aliases = _string_mapping(
        naming_contract["identifier_migration"], "identifier_migration"
    )
    historical = {current: legacy for legacy, current in aliases.items()}
    for identifier, path in sorted(identifiers.items()):
        successors = tuple(
            historical.get(successor, successor)
            for successor in RETIRED_SUCCESSORS.get(identifier, ())
        )
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
    for path in sorted(root.glob("packs/*/relations/DREL-*.json")):
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
    naming_contract = _load_naming_contract(root)
    canonical = _canonical_inventory(inventory, naming_contract)
    _check_live_identity(root, canonical)
    procedures = _read_frozen(root, inventory, canonical, naming_contract)
    doctrines, labels, doctrine_ledger = _load_doctrines(root)
    live_relations = _live_relation_ids(root)

    rendered: dict[str, str] = {}
    rows = []
    ordered = sorted(
        procedures.values(), key=lambda procedure: procedure.source_identifier
    )
    for procedure in ordered:
        text, row = render_procedure(
            procedure,
            doctrines,
            labels,
            live_relations,
            naming_contract,
        )
        rendered[procedure.path] = text
        rows.append(row)

    retired = _retired_rows(root, naming_contract)
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
