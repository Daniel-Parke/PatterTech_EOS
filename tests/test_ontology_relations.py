"""Focused relation semantics added after the frozen ontology oracle."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

from tools.eos.ontology import KnowledgeResolver, match_knowledge


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
