"""Acceptance tests for the applied T-0026 Doctrine content migration."""

from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

import jsonschema

from tools.eos.frontmatter import parse as parse_frontmatter
from tools.eos.knowledge_migration import (
    BASELINE_COMMIT,
    EXPECTED_INVENTORY_SHA256,
    read_baseline,
)
from tools.eos.migrate_doctrines import (
    API_WEBHOOK,
    ARCH_GENERATED,
    ARCH_WEBHOOK,
    AUTHORITY_DEFAULT_OVERRIDES,
    CODING_ORACLE,
    DELIVERY_ORACLE,
    IDENTITY_CREDENTIAL,
    NATIVE_PREFERENCE,
    PACK_DEPENDENCIES,
    SECURITY_APPROVAL,
    UI_OVERLAY,
    WRITING_BRAND_VOICE,
    build_migration,
    check_fixpoint,
)
from tools.eos.ontology import KnowledgeResolver


REPO = Path(__file__).resolve().parents[1]
INVENTORY = json.loads((
    REPO / "org" / "migration" / "DOCTRINE_SOURCE_INVENTORY.json"
).read_text(encoding="utf-8"))
LEDGER = json.loads((
    REPO / "org" / "migration" / "DOCTRINE_MIGRATION.json"
).read_text(encoding="utf-8"))
DOC_PATHS = sorted(REPO.glob("packs/*/doctrines/DOC-*.md"))
DOCS = {
    parse_frontmatter(path.read_text(encoding="utf-8")).data["id"]:
        (path, parse_frontmatter(path.read_text(encoding="utf-8")).data)
    for path in DOC_PATHS
}


def _ledger_row(source_key):
    return next(row for row in LEDGER["rows"] if row["source_key"] == source_key)


def _authorities(source_key):
    return {DOCS[target][1]["authority"] for target in _ledger_row(source_key)["targets"]}


def test_all_501_sources_have_one_final_reviewed_disposition():
    assert LEDGER["version"] == 1
    assert LEDGER["baseline_commit"] == BASELINE_COMMIT
    assert LEDGER["inventory_sha256"] == EXPECTED_INVENTORY_SHA256
    assert len(LEDGER["rows"]) == 501
    assert len({row["source_key"] for row in LEDGER["rows"]}) == 501
    assert {row["source_key"] for row in LEDGER["rows"]} == {
        row["source_key"] for row in INVENTORY["rows"]
    }
    assert set(row["disposition"] for row in LEDGER["rows"]) == {
        "create", "merge_into", "retain_explanatory",
    }
    assert "pending_review" not in json.dumps(LEDGER)
    assert all(len(row["reason"]) >= 60 for row in LEDGER["rows"])
    assert Counter(row["disposition"] for row in LEDGER["rows"]) == {
        "create": 496,
        "merge_into": 4,
        "retain_explanatory": 1,
    }


def test_ledger_and_every_doctrine_satisfy_their_schemas():
    ledger_schema = json.loads((
        REPO / "kernel" / "schemas" / "knowledge-migration.schema.json"
    ).read_text(encoding="utf-8"))
    doctrine_schema = json.loads((
        REPO / "kernel" / "schemas" / "doctrine.schema.json"
    ).read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(ledger_schema).validate(LEDGER)
    assert len(DOCS) == len(DOC_PATHS) == 513
    for identifier, (path, metadata) in DOCS.items():
        jsonschema.Draft202012Validator(doctrine_schema).validate(metadata)
        assert path.name.startswith(identifier + "-")
        assert metadata["migration_sources"]


def test_targets_have_one_canonical_definition_and_complete_provenance():
    target_ids = [
        target
        for row in LEDGER["rows"]
        for target in row.get("targets", [])
    ]
    assert set(target_ids) == set(DOCS)
    assert all(target_ids.count(identifier) >= 1 for identifier in DOCS)
    assert len(DOCS) == len(set(DOCS))
    statements = [
        " ".join(metadata["statement"].lower().split())
        for _, metadata in DOCS.values()
    ]
    assert len(statements) == len(set(statements))
    for identifier, (_, metadata) in DOCS.items():
        sources = set(metadata["migration_sources"])
        ledger_sources = {
            row["source_key"] for row in LEDGER["rows"]
            if identifier in row.get("targets", [])
        }
        assert sources == ledger_sources


def test_required_splits_are_independently_challengeable():
    assert len(_ledger_row(SECURITY_APPROVAL)["targets"]) == 5
    assert len(_ledger_row(UI_OVERLAY)["targets"]) == 2
    assert _authorities(UI_OVERLAY) == {"binding", "default"}
    assert len(_ledger_row(IDENTITY_CREDENTIAL)["targets"]) == 6
    assert len(_ledger_row(NATIVE_PREFERENCE)["targets"]) == 6
    assert _authorities(NATIVE_PREFERENCE) == {"preference"}
    assert len(_ledger_row(CODING_ORACLE)["targets"]) == 2
    assert len(_ledger_row(ARCH_GENERATED)["targets"]) == 2


def test_reviewed_merges_share_only_a_genuinely_common_proposition():
    api = _ledger_row(API_WEBHOOK)["targets"]
    architecture = _ledger_row(ARCH_WEBHOOK)["targets"]
    assert api == architecture
    assert DOCS[api[0]][0].as_posix().endswith(
        f"packs/api-integration/doctrines/{DOCS[api[0]][0].name}"
    )
    assert _ledger_row(DELIVERY_ORACLE)["targets"] == [
        _ledger_row(CODING_ORACLE)["targets"][0]
    ]

    distinct = [
        (
            "packs/security-privacy/PACK.md:requirements:001",
            "packs/research-knowledge/PACK.md:requirements:002",
        ),
        (
            "packs/docs-dx/PACK.md:requirements:004",
            "packs/ui-ux/PACK.md:requirements:005",
        ),
        (
            "packs/agentic-development/PACK.md:requirements:001",
            "packs/agentic-swarm/PACK.md:requirements:009",
        ),
    ]
    for first, second in distinct:
        assert set(_ledger_row(first)["targets"]).isdisjoint(
            _ledger_row(second)["targets"]
        )


def test_authority_reconciliation_is_explicit_not_heading_derived():
    for source_key in AUTHORITY_DEFAULT_OVERRIDES:
        assert _authorities(source_key) == {"default"}
    house = [
        row["source_key"] for row in INVENTORY["rows"]
        if row["path"] == "packs/pattertech-house/PACK.md"
        and row["family"] == "requirements"
    ]
    assert house and all(_authorities(source) == {"preference"} for source in house)
    security = [
        row["source_key"] for row in INVENTORY["rows"]
        if row["path"] == "packs/security-privacy/PACK.md"
        and row["family"] == "requirements"
    ]
    devops = [
        row["source_key"] for row in INVENTORY["rows"]
        if row["path"] == "packs/devops-reliability/PACK.md"
        and row["family"] == "requirements"
    ]
    assert all(_authorities(source) == {"binding"} for source in security + devops)
    decision_binding = [
        metadata for _, metadata in DOCS.values()
        if metadata["authority"] == "binding" and metadata["basis"] == "decision"
    ]
    assert decision_binding
    assert all(metadata.get("accepted_adr") for metadata in decision_binding)


def test_brand_voice_remains_explanatory_until_adoption():
    row = _ledger_row(WRITING_BRAND_VOICE)
    assert row["disposition"] == "retain_explanatory"
    assert "targets" not in row
    assert row["destination"] == "packs/writing-content/PACK.md#voice-scopes"
    pack = (REPO / "packs" / "writing-content" / "PACK.md").read_text(
        encoding="utf-8"
    )
    assert "Brand voice remains explanatory and empty" in pack


def test_pack_routers_remove_source_blocks_and_expose_every_anchor():
    inventory_by_key = {row["source_key"]: row for row in INVENTORY["rows"]}
    blocks = read_baseline(REPO)
    for pack_name, dependencies in PACK_DEPENDENCIES.items():
        path = REPO / "packs" / pack_name / "PACK.md"
        text = path.read_text(encoding="utf-8")
        metadata = parse_frontmatter(text).data
        assert metadata["kind"] == "record"
        assert metadata["authority"] == "none"
        assert metadata["depends_on"] == dependencies
        for heading in (
            "Binding requirements", "Requirements", "House requirements",
            "Defaults", "Preferences",
        ):
            assert f"## {heading}\n" not in text
        for block in [row for row in blocks if row.path == f"packs/{pack_name}/PACK.md"]:
            assert block.text not in text
            anchor = inventory_by_key[block.source_key].get("legacy_anchor")
            if not anchor and block.family == "requirements" \
                    and re.match(r"^\d+\.\s+\*\*", block.text):
                anchor = f"B{block.ordinal}"
            if anchor:
                assert re.search(fr'<a id="{re.escape(anchor)}"></a>', text)


def test_dependency_order_is_acyclic_deterministic_and_prerequisite_first():
    resolver = KnowledgeResolver.open(REPO)
    one = resolver.pack_order()
    two = resolver.pack_order(set(reversed(sorted(PACK_DEPENDENCIES))))
    assert one == two
    assert set(one) == set(PACK_DEPENDENCIES)
    positions = {pack: index for index, pack in enumerate(one)}
    for pack, prerequisites in PACK_DEPENDENCIES.items():
        for prerequisite in prerequisites:
            assert positions[prerequisite] < positions[pack]


def test_applied_generation_is_a_fixpoint():
    assert check_fixpoint(REPO) == []
    outputs = build_migration(REPO)
    assert len(outputs) == 539
    assert all((REPO / path).read_text(encoding="utf-8") == content
               for path, content in outputs.items())

