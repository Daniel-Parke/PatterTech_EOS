"""Drill runner tests: real verdicts, honest manuals, no false greens.

The twenty shipped drills have no scenarios and no graders yet, so the
tests that prove the runner actually evaluates anything build their own
synthetic drill root: a manifest, a spec, a scenario tree and graders.
That way pass, fail and manual are all exercised for real rather than
asserted about a stub.
"""

import hashlib
import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools.eos import benchcli, drills  # noqa: E402

SPEC = """---
summary: A synthetic drill used only by the tests
type: example
tags: [eos]
---

# Drill: the synthetic one

## Scenario

A cold agent gets a tree with one file in it.

## Deterministic criteria

1. The marker file exists.
2. The marker file says yes.
3. Something a human has to read and judge.

## Scoring

Pass requires all three.
"""

_PASS_GRADER = (
    "import json, sys\n"
    "from pathlib import Path\n"
    "ok = (Path(sys.argv[1]) / 'marker.txt').is_file()\n"
    "print(json.dumps({'id': 'c1', 'pass': ok, 'reason': 'marker present'}))\n"
    "sys.exit(0 if ok else 1)\n"
)

_FAIL_GRADER = (
    "import json, sys\n"
    "print(json.dumps({'id': 'c2', 'pass': False, "
    "'reason': 'marker says no'}))\n"
    "sys.exit(1)\n"
)


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


@pytest.fixture
def drill_root(tmp_path):
    """A minimal repo root holding one synthetic drill."""
    root = tmp_path / "repo"
    spec = _write(root / "benchmark" / "drills" / "synthetic.md", SPEC)
    digest = hashlib.sha256(spec.read_bytes()).hexdigest()
    _write(root / drills.MANIFEST_REL, json.dumps({
        "version": 2,
        "drills": {
            "synthetic": {
                "spec": "benchmark/drills/synthetic.md",
                "sha256": digest,
                "wave": "B",
                "frozen_before_authoring": False,
            },
        },
    }))
    return root


def _add_scenario(root):
    _write(root / drills.SCENARIOS_REL / "synthetic" / "marker.txt", "yes\n")


def _add_graders(root, *, c1=True, c2=False, c3=False):
    base = root / drills.GRADERS_REL / "synthetic"
    if c1:
        _write(base / "c1.py", _PASS_GRADER)
    if c2:
        _write(base / "c2.py", _FAIL_GRADER)
    if c3:
        _write(base / "c3.py", _PASS_GRADER)


# ------------------------------------------------------------- parsing


def test_parse_spec_reads_only_the_criteria_section():
    parsed = drills.parse_spec(SPEC)
    assert parsed["drill"] == "Drill: the synthetic one"
    assert [c["id"] for c in parsed["criteria"]] == ["c1", "c2", "c3"]
    # The numbered list under Scoring must not leak in.
    assert len(parsed["criteria"]) == 3


def test_parse_spec_refuses_criteria_that_are_not_numbered_in_order():
    broken = SPEC.replace("2. The marker file says yes.",
                          "4. The marker file says yes.")
    with pytest.raises(drills.DrillError):
        drills.parse_spec(broken)


def test_every_shipped_spec_parses_and_matches_its_frozen_hash():
    manifest = drills.load_manifest(REPO)
    assert len(manifest["drills"]) == 20
    for pack in drills.packs(REPO, manifest):
        spec = drills.read_spec(REPO, pack, manifest=manifest)
        assert spec["criteria"], "%s parsed no criteria" % pack
        assert spec["frozen_before_authoring"] in (True, False)


def test_the_manifest_records_which_drills_predate_their_pack():
    manifest = drills.load_manifest(REPO)
    flags = [e["frozen_before_authoring"] for e in manifest["drills"].values()]
    assert flags.count(True) == 8, "the Wave A eight predate their packs"
    assert flags.count(False) == 12, "the Wave B twelve do not"


def test_a_changed_spec_is_refused_rather_than_re_baselined(drill_root):
    spec = drill_root / "benchmark" / "drills" / "synthetic.md"
    spec.write_text(SPEC + "\nan edit after the freeze\n", encoding="utf-8")
    with pytest.raises(drills.DrillError) as exc:
        drills.read_spec(drill_root, "synthetic")
    assert "changed since freeze" in str(exc.value)


def test_unknown_pack_is_a_cannot_run(drill_root):
    with pytest.raises(drills.DrillError):
        drills.read_spec(drill_root, "no-such-pack")


# ------------------------------------------------------------- verdicts


def test_no_scenario_and_no_graders_gives_every_criterion_manual(drill_root):
    row = drills.run_drill(drill_root, "synthetic")
    assert row["pass"] is None
    assert row["reason"]
    assert [c["verdict"] for c in row["criteria"]] == ["manual"] * 3
    assert row["counts"] == {"total": 3, "pass": 0, "fail": 0, "manual": 3}


def test_a_grader_with_no_scenario_still_reports_manual(drill_root):
    _add_graders(drill_root, c1=True)
    row = drills.run_drill(drill_root, "synthetic")
    assert row["pass"] is None
    assert row["criteria"][0]["verdict"] == "manual"
    assert "never built" in row["criteria"][0]["reason"]


def test_a_real_grader_against_a_real_scenario_passes(drill_root):
    _add_scenario(drill_root)
    _add_graders(drill_root, c1=True)
    row = drills.run_drill(drill_root, "synthetic")
    assert row["criteria"][0]["verdict"] == "pass"
    assert row["criteria"][0]["reason"] == "marker present"
    # Two criteria remain manual, so the drill still has no verdict.
    assert row["pass"] is None
    assert row["counts"] == {"total": 3, "pass": 1, "fail": 0, "manual": 2}


def test_a_failing_grader_makes_the_drill_fail(drill_root):
    _add_scenario(drill_root)
    _add_graders(drill_root, c1=True, c2=True)
    row = drills.run_drill(drill_root, "synthetic")
    assert row["pass"] is False
    assert "c2" in row["reason"]
    assert row["criteria"][1]["verdict"] == "fail"


def test_a_fail_outranks_the_manuals(drill_root):
    _add_scenario(drill_root)
    _add_graders(drill_root, c1=False, c2=True)
    row = drills.run_drill(drill_root, "synthetic")
    assert row["pass"] is False
    assert row["counts"]["manual"] == 2


def test_every_criterion_graded_and_green_is_the_only_true(drill_root):
    _add_scenario(drill_root)
    _add_graders(drill_root, c1=True, c2=False, c3=True)
    (drill_root / drills.GRADERS_REL / "synthetic" / "c2.py").write_text(
        _PASS_GRADER, encoding="utf-8")
    row = drills.run_drill(drill_root, "synthetic")
    assert row["pass"] is True
    assert row["counts"] == {"total": 3, "pass": 3, "fail": 0, "manual": 0}


def test_manual_criteria_never_count_towards_a_pass(drill_root):
    _add_scenario(drill_root)
    _add_graders(drill_root, c1=True, c3=True)
    row = drills.run_drill(drill_root, "synthetic")
    assert row["pass"] is not True
    assert row["counts"]["pass"] == 2
    assert row["counts"]["manual"] == 1


def test_the_scenario_is_materialised_into_scratch_not_the_repo(
        drill_root, tmp_path):
    _add_scenario(drill_root)
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    drills.run_drill(drill_root, "synthetic", scratch_root=scratch)
    assert (scratch / "synthetic" / "marker.txt").is_file()
    source = drill_root / drills.SCENARIOS_REL / "synthetic" / "marker.txt"
    assert source.read_text(encoding="utf-8") == "yes\n"


# ----------------------------------------------------------- exit codes


def test_exit_code_is_one_for_unresolved_and_for_failed(drill_root):
    unresolved = [{"pass": None}]
    failed = [{"pass": False}]
    passed = [{"pass": True}]
    assert drills.exit_code(unresolved) == 1
    assert drills.exit_code(failed) == 1
    assert drills.exit_code(passed) == 0
    assert drills.exit_code([]) == 2


def test_benchcli_run_returns_the_contract_shape_and_exit_one(drill_root):
    payload, code = benchcli.drills(drill_root, "run", pack="synthetic")
    assert code == 1
    for key in ("pack", "drill", "pass", "criteria"):
        assert key in payload
    assert payload["pass"] is None


def test_benchcli_list_reports_hash_and_freeze_flag(drill_root):
    payload, code = benchcli.drills(drill_root, "list")
    assert code == 0
    row = payload["drills"][0]
    assert row["pack"] == "synthetic"
    assert row["spec"] == "benchmark/drills/synthetic.md"
    assert len(row["sha256"]) == 64
    assert row["frozen_before_authoring"] is False
    assert row["runnable"] is False


def test_benchcli_list_flags_a_hash_mismatch_as_cannot_run(drill_root):
    spec = drill_root / "benchmark" / "drills" / "synthetic.md"
    spec.write_text(SPEC + "\ntampered\n", encoding="utf-8")
    payload, code = benchcli.drills(drill_root, "list")
    assert code == 2
    assert payload["hash_mismatch"] == ["synthetic"]


def test_benchcli_run_reports_a_missing_manifest_as_cannot_run(tmp_path):
    payload, code = benchcli.drills(tmp_path, "run", pack="anything")
    assert code == 2
    assert "manifest" in payload["error"]


def test_benchcli_rejects_an_unknown_action(drill_root):
    with pytest.raises(ValueError):
        benchcli.drills(drill_root, "frobnicate")


def test_findings_name_the_unresolved_drill(drill_root):
    payload, _ = benchcli.drills(drill_root, "run", pack="synthetic")
    findings = benchcli.drill_findings(payload)
    assert [f.check_id for f in findings] == ["DR001"]
    assert "synthetic" in findings.errors[0].message


# -------------------------------------------------------------- results


def test_results_ledger_appends_and_never_rewrites(drill_root):
    first = drills.run_all(drill_root)
    added = drills.append_results(drill_root, first, date="2026-08-03")
    assert added == 1
    drills.append_results(drill_root, first, date="2026-08-04")
    doc = json.loads(
        (drill_root / drills.RESULTS_REL).read_text(encoding="utf-8"))
    assert len(doc["runs"]) == 2
    assert [r["date"] for r in doc["runs"]] == ["2026-08-03", "2026-08-04"]
    assert doc["runs"][0]["pass"] is None
    assert doc["runs"][0]["criteria"]


def test_the_shipped_results_ledger_holds_all_twenty_packs():
    path = REPO / drills.RESULTS_REL
    assert path.is_file(), "the twenty drills have not been run and recorded"
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert len(doc["runs"]) >= 20
    recorded = {r["pack"] for r in doc["runs"]}
    assert recorded == set(drills.packs(REPO))
    for run in doc["runs"]:
        assert run["pass"] in (True, False, None)
        if run["pass"] is None:
            assert run["reason"], "a null verdict must carry a reason"
