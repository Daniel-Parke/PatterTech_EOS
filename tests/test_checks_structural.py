"""Structural E-series tests: one defect per check, exact findings.

Includes the parity hard gate: the registry's E-checks over this
repository must produce exactly the findings the v1 checker prints.
"""

import re
import shutil
import subprocess
import sys
from datetime import date

from conftest import REPO_ROOT, make_repo
from tools.eos.checks import run_all
from tools.eos.checks.structural import build_index, build_wargame_index, write_indexes
from tools.eos.repo import SKIP_DIRS, RepoModel

TODAY = date(2026, 8, 3)


def ctx_for(root, today=TODAY):
    model = RepoModel.load(root, today=today)
    return {"model": model, "root": model.root, "today": today, "offline": True}


def run_e(root, today=TODAY):
    return run_all(ctx_for(root, today), series="E")


def only(findings, check_id):
    return [(f.severity, f.path, f.message) for f in findings if f.check_id == check_id]


def edit(root, rel, old, new):
    p = root / rel
    text = p.read_text(encoding="utf-8")
    assert old in text, f"marker not found in {rel}: {old}"
    p.write_text(text.replace(old, new), encoding="utf-8")


# --- parity hard gate ---------------------------------------------------


V1_LINE = re.compile(r"^(ERROR|warn)\s+(E\d{3})\s+(.+?): (.*)$")


def test_v1_checker_is_a_forwarding_shim():
    """The v1 checker was the port's parity gate and is now retired.

    It proved the E-series port faithful while both could see the same
    tree. The pack restructure moved the knowledge layer, so v1's
    hardcoded doctrine and wargame-index paths no longer resolve and
    parity is not a meaningful assertion. The original is kept at
    archive/v1/tools/eos_check.py; the live path forwards.
    """
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "eos_check.py"), "--repo"],
        capture_output=True, text=True, encoding="utf-8", cwd=str(REPO_ROOT),
    )
    assert "deprecated" in proc.stderr
    assert "errors," in proc.stderr or "errors," in proc.stdout

def test_minirepo_is_green(tmp_path):
    assert run_e(make_repo(tmp_path)) == []


# --- E001 ---------------------------------------------------------------


def test_e001_stale_index(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "GOVERNANCE.md", "summary: Minirepo governance", "summary: Edited governance")
    fs = run_e(root)
    assert only(fs, "E001") == [("error", "INDEX.md", "stale, run --write-index")]


def test_e001_missing_index(tmp_path):
    root = make_repo(tmp_path)
    (root / "INDEX.md").unlink()
    fs = run_e(root)
    assert only(fs, "E001") == [("error", "INDEX.md", "missing, run --write-index")]


def test_e001_write_then_reverify(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "GOVERNANCE.md", "summary: Minirepo governance", "summary: Edited governance")
    assert write_indexes(ctx_for(root)) == []
    assert run_e(root) == []


def test_index_golden_byte_round_trip(tmp_path):
    root = make_repo(tmp_path)
    model = RepoModel.load(root, today=TODAY)
    want_idx = build_index(model)
    want_widx = build_wargame_index(model)
    assert model.read("INDEX.md") == want_idx
    assert model.read("packs/GUIDE_INDEX.md") == want_widx
    write_indexes(ctx_for(root))
    assert (root / "INDEX.md").read_bytes() == want_idx.encode("utf-8")
    assert (root / "packs" / "GUIDE_INDEX.md").read_bytes() == want_widx.encode("utf-8")


# --- E002 ---------------------------------------------------------------


def test_e002_no_front_matter(tmp_path):
    root = make_repo(tmp_path)
    (root / "NAKED.md").write_text("# Naked\n\nNo header.\n", encoding="utf-8")
    fs = run_e(root)
    assert ("error", "NAKED.md", "no front-matter block") in only(fs, "E002")


def test_e002_missing_key(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "tags: [eos]\n", "")
    fs = run_e(root)
    assert only(fs, "E002") == [("error", "org/STATE.md", "missing front-matter key: tags")]


def test_e002_unknown_type(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "type: org", "type: mystery")
    fs = run_e(root)
    assert ("error", "org/STATE.md", "unknown type: mystery") in only(fs, "E002")


def test_e002_type_requires_status_and_review(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/guides/WG-TST-001-sample.md", "status: active\n", "")
    edit(root, "packs/testmod/guides/WG-TST-001-sample.md", "review_by: 2030-01\n", "")
    fs = run_e(root)
    got = only(fs, "E002")
    assert ("error", "packs/testmod/guides/WG-TST-001-sample.md", "type requires status") in got
    assert ("error", "packs/testmod/guides/WG-TST-001-sample.md", "type requires review_by") in got


def test_e002_unterminated_block_reported(tmp_path):
    root = make_repo(tmp_path)
    (root / "BROKEN.md").write_text("---\nsummary: never closed\n", encoding="utf-8")
    fs = run_e(root)
    got = only(fs, "E002")
    assert ("error", "BROKEN.md", "no front-matter block") in got
    assert ("error", "BROKEN.md", "front-matter line 1: unterminated front-matter block") in got


# --- E003 ---------------------------------------------------------------


def test_e003_router_divergence(tmp_path):
    root = make_repo(tmp_path)
    (root / "CLAUDE.md").write_text(
        (root / "CLAUDE.md").read_text(encoding="utf-8") + "extra\n", encoding="utf-8")
    fs = run_e(root)
    assert only(fs, "E003") == [("error", "AGENTS.md", "CLAUDE.md is not a byte-identical copy")]


def test_e003_router_missing(tmp_path):
    root = make_repo(tmp_path)
    (root / "CLAUDE.md").unlink()
    fs = run_e(root)
    assert only(fs, "E003") == [("error", "AGENTS.md", "router file missing")]


# --- E004 ---------------------------------------------------------------


def test_e004_em_dash(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "The fixture repo — at rest.")
    fs = run_e(root)
    assert only(fs, "E004") == [("error", "org/STATE.md", "em-dash found")]


def test_e004_exclamation(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "The fixture repo is at rest.", "The fixture repo rests!")
    fs = run_e(root)
    assert only(fs, "E004") == [("warn", "org/STATE.md", "exclamation mark in prose")]


def test_e004_cliche(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "We delve into the fixture repo.")
    fs = run_e(root)
    assert only(fs, "E004") == [("warn", "org/STATE.md", "possible cliche: delve")]


# --- E005 ---------------------------------------------------------------


def test_e005_wargame_without_id(tmp_path):
    root = make_repo(tmp_path)
    (root / "packs" / "testmod" / "guides" / "nameless.md").write_text(
        "---\nsummary: A nameless wargame\ntype: wargame\ntags: [eos, wargame]\n"
        "status: active\nreview_by: 2030-01\n---\n\nBody.\n", encoding="utf-8")
    fs = run_e(root)
    assert only(fs, "E005") == [(
        "error", "packs/testmod/guides/nameless.md",
        "wargame filename lacks a WG-<MOD>-NNN id")]


def test_e005_duplicate_id(tmp_path):
    root = make_repo(tmp_path)
    src = root / "packs" / "testmod" / "guides" / "WG-TST-001-sample.md"
    shutil.copy(src, src.with_name("WG-TST-001-copy.md"))
    fs = run_e(root)
    assert ("error", "packs/testmod/guides/WG-TST-001-sample.md",
            "duplicate wargame id WG-TST-001") in only(fs, "E005")


def test_e005_undefined_reference(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/PACK.md",
         "The single ruling surface is WG-TST-001.",
         "The single ruling surface is WG-TST-001. See also WG-TST-999.")
    fs = run_e(root)
    assert only(fs, "E005") == [("warn", "packs/testmod/PACK.md",
                                 "reference to undefined wargame WG-TST-999")]


def test_e005_zero_suffix_reference_allowed(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/PACK.md",
         "The single ruling surface is WG-TST-001.",
         "The single ruling surface is WG-TST-001, described in WG-TST-000.")
    fs = run_e(root)
    assert only(fs, "E005") == []


# --- E006 ---------------------------------------------------------------


def test_e006_past_review(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/README.md", "review_by: 2030-01", "review_by: 2020-01")
    fs = run_e(root)
    assert only(fs, "E006") == [("warn", "packs/testmod/README.md",
                                 "past review_by 2020-01, verify before relying")]


def test_e006_malformed_review(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/README.md", "review_by: 2030-01", "review_by: soonish")
    fs = run_e(root)
    assert only(fs, "E006") == [("error", "packs/testmod/README.md",
                                 "review_by not YYYY-MM: soonish")]


def test_e006_current_month_not_flagged(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/README.md", "review_by: 2030-01", "review_by: 2026-08")
    fs = run_e(root)
    assert only(fs, "E006") == []


# --- E007 ---------------------------------------------------------------


def test_e007_router_cap(tmp_path):
    root = make_repo(tmp_path)
    filler = "".join(f"Line {i} of filler prose.\n" for i in range(40))
    for name in ("AGENTS.md", "CLAUDE.md"):
        p = root / name
        p.write_text(p.read_text(encoding="utf-8") + filler, encoding="utf-8")
    fs = run_e(root)
    n = len((root / "AGENTS.md").read_text(encoding="utf-8").splitlines())
    assert ("error", "AGENTS.md", f"router is {n} lines, cap 40") in only(fs, "E007")
    assert ("error", "CLAUDE.md", f"router is {n} lines, cap 40") in only(fs, "E007")


def test_e007_budget_and_waiver(tmp_path):
    root = make_repo(tmp_path)
    p = root / "packs" / "testmod" / "PACK.md"
    filler = "".join(f"Filler line {i}.\n" for i in range(150))
    p.write_text(p.read_text(encoding="utf-8") + filler, encoding="utf-8")
    n = len(p.read_text(encoding="utf-8").splitlines())
    fs = run_e(root)
    assert only(fs, "E007") == [("error", "packs/testmod/PACK.md",
                                 f"{n} lines over the 150 budget, no length_waiver")]
    edit(root, "packs/testmod/PACK.md", "review_by: 2030-01",
         "review_by: 2030-01\nlength_waiver: agreed for the test")
    fs = run_e(root)
    n2 = n + 1
    assert only(fs, "E007") == [("warn", "packs/testmod/PACK.md",
                                 f"{n2} lines under waiver: agreed for the test")]


# --- E008 ---------------------------------------------------------------


def test_e008_unfilled_slot(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "The fixture repo is at rest. {{UNFILLED}}")
    fs = run_e(root)
    assert only(fs, "E008") == [("error", "org/STATE.md",
                                 "unfilled {{SLOT}} outside a template")]


def test_e008_template_files_exempt(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "type: org", "type: org\ntemplate: true")
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "The fixture repo is at rest. {{UNFILLED}}")
    fs = run_e(root)
    assert only(fs, "E008") == []


# --- E009 ---------------------------------------------------------------


def test_e009_unknown_tag(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "tags: [eos]", "tags: [eos, nonsense]")
    fs = run_e(root)
    assert only(fs, "E009") == [("error", "org/STATE.md",
                                 "tag not in GOVERNANCE vocabulary: nonsense")]


def test_e009_skipped_when_vocabulary_missing(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "GOVERNANCE.md", "## Tag vocabulary", "## Tags renamed")
    edit(root, "org/STATE.md", "tags: [eos]", "tags: [eos, nonsense]")
    fs = run_e(root)
    assert only(fs, "E009") == []


# --- E010 ---------------------------------------------------------------


def test_e010_stale_session(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "active_session: none",
         "active_session: S-0001 started 2020-01-01")
    fs = run_e(root)
    assert only(fs, "E010") == [("warn", "org/STATE.md",
                                 "active_session set since 2020-01-01, likely stale")]


def test_e010_session_without_date(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "active_session: none", "active_session: S-0001")
    fs = run_e(root)
    assert only(fs, "E010") == [("warn", "org/STATE.md",
                                 "active_session set with no date")]


def test_e010_yesterday_not_stale(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "active_session: none",
         "active_session: S-0001 started 2026-08-02")
    fs = run_e(root)
    assert only(fs, "E010") == []
