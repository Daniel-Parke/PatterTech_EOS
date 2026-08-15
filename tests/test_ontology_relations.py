"""Focused relation semantics added after the frozen ontology oracle."""

from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path

from tools.eos.ontology import (
    KnowledgeResolver,
    match_knowledge,
    validate_rulings,
)


REPO = Path(__file__).resolve().parents[1]


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def _fixture(tmp_path, relation_target="missing-capability"):
    root = tmp_path / "repo"
    root.mkdir()
    _write(root / "packs" / "test" / "PACK.md", """---
summary: Test pack
type: guide
tags: [eos]
applies_when: [has_test]
depends_on: []
---
""")
    _write(root / "packs" / "test" / "doctrines" / "DOC-TEST-001-rule.md", """---
id: DOC-TEST-001
statement: Keep the fixture honest.
summary: Keep the fixture honest.
kind: doctrine
type: doctrine
authority: default
basis: decision
evidence_grade: asserted
scope: estate
applies_when: [has_test]
challenge_triggers: [missing_pressure]
sources: [EV-TEST]
review: 2030-01
lifecycle: active
verification_refs: [test]
---
""")
    _write(root / "packs" / "test" / "guides" / "WG-TEST-001-gap.md", """---
id: WG-TEST-001
summary: Cover the missing capability.
kind: wargame
type: wargame
scenario_modes: [gap]
gap_domain: missing-capability
applies_when: [has_test]
engages_when: [missing_pressure]
consequence: high
relations: [DREL-TEST-001]
sources: [EV-TEST]
review: 2030-01
lifecycle: active
---
""")
    relation = {
        "id": "DREL-TEST-001",
        "owner_doctrine": "DOC-TEST-001",
        "relation": "covers_gap",
        "target": relation_target,
        "conditions": ["missing_pressure"],
        "status": "covered",
        "evidence": ["EV-TEST"],
        "fallback": "Keep the current default.",
        "wargame": "WG-TEST-001",
    }
    _write(
        root / "packs" / "test" / "doctrines" / "relations" /
        "DREL-TEST-001.json",
        json.dumps(relation, indent=2) + "\n",
    )
    return root


def test_covers_gap_targets_the_wargames_declared_gap(tmp_path):
    resolver = KnowledgeResolver.open(_fixture(tmp_path))
    assert resolver.problems == ()


def test_covers_gap_rejects_a_mismatched_gap_target(tmp_path):
    resolver = KnowledgeResolver.open(_fixture(tmp_path, "another-gap"))
    assert [(problem.code, problem.identifier) for problem in resolver.problems] == [
        ("relation-gap", "DREL-TEST-001")
    ]


def _write_pressure_registry(root, *, wargames=None, relations=None):
    document = {
        "version": 1,
        "kind": "pressure-dispositions",
        "source": "test",
        "accepted_by": "ADR-TEST",
        "governed_by": "ADR-0001",
        "review": "2030-01",
        "rows": [{
            "case": 1,
            "name": "Missing capability",
            "pressure": "missing_pressure",
            "disposition": "relation-only",
            "consequence": "high",
            "wargames": list(wargames if wargames is not None else []),
            "relations": list(
                relations if relations is not None else ["DREL-TEST-001"]
            ),
            "fallback": "Keep the current default.",
        }],
    }
    _write(
        root / "registry" / "pressure-dispositions.json",
        json.dumps(document, indent=2) + "\n",
    )


def test_pressure_registry_resolves_relations_and_drives_tri_state_match(tmp_path):
    root = _fixture(tmp_path)
    _write_pressure_registry(root)
    resolver = KnowledgeResolver.open(root)

    assert resolver.problems == ()
    result = match_knowledge(resolver, {
        "has_test": "true",
        "missing_pressure": "true",
    })
    assert result["pressure_dispositions"] == [{
        "case": 1,
        "pressure": "missing_pressure",
        "disposition": "relation-only",
        "state": "fallback-required",
        "wargames": [],
        "relations": ["DREL-TEST-001"],
        "fallback": "Keep the current default.",
        "reopen_trigger": None,
        "reason": "relation fallback covers this pressure without a Wargame",
    }]
    assert result["uncovered_pressures"] == []


def test_pressure_registry_rejects_a_non_live_reference(tmp_path):
    root = _fixture(tmp_path)
    _write_pressure_registry(root, wargames=["WG-TEST-999"], relations=[])
    resolver = KnowledgeResolver.open(root)

    assert [(problem.code, problem.identifier) for problem in resolver.problems] == [
        ("pressure-wargame", "missing_pressure")
    ]


def test_pressure_registry_rejects_an_edge_that_does_not_engage_pressure(tmp_path):
    root = _fixture(tmp_path)
    _write_pressure_registry(root, wargames=["WG-TEST-001"], relations=[])
    path = root / "registry" / "pressure-dispositions.json"
    document = json.loads(path.read_text(encoding="utf-8"))
    document["rows"][0]["pressure"] = "another_pressure"
    document["rows"][0]["disposition"] = "new-wargame"
    _write(path, json.dumps(document, indent=2) + "\n")

    resolver = KnowledgeResolver.open(root)

    assert [(problem.code, problem.identifier) for problem in resolver.problems] == [
        ("pressure-engagement", "another_pressure")
    ]


def test_applicability_predicates_are_alternative_entrances(tmp_path):
    root = _fixture(tmp_path)
    path = root / "packs" / "test" / "guides" / "WG-TEST-001-gap.md"
    text = path.read_text(encoding="utf-8").replace(
        "applies_when: [has_test]",
        "applies_when: [has_test, has_second_surface]",
    )
    _write(path, text)
    resolver = KnowledgeResolver.open(root)

    result = match_knowledge(resolver, {
        "has_test": "false",
        "has_second_surface": "true",
        "missing_pressure": "true",
    })

    assert [row["id"] for row in result["required_wargames"]] == [
        "WG-TEST-001"
    ]


def test_all_false_facts_do_not_activate_every_pack(tmp_path):
    resolver = KnowledgeResolver.open(_fixture(tmp_path))

    result = match_knowledge(resolver, {
        "has_test": "false",
        "missing_pressure": "false",
    })

    assert result["applicable_doctrines"] == []
    assert result["required_wargames"] == []
    assert result["candidate_wargames"] == []
    assert result["pack_order"] == []


def test_operator_cannot_omit_an_always_walk_wargame(tmp_path):
    root = _fixture(tmp_path)
    path = root / "packs" / "test" / "guides" / "WG-TEST-001-gap.md"
    _write(path, path.read_text(encoding="utf-8").replace(
        "consequence: high", "consequence: high\nalways_walk: true"))
    resolver = KnowledgeResolver.open(root)

    try:
        match_knowledge(
            resolver,
            {"has_test": "true", "missing_pressure": "true"},
            omit={"WG-TEST-001": "The operator wants to skip it."},
        )
    except ValueError as exc:
        assert "always-walk" in str(exc)
    else:
        raise AssertionError("always-walk Wargame was omitted")


def _rulings(*, doctrine="DOC-TEST-001", wargame="WG-TEST-001"):
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
            "doctrines": [doctrine],
            "decision": "Use the reversible option.",
            "execution": "argued",
            "reason": "The cheapest test discriminated the options.",
            "decided": "2030-01-02",
            "departures": [],
            "binding_scope_changes": [],
        }],
    }


def test_an_ordinary_ruling_cannot_depart_from_binding_doctrine(tmp_path):
    root = _fixture(tmp_path)
    path = root / "packs" / "test" / "doctrines" / "DOC-TEST-001-rule.md"
    _write(path, path.read_text(encoding="utf-8").replace(
        "authority: default", "authority: binding"))
    document = _rulings()
    document["rulings"][0]["departures"] = [{
        "doctrine": "DOC-TEST-001",
        "reason": "The venture would prefer to waive it.",
    }]

    problems = validate_rulings(document, KnowledgeResolver.open(root))

    assert [(row.code, row.identifier) for row in problems] == [
        ("binding-departure", "DOC-TEST-001")
    ]


def test_binding_scope_change_must_name_a_live_binding_doctrine(tmp_path):
    root = _fixture(tmp_path)
    document = _rulings()
    document["rulings"][0]["binding_scope_changes"] = [{
        "doctrine": "DOC-TEST-999",
        "proposal": "Narrow the binding scope.",
        "operator_ref": "operator:T-TEST",
    }]

    problems = validate_rulings(document, KnowledgeResolver.open(root))

    assert [(row.code, row.identifier) for row in problems] == [
        ("binding-change-doctrine", "DOC-TEST-999")
    ]


def test_selection_and_ruling_links_are_bijective(tmp_path):
    resolver = KnowledgeResolver.open(_fixture(tmp_path))

    duplicate = _rulings()
    duplicate["selection_log"].append(dict(duplicate["selection_log"][0]))
    duplicate_codes = {row.code for row in validate_rulings(duplicate, resolver)}
    assert "duplicate-selection" in duplicate_codes
    assert "duplicate-ruling-reference" in duplicate_codes

    missing = _rulings()
    missing["selection_log"][0]["ruling"] = "RUL-TEST-999"
    missing_codes = {row.code for row in validate_rulings(missing, resolver)}
    assert "selection-ruling" in missing_codes
    assert "unreferenced-ruling" in missing_codes

    mismatch = _rulings()
    mismatch["rulings"][0]["wargame"] = "WG-TEST-999"
    mismatch_messages = [
        row.message for row in validate_rulings(mismatch, resolver)
    ]
    assert any("belongs to WG-TEST-999" in message
               for message in mismatch_messages)


def test_every_always_walk_wargame_is_selected_and_ruled(tmp_path):
    root = _fixture(tmp_path)
    path = root / "packs" / "test" / "guides" / "WG-TEST-001-gap.md"
    _write(path, path.read_text(encoding="utf-8").replace(
        "consequence: high", "consequence: high\nalways_walk: true"))
    document = _rulings(wargame="WG-TEST-001")
    document["selection_log"] = []
    document["rulings"] = []

    problems = validate_rulings(document, KnowledgeResolver.open(root))

    assert [(row.code, row.identifier) for row in problems] == [
        ("always-walk", "WG-TEST-001")
    ]


def test_accepted_pressure_backlog_has_one_disposition_per_case():
    document = json.loads(
        (REPO / "registry" / "pressure-dispositions.json").read_text(
            encoding="utf-8"
        )
    )
    rows = document["rows"]

    assert [row["case"] for row in rows] == list(range(1, 26))
    assert document["accepted_by"] == (
        "Operator instruction for T-0026, 2026-08-15"
    )
    assert document["governed_by"] == "ADR-0014"
    assert len({row["pressure"] for row in rows}) == 25
    assert Counter(row["disposition"] for row in rows) == {
        "new-wargame": 14,
        "existing-wargame-refreshed": 7,
        "relation-only": 3,
        "rejected": 1,
    }


def test_accepted_pressure_backlog_resolves_every_live_edge():
    resolver = KnowledgeResolver.open(REPO)

    assert resolver.problems == ()
    assert len(resolver.pressure_dispositions) == 25


def test_two_pack_match_stays_below_the_old_full_pack_context_bound():
    resolver = KnowledgeResolver.open(REPO)
    predicates: set[str] = set()
    for row in resolver.list():
        for key in ("applies_when", "engages_when", "engage_when"):
            values = row.metadata.get(key) or []
            if isinstance(values, str):
                values = [values]
            predicates.update(str(value) for value in values)
    predicates.update(
        str(row["pressure"])
        for row in resolver.pressure_dispositions
        if row.get("pressure")
    )
    encoded = json.dumps(
        sorted(predicates), separators=(",", ":"),
    ).encode("utf-8")

    assert len(predicates) == 94
    assert hashlib.sha256(encoded).hexdigest() == (
        "505d7c88a99cdc8810d551d1da00a88afaf413ef1ce134b680c7e97b9cc5a02d"
    )
    facts = {name: "false" for name in predicates}
    facts.update({
        "has_server_code": "true",
        "publishes_analytics_table": "true",
    })

    result = match_knowledge(resolver, facts)

    assert len(result["applicable_doctrines"]) == 34
    assert result["required_wargames"] == []
    assert result["candidate_wargames"] == []
    assert len(result["omitted_wargames"]) == 127
    assert result["pack_order"] == [
        "product-discovery",
        "business-logic-modelling",
        "architecture",
        "data-analytics",
    ]
    assert result["uncovered_pressures"] == []
    assert len(json.dumps(result, indent=1).encode("utf-8")) <= 41_966
