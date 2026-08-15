"""Focused relation semantics added after the frozen ontology oracle."""

from __future__ import annotations

import json

from tools.eos.ontology import KnowledgeResolver, match_knowledge


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
        "review": "2030-01",
        "rows": [{
            "case": 1,
            "name": "Missing capability",
            "pressure": "missing_pressure",
            "disposition": "relation-only",
            "consequence": "high",
            "wargames": list(wargames or []),
            "relations": list(relations or ["DREL-TEST-001"]),
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
