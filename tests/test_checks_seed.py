"""Seed check tests: the frozen v1 fixtures read-only, plus mutants.

The fixture seeds pass the whole v1 A-rubric. Under the v2 D-series
they each carry exactly one genuine finding: their lock-books defer
design values to a first-build lock-in that no queue item schedules
(D004). The mutants each introduce one defect and assert the exact
finding it produces.
"""

import shutil
from datetime import date

from conftest import REPO_ROOT, make_seed
from tools.eos.checks.seed import parse_matrix, run_seed

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
    required, addons, empty_dirs = parse_matrix(REPO_ROOT)
    assert "docs/WORKLOG.md" in required["S"]
    assert "docs/WORKLOG.md" not in required["M"]
    assert "org/QUEUE.md" in required["M"]
    assert "org/work/NEXT.md" in required["L"]
    assert set(addons) == {"compliance", "ops-runbook", "restore-test"}
    assert empty_dirs["S"] == []
    assert empty_dirs["M"] == ["org/decisions/", "org/logs/"]
    assert set(empty_dirs["M"]).issubset(set(empty_dirs["L"]))
    assert "org/work/items/" in empty_dirs["L"]


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
    assert only(fs, "D002") == [("warn", "docs/LOCKBOOK.md",
                                 "eos_commit 1111111 not in the EOS history, "
                                 "degrading to worktree checks")]


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


def test_d005_missing_genesis_directory(tmp_path):
    seed = make_seed(tmp_path, "M")
    shutil.rmtree(seed / "org" / "logs")
    fs = run_seed(seed, ctx())
    assert only(fs, "D005") == [("error", "org/logs/",
                                 "directory required empty at scale M, missing")]


def test_d006_unresolvable_wargame_id(tmp_path):
    seed = make_seed(tmp_path, "S")
    edit(seed, "docs/LOCKBOOK.md",
         "rulings:",
         "rulings:\n  - WG-ZZZ-999 · thing · argued · a ruling citing nothing")
    fs = run_seed(seed, ctx())
    assert only(fs, "D006") == [("error", "docs/LOCKBOOK.md",
                                 "ruling cites WG-ZZZ-999, which does not resolve "
                                 "in eos_commit 6590a82")]
