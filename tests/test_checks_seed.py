"""Seed check tests: the frozen v1 fixtures read-only, plus mutants.

The fixture seeds pass the whole v1 A-rubric. Under the v2 D-series
they each carry exactly one genuine finding: their lock-books defer
design values to a first-build lock-in that no queue item schedules
(D004). The mutants each introduce one defect and assert the exact
finding it produces.

The governing scale matrix resolves at the seed's pinned eos_commit:
the frozen fixtures stay green against the matrix at their pin even
after the working-tree matrix changes, and the D007 to D009 checks
only engage when the matrix at the pin requires the policy and claims
files, so v1 seeds never see them.
"""

import subprocess
import json
import re
import shutil
from datetime import date

from conftest import REPO_ROOT, git, make_seed
from tools.eos.checks.seed import parse_matrix, parse_matrix_text, run_seed
from tools.eos.frontmatter import parse as parse_frontmatter

TODAY = date(2026, 8, 3)


def ctx():
    return {"root": REPO_ROOT, "today": TODAY, "offline": True}


def only(findings, check_id):
    return [(f.severity, f.path, f.message) for f in findings if f.check_id == check_id]


def edit(seed, rel, old, new):
    p = seed / rel
    text = p.read_text(encoding="utf-8")
    assert old in text, f"marker not found in {rel}: {old}"
    p.write_text(text.replace(old, new), encoding="utf-8")


# --- the frozen fixtures, read-only ------------------------------------


def test_seed_v1_s_fixture_only_finding_is_the_unscheduled_lockin():
    fs = run_seed(REPO_ROOT / "benchmark" / "fixtures" / "seed-v1-S", ctx())
    assert [(f.severity, f.check_id, f.path) for f in fs] == [
        ("error", "D004", "docs/LOCKBOOK.md")]
    assert "first-build lock-in in docs/WORKLOG.md" in fs.errors[0].message


def test_seed_v1_m_fixture_only_finding_is_the_unscheduled_lockin():
    fs = run_seed(REPO_ROOT / "benchmark" / "fixtures" / "seed-v1-M", ctx())
    assert [(f.severity, f.check_id, f.path) for f in fs] == [
        ("error", "D004", "docs/LOCKBOOK.md")]
    assert "first-build lock-in in org/QUEUE.md" in fs.errors[0].message


def test_matrix_parses():
    """The live matrix is v2 (S and ORG); v1's is at the archive tag.

    ADR-0003 moved the archive of record from a directory to a pushed
    tag, so the v1 matrix is read with git show rather than from the
    tree. A seed pinned before the swap still resolves v1's matrix, and
    this asserts that shape stays parseable.
    """
    required, addons, empty_dirs = parse_matrix(REPO_ROOT)
    assert set(required) == {"S", "ORG"}
    assert "docs/TASKS.md" in required["S"]
    assert "org/policy.json" in required["ORG"]
    proc = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "show",
         "archive/v1-final:kernel/SCALE_MATRIX.md"],
        capture_output=True, text=True, encoding="utf-8", check=True)
    v1 = parse_matrix_text(proc.stdout)[0]
    assert "docs/WORKLOG.md" in v1["S"]
    assert "org/QUEUE.md" in v1["M"]
    assert "org/work/NEXT.md" in v1["L"]
    assert set(addons) == {"compliance", "ops-runbook", "restore-test"}
    # v2 creates directories on first use, so the live matrix seeds none.
    assert empty_dirs.get("S", []) == []
    assert empty_dirs.get("ORG", []) == []
    v1_dirs = parse_matrix_text(proc.stdout)[2]
    assert v1_dirs["M"] == ["org/decisions/", "org/logs/"]
    assert set(v1_dirs["M"]).issubset(set(v1_dirs["L"]))
    assert "org/work/items/" in v1_dirs["L"]


# --- cannot-run shapes --------------------------------------------------


def test_missing_seed_path(tmp_path):
    fs = run_seed(tmp_path / "nowhere", ctx())
    assert [(f.severity, f.check_id, f.message) for f in fs] == [
        ("error", "D001", "seed path not found")]


def test_missing_matrix(tmp_path):
    seed = make_seed(tmp_path, "S")
    bad_ctx = {"root": tmp_path / "empty-eos", "today": TODAY, "offline": True}
    (tmp_path / "empty-eos").mkdir()
    fs = run_seed(seed, bad_ctx)
    assert [(f.severity, f.check_id, f.path) for f in fs] == [
        ("error", "D003", "kernel/SCALE_MATRIX.md")]


# --- A-rubric mutants ---------------------------------------------------


def test_a2_lockbook_header_missing_key(tmp_path):
    seed = make_seed(tmp_path, "S")
    edit(seed, "docs/LOCKBOOK.md", "eos_version: 1.0.0\n", "")
    fs = run_seed(seed, ctx())
    assert ("error", "docs/LOCKBOOK.md", "header missing eos_version") in only(fs, "E002")


def test_a2_lockbook_bad_scale(tmp_path):
    seed = make_seed(tmp_path, "S")
    edit(seed, "docs/LOCKBOOK.md", "scale: S", "scale: X")
    fs = run_seed(seed, ctx())
    assert ("error", "docs/LOCKBOOK.md", "scale must be S, M or L: X") in only(fs, "E002")


def test_a3_ruling_row_unmarked(tmp_path):
    seed = make_seed(tmp_path, "S")
    edit(seed, "docs/LOCKBOOK.md",
         "  - WG-EOS-001 · S · argued · no money, no server state, no personal data, one operator",
         "  - WG-EOS-001 · S · someday · no money, no server state, no personal data, one operator")
    fs = run_seed(seed, ctx())
    assert only(fs, "E002") == [("error", "docs/LOCKBOOK.md",
                                 "ruling row not marked argued or inherited: "
                                 "- WG-EOS-001 · S · someday · no money, no server state, "
                                 "no personal data, one operator")]


def _append(seed, rel, extra):
    p = seed / rel
    p.write_text(p.read_text(encoding="utf-8") + extra, encoding="utf-8")


def test_a4_unfilled_slot(tmp_path):
    seed = make_seed(tmp_path, "S")
    _append(seed, "docs/VENTURE_BRIEF.md", "\n{{VENTURE_NAME}}\n")
    fs = run_seed(seed, ctx())
    assert ("error", "docs/VENTURE_BRIEF.md",
            "unfilled {{SLOT}} in compiled seed") in only(fs, "E008")


def test_a4_unfilled_slot_carrying_a_digit(tmp_path):
    """{{SUCCESS_90}} is a real kernel slot, in VENTURE_BRIEF.tpl.md, and
    a slot pattern of [A-Z_]+ could not see it: rubric item A4 passed a
    seed shipping an empty slot in the brief a stranger reads first. The
    structural check was widened for this case and this one was left
    behind."""
    seed = make_seed(tmp_path, "S")
    _append(seed, "docs/VENTURE_BRIEF.md", "\n{{SUCCESS_90}}\n")
    fs = run_seed(seed, ctx())
    assert ("error", "docs/VENTURE_BRIEF.md",
            "unfilled {{SLOT}} in compiled seed") in only(fs, "E008")


def test_a5_leftover_scale_fence(tmp_path):
    seed = make_seed(tmp_path, "S")
    _append(seed, "docs/EOS_FEEDBACK.md", "\n<!-- scale: M -->\n")
    fs = run_seed(seed, ctx())
    assert ("error", "docs/EOS_FEEDBACK.md",
            "leftover scale marker in compiled seed") in only(fs, "E008")


def test_a6_required_file_missing(tmp_path):
    seed = make_seed(tmp_path, "S")
    (seed / "docs" / "VENTURE_BRIEF.md").unlink()
    fs = run_seed(seed, ctx())
    got = only(fs, "E008")
    assert ("error", "docs/VENTURE_BRIEF.md", "required at scale S, missing") in got
    assert ("error", "docs/COMPILE_REPORT.md",
            "report names absent file docs/VENTURE_BRIEF.md") in got


def test_a7_unknown_addon(tmp_path):
    seed = make_seed(tmp_path, "S")
    edit(seed, "docs/LOCKBOOK.md", "addons: []", "addons: [bogus]")
    fs = run_seed(seed, ctx())
    assert ("error", "docs/LOCKBOOK.md", "addon not in SCALE_MATRIX: bogus") in only(fs, "E008")


def test_a7_addon_file_missing(tmp_path):
    seed = make_seed(tmp_path, "S")
    edit(seed, "docs/LOCKBOOK.md", "addons: []", "addons: [ops-runbook]")
    fs = run_seed(seed, ctx())
    assert ("error", "ops/runbooks/deploy.md",
            "addon ops-runbook file missing") in only(fs, "E008")


def test_a7_addon_pattern_missing(tmp_path):
    seed = make_seed(tmp_path, "S")
    edit(seed, "docs/LOCKBOOK.md", "addons: []", "addons: [compliance]")
    fs = run_seed(seed, ctx())
    got = only(fs, "E008")
    assert any("addon compliance file missing (pattern)" == msg for _, _, msg in got)


def test_a8_ancestry_missing_row(tmp_path):
    seed = make_seed(tmp_path, "S")
    edit(seed, "docs/COMPILE_REPORT.md",
         "| docs/WORKLOG.md | kernel/templates/WORKLOG.tpl.md | 0 | 0 |\n", "")
    fs = run_seed(seed, ctx())
    assert ("error", "docs/COMPILE_REPORT.md",
            "ancestry missing for docs/WORKLOG.md") in only(fs, "E008")


def test_a9_router_divergence(tmp_path):
    seed = make_seed(tmp_path, "S")
    p = seed / "CLAUDE.md"
    p.write_text(p.read_text(encoding="utf-8") + "drift\n", encoding="utf-8")
    fs = run_seed(seed, ctx())
    assert only(fs, "E003") == [("error", "AGENTS.md",
                                 "CLAUDE.md is not a byte-identical copy")]


def test_a10_router_cap(tmp_path):
    seed = make_seed(tmp_path, "S")
    filler = "".join(f"Line {i} of filler.\n" for i in range(40))
    for name in ("AGENTS.md", "CLAUDE.md"):
        p = seed / name
        p.write_text(p.read_text(encoding="utf-8") + filler, encoding="utf-8")
    n = len((seed / "AGENTS.md").read_text(encoding="utf-8").splitlines())
    fs = run_seed(seed, ctx())
    assert only(fs, "E007") == [("error", "AGENTS.md",
                                 f"compiled router is {n} lines, cap 40")]


# --- D-series mutants ---------------------------------------------------


def test_d001_missing_compiled_from(tmp_path):
    seed = make_seed(tmp_path, "S")
    edit(seed, "docs/EOS_FEEDBACK.md",
         "compiled_from: kernel/templates/EOS_FEEDBACK.tpl.md\n", "")
    fs = run_seed(seed, ctx())
    assert only(fs, "D001") == [("error", "docs/EOS_FEEDBACK.md", "missing compiled_from")]


def test_d001_forbidden_template_key(tmp_path):
    seed = make_seed(tmp_path, "S")
    edit(seed, "docs/EOS_FEEDBACK.md", "compiled_from:",
         "template: true\ncompiled_from:")
    fs = run_seed(seed, ctx())
    assert only(fs, "D001") == [("error", "docs/EOS_FEEDBACK.md",
                                 "forbidden key in a compiled seed: template")]


def test_d001_missing_summary(tmp_path):
    seed = make_seed(tmp_path, "S")
    p = seed / "docs" / "EOS_FEEDBACK.md"
    text = p.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)
    lines = [ln for ln in lines if not ln.startswith("summary:")]
    p.write_text("".join(lines), encoding="utf-8")
    fs = run_seed(seed, ctx())
    assert only(fs, "D001") == [("error", "docs/EOS_FEEDBACK.md",
                                 "missing front-matter key: summary")]


def test_d002_compiled_from_absent_at_pin(tmp_path):
    seed = make_seed(tmp_path, "S")
    edit(seed, "docs/EOS_FEEDBACK.md",
         "compiled_from: kernel/templates/EOS_FEEDBACK.tpl.md",
         "compiled_from: kernel/templates/NOPE.tpl.md")
    fs = run_seed(seed, ctx())
    assert only(fs, "D002") == [("error", "docs/EOS_FEEDBACK.md",
                                 "compiled_from kernel/templates/NOPE.tpl.md "
                                 "absent at eos_commit 6590a82")]


def test_d002_unknown_pin_degrades_to_worktree(tmp_path):
    seed = make_seed(tmp_path, "S")
    edit(seed, "docs/LOCKBOOK.md", "eos_commit: 6590a82", "eos_commit: 1111111")
    fs = run_seed(seed, ctx())
    got = only(fs, "D002")
    assert ("warn", "docs/LOCKBOOK.md",
            "eos_commit 1111111 not in the EOS history, "
            "degrading to worktree checks") in got
    # The worktree no longer carries the v1 WORKLOG template, so the
    # degraded compiled_from check genuinely fails there.
    assert ("error", "docs/WORKLOG.md",
            "compiled_from kernel/templates/WORKLOG.tpl.md "
            "absent from the EOS worktree") in got
    # The matrix falls back to the working tree too, with a warning. That
    # tree now carries the v2 matrix, so a v1 seed also reports the v2
    # files it lacks: the fallback is visibly lossy, which is the point.
    d003 = [(sev, path) for sev, path, _ in only(fs, "D003")]
    assert ("warn", "kernel/SCALE_MATRIX.md") in d003


def test_d003_rogue_file(tmp_path):
    seed = make_seed(tmp_path, "S")
    p = seed / "extra" / "ROGUE.md"
    p.parent.mkdir()
    p.write_text("---\nsummary: A rogue file\ntype: template\ntags: [eos]\n"
                 "compiled_from: kernel/templates/AGENTS.tpl.md\n---\nBody.\n",
                 encoding="utf-8")
    fs = run_seed(seed, ctx())
    assert only(fs, "D003") == [("error", "extra/ROGUE.md",
                                 "not required at scale S, not an add-on, "
                                 "not marked authored in the compile report")]


def test_d003_authored_file_allowed(tmp_path):
    seed = make_seed(tmp_path, "S")
    p = seed / "extra" / "AUTHORED.md"
    p.parent.mkdir()
    p.write_text("---\nsummary: Authored at Session 0\ntype: template\ntags: [eos]\n"
                 "compiled_from: kernel/templates/AGENTS.tpl.md\n---\nBody.\n",
                 encoding="utf-8")
    edit(seed, "docs/COMPILE_REPORT.md",
         "| docs/COMPILE_REPORT.md | kernel/templates/COMPILE_REPORT.tpl.md | 12 | 0 |",
         "| docs/COMPILE_REPORT.md | kernel/templates/COMPILE_REPORT.tpl.md | 12 | 0 |\n"
         "| extra/AUTHORED.md | authored per doctrine | 0 | 0 |")
    fs = run_seed(seed, ctx())
    assert only(fs, "D003") == []


def test_d004_scheduled_lockin_clears_the_gate(tmp_path):
    seed = make_seed(tmp_path, "S")
    edit(seed, "docs/WORKLOG.md", "1. (none yet)",
         "1. Run the first-build lock-in and replace every deferral")
    fs = run_seed(seed, ctx())
    assert len(fs) == 0


def test_d004_missing_queue_file(tmp_path):
    seed = make_seed(tmp_path, "S")
    (seed / "docs" / "WORKLOG.md").unlink()
    fs = run_seed(seed, ctx())
    assert ("error", "docs/LOCKBOOK.md",
            "'set at first build' deferrals but the queue file "
            "docs/WORKLOG.md is missing") in only(fs, "D004")


def test_d005_missing_first_use_directory(tmp_path):
    seed = make_seed(tmp_path, "M")
    shutil.rmtree(seed / "org" / "logs")
    fs = run_seed(seed, ctx())
    assert only(fs, "D005") == [("error", "org/logs/",
                                 "directory required empty at scale M, missing")]


def test_d005_serves_v1_pinned_seeds_and_no_others(tmp_path):
    """The v2 matrix ships nothing empty, so D005 passes a v2 seed
    vacuously. It is kept because a seed pinned to a v1 commit resolves
    the v1 matrix, which does declare directories, and seeds in the
    estate are pinned that way."""
    _required, _addons, empty = parse_matrix(REPO_ROOT)
    assert empty == {"S": [], "ORG": []}
    eos = _v2_eos(tmp_path)
    assert only(run_seed(_v2_seed(tmp_path, scale="ORG"), _v2_ctx(eos)),
                "D005") == []
    # A v1-pinned seed still has directories to be missing.
    v1 = parse_matrix_text(subprocess.run(
        ["git", "-C", str(REPO_ROOT), "show",
         "archive/v1-final:kernel/SCALE_MATRIX.md"],
        capture_output=True, text=True, encoding="utf-8", check=True).stdout)[2]
    assert v1["M"] == ["org/decisions/", "org/logs/"]


def test_d006_unresolvable_wargame_id(tmp_path):
    seed = make_seed(tmp_path, "S")
    edit(seed, "docs/LOCKBOOK.md",
         "rulings:",
         "rulings:\n  - WG-ZZZ-999 · thing · argued · a ruling citing nothing")
    fs = run_seed(seed, ctx())
    assert only(fs, "D006") == [("error", "docs/LOCKBOOK.md",
                                 "ruling cites WG-ZZZ-999, which does not resolve "
                                 "in eos_commit 6590a82")]


# --- the matrix resolves at the pin, not the working tree ---------------


def _real_v1_matrix():
    """The v1 matrix exactly as the frozen fixtures pinned it, read
    from this repository's history so later worktree edits cannot
    reach it."""
    return git(REPO_ROOT, "show", "6590a82:kernel/SCALE_MATRIX.md")


def _eos_repo_for(tmp_path, seed):
    """A tmp EOS repo whose first commit is the seed's world: the real
    v1 matrix, every compiled_from target, every cited wargame. A
    second commit then trashes the working-tree matrix, so any check
    that reads the worktree instead of the pin fails loudly."""
    eos = tmp_path / "eos-at-pin"
    eos.mkdir()
    git(eos, "init", "-q", "-b", "main")
    git(eos, "config", "user.email", "suite@example.invalid")
    git(eos, "config", "user.name", "Test Suite")
    git(eos, "config", "commit.gpgsign", "false")
    matrix = eos / "kernel" / "SCALE_MATRIX.md"
    matrix.parent.mkdir(parents=True)
    matrix.write_text(_real_v1_matrix(), encoding="utf-8")
    for p in sorted(seed.rglob("*.md")):
        fm = parse_frontmatter(p.read_text(encoding="utf-8"))
        source = fm.data.get("compiled_from", "")
        if isinstance(source, str) and "/" in source:
            target = eos / source
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("template body\n", encoding="utf-8")
    lockbook = (seed / "docs" / "LOCKBOOK.md").read_text(encoding="utf-8")
    for wid in sorted(set(re.findall(r"WG-[A-Z]+-\d{3}", lockbook))):
        wg = eos / "doctrine" / "wargames" / (wid + "-fixture.md")
        wg.parent.mkdir(parents=True, exist_ok=True)
        wg.write_text("wargame body\n", encoding="utf-8")
    git(eos, "add", ".")
    git(eos, "commit", "-q", "-m", "the pinned v1 EOS")
    pin = git(eos, "rev-parse", "HEAD").strip()
    matrix.write_text("garbage, not a matrix at all\n", encoding="utf-8")
    git(eos, "add", ".")
    git(eos, "commit", "-q", "-m", "the worktree matrix is garbage now")
    return eos, pin


def test_fixture_seed_validates_against_the_matrix_at_its_pin(tmp_path):
    seed = make_seed(tmp_path, "S")
    edit(seed, "docs/WORKLOG.md", "1. (none yet)",
         "1. Run the first-build lock-in and replace every deferral")
    eos, pin = _eos_repo_for(tmp_path, seed)
    edit(seed, "docs/LOCKBOOK.md", "eos_commit: 6590a82", "eos_commit: " + pin)
    fs = run_seed(seed, {"root": eos, "today": TODAY, "offline": True})
    # Zero errors and zero warnings: the garbage working-tree matrix
    # never entered the check because the pinned matrix governs.
    assert [(f.severity, f.check_id, f.path, f.message) for f in fs] == []


def test_matrix_absent_at_pin_falls_back_to_worktree_with_warning(tmp_path):
    seed = make_seed(tmp_path, "S")
    edit(seed, "docs/WORKLOG.md", "1. (none yet)",
         "1. Run the first-build lock-in and replace every deferral")
    eos, pin = _eos_repo_for(tmp_path, seed)
    # A pin from before the matrix existed: resolvable commit, no blob.
    (eos / "seedless.txt").write_text("one\n", encoding="utf-8")
    git(eos, "add", ".")
    git(eos, "commit", "-q", "-m", "no matrix yet")
    early = git(eos, "rev-parse", "HEAD").strip()
    git(eos, "rm", "-q", "-r", "kernel")
    git(eos, "commit", "-q", "-m", "drop the kernel")
    matrixless = git(eos, "rev-parse", "HEAD").strip()
    # Restore a real worktree matrix so the fallback has law to read.
    matrix = eos / "kernel" / "SCALE_MATRIX.md"
    matrix.parent.mkdir(parents=True)
    matrix.write_text(_real_v1_matrix(), encoding="utf-8")
    assert early != matrixless
    edit(seed, "docs/LOCKBOOK.md", "eos_commit: 6590a82",
         "eos_commit: " + matrixless)
    fs = run_seed(seed, {"root": eos, "today": TODAY, "offline": True})
    got = only(fs, "D003")
    assert [(sev, path) for sev, path, _ in got] == [
        ("warn", "kernel/SCALE_MATRIX.md")]
    assert "matrix read from the working tree" in got[0][2]


def test_v2_matrix_layout_parses():
    required, addons, empty_dirs = parse_matrix_text(
        (REPO_ROOT / "kernel" / "SCALE_MATRIX.md")
        .read_text(encoding="utf-8"))
    assert set(required) == {"S", "ORG"}
    assert "docs/policy.json" in required["S"]
    assert "docs/policy.json" not in required["ORG"]
    assert "org/policy.json" in required["ORG"]
    assert "org/claims.json" in required["ORG"]
    assert "org/cadence.json" in required["ORG"]
    assert set(addons) == {"compliance", "ops-runbook", "restore-test"}
    assert empty_dirs == {"S": [], "ORG": []}


# --- D007, D008, D009 (matrix-gated policy, guard and claims) -----------


V2_TEST_MATRIX = """---
summary: Test matrix in the v2 layout
type: kernel
tags: [eos]
---

# SCALE_MATRIX

## The matrix

| path | source | S | ORG |
| --- | --- | --- | --- |
| AGENTS.md | kernel/templates/AGENTS.tpl.md | x | x |
| CLAUDE.md | byte copy of AGENTS.md | x | x |
| docs/LOCKBOOK.md | kernel/templates/LOCKBOOK.tpl.md | x | x |
| docs/policy.json | kernel/templates/org/policy.tpl.json | x | |
| org/policy.json | kernel/templates/org/policy.tpl.json | | x |
| org/claims.json | seeded empty per kernel/schemas/claims.schema.json | | x |

## Trigger add-ons

| addon | file | source | trigger |
| --- | --- | --- | --- |
| ops-runbook | ops/runbooks/deploy.md | authored per the stack profile | server state |
"""


def _valid_policy():
    doc = json.loads(
        (REPO_ROOT / "kernel" / "templates" / "org" / "policy.tpl.json")
        .read_text(encoding="utf-8"))
    doc.pop("_slots")
    doc["venture"] = "Testfield"
    doc["capability_profile"] = "docs/capability-profile.json"
    doc["risk"]["path_patterns"] = {
        "reversible": ["docs/**"],
        "sensitive": ["src/auth/**"],
        "protected": ["docs/policy.json"],
    }
    doc["guard"]["mapping_ref"] = "docs/guard-mapping.json"
    return doc


def _v2_eos(tmp_path, matrix=V2_TEST_MATRIX):
    eos = tmp_path / "v2eos"
    (eos / "kernel" / "schemas").mkdir(parents=True)
    (eos / "kernel" / "SCALE_MATRIX.md").write_text(matrix, encoding="utf-8")
    for name in ("policy.schema.json", "claims.schema.json"):
        shutil.copy(REPO_ROOT / "kernel" / "schemas" / name,
                    eos / "kernel" / "schemas" / name)
    return eos


def _v2_seed(tmp_path, scale="S", policy=None):
    seed = tmp_path / "v2seed"
    (seed / "docs").mkdir(parents=True)
    (seed / "docs" / "LOCKBOOK.md").write_text(
        "---\nsummary: Test lock-book\ntype: template\ntags: [eos]\n"
        "compiled_from: kernel/templates/LOCKBOOK.tpl.md\n"
        "eos_version: 2.0.0\neos_commit: 0000000\nscale: %s\n"
        "stack: STACK-test\naddons: []\n---\nBody.\n" % scale,
        encoding="utf-8")
    if policy is not None:
        rel = "docs/policy.json" if scale == "S" else "org/policy.json"
        target = seed / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(policy, indent=2) + "\n", encoding="utf-8")
    return seed


def _v2_ctx(eos):
    return {"root": eos, "today": TODAY, "offline": True}


def test_d007_valid_policy_is_quiet(tmp_path):
    eos = _v2_eos(tmp_path)
    seed = _v2_seed(tmp_path, policy=_valid_policy())
    fs = run_seed(seed, _v2_ctx(eos))
    assert only(fs, "D007") == []
    assert only(fs, "D008") == []


def test_d007_org_scale_reads_org_policy(tmp_path):
    eos = _v2_eos(tmp_path)
    policy = _valid_policy()
    del policy["approvals"]
    seed = _v2_seed(tmp_path, scale="ORG", policy=policy)
    got = only(fs := run_seed(seed, _v2_ctx(eos)), "D007")
    assert len(got) == 1
    sev, path, msg = got[0]
    assert (sev, path) == ("error", "org/policy.json")
    assert "'approvals' is a required property" in msg
    # And the v2 scale name itself is legal under the v2 matrix.
    assert only(fs, "E002") == []


def test_d007_malformed_policy_json(tmp_path):
    eos = _v2_eos(tmp_path)
    seed = _v2_seed(tmp_path, policy=_valid_policy())
    (seed / "docs" / "policy.json").write_text("{not json", encoding="utf-8")
    got = only(run_seed(seed, _v2_ctx(eos)), "D007")
    assert len(got) == 1
    assert got[0][0] == "error"
    assert got[0][2].startswith("malformed JSON")


def test_d007_schema_invalid_policy(tmp_path):
    eos = _v2_eos(tmp_path)
    policy = _valid_policy()
    policy["protected_pointers"] = ["/approvals"]  # /risk missing
    seed = _v2_seed(tmp_path, policy=policy)
    got = only(run_seed(seed, _v2_ctx(eos)), "D007")
    assert got, "a policy without /risk protected must fail D007"
    assert all(sev == "error" and path == "docs/policy.json"
               for sev, path, _ in got)


def test_d007_missing_jsonschema_names_the_install_command(tmp_path, monkeypatch):
    import builtins
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "jsonschema":
            raise ImportError("no jsonschema")
        return real_import(name, *args, **kwargs)

    eos = _v2_eos(tmp_path)
    seed = _v2_seed(tmp_path, policy=_valid_policy())
    monkeypatch.setattr(builtins, "__import__", fake_import)
    got = only(run_seed(seed, _v2_ctx(eos)), "D007")
    assert len(got) == 1
    assert got[0][0] == "error"
    assert "pip install" in got[0][2]


def test_d008_validated_true_needs_the_mapping_shipped(tmp_path):
    eos = _v2_eos(tmp_path)
    policy = _valid_policy()
    policy["guard"]["validated"] = True
    seed = _v2_seed(tmp_path, policy=policy)
    got = only(run_seed(seed, _v2_ctx(eos)), "D008")
    assert len(got) == 1
    sev, path, msg = got[0]
    assert (sev, path) == ("error", "docs/policy.json")
    assert "not shipped in the seed" in msg
    assert "fails closed" in msg


def test_d008_validated_true_with_shipped_mapping_is_quiet(tmp_path):
    eos = _v2_eos(tmp_path)
    policy = _valid_policy()
    policy["guard"]["validated"] = True
    seed = _v2_seed(tmp_path, policy=policy)
    (seed / "docs" / "guard-mapping.json").write_text(
        "{\"classes\": {}}\n", encoding="utf-8")
    assert only(run_seed(seed, _v2_ctx(eos)), "D008") == []


def test_d008_validated_false_is_the_manual_only_declaration(tmp_path):
    eos = _v2_eos(tmp_path)
    seed = _v2_seed(tmp_path, policy=_valid_policy())  # validated: false
    assert only(run_seed(seed, _v2_ctx(eos)), "D008") == []


def test_d008_absent_validated_reads_the_same_as_false(tmp_path):
    """The seed check, the policy schema and tools/eos/guard.py all
    read an absent validated key as fail-closed. The guard used to read
    it as "not withdrawn", which was the one permissive reading of the
    three, and tests/test_guard.py pins the other half of this."""
    eos = _v2_eos(tmp_path)
    policy = _valid_policy()
    del policy["guard"]["validated"]
    seed = _v2_seed(tmp_path, policy=policy)
    assert only(run_seed(seed, _v2_ctx(eos)), "D008") == []


def test_d008_missing_guard_section(tmp_path):
    eos = _v2_eos(tmp_path)
    policy = _valid_policy()
    del policy["guard"]
    seed = _v2_seed(tmp_path, policy=policy)
    got = only(run_seed(seed, _v2_ctx(eos)), "D008")
    assert got == [("error", "docs/policy.json",
                    "policy has no guard section; guarded classes must ship "
                    "an adapter mapping or stay manual-only")]


def test_d008_guard_without_mapping_ref(tmp_path):
    eos = _v2_eos(tmp_path)
    policy = _valid_policy()
    del policy["guard"]["mapping_ref"]
    policy["guard"]["validated"] = True
    seed = _v2_seed(tmp_path, policy=policy)
    got = only(run_seed(seed, _v2_ctx(eos)), "D008")
    assert ("error", "docs/policy.json", "guard names no mapping_ref") in got
    assert any("autonomous guarded actions fail closed" in msg
               for _, _, msg in got)


def _claims_seed(tmp_path, claims_text):
    seed = _v2_seed(tmp_path, scale="ORG", policy=_valid_policy())
    (seed / "org" / "claims.json").write_text(claims_text, encoding="utf-8")
    return seed


def test_d009_seeded_empty_claims_are_quiet(tmp_path):
    eos = _v2_eos(tmp_path)
    seed = _claims_seed(tmp_path, json.dumps(
        {"version": 1, "assigned": "2026-08-02", "lanes": []}) + "\n")
    assert only(run_seed(seed, _v2_ctx(eos)), "D009") == []


def test_d009_schema_invalid_claims(tmp_path):
    eos = _v2_eos(tmp_path)
    seed = _claims_seed(tmp_path, json.dumps(
        {"version": 1, "lanes": []}) + "\n")  # assigned missing
    got = only(run_seed(seed, _v2_ctx(eos)), "D009")
    assert len(got) == 1
    sev, path, msg = got[0]
    assert (sev, path) == ("error", "org/claims.json")
    assert "'assigned' is a required property" in msg


def test_d009_seeded_claims_must_be_empty(tmp_path):
    eos = _v2_eos(tmp_path)
    lane = {"lane_id": "lane/p4-a1", "task_id": "T-0001",
            "session_id": "sess-1", "host": "box-1",
            "path_claims": ["src/"], "acquired": "2026-08-02T09:00",
            "expires": "2026-08-03T09:00"}
    seed = _claims_seed(tmp_path, json.dumps(
        {"version": 1, "assigned": "2026-08-02", "lanes": [lane]}) + "\n")
    got = only(run_seed(seed, _v2_ctx(eos)), "D009")
    assert got == [("error", "org/claims.json",
                    "seeded claims must be an empty lanes list")]


def test_d007_gate_v1_matrix_never_fires_policy_checks(tmp_path):
    # A v1 seed with a rogue policy file: the v1 matrix requires no
    # policy file at any scale, so D007 to D009 stay silent.
    seed = make_seed(tmp_path, "S")
    (seed / "docs" / "policy.json").write_text("{not even json",
                                               encoding="utf-8")
    fs = run_seed(seed, ctx())
    assert only(fs, "D007") == []
    assert only(fs, "D008") == []
    assert only(fs, "D009") == []


# --- D010, D011 the Genesis blueprint set -------------------------------


GENESIS_DESTINATIONS = {
    "kernel/templates/PRODUCT_MAP.tpl.md": "docs/genesis/PRODUCT_MAP.md",
    "kernel/templates/WORK_PACKAGE.tpl.md": "docs/genesis/WORK_PACKAGE.md",
    "kernel/templates/RESEARCH_PACKET.tpl.md": "docs/genesis/RESEARCH_PACKET.md",
    "kernel/templates/ACCEPTANCE_SPINE.tpl.md": "docs/genesis/ACCEPTANCE_SPINE.md",
    "kernel/templates/LENS.tpl.md": "docs/lenses/LENS.md",
}
GENESIS_MATRIX = V2_TEST_MATRIX.replace(
    "\n\n## Trigger add-ons",
    "\n" + "".join("| %s | %s | | x |\n" % (dest, src)
                   for src, dest in GENESIS_DESTINATIONS.items())
    + "\n## Trigger add-ons")
# The shape the live kernel matrix has: the Genesis rows marked at both
# scales. D010 and D011 follow the matrix, so this is the matrix that
# puts them to work at S.
GENESIS_MATRIX_BOTH_SCALES = V2_TEST_MATRIX.replace(
    "\n\n## Trigger add-ons",
    "\n" + "".join("| %s | %s | x | x |\n" % (dest, src)
                   for src, dest in GENESIS_DESTINATIONS.items())
    + "\n## Trigger add-ons")

SPINE_BODY = """
## The manifest

| journey | condition id | check id | state | package |
| --- | --- | --- | --- | --- |
| J1 | A1.1 |  | expected-fail | WP-01 |
"""


def _genesis_file(seed, rel, source, body="Body.\n"):
    target = seed / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        "---\nsummary: A compiled Genesis file\ntype: template\ntags: [eos]\n"
        "compiled_from: %s\n---\n%s" % (source, body),
        encoding="utf-8")


def _genesis_seed(tmp_path, missing=(), spine_body=SPINE_BODY, scale="ORG"):
    seed = _v2_seed(tmp_path, scale=scale)
    for source, dest in GENESIS_DESTINATIONS.items():
        if source in missing:
            continue
        body = spine_body if source.endswith("ACCEPTANCE_SPINE.tpl.md") \
            else "Body.\n"
        _genesis_file(seed, dest, source, body)
    return seed


def test_d010_reports_every_missing_genesis_template(tmp_path):
    eos = _v2_eos(tmp_path, GENESIS_MATRIX)
    seed = _genesis_seed(tmp_path, missing=GENESIS_DESTINATIONS)
    paths = [p for _s, p, _m in only(run_seed(seed, _v2_ctx(eos)), "D010")]
    assert paths == list(GENESIS_DESTINATIONS)


def test_d010_is_quiet_when_the_set_is_compiled_in(tmp_path):
    eos = _v2_eos(tmp_path, GENESIS_MATRIX)
    seed = _genesis_seed(tmp_path)
    fs = run_seed(seed, _v2_ctx(eos))
    assert only(fs, "D010") == []
    assert only(fs, "D011") == []


def test_d010_matches_on_the_source_not_the_destination(tmp_path):
    """The matrix decides where a compiled file lands. D010 reads
    compiled_from so it does not have to agree with the matrix twice."""
    eos = _v2_eos(tmp_path, GENESIS_MATRIX)
    seed = _genesis_seed(tmp_path, missing=["kernel/templates/LENS.tpl.md"])
    _genesis_file(seed, "docs/lenses/LENS-0001.md",
                  "kernel/templates/LENS.tpl.md")
    assert only(run_seed(seed, _v2_ctx(eos)), "D010") == []


def test_d010_stays_quiet_where_the_matrix_marks_the_rows_org_only(tmp_path):
    """The matrix rules the scale, not a list kept beside the check.
    This matrix marks the Genesis rows at ORG and not at S, so an S seed
    is not asked for a file it was never told to compile."""
    eos = _v2_eos(tmp_path, GENESIS_MATRIX)
    seed = _v2_seed(tmp_path, scale="S")
    assert only(run_seed(seed, _v2_ctx(eos)), "D010") == []


def test_d010_runs_at_s_where_the_matrix_marks_the_rows_there(tmp_path):
    """Which is the live matrix's ruling. ADR-0006 scopes the lite form
    to running the phase, not to the file set, so an S seed carries the
    blank forms and D010 asks for them."""
    eos = _v2_eos(tmp_path, GENESIS_MATRIX_BOTH_SCALES)
    seed = _v2_seed(tmp_path, scale="S")
    paths = [p for _s, p, _m in only(run_seed(seed, _v2_ctx(eos)), "D010")]
    assert paths == list(GENESIS_DESTINATIONS)


def test_d011_reads_an_s_scale_spine(tmp_path):
    """The gap this closes: the spine is required at S, and D011 sat
    behind an ORG-only gate, so an S seed whose spine had lost its
    marking passed the auto gate silently."""
    eos = _v2_eos(tmp_path, GENESIS_MATRIX_BOTH_SCALES)
    seed = _genesis_seed(tmp_path, scale="S",
                         spine_body="No marking and no manifest here.\n")
    got = only(run_seed(seed, _v2_ctx(eos)), "D011")
    assert [p for _s, p, _m in got] == ["docs/genesis/ACCEPTANCE_SPINE.md"] * 2
    assert "never says expected-fail" in got[0][2]
    assert "no manifest table with a state column" in got[1][2]


def test_d010_stays_quiet_when_the_matrix_predates_genesis(tmp_path):
    """A seed pinned to a commit from before the templates existed could
    not have carried them, so it is not asked to."""
    eos = _v2_eos(tmp_path)
    seed = _v2_seed(tmp_path, scale="ORG")
    assert only(run_seed(seed, _v2_ctx(eos)), "D010") == []


def _live_matrix_seed(tmp_path, scale, spine_body=SPINE_BODY, missing=()):
    """An ORG or S seed judged by this repository's own scale matrix.

    The lock-book pins a commit that does not resolve, so the check
    falls back to the working-tree matrix with a D003 warning. That is
    what puts the live matrix, the live GENESIS_TEMPLATES tuple and the
    live destinations under one test: the synthetic matrices elsewhere
    in this file prove the logic, and this proves the wiring.
    """
    from tools.eos.checks.seed import (
        GENESIS_TEMPLATES,
        SPINE_TEMPLATE,
        parse_matrix_sources,
    )

    text = (REPO_ROOT / "kernel" / "SCALE_MATRIX.md").read_text(encoding="utf-8")
    destinations = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and cells[1] in GENESIS_TEMPLATES:
            destinations[cells[1]] = cells[0]
    assert set(destinations) == set(GENESIS_TEMPLATES), sorted(destinations)
    assert set(GENESIS_TEMPLATES) <= parse_matrix_sources(text, scale=scale)

    seed = _v2_seed(tmp_path, scale=scale)
    for source, dest in destinations.items():
        if source in missing:
            continue
        body = spine_body if source == SPINE_TEMPLATE else "Body.\n"
        _genesis_file(seed, dest, source, body)
    return seed, destinations


def test_d010_and_d011_engage_against_the_live_matrix(tmp_path):
    """D010 and D011 had never run outside a synthetic matrix.

    Both engage through the source column of kernel/SCALE_MATRIX.md, so
    a renamed template path there switches both off with every other
    test still green. Here the seed carries the whole Genesis set and a
    spine that has lost its marking, and both checks have to speak.
    """
    seed, _dest = _live_matrix_seed(
        tmp_path, "ORG", spine_body="No marking and no manifest here.\n")
    fs = run_seed(seed, ctx())
    assert only(fs, "D010") == []
    messages = [m for _s, _p, m in only(fs, "D011")]
    assert len(messages) == 2
    assert any("never says expected-fail" in m for m in messages)
    assert any("no manifest table with a state column" in m for m in messages)


def test_d010_reports_the_live_genesis_set_a_seed_did_not_compile(tmp_path):
    from tools.eos.checks.seed import GENESIS_TEMPLATES

    seed, destinations = _live_matrix_seed(tmp_path, "ORG",
                                           missing=GENESIS_TEMPLATES)
    reported = [p for _s, p, _m in only(run_seed(seed, ctx()), "D010")]
    assert reported == list(GENESIS_TEMPLATES)
    assert set(destinations.values()) == {
        "docs/PRODUCT_MAP.md", "docs/ACCEPTANCE_SPINE.md",
        "docs/genesis/WORK_PACKAGE.md", "docs/genesis/RESEARCH_PACKET.md",
        "docs/genesis/LENS.md"}


def test_d011_engages_at_s_under_the_live_matrix(tmp_path):
    """The scope question, settled against the matrix rather than a
    scale list kept beside the check: the live matrix marks the Genesis
    rows at S as well as ORG, so an S spine is checked too."""
    seed, _dest = _live_matrix_seed(
        tmp_path, "S", spine_body="Every check starts expected-fail.\n")
    got = only(run_seed(seed, ctx()), "D011")
    assert [p for _s, p, _m in got] == ["docs/ACCEPTANCE_SPINE.md"]
    assert "no manifest table with a state column" in got[0][2]


def test_the_shipped_matrix_still_names_every_genesis_template():
    """D010 and D011 engage through the source column of
    kernel/SCALE_MATRIX.md. Nothing else binds the two together, so a
    renamed template path there would switch both checks off with every
    other test still green. The matrix's own prose rules that the five
    Genesis forms ship at both scales; this holds it to that."""
    from tools.eos.checks.seed import GENESIS_TEMPLATES, parse_matrix_sources

    text = (REPO_ROOT / "kernel" / "SCALE_MATRIX.md").read_text(encoding="utf-8")
    missing = set(GENESIS_TEMPLATES) - parse_matrix_sources(text)
    assert missing == set(), "matrix no longer names: %s" % sorted(missing)
    for scale in ("S", "ORG"):
        at_scale = parse_matrix_sources(text, scale=scale)
        assert set(GENESIS_TEMPLATES) <= at_scale, (
            "%s no longer requires: %s"
            % (scale, sorted(set(GENESIS_TEMPLATES) - at_scale)))


def test_d010_leaves_the_frozen_org_fixture_alone():
    seed = REPO_ROOT / "benchmark" / "fixtures" / "seed-v2-ORG"
    fs = run_seed(seed, ctx())
    assert only(fs, "D010") == []
    assert only(fs, "D011") == []


def test_d011_wants_the_expected_fail_marking(tmp_path):
    eos = _v2_eos(tmp_path, GENESIS_MATRIX)
    seed = _genesis_seed(tmp_path, spine_body="""
## The manifest

| journey | condition id | check id | state | package |
| --- | --- | --- | --- | --- |
| J1 | A1.1 |  | green | WP-01 |
""")
    got = only(run_seed(seed, _v2_ctx(eos)), "D011")
    assert len(got) == 1
    assert got[0][1] == "docs/genesis/ACCEPTANCE_SPINE.md"
    assert "never says expected-fail" in got[0][2]
    assert "nothing here runs the suite" in got[0][2]


def test_d011_wants_a_manifest_with_a_state_column(tmp_path):
    eos = _v2_eos(tmp_path, GENESIS_MATRIX)
    seed = _genesis_seed(
        tmp_path,
        spine_body="Every check starts expected-fail. No table here.\n")
    got = only(run_seed(seed, _v2_ctx(eos)), "D011")
    assert len(got) == 1
    assert "no manifest table with a state column" in got[0][2]


# --- cannot-run findings are named at source ----------------------------


def test_cannot_run_names_the_two_findings_the_cli_maps_to_exit_two(tmp_path):
    """The CLI used to look for the words "cannot run" in the message.
    Neither message says them, so the exit-2 branch never ran once."""
    from tools.eos.checks.seed import cannot_run

    missing_seed = run_seed(tmp_path / "nowhere", ctx())
    assert [f.check_id for f in cannot_run(missing_seed)] == ["D001"]

    (tmp_path / "empty-eos").mkdir()
    seed = make_seed(tmp_path, "S")
    no_matrix = run_seed(seed, {"root": tmp_path / "empty-eos",
                                "today": TODAY, "offline": True})
    assert [f.check_id for f in cannot_run(no_matrix)] == ["D003"]

    # A seed that merely fails its rubric is not a run that could not
    # happen, and must not be reported as one.
    assert cannot_run(run_seed(make_seed(tmp_path, "M"), ctx())) == []
