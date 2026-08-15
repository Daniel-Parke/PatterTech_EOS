"""Focused acceptance tests for the frozen Wargame migration."""

from __future__ import annotations

import json
import re
from pathlib import Path

import jsonschema
import pytest

from tests.test_ontology_oracle import FROZEN_PROCEDURES
from tools.eos.frontmatter import parse as parse_frontmatter
from tools.eos.migrate_wargames import (
    FROZEN_COUNT,
    PRESSURE_MAP,
    SOURCE_OVERRIDES,
    WARGAME_HEADINGS,
    build_migration,
    frozen_procedures,
)
from tools.eos.ontology import KnowledgeResolver


REPO = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def migration():
    return build_migration(REPO)


def test_frozen_inventory_is_the_independent_exact_114_id_path_set():
    assert FROZEN_COUNT == 114
    assert frozen_procedures(REPO) == FROZEN_PROCEDURES


def test_migration_is_deterministic_and_current_tree_is_a_fixpoint(migration):
    first_files, first_ledger = migration
    second_files, second_ledger = build_migration(REPO)
    assert first_files == second_files
    assert first_ledger == second_ledger
    for path, text in first_files.items():
        assert (REPO / path).read_text(encoding="utf-8") == text
    assert json.loads(
        (REPO / "org/migration/WARGAME_MIGRATION.json").read_text(encoding="utf-8")
    ) == first_ledger


def test_all_114_wargames_pass_schema_and_complete_body_contract(migration):
    rendered, _ledger = migration
    schema = json.loads(
        (REPO / "kernel/schemas/wargame.schema.json").read_text(encoding="utf-8")
    )
    validator = jsonschema.Draft202012Validator(schema)
    assert set(rendered) == set(FROZEN_PROCEDURES.values())

    for identifier, path in FROZEN_PROCEDURES.items():
        text = rendered[path]
        parsed = parse_frontmatter(text)
        assert parsed.present and not parsed.errors, path
        assert parsed.data["id"] == identifier
        assert parsed.data["kind"] == "wargame"
        assert parsed.data["type"] == "wargame"
        assert not list(validator.iter_errors(parsed.data)), path

        headings = tuple(re.findall(r"(?m)^## (.+?)\s*$", parsed.body))
        assert headings == WARGAME_HEADINGS, path
        options = re.search(
            r"(?ms)^## Options\s*$\n(.*?)(?=^## |\Z)", parsed.body
        )
        assert options is not None, path
        option_count = len(re.findall(r"(?m)^### ", options.group(1)))
        assert option_count >= 2, path
        failures = re.search(
            r"(?ms)^## Failure premises\s*$\n(.*?)(?=^## |\Z)", parsed.body
        )
        assert failures is not None, path
        assert len(re.findall(r"(?m)^### Premortem for ", failures.group(1))) == option_count
        assert "**Fallback `safe-default`:**" in parsed.body
        assert "**Exit condition:**" in parsed.body
        assert "**Revisit trigger:**" in parsed.body
        assert "## Worked rulings" not in parsed.body


def test_every_migrated_wargame_has_substantive_counter_evidence(migration):
    rendered, _ledger = migration
    for path, text in rendered.items():
        body = parse_frontmatter(text).body
        section = re.search(
            r"(?ms)^## Counter-evidence and transfer limits\s*$\n(.*)\Z",
            body,
        )
        assert section is not None, path
        before_history_or_transfer = re.split(
            r"(?m)^### (?:Historical ruling boundary|Transfer limit)\s*$",
            section.group(1),
            maxsplit=1,
        )[0].strip()
        assert before_history_or_transfer, path


def test_imported_pack_placeholders_are_replaced_by_reviewed_evidence(migration):
    rendered, _ledger = migration
    evidence = json.loads(
        (REPO / "registry/evidence.json").read_text(encoding="utf-8")
    )
    live_evidence = {row["id"] for row in evidence["records"]}
    for identifier, path in FROZEN_PROCEDURES.items():
        sources = parse_frontmatter(rendered[path]).data.get("sources") or []
        assert not [source for source in sources if str(source).startswith("pending-")], path
        if identifier in SOURCE_OVERRIDES:
            assert tuple(sources) == SOURCE_OVERRIDES[identifier], path
            assert set(sources) <= live_evidence, path


def test_every_applicable_doctrine_reference_resolves_live(migration):
    rendered, _ledger = migration
    resolver = KnowledgeResolver.open(REPO)
    for path, text in rendered.items():
        metadata = parse_frontmatter(text).data
        doctrines = metadata.get("applicable_doctrines") or []
        if not doctrines:
            assert metadata.get("gap_domain") == "inception", path
            continue
        for identifier in doctrines:
            resolution = resolver.resolve(identifier)
            assert resolution is not None, (path, identifier)
            assert resolution.state == "live", (path, identifier)
            assert resolution.kind == "doctrine", (path, identifier)
        for identifier in metadata.get("relations") or []:
            resolution = resolver.resolve(identifier)
            assert resolution is not None, (path, identifier)
            assert resolution.state == "live", (path, identifier)
            assert resolution.kind == "relation", (path, identifier)


def test_only_reviewed_existing_coverage_receives_pressure_predicates(migration):
    rendered, _ledger = migration
    for identifier, path in FROZEN_PROCEDURES.items():
        metadata = parse_frontmatter(rendered[path]).data
        expected = list(PRESSURE_MAP.get(identifier, ("operator_requests_wargame",)))
        assert metadata["engages_when"] == expected, path


def test_inception_and_security_floors_are_always_walk_high_consequence(migration):
    rendered, _ledger = migration
    always = {
        "WG-EOS-001", "WG-EOS-002",
        "GD-SEC-001", "GD-SEC-002", "GD-SEC-003", "GD-SEC-004",
    }
    for identifier in always:
        metadata = parse_frontmatter(rendered[FROZEN_PROCEDURES[identifier]]).data
        assert metadata["always_walk"] == "true"
        assert metadata["consequence"] == "high"
        assert metadata["applies_when"] == ["runs_agents"]
    for identifier in ("WG-EOS-001", "WG-EOS-002"):
        metadata = parse_frontmatter(rendered[FROZEN_PROCEDURES[identifier]]).data
        assert "gap" in metadata["scenario_modes"]
        assert metadata["gap_domain"] == "inception"


def test_scale_wargame_takes_seed_accounting_from_the_live_matrix(migration):
    rendered, _ledger = migration
    text = rendered[FROZEN_PROCEDURES["WG-EOS-001"]]
    assert "kernel/SCALE_MATRIX.md" in text
    assert "Fourteen files" not in text
    assert "Twenty-five files" not in text


def test_retired_ids_are_reserved_and_absent_from_live_migrated_content(migration):
    rendered, ledger = migration
    manifest = json.loads(
        (REPO / "archive/RETIRED_IDS.json").read_text(encoding="utf-8")
    )
    retired = set(manifest["ids"])
    assert len(retired) == 22
    assert {row["id"] for row in ledger["retired"]} == retired
    assert all(row["active_ruling_allowed"] is False for row in ledger["retired"])
    for path, text in rendered.items():
        assert not [identifier for identifier in retired if identifier in text], path


def test_migration_ledger_disposes_every_live_and_retired_identity_once(migration):
    _rendered_files, ledger = migration
    live = ledger["procedures"]
    retired = ledger["retired"]
    assert ledger["procedure_count"] == len(live) == 114
    assert ledger["retired_count"] == len(retired) == 22
    assert len({row["id"] for row in live}) == 114
    assert len({row["path"] for row in live}) == 114
    assert all(row["disposition"] == "live-convert" for row in live)
    assert all(row["ruling_disposition"] == "not-extracted" for row in live)
    assert len({row["id"] for row in retired}) == 22
    assert not ({row["id"] for row in live} & {row["id"] for row in retired})
