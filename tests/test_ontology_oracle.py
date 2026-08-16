"""Frozen acceptance oracle for the Doctrine and Wargaming rebuild.

Authored independently before ``tools.eos.ontology`` exists. The tests
import that future module only inside test functions, so pytest can
collect and hash this oracle before implementation. Missing ontology
code is an explicit test failure, never a collection error.

This file is frozen for T-0026. Amendments are append-only and need an
independent author recorded on the task. The original 114 procedure
identities and paths below were read from main at 7f56e4e. They are
identities, not a target count: later procedures may be added as WG ids,
but none of these may be renumbered, moved or silently disappear.
"""

from __future__ import annotations

import importlib
import json
import re
import shutil
import subprocess
from collections.abc import Mapping
from pathlib import Path

import pytest

from tools.eos.frontmatter import parse as parse_frontmatter


REPO = Path(__file__).resolve().parents[1]

FROZEN_PROCEDURES = {
    "WG-EOS-001": "inception/wargames/WG-EOS-001-venture-scale.md",
    "WG-EOS-002": "inception/wargames/WG-EOS-002-repo-shape.md",
    "GD-AGENT-001": "packs/agentic-development/guides/GD-AGENT-001-topology-selection.md",
    "GD-AGENT-002": "packs/agentic-development/guides/GD-AGENT-002-context-engineering.md",
    "GD-AGENT-003": "packs/agentic-development/guides/GD-AGENT-003-spawn-a-subagent.md",
    "GD-AGENT-004": "packs/agentic-development/guides/GD-AGENT-004-verification-oracle.md",
    "GD-SWARM-001": "packs/agentic-swarm/guides/GD-SWARM-001-swarm-or-single-agent.md",
    "GD-SWARM-002": "packs/agentic-swarm/guides/GD-SWARM-002-cut-the-partition.md",
    "GD-SWARM-003": "packs/agentic-swarm/guides/GD-SWARM-003-who-holds-the-plan.md",
    "GD-SWARM-004": "packs/agentic-swarm/guides/GD-SWARM-004-verifying-a-lane.md",
    "GD-AIML-001": "packs/ai-ml-llm/guides/GD-AIML-001-acceptance-evidence.md",
    "GD-AIML-002": "packs/ai-ml-llm/guides/GD-AIML-002-knowledge-source.md",
    "GD-AIML-003": "packs/ai-ml-llm/guides/GD-AIML-003-who-grades-the-output.md",
    "GD-AIML-004": "packs/ai-ml-llm/guides/GD-AIML-004-prompt-maintenance.md",
    "GD-AIML-005": "packs/ai-ml-llm/guides/GD-AIML-005-model-lifecycle-and-cost.md",
    "GD-API-001": "packs/api-integration/guides/GD-API-001-contract-authoring.md",
    "GD-API-002": "packs/api-integration/guides/GD-API-002-versioning-and-breaking-change.md",
    "GD-API-003": "packs/api-integration/guides/GD-API-003-webhook-trust.md",
    "GD-API-004": "packs/api-integration/guides/GD-API-004-boundary-shape.md",
    "GD-API-005": "packs/api-integration/guides/GD-API-005-collection-traversal.md",
    "GD-ARCH-001": "packs/architecture/guides/GD-ARCH-001-deployment-shape.md",
    "WG-ARCH-001": "packs/architecture/guides/WG-ARCH-001-boundary-enforcement.md",
    "WG-ARCH-002": "packs/architecture/guides/WG-ARCH-002-orm-or-raw-sql.md",
    "WG-ARCH-003": "packs/architecture/guides/WG-ARCH-003-derived-state.md",
    "WG-ARCH-004": "packs/architecture/guides/WG-ARCH-004-job-execution.md",
    "WG-ARCH-005": "packs/architecture/guides/WG-ARCH-005-contract-seam.md",
    "WG-ARCH-006": "packs/architecture/guides/WG-ARCH-006-change-proof.md",
    "WG-ARCH-007": "packs/architecture/guides/WG-ARCH-007-vendor-seams.md",
    "WG-ARCH-008": "packs/architecture/guides/WG-ARCH-008-database-topology.md",
    "GD-BLM-001": "packs/business-logic-modelling/guides/GD-BLM-001-model-shape.md",
    "GD-BLM-002": "packs/business-logic-modelling/guides/GD-BLM-002-rule-placement.md",
    "GD-BLM-003": "packs/business-logic-modelling/guides/GD-BLM-003-money-representation.md",
    "GD-BLM-004": "packs/business-logic-modelling/guides/GD-BLM-004-time-modelling.md",
    "GD-BLM-005": "packs/business-logic-modelling/guides/GD-BLM-005-state-or-events.md",
    "GD-BMP-001": "packs/business-model-pricing/guides/GD-BMP-001-price-anchor.md",
    "GD-BMP-002": "packs/business-model-pricing/guides/GD-BMP-002-charging-unit.md",
    "GD-BMP-003": "packs/business-model-pricing/guides/GD-BMP-003-try-before-paying.md",
    "GD-BMP-004": "packs/business-model-pricing/guides/GD-BMP-004-repricing-trigger.md",
    "GD-COD-001": "packs/coding/guides/GD-COD-001-oracle-strategy.md",
    "GD-COD-002": "packs/coding/guides/GD-COD-002-review-gate.md",
    "GD-COD-003": "packs/coding/guides/GD-COD-003-failure-mode-contract.md",
    "GD-COD-004": "packs/coding/guides/GD-COD-004-pin-then-change.md",
    "GD-COD-005": "packs/coding/guides/GD-COD-005-repo-shape.md",
    "GD-DATA-001": "packs/data-analytics/guides/GD-DATA-001-quality-gate-placement.md",
    "GD-DATA-002": "packs/data-analytics/guides/GD-DATA-002-model-shape.md",
    "GD-DATA-003": "packs/data-analytics/guides/GD-DATA-003-experiment-stopping.md",
    "GD-DATA-004": "packs/data-analytics/guides/GD-DATA-004-storage-shape.md",
    "GD-DATA-005": "packs/data-analytics/guides/GD-DATA-005-event-contract.md",
    "GD-DATAENG-001": "packs/data-engineering/guides/GD-DATAENG-001-ingestion-shape.md",
    "GD-DATAENG-002": "packs/data-engineering/guides/GD-DATAENG-002-idempotent-reprocess.md",
    "GD-DATAENG-003": "packs/data-engineering/guides/GD-DATAENG-003-processing-window.md",
    "GD-DATAENG-004": "packs/data-engineering/guides/GD-DATAENG-004-late-arrivals.md",
    "WG-DEL-005": "packs/delivery-testing/guides/WG-DEL-005-test-doubles.md",
    "WG-DEL-006": "packs/delivery-testing/guides/WG-DEL-006-oracle-independence.md",
    "WG-DEL-007": "packs/delivery-testing/guides/WG-DEL-007-test-timing.md",
    "GD-DEVOPS-001": "packs/devops-reliability/guides/GD-DEVOPS-001-schema-change-strategy.md",
    "GD-DEVOPS-002": "packs/devops-reliability/guides/GD-DEVOPS-002-release-control.md",
    "GD-DEVOPS-003": "packs/devops-reliability/guides/GD-DEVOPS-003-error-budget-dial.md",
    "GD-DEVOPS-004": "packs/devops-reliability/guides/GD-DEVOPS-004-reliability-measures.md",
    "WG-OPS-003": "packs/devops-reliability/guides/WG-OPS-003-restore-proof.md",
    "GD-DOCS-001": "packs/docs-dx/guides/GD-DOCS-001-truth-location.md",
    "GD-DOCS-002": "packs/docs-dx/guides/GD-DOCS-002-executable-examples.md",
    "GD-DOCS-003": "packs/docs-dx/guides/GD-DOCS-003-changelog-ownership.md",
    "GD-DOCS-004": "packs/docs-dx/guides/GD-DOCS-004-failure-messages.md",
    "GD-DOCS-005": "packs/docs-dx/guides/GD-DOCS-005-blocking-checks.md",
    "GD-IDENT-001": "packs/identity-access/guides/GD-IDENT-001-authorisation-model.md",
    "GD-IDENT-002": "packs/identity-access/guides/GD-IDENT-002-session-or-token.md",
    "GD-IDENT-003": "packs/identity-access/guides/GD-IDENT-003-provider-or-self-hosted.md",
    "GD-IDENT-004": "packs/identity-access/guides/GD-IDENT-004-tenant-isolation.md",
    "GD-LEGAL-001": "packs/legal-licensing/guides/GD-LEGAL-001-copyleft-trigger.md",
    "GD-LEGAL-002": "packs/legal-licensing/guides/GD-LEGAL-002-compliance-posture.md",
    "GD-LEGAL-003": "packs/legal-licensing/guides/GD-LEGAL-003-outbound-licence.md",
    "GD-LEGAL-004": "packs/legal-licensing/guides/GD-LEGAL-004-inbound-rights.md",
    "GD-LEGAL-005": "packs/legal-licensing/guides/GD-LEGAL-005-lawful-extraction.md",
    "GD-MKTG-001": "packs/marketing-growth/guides/GD-MKTG-001-growth-philosophy.md",
    "GD-MKTG-002": "packs/marketing-growth/guides/GD-MKTG-002-consent-route.md",
    "GD-MKTG-003": "packs/marketing-growth/guides/GD-MKTG-003-effect-measurement.md",
    "GD-MKTG-004": "packs/marketing-growth/guides/GD-MKTG-004-content-provenance.md",
    "GD-NAT-001": "packs/native-client/guides/GD-NAT-001-client-architecture.md",
    "GD-NAT-002": "packs/native-client/guides/GD-NAT-002-offline-write-model.md",
    "GD-NAT-003": "packs/native-client/guides/GD-NAT-003-release-path.md",
    "GD-NAT-004": "packs/native-client/guides/GD-NAT-004-a11y-profile.md",
    "GD-HOUSE-001": "packs/pattertech-house/guides/GD-HOUSE-001-light-posture.md",
    "GD-HOUSE-002": "packs/pattertech-house/guides/GD-HOUSE-002-container-choice.md",
    "GD-HOUSE-003": "packs/pattertech-house/guides/GD-HOUSE-003-polarity-register.md",
    "GD-HOUSE-004": "packs/pattertech-house/guides/GD-HOUSE-004-figure-austerity.md",
    "GD-DISC-001": "packs/product-discovery/guides/GD-DISC-001-discovery-depth.md",
    "GD-DISC-002": "packs/product-discovery/guides/GD-DISC-002-user-evidence-source.md",
    "GD-DISC-003": "packs/product-discovery/guides/GD-DISC-003-choosing-between-opportunities.md",
    "GD-DISC-004": "packs/product-discovery/guides/GD-DISC-004-acceptance-criteria-form.md",
    "GD-RESEARCH-001": "packs/research-knowledge/guides/GD-RESEARCH-001-when-to-stop.md",
    "GD-RESEARCH-002": "packs/research-knowledge/guides/GD-RESEARCH-002-where-the-base-lives.md",
    "GD-RESEARCH-003": "packs/research-knowledge/guides/GD-RESEARCH-003-superseding-a-source.md",
    "GD-RESEARCH-004": "packs/research-knowledge/guides/GD-RESEARCH-004-a-source-that-speaks-to-you.md",
    "GD-SEC-001": "packs/security-privacy/guides/GD-SEC-001-injection-defence.md",
    "GD-SEC-002": "packs/security-privacy/guides/GD-SEC-002-secret-protection.md",
    "GD-SEC-003": "packs/security-privacy/guides/GD-SEC-003-assurance-grading.md",
    "GD-SEC-004": "packs/security-privacy/guides/GD-SEC-004-external-action-approval.md",
    "GD-SUPPLY-001": "packs/supply-chain-integrity/guides/GD-SUPPLY-001-provenance-and-verification.md",
    "GD-SUPPLY-002": "packs/supply-chain-integrity/guides/GD-SUPPLY-002-signing-identity.md",
    "GD-SUPPLY-003": "packs/supply-chain-integrity/guides/GD-SUPPLY-003-pinning-cadence.md",
    "GD-SUPPLY-004": "packs/supply-chain-integrity/guides/GD-SUPPLY-004-vendor-or-depend.md",
    "GD-SUPPORT-001": "packs/support-operations/guides/GD-SUPPORT-001-triage-pattern.md",
    "GD-SUPPORT-002": "packs/support-operations/guides/GD-SUPPORT-002-close-policy.md",
    "GD-SUPPORT-003": "packs/support-operations/guides/GD-SUPPORT-003-declaration-route.md",
    "GD-SUPPORT-004": "packs/support-operations/guides/GD-SUPPORT-004-support-measurement.md",
    "GD-UIUX-001": "packs/ui-ux/guides/GD-UIUX-001-design-philosophy.md",
    "GD-UIUX-002": "packs/ui-ux/guides/GD-UIUX-002-component-sourcing.md",
    "GD-UIUX-003": "packs/ui-ux/guides/GD-UIUX-003-a11y-assurance.md",
    "GD-UIUX-004": "packs/ui-ux/guides/GD-UIUX-004-token-source.md",
    "GD-WRIT-001": "packs/writing-content/guides/GD-WRIT-001-clarity-philosophy.md",
    "GD-WRIT-002": "packs/writing-content/guides/GD-WRIT-002-message-structure.md",
    "GD-WRIT-003": "packs/writing-content/guides/GD-WRIT-003-voice-scope.md",
    "GD-WRIT-004": "packs/writing-content/guides/GD-WRIT-004-prose-gate.md",
}

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

ARCHITECTURE_COMPATIBILITY_ANCHORS = (
    "B1", "B4", "B5", "D1", "D2", "D3", "D4", "D5", "D6",
    "D7", "D8", "D9", "D10", "D11", "D12",
)
DATA_COMPATIBILITY_ANCHORS = (
    "B3", "B4", "B5", "D1", "D2", "D3", "D4", "D5", "D6",
    "D7", "D8", "D9", "D10", "D11",
)


def _api():
    """Load the future API lazily and fail with the missing contract."""
    try:
        module = importlib.import_module("tools.eos.ontology")
    except ModuleNotFoundError as exc:
        if exc.name == "tools.eos.ontology":
            pytest.fail(
                "T-0026 ontology implementation is absent: create "
                "tools/eos/ontology.py with KnowledgeResolver, "
                "match_knowledge and validate_rulings"
            )
        raise
    required = ("KnowledgeResolver", "match_knowledge", "validate_rulings")
    missing = [name for name in required if not hasattr(module, name)]
    assert not missing, "ontology API missing: " + ", ".join(missing)
    return module


def _value(obj, *names):
    for name in names:
        if isinstance(obj, Mapping) and name in obj:
            return obj[name]
        if hasattr(obj, name):
            return getattr(obj, name)
    raise AssertionError(f"none of {names!r} found on {obj!r}")


def _resolution_id(obj):
    return _value(obj, "canonical_id", "identifier", "id")


def _item_ids(rows):
    out = set()
    for row in rows:
        if isinstance(row, str):
            out.add(row)
        else:
            out.add(_resolution_id(row))
    return out


def _problem_text(problems):
    rendered = []
    for problem in problems:
        if isinstance(problem, Mapping):
            rendered.append(" ".join(str(v) for v in problem.values()))
        else:
            rendered.append(" ".join(
                str(getattr(problem, name, ""))
                for name in ("code", "path", "identifier", "message")
            ))
    return "\n".join(rendered).lower()


def _copy_schemas(root):
    source = REPO / "kernel" / "schemas"
    if source.is_dir():
        shutil.copytree(source, root / "kernel" / "schemas",
                        dirs_exist_ok=True)


def _write_pack(root, name, *, depends_on=()):
    path = root / "packs" / name / "PACK.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    dependencies = ", ".join(depends_on)
    path.write_text(
        "---\n"
        f"summary: Fixture pack {name}\n"
        "kind: rule\n"
        "authority: default\n"
        "applies_when: [has_ui]\n"
        "sources: [EV-TEST-001]\n"
        "review: 2030-01\n"
        "type: guide\n"
        "tags: [eos]\n"
        f"depends_on: [{dependencies}]\n"
        "---\n\n"
        f"# {name}\n\nFixture pack.\n",
        encoding="utf-8", newline="\n",
    )
    return path


def _write_doctrine(root, identifier, *, pack="test", applies="has_ui",
                    challenge="expert_users"):
    path = root / "packs" / pack / "doctrines" / f"{identifier}-fixture.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "---\n"
        f"id: {identifier}\n"
        "statement: Prefer the reversible choice while evidence is weak.\n"
        "kind: doctrine\n"
        "type: doctrine\n"
        "authority: default\n"
        "basis: decision\n"
        "evidence_grade: asserted\n"
        "scope: estate\n"
        f"applies_when: [{applies}]\n"
        f"challenge_triggers: [{challenge}]\n"
        "sources: [EV-TEST-001]\n"
        "review: 2030-01\n"
        "lifecycle: active\n"
        "verification_refs: [checks/fixture]\n"
        "---\n\n"
        f"# {identifier}\n\nThe statement above is the atomic rule.\n",
        encoding="utf-8", newline="\n",
    )
    return path


def _write_wargame(root, identifier, *, pack="test",
                   doctrine="DOC-TEST-001", engagement="expert_users",
                   consequence="routine", relation=""):
    path = root / "packs" / pack / "guides" / f"{identifier}-fixture.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    relation_list = relation if relation else ""
    headings = "\n\n".join(
        f"## {heading}\n\nFixture content for {heading.lower()}."
        for heading in WARGAME_HEADINGS
    )
    path.write_text(
        "---\n"
        f"id: {identifier}\n"
        "summary: Decide the fixture pressure without choosing an outcome.\n"
        "kind: wargame\n"
        "type: wargame\n"
        "scenario_modes: [selection, conflict]\n"
        f"applicable_doctrines: [{doctrine}]\n"
        "applies_when: [has_ui]\n"
        f"engages_when: [{engagement}]\n"
        f"consequence: {consequence}\n"
        f"relations: [{relation_list}]\n"
        "sources: [EV-TEST-001]\n"
        "review: 2030-01\n"
        "lifecycle: active\n"
        "scope: estate\n"
        "---\n\n"
        f"# {identifier}: fixture pressure\n\n{headings}\n",
        encoding="utf-8", newline="\n",
    )
    return path


def _write_relation(root, identifier, *, pack="test",
                    owner="DOC-TEST-001", relation="tensions_with",
                    target="DOC-TEST-002", wargame="WG-TEST-001"):
    path = (root / "packs" / pack / "doctrines" / "relations" /
            f"{identifier}.json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({
        "id": identifier,
        "owner_doctrine": owner,
        "relation": relation,
        "target": target,
        "conditions": ["expert_users"],
        "status": "active",
        "evidence": ["EV-TEST-001"],
        "fallback": "Keep the current default and run the named Wargame.",
        "wargame": wargame,
    }, indent=1) + "\n", encoding="utf-8", newline="\n")
    return path


def _knowledge_repo(tmp_path):
    root = tmp_path / "knowledge"
    root.mkdir()
    _copy_schemas(root)
    _write_pack(root, "base")
    _write_pack(root, "test", depends_on=("base",))
    _write_doctrine(root, "DOC-TEST-001")
    _write_doctrine(root, "DOC-TEST-002", challenge="safety_unknown")
    _write_wargame(root, "WG-TEST-001", engagement="expert_users")
    _write_wargame(root, "WG-TEST-002", doctrine="DOC-TEST-002",
                   engagement="safety_unknown", consequence="high")
    _write_wargame(root, "WG-TEST-003", engagement="routine_pressure")
    _write_relation(root, "DREL-TEST-001")
    return root


def _git(root, *args):
    return subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, text=True,
        encoding="utf-8", check=True,
    ).stdout.strip()


def _init_git(root):
    _git(root, "init", "-q", "-b", "main")
    _git(root, "config", "user.email", "oracle@example.invalid")
    _git(root, "config", "user.name", "Ontology Oracle")
    _git(root, "config", "commit.gpgsign", "false")


def _commit(root, message):
    _git(root, "add", ".")
    _git(root, "commit", "-q", "-m", message)
    return _git(root, "rev-parse", "HEAD")


def _retired_repo(tmp_path):
    root = tmp_path / "retired"
    root.mkdir()
    _init_git(root)
    _write_pack(root, "gone")
    old = _write_wargame(root, "WG-GONE-001", pack="gone")
    _commit(root, "live definition")
    _git(root, "tag", "archive/v1-final")
    old.unlink()
    manifest = root / "archive" / "RETIRED_IDS.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps({
        "version": 1,
        "tag": "archive/v1-final",
        "ids": {
            "WG-GONE-001":
                "packs/gone/guides/WG-GONE-001-fixture.md",
        },
    }, indent=1) + "\n", encoding="utf-8", newline="\n")
    _commit(root, "retire definition")
    return root


def _valid_rulings(wargame="WG-TEST-001"):
    return {
        "version": 1,
        "venture": "Fixture",
        "eos_commit": "WORKTREE",
        "selection_log": [{
            "wargame": wargame,
            "disposition": "selected",
            "reason": "The pressure is true.",
            "ruling": "RUL-TEST-001",
        }],
        "rulings": [{
            "id": "RUL-TEST-001",
            "wargame": wargame,
            "doctrines": ["DOC-TEST-001"],
            "decision": "Option A",
            "execution": "argued",
            "reason": "The cheapest test discriminated the options.",
            "decided": "2030-01-02",
            "departures": [],
            "binding_scope_changes": [],
        }],
    }


# --- Frozen estate identities -----------------------------------------


def test_frozen_inventory_is_114_distinct_id_path_pairs():
    assert len(FROZEN_PROCEDURES) == 114
    assert len(set(FROZEN_PROCEDURES.values())) == 114
    assert all(re.fullmatch(r"(?:GD|WG)-[A-Z]+-\d{3}", identifier)
               for identifier in FROZEN_PROCEDURES)


def test_frozen_paths_still_exist_without_relocation():
    missing = [path for path in FROZEN_PROCEDURES.values()
               if not (REPO / path).is_file()]
    assert missing == []


def test_every_frozen_identity_resolves_to_its_frozen_path():
    api = _api()
    resolver = api.KnowledgeResolver.open(REPO)
    mismatches = []
    for identifier, path in FROZEN_PROCEDURES.items():
        resolved = resolver.resolve(identifier)
        if resolved is None or _value(resolved, "path") != path:
            mismatches.append((identifier, path, resolved))
    assert mismatches == []


def test_no_new_gd_identity_is_issued():
    api = _api()
    resolver = api.KnowledgeResolver.open(REPO)
    current = {_resolution_id(row) for row in resolver.list("wargame")}
    introduced_gd = sorted(identifier for identifier in current
                           if identifier.startswith("GD-")
                           and identifier not in FROZEN_PROCEDURES)
    assert introduced_gd == []


def test_gd_and_wg_with_the_same_pack_and_number_do_not_collide():
    api = _api()
    resolver = api.KnowledgeResolver.open(REPO)
    gd = resolver.resolve("GD-ARCH-001")
    wg = resolver.resolve("WG-ARCH-001")
    assert gd is not None and wg is not None
    assert _resolution_id(gd) == "GD-ARCH-001"
    assert _resolution_id(wg) == "WG-ARCH-001"
    assert _value(gd, "path") != _value(wg, "path")


def test_all_frozen_procedures_have_the_unified_wargame_contract():
    required = {
        "id", "kind", "type", "scenario_modes", "applies_when",
        "engages_when", "consequence", "relations", "sources", "review",
        "lifecycle",
    }
    failures = []
    for identifier, rel in FROZEN_PROCEDURES.items():
        parsed = parse_frontmatter((REPO / rel).read_text(encoding="utf-8"))
        missing = sorted(required - set(parsed.data))
        if missing:
            failures.append(f"{identifier}: missing {', '.join(missing)}")
        if parsed.data.get("id") != identifier:
            failures.append(f"{identifier}: front-matter id differs")
        if parsed.data.get("kind") != "wargame":
            failures.append(f"{identifier}: kind is not wargame")
        if parsed.data.get("type") != "wargame":
            failures.append(f"{identifier}: type is not wargame")
        if not (parsed.data.get("applicable_doctrines") or
                parsed.data.get("gap_domain")):
            failures.append(f"{identifier}: no doctrine or gap domain")
        for heading in WARGAME_HEADINGS:
            if f"## {heading}" not in parsed.body:
                failures.append(f"{identifier}: missing section {heading}")
        options = re.search(
            r"(?ms)^## Options\s*$\n(.*?)(?=^## |\Z)", parsed.body)
        if options is None or len(re.findall(r"(?m)^### ", options.group(1))) < 2:
            failures.append(f"{identifier}: fewer than two material options")
    assert failures == []


@pytest.mark.parametrize(
    ("path", "anchors"),
    [
        ("packs/architecture/PACK.md", ARCHITECTURE_COMPATIBILITY_ANCHORS),
        ("packs/data-analytics/PACK.md", DATA_COMPATIBILITY_ANCHORS),
    ],
)
def test_two_pack_spike_preserves_explicit_legacy_anchors(path, anchors):
    text = (REPO / path).read_text(encoding="utf-8")
    missing = [anchor for anchor in anchors
               if not re.search(fr"<a\s+id=[\"']{anchor}[\"']\s*>", text)]
    assert missing == []


# --- One resolver, current and historical -----------------------------


def test_duplicate_live_definition_is_a_problem(tmp_path):
    api = _api()
    root = _knowledge_repo(tmp_path)
    _write_doctrine(root, "DOC-TEST-001", pack="base")
    resolver = api.KnowledgeResolver.open(root)
    text = _problem_text(resolver.problems)
    assert "doc-test-001" in text and "duplicate" in text


def test_a_prose_mention_never_becomes_a_definition(tmp_path):
    api = _api()
    root = _knowledge_repo(tmp_path)
    note = root / "NOTE.md"
    note.write_text("WG-GHOST-001 is only mentioned here.\n", encoding="utf-8")
    resolver = api.KnowledgeResolver.open(root)
    assert resolver.resolve("WG-GHOST-001") is None


def test_alias_resolves_to_one_canonical_identity(tmp_path):
    api = _api()
    root = _knowledge_repo(tmp_path)
    aliases = root / "registry" / "identifier-aliases.json"
    aliases.parent.mkdir(parents=True, exist_ok=True)
    aliases.write_text(json.dumps({
        "version": 1,
        "aliases": {"DOC-OLD-001": "DOC-TEST-001"},
    }), encoding="utf-8")
    resolver = api.KnowledgeResolver.open(root)
    resolved = resolver.resolve("DOC-OLD-001")
    assert resolved is not None
    assert _resolution_id(resolved) == "DOC-TEST-001"


def test_alias_cycle_is_a_problem(tmp_path):
    api = _api()
    root = _knowledge_repo(tmp_path)
    aliases = root / "registry" / "identifier-aliases.json"
    aliases.parent.mkdir(parents=True, exist_ok=True)
    aliases.write_text(json.dumps({
        "version": 1,
        "aliases": {
            "DOC-OLD-001": "DOC-OLD-002",
            "DOC-OLD-002": "DOC-OLD-001",
        },
    }), encoding="utf-8")
    resolver = api.KnowledgeResolver.open(root)
    assert "alias" in _problem_text(resolver.problems)
    assert "cycle" in _problem_text(resolver.problems)


def test_retired_id_resolves_for_provenance_but_not_as_live(tmp_path):
    api = _api()
    root = _retired_repo(tmp_path)
    resolver = api.KnowledgeResolver.open(root)
    resolved = resolver.resolve("WG-GONE-001")
    assert resolved is not None
    assert _value(resolved, "state") == "retired"
    with pytest.raises(Exception):
        resolver.require_live("WG-GONE-001", {"wargame"})


def test_retired_manifest_location_is_verified(tmp_path):
    api = _api()
    root = _retired_repo(tmp_path)
    manifest = root / "archive" / "RETIRED_IDS.json"
    doc = json.loads(manifest.read_text(encoding="utf-8"))
    doc["ids"]["WG-GONE-001"] = "missing/WG-GONE-001.md"
    manifest.write_text(json.dumps(doc), encoding="utf-8")
    resolver = api.KnowledgeResolver.open(root)
    text = _problem_text(resolver.problems)
    assert "wg-gone-001" in text
    assert "missing" in text or "retired" in text


def test_one_id_cannot_be_both_live_and_retired(tmp_path):
    api = _api()
    root = _retired_repo(tmp_path)
    _write_wargame(root, "WG-GONE-001", pack="gone")
    resolver = api.KnowledgeResolver.open(root)
    text = _problem_text(resolver.problems)
    assert "wg-gone-001" in text
    assert "live" in text and "retired" in text


def test_valid_historical_ref_never_falls_back_to_the_worktree(tmp_path):
    api = _api()
    root = tmp_path / "history"
    root.mkdir()
    _init_git(root)
    _write_pack(root, "hist")
    _write_doctrine(root, "DOC-HIST-001", pack="hist")
    first = _commit(root, "old tree")
    _write_doctrine(root, "DOC-HIST-002", pack="hist")
    _commit(root, "new tree")
    at_first = api.KnowledgeResolver.open(root, first)
    at_worktree = api.KnowledgeResolver.open(root)
    assert at_first.resolve("DOC-HIST-001") is not None
    assert at_first.resolve("DOC-HIST-002") is None
    assert at_worktree.resolve("DOC-HIST-002") is not None


def test_unknown_commit_is_cannot_run_not_an_empty_index(tmp_path):
    api = _api()
    root = tmp_path / "history"
    root.mkdir()
    _init_git(root)
    _write_pack(root, "hist")
    _commit(root, "one")
    with pytest.raises(Exception, match=r"(?i)(commit|ref|revision)"):
        api.KnowledgeResolver.open(root, "not-a-ref")


# --- Relations and dependency order -----------------------------------


def test_relation_missing_target_is_a_problem(tmp_path):
    api = _api()
    root = _knowledge_repo(tmp_path)
    _write_relation(root, "DREL-TEST-002", target="DOC-MISSING-001")
    resolver = api.KnowledgeResolver.open(root)
    text = _problem_text(resolver.problems)
    assert "drel-test-002" in text and "doc-missing-001" in text


@pytest.mark.parametrize("relation", ["depends_on", "supersedes"])
def test_directed_relation_cycles_are_problems(tmp_path, relation):
    api = _api()
    root = _knowledge_repo(tmp_path)
    _write_relation(root, "DREL-TEST-010", owner="DOC-TEST-001",
                    relation=relation, target="DOC-TEST-002")
    _write_relation(root, "DREL-TEST-011", owner="DOC-TEST-002",
                    relation=relation, target="DOC-TEST-001")
    resolver = api.KnowledgeResolver.open(root)
    text = _problem_text(resolver.problems)
    assert relation in text and "cycle" in text


def test_reciprocal_tension_is_not_misread_as_a_cycle(tmp_path):
    api = _api()
    root = _knowledge_repo(tmp_path)
    _write_relation(root, "DREL-TEST-010", owner="DOC-TEST-001",
                    target="DOC-TEST-002")
    _write_relation(root, "DREL-TEST-011", owner="DOC-TEST-002",
                    target="DOC-TEST-001")
    resolver = api.KnowledgeResolver.open(root)
    relevant = [p for p in resolver.problems
                if "drel-test-01" in _problem_text([p])]
    assert "cycle" not in _problem_text(relevant)


def test_pack_dependencies_are_deterministic_and_prerequisites_first(tmp_path):
    api = _api()
    root = _knowledge_repo(tmp_path)
    resolver = api.KnowledgeResolver.open(root)
    one = api.match_knowledge(resolver, {
        "has_ui": "true",
        "expert_users": "true",
        "safety_unknown": "false",
        "routine_pressure": "false",
    })
    two = api.match_knowledge(resolver, {
        "routine_pressure": "false",
        "safety_unknown": "false",
        "expert_users": "true",
        "has_ui": "true",
    })
    assert one["pack_order"] == two["pack_order"]
    assert one["pack_order"].index("base") < one["pack_order"].index("test")


def test_missing_pack_dependency_is_a_problem(tmp_path):
    api = _api()
    root = _knowledge_repo(tmp_path)
    _write_pack(root, "test", depends_on=("missing-pack",))
    resolver = api.KnowledgeResolver.open(root)
    text = _problem_text(resolver.problems)
    assert "missing-pack" in text


def test_pack_dependency_cycle_is_a_problem(tmp_path):
    api = _api()
    root = _knowledge_repo(tmp_path)
    _write_pack(root, "base", depends_on=("test",))
    resolver = api.KnowledgeResolver.open(root)
    text = _problem_text(resolver.problems)
    assert "pack" in text and "cycle" in text


# --- Tri-state matching ------------------------------------------------


def test_true_pressure_requires_its_wargame(tmp_path):
    api = _api()
    resolver = api.KnowledgeResolver.open(_knowledge_repo(tmp_path))
    result = api.match_knowledge(resolver, {
        "has_ui": "true", "expert_users": "true",
        "safety_unknown": "false", "routine_pressure": "false",
    })
    assert "WG-TEST-001" in _item_ids(result["required_wargames"])
    assert result["selection_reasons"]["WG-TEST-001"]


def test_false_pressure_records_omission_and_reason(tmp_path):
    api = _api()
    resolver = api.KnowledgeResolver.open(_knowledge_repo(tmp_path))
    result = api.match_knowledge(resolver, {
        "has_ui": "true", "expert_users": "false",
        "safety_unknown": "false", "routine_pressure": "false",
    })
    assert "WG-TEST-001" in _item_ids(result["omitted_wargames"])
    assert result["selection_reasons"]["WG-TEST-001"]


def test_unknown_high_consequence_pressure_is_required(tmp_path):
    api = _api()
    resolver = api.KnowledgeResolver.open(_knowledge_repo(tmp_path))
    result = api.match_knowledge(resolver, {
        "has_ui": "true", "expert_users": "false",
        "safety_unknown": "unknown", "routine_pressure": "false",
    })
    assert "WG-TEST-002" in _item_ids(result["required_wargames"])
    assert "safety_unknown" in result["unresolved_facts"]


def test_unknown_routine_pressure_is_a_candidate(tmp_path):
    api = _api()
    resolver = api.KnowledgeResolver.open(_knowledge_repo(tmp_path))
    result = api.match_knowledge(resolver, {
        "has_ui": "true", "expert_users": "unknown",
        "safety_unknown": "false", "routine_pressure": "false",
    })
    assert "WG-TEST-001" in _item_ids(result["candidate_wargames"])


def test_operator_include_and_omit_need_reasons(tmp_path):
    api = _api()
    resolver = api.KnowledgeResolver.open(_knowledge_repo(tmp_path))
    facts = {
        "has_ui": "true", "expert_users": "false",
        "safety_unknown": "false", "routine_pressure": "false",
    }
    with pytest.raises(ValueError, match=r"(?i)reason"):
        api.match_knowledge(resolver, facts, include={"WG-TEST-001": ""})
    with pytest.raises(ValueError, match=r"(?i)reason"):
        api.match_knowledge(resolver, facts, omit={"WG-TEST-001": ""})


def test_operator_override_is_recorded_not_silently_applied(tmp_path):
    api = _api()
    resolver = api.KnowledgeResolver.open(_knowledge_repo(tmp_path))
    facts = {
        "has_ui": "true", "expert_users": "false",
        "safety_unknown": "false", "routine_pressure": "false",
    }
    included = api.match_knowledge(
        resolver, facts,
        include={"WG-TEST-001": "The operator wants the comparison."})
    assert "WG-TEST-001" in _item_ids(included["required_wargames"])
    assert "operator" in " ".join(
        included["selection_reasons"]["WG-TEST-001"]).lower()

    omitted = api.match_knowledge(
        resolver, {**facts, "expert_users": "true"},
        omit={"WG-TEST-001": "A dated experiment already settled it."})
    assert "WG-TEST-001" in _item_ids(omitted["omitted_wargames"])
    assert "operator" in " ".join(
        omitted["selection_reasons"]["WG-TEST-001"]).lower()


def test_match_returns_summaries_and_never_chooses_an_outcome(tmp_path):
    api = _api()
    resolver = api.KnowledgeResolver.open(_knowledge_repo(tmp_path))
    result = api.match_knowledge(resolver, {
        "has_ui": "true", "expert_users": "true",
        "safety_unknown": "false", "routine_pressure": "false",
    })
    serialised = json.dumps(result).lower()
    assert "fixture content for cheapest discriminating test" not in serialised
    assert "chosen_option" not in serialised
    assert "chosen_outcome" not in serialised
    assert '"decision":' not in serialised
    assert "DOC-TEST-001" in _item_ids(result["applicable_doctrines"])


# --- Structured venture rulings ---------------------------------------


def test_valid_structured_ruling_resolves_every_reference(tmp_path):
    api = _api()
    resolver = api.KnowledgeResolver.open(_knowledge_repo(tmp_path))
    assert api.validate_rulings(_valid_rulings(), resolver) == ()


def test_duplicate_rul_id_is_rejected(tmp_path):
    api = _api()
    resolver = api.KnowledgeResolver.open(_knowledge_repo(tmp_path))
    document = _valid_rulings()
    document["rulings"].append(dict(document["rulings"][0]))
    text = _problem_text(api.validate_rulings(document, resolver))
    assert "rul-test-001" in text and "duplicate" in text


def test_retired_wargame_cannot_receive_an_active_ruling():
    api = _api()
    resolver = api.KnowledgeResolver.open(REPO)
    document = _valid_rulings("WG-DEL-001")
    document["rulings"][0]["doctrines"] = []
    text = _problem_text(api.validate_rulings(document, resolver))
    assert "wg-del-001" in text and "retired" in text


def test_default_departure_requires_a_reason(tmp_path):
    api = _api()
    resolver = api.KnowledgeResolver.open(_knowledge_repo(tmp_path))
    document = _valid_rulings()
    document["rulings"][0]["departures"] = [{
        "doctrine": "DOC-TEST-001",
    }]
    text = _problem_text(api.validate_rulings(document, resolver))
    assert "doc-test-001" in text and "reason" in text


def test_binding_scope_change_requires_adr_or_operator_reference(tmp_path):
    api = _api()
    resolver = api.KnowledgeResolver.open(_knowledge_repo(tmp_path))
    document = _valid_rulings()
    document["rulings"][0]["binding_scope_changes"] = [{
        "doctrine": "DOC-TEST-001",
        "proposal": "Narrow the applicability for this venture.",
    }]
    text = _problem_text(api.validate_rulings(document, resolver))
    assert "doc-test-001" in text
    assert "adr" in text or "operator" in text
