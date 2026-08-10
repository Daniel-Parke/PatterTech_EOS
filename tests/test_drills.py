"""Drill runner tests: real verdicts, honest manuals, no false greens.

Most shipped drills still have no scenario and no graders, so the tests
that prove the runner actually evaluates anything build their own
synthetic drill root: a manifest, a spec, a scenario tree and graders.
That way pass, fail and manual are all exercised for real rather than
asserted about a stub.

The architecture drill is the exception and has both, so it is also
tested end to end against the fixture it ships with.
"""

import json
import shutil
import subprocess
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
    # Through the same function the manifest is recorded with. Hashing
    # raw bytes here made the fixture depend on the platform: _write
    # goes through text mode, so Windows puts CRLF on disk and the
    # digest stopped matching the moment the drill hasher normalised.
    digest = drills.sha256_file(spec)
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
    # Counted against the specs on disk rather than against a literal.
    # This assertion used to read `== 20`, which meant adding a drill
    # broke a test that had nothing to say about the new drill; what it
    # is really for is that the manifest and the directory agree.
    on_disk = {p.stem for p in
               (REPO / "benchmark" / "drills").glob("*.md")
               if p.name != "README.md"}
    assert set(manifest["drills"]) == on_disk
    for pack in drills.packs(REPO, manifest):
        spec = drills.read_spec(REPO, pack, manifest=manifest)
        assert spec["criteria"], "%s parsed no criteria" % pack
        assert spec["frozen_before_authoring"] in (True, False)


def test_the_manifest_records_which_drills_predate_their_pack():
    manifest = drills.load_manifest(REPO)
    entries = manifest["drills"].values()
    flags = [e["frozen_before_authoring"] for e in entries]
    # The Wave A eight are the only independent oracles in the set, and
    # that number is a historical fact worth pinning. Everything else
    # was written after its pack, so the complement is derived rather
    # than hardcoded and a new drill does not break this test.
    wave_a = [e for e in entries if e.get("wave") == "A"]
    assert len(wave_a) == 8, "the Wave A eight predate their packs"
    assert all(e["frozen_before_authoring"] for e in wave_a)
    assert flags.count(True) == 8
    assert flags.count(False) == len(flags) - 8


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


def test_the_shipped_results_ledger_holds_a_row_for_every_drill():
    path = REPO / drills.RESULTS_REL
    assert path.is_file(), "the drills have not been run and recorded"
    doc = json.loads(path.read_text(encoding="utf-8"))
    recorded = {r["pack"] for r in doc["runs"]}
    assert recorded == set(drills.packs(REPO))
    for run in doc["runs"]:
        assert run["pass"] in (True, False, None)
        if run["pass"] is None:
            assert run["reason"], "a null verdict must carry a reason"


# --------------------------------------------- the unsettled exit code


def test_exit_two_is_manual_not_a_failure(tmp_path):
    """A grader that cannot look must not report the work as broken.

    Three of the architecture graders drive lint-imports. On a machine
    without import-linter the honest answer is that nothing was
    settled, and reporting that as a fail invents findings against a
    tree nobody inspected.
    """
    grader = tmp_path / "c1.py"
    grader.write_text(
        "import json, sys\n"
        "print(json.dumps({'id': 'c1', 'pass': False,"
        " 'reason': 'tool missing'}))\n"
        "sys.exit(2)\n", encoding="utf-8")
    verdict, reason = drills.run_grader(grader, tmp_path)
    assert verdict == drills.MANUAL
    assert reason == "tool missing"


def test_a_nonzero_that_is_not_two_is_still_a_failure(tmp_path):
    grader = tmp_path / "c1.py"
    grader.write_text(
        "import json, sys\n"
        "print(json.dumps({'id': 'c1', 'pass': False, 'reason': 'no'}))\n"
        "sys.exit(1)\n", encoding="utf-8")
    verdict, _ = drills.run_grader(grader, tmp_path)
    assert verdict == drills.FAIL


# ------------------------------------------- the architecture drill


def test_the_architecture_drill_ships_a_scenario_and_ten_graders():
    scenario = REPO / drills.SCENARIOS_REL / "architecture"
    assert scenario.is_dir(), "the drill spec says the toy repo is stored"
    for pkg in ("billing", "catalogue", "shared"):
        assert (scenario / pkg).is_dir()
    for n in range(1, 11):
        assert drills.grader_for(REPO, "architecture", n) is not None


def test_the_architecture_graders_reject_the_untouched_fixture():
    """A grader that cannot fail is not a grader.

    The fixture is the repo before the agent does anything: no
    contract, no record, no view, no price lookup. Every criterion that
    can be settled without import-linter must come back fail.
    """
    row = drills.run_drill(REPO, "architecture")
    assert row["pass"] is not True
    verdicts = {c["id"]: c["verdict"] for c in row["criteria"]}
    for cid in ("c1", "c2", "c5", "c6", "c7", "c8", "c9", "c10"):
        assert verdicts[cid] == drills.FAIL, cid


def test_the_architecture_graders_accept_a_correct_tree(tmp_path):
    """And the other direction: a correct delivery passes.

    Built here rather than committed, so the expected solution is not
    sitting in the repository next to the drill for an agent to find.
    """
    import shutil
    tree = tmp_path / "attempt"
    shutil.copytree(REPO / drills.SCENARIOS_REL / "architecture", tree)

    (tree / ".importlinter").write_text(
        "[importlinter]\n"
        "root_packages =\n    billing\n    catalogue\n    shared\n\n"
        "[importlinter:contract:catalogue-independent]\n"
        "name = The catalogue must never know about billing\n"
        "type = forbidden\n"
        "source_modules =\n    catalogue\n"
        "forbidden_modules =\n    billing\n", encoding="utf-8")

    (tree / "docs" / "decisions").mkdir(parents=True)
    (tree / "docs" / "decisions" / "0001-boundary.md").write_text(
        "# Boundary\n\n## Considered Options\n\n"
        "- Enforce with import-linter in CI\n- Rely on review\n\n"
        "## Decision Outcome\n\n"
        "Enforce with import-linter. Billing may read the catalogue\n"
        "through its public interface; the catalogue must never import\n"
        "billing.\n", encoding="utf-8")

    (tree / ".github" / "workflows").mkdir(parents=True)
    (tree / ".github" / "workflows" / "ci.yml").write_text(
        "jobs:\n  b:\n    steps:\n      - run: lint-imports\n",
        encoding="utf-8")

    (tree / "docs" / "architecture.md").write_text(
        "# Architecture\n\n## Building Block View\n\n"
        "billing reads catalogue through its public interface.\n",
        encoding="utf-8")

    (tree / "billing" / "price_lookup.py").write_text(
        "from catalogue import api\n\n\n"
        "def list_price(pid):\n    return api.get_product(pid)\n",
        encoding="utf-8")

    row = drills.run_drill(REPO, "architecture", attempt=str(tree))
    verdicts = {c["id"]: c["verdict"] for c in row["criteria"]}
    reasons = {c["id"]: c["reason"] for c in row["criteria"]}
    for cid in ("c1", "c2", "c5", "c6", "c7", "c8", "c9"):
        assert verdicts[cid] == drills.PASS, (cid, reasons[cid])
    # c3, c4 and c10 need import-linter; pass or manual, never fail.
    for cid in ("c3", "c4", "c10"):
        assert verdicts[cid] in (drills.PASS, drills.MANUAL), reasons[cid]


def test_the_wrong_direction_contract_does_not_satisfy_c2(tmp_path):
    """Both package names in one contract is not the same as the rule.

    A forbidden contract from billing to catalogue permits exactly what
    the prompt forbade, and a grader matching on names alone would pass
    it.
    """
    import shutil
    tree = tmp_path / "attempt"
    shutil.copytree(REPO / drills.SCENARIOS_REL / "architecture", tree)
    (tree / ".importlinter").write_text(
        "[importlinter]\nroot_packages =\n    billing\n    catalogue\n\n"
        "[importlinter:contract:backwards]\n"
        "name = Backwards\ntype = forbidden\n"
        "source_modules =\n    billing\n"
        "forbidden_modules =\n    catalogue\n", encoding="utf-8")

    grader = drills.grader_for(REPO, "architecture", 2)
    verdict, reason = drills.run_grader(grader, tree)
    assert verdict == drills.FAIL
    assert "wrong direction" in reason


# ------------------------------------------------- the coding drill


def test_the_coding_drill_ships_a_scenario_and_seven_graders():
    scenario = REPO / drills.SCENARIOS_REL / "coding"
    assert scenario.is_dir()
    assert (scenario / "readings" / "parser.py").is_file()
    assert (scenario / "golden_input.txt").is_file()
    for n in range(1, 8):
        assert drills.grader_for(REPO, "coding", n) is not None
    # Criterion 8 is wall clock and no network, which nothing here can
    # settle, so it has no grader and reports manual.
    assert drills.grader_for(REPO, "coding", 8) is None


def test_the_coding_graders_reject_the_untouched_fixture():
    """A grader that cannot fail is not a grader.

    The fixture is the package before the agent touches it: no tests, no
    declared failure mode, and a bare except that drops malformed rows.
    """
    row = drills.run_drill(REPO, "coding")
    assert row["pass"] is not True
    verdicts = {c["id"]: c["verdict"] for c in row["criteria"]}
    reasons = {c["id"]: c["reason"] for c in row["criteria"]}
    for cid in ("c1", "c2", "c3", "c4", "c5", "c6"):
        assert verdicts[cid] == drills.FAIL, (cid, reasons[cid])
    assert "dropped silently" in reasons["c3"]


@pytest.mark.skipif(shutil.which("git") is None, reason="needs git")
def test_a_narrower_except_does_not_satisfy_the_coding_criteria(tmp_path):
    """The swallow the frozen grep misses, and the call that catches it.

    `except ValueError: continue` drops the malformed row exactly as the
    fixture's bare `except:` does, and the grep the spec writes out
    returns nothing for it. Criterion 4 is about the swallow and
    criterion 3 about what the caller sees, so both have to say no, and
    neither may say it because of a missing token.
    """
    tree = tmp_path / "attempt"
    shutil.copytree(REPO / drills.SCENARIOS_REL / "coding", tree)
    source = tree / "readings" / "parser.py"
    text = source.read_text(encoding="utf-8")
    source.write_text(text.replace("        except:\n",
                                   "        except ValueError:\n"),
                      encoding="utf-8")
    for args in (("init", "-q"), ("add", "-A"),
                 ("-c", "user.name=t", "-c", "user.email=t@t.invalid",
                  "commit", "-q", "-m", "baseline")):
        subprocess.run(["git", "-C", str(tree), *args], check=True,
                       capture_output=True)

    verdict, reason = drills.run_grader(
        drills.grader_for(REPO, "coding", 4), tree)
    assert verdict == drills.FAIL, reason
    assert "do nothing with it" in reason

    verdict, reason = drills.run_grader(
        drills.grader_for(REPO, "coding", 3), tree)
    assert verdict == drills.FAIL, reason
    assert "dropped silently" in reason
