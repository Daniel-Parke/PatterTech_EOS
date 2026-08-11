"""Structural E-series tests: one defect per check, exact findings.

Each check gets a case that makes it fire and a case that proves it
stays quiet on the shape it is not there to catch, because a check
that fires on everything is as useless as one that fires on nothing.
"""

import hashlib
import json
import shutil
import subprocess
import sys
from datetime import date

from conftest import REPO_ROOT, make_repo
from tools.eos.checks import run_all
from tools.eos.checks.structural import (
    build_guide_index,
    build_index,
    build_pack_index,
    write_indexes,
)
from tools.eos.repo import RepoModel

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


def test_the_v1_checker_path_still_resolves_and_forwards():
    """ADR-0001 is accepted and append-only and names tools/eos_check.py
    as the sanctioned executable, so check S003 holds that path. The
    file is a shim: it says it is deprecated and forwards to the
    package. Delete it and the ADR starts pointing at nothing.
    """
    proc = subprocess.run(
        [sys.executable, str(REPO_ROOT / "tools" / "eos_check.py"), "--repo"],
        capture_output=True, text=True, encoding="utf-8", cwd=str(REPO_ROOT),
    )
    assert "deprecated" in proc.stderr
    assert "errors," in proc.stderr


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
    want = {
        "INDEX.md": build_index(model),
        "packs/INDEX.md": build_pack_index(model),
        "packs/GUIDE_INDEX.md": build_guide_index(model),
    }
    for rel, text in want.items():
        assert model.read(rel) == text
    write_indexes(ctx_for(root))
    for rel, text in want.items():
        assert (root / rel).read_bytes() == text.encode("utf-8")


def test_e001_catches_a_stale_pack_index(tmp_path):
    """The defect that shipped: packs/INDEX.md drifted twelve packs
    short of reality and nothing compared it."""
    root = make_repo(tmp_path)
    p = root / "packs" / "INDEX.md"
    p.write_text(
        p.read_text(encoding="utf-8").replace("1 built packs", "9 built packs"),
        encoding="utf-8", newline="\n")
    fs = run_e(root)
    assert only(fs, "E001") == [("error", "packs/INDEX.md", "stale, run --write-index")]


def test_e001_catches_an_unindexed_pack(tmp_path):
    """A new pack on disk with no row in the always-loaded surface is
    unreachable. E001 must say so."""
    root = make_repo(tmp_path)
    new = root / "packs" / "second" / "PACK.md"
    new.parent.mkdir(parents=True)
    new.write_text(
        "---\nsummary: A second pack for the fixture\ntype: doctrine\n"
        "tags: [eos]\nreview_by: 2030-01\napplies_when: [does_a_thing]\n"
        "authority: default\n---\n\n# Second\n\nThis pack covers a second"
        " thing, and it activates when that thing happens.\n",
        encoding="utf-8", newline="\n")
    assert ("error", "packs/INDEX.md", "stale, run --write-index") in only(run_e(root), "E001")


def test_guide_index_covers_gd_guides_not_only_wargames(tmp_path):
    """79 of 86 guides were invisible because the generator selected on
    type: wargame and the guides carry type: guide."""
    root = make_repo(tmp_path)
    guide = root / "packs" / "testmod" / "guides" / "GD-TST-001-a-fork.md"
    guide.write_text(
        "---\nsummary: Which of two ways should the fixture go?\n"
        "type: guide\ntags: [eos]\nauthority: default\nreview: 2030-01\n"
        "review_by: 2030-01\n---\n\n# GD-TST-001\n\nBody.\n",
        encoding="utf-8", newline="\n")
    model = RepoModel.load(root, today=TODAY)
    assert "GD-TST-001" in build_guide_index(model)


def test_indexes_exclude_frozen_trees(tmp_path):
    """A benchmark fixture's wargames are not EOS guidance."""
    root = make_repo(tmp_path)
    fixture = root / "benchmark" / "fixtures" / "mini" / "guides" / "WG-FIX-001-x.md"
    fixture.parent.mkdir(parents=True)
    fixture.write_text(
        "---\nsummary: A fixture wargame that must never reach an agent\n"
        "type: wargame\ntags: [eos]\nstatus: active\nreview_by: 2030-01\n---\n\n# WG-FIX-001\n",
        encoding="utf-8", newline="\n")
    model = RepoModel.load(root, today=TODAY)
    assert "WG-FIX-001" not in build_guide_index(model)
    assert "benchmark/fixtures" not in build_index(model)


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
    edit(root, "packs/testmod/guides/WG-TST-001-sample.md", "review: 2030-01\n", "")
    fs = run_e(root)
    got = only(fs, "E002")
    assert ("error", "packs/testmod/guides/WG-TST-001-sample.md", "type requires status") in got
    assert ("error", "packs/testmod/guides/WG-TST-001-sample.md", "type requires review") in got


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


def test_e004_judges_prose_and_not_code(tmp_path):
    """The voice rules are about what a reader reads. A command, a
    regex or a sample string is quoted material: flagging it would make
    the check unusable in any file that shows a command line."""
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "Run `python -m tools.eos check --repo` first.\n\n"
         "```\nprint('unlock the seamless thing!')\nlabel = 'a b'\n```\n")
    assert only(run_e(root), "E004") == []


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
    edit(root, "packs/testmod/README.md", "review: 2030-01", "review: 2020-01")
    fs = run_e(root)
    assert only(fs, "E006") == [("warn", "packs/testmod/README.md",
                                 "past review 2020-01, verify before relying")]


def test_e006_malformed_review(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/README.md", "review: 2030-01", "review: soonish")
    fs = run_e(root)
    assert only(fs, "E006") == [("error", "packs/testmod/README.md",
                                 "review not YYYY-MM: soonish")]


def test_e006_current_month_not_flagged(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/README.md", "review: 2030-01", "review: 2026-08")
    fs = run_e(root)
    assert only(fs, "E006") == []


# --- E007 ---------------------------------------------------------------


def test_e007_router_cap_is_still_an_error(tmp_path):
    """The one budget ADR-0008 left binding, decision 5.

    Every other budget warns now. This one errors, because the router
    is in every agent's context and its cost is paid on every task.
    """
    root = make_repo(tmp_path)
    filler = "".join(f"Line {i} of filler prose.\n" for i in range(40))
    for name in ("AGENTS.md", "CLAUDE.md"):
        p = root / name
        p.write_text(p.read_text(encoding="utf-8") + filler, encoding="utf-8")
    fs = run_e(root)
    n = len((root / "AGENTS.md").read_text(encoding="utf-8").splitlines())
    assert ("error", "AGENTS.md", f"router is {n} lines, cap 40") in only(fs, "E007")
    assert ("error", "CLAUDE.md", f"router is {n} lines, cap 40") in only(fs, "E007")


def test_e007_budget_warns_and_the_waiver_records_why(tmp_path):
    """A budgeted type over the budget warns, waived or not (ADR-0008).

    The waiver stopped being the downgrade from error to warning when
    the budget stopped erroring. It is the recorded reason instead, and
    the two messages stay different so a review pass can tell an argued
    length from one nobody has looked at.
    """
    root = make_repo(tmp_path)
    p = root / "packs" / "testmod" / "PACK.md"
    filler = "".join(f"Filler line {i}.\n" for i in range(150))
    p.write_text(p.read_text(encoding="utf-8") + filler, encoding="utf-8")
    n = len(p.read_text(encoding="utf-8").splitlines())
    fs = run_e(root)
    assert only(fs, "E007") == [("warn", "packs/testmod/PACK.md",
                                 f"{n} lines over the 150 budget, "
                                 f"prune it or record a length_waiver")]
    edit(root, "packs/testmod/PACK.md", "review: 2030-01",
         "review_by: 2030-01\nlength_waiver: agreed for the test")
    fs = run_e(root)
    n2 = n + 1
    assert only(fs, "E007") == [("warn", "packs/testmod/PACK.md",
                                 f"{n2} lines under waiver: agreed for the test")]


def test_e007_silent_inside_the_budget_and_off_it(tmp_path):
    """No finding for a budgeted file at the budget, none for a long
    file whose type carries no budget at all."""
    root = make_repo(tmp_path)
    p = root / "packs" / "testmod" / "PACK.md"
    text = p.read_text(encoding="utf-8")
    pad = 150 - len(text.splitlines())
    assert pad > 0
    p.write_text(text + "".join(f"Filler line {i}.\n" for i in range(pad)),
                 encoding="utf-8")
    assert len(p.read_text(encoding="utf-8").splitlines()) == 150
    # org/STATE.md is type: org, which has no budget, so length says
    # nothing about it however far it runs.
    s = root / "org" / "STATE.md"
    s.write_text(s.read_text(encoding="utf-8")
                 + "".join(f"State filler line {i}.\n" for i in range(200)),
                 encoding="utf-8")
    assert only(run_e(root), "E007") == []


# --- E008 ---------------------------------------------------------------


def test_e008_unfilled_slot(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "The fixture repo is at rest. {{UNFILLED}}")
    fs = run_e(root)
    assert only(fs, "E008") == [("error", "org/STATE.md",
                                 "unfilled {{SLOT}} outside a template")]


def test_e008_slot_with_digits(tmp_path):
    """The kernel ships {{SUCCESS_90}}. A pattern of [A-Z_]+ let it
    through a green seed check unfilled; Venture C's cold-start probe
    found it, and the harvest of 2026-08-08 brought it back."""
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "The fixture repo is at rest. {{SUCCESS_90}}")
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


def test_e009_unknown_tag_warns(tmp_path):
    """ADR-0008 decision 6: the GOVERNANCE list is the known set, not
    the permitted set, so a tag outside it is flagged and not refused."""
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "tags: [eos]", "tags: [eos, nonsense]")
    fs = run_e(root)
    assert only(fs, "E009") == [("warn", "org/STATE.md",
                                 "tag not in GOVERNANCE vocabulary: nonsense")]


def test_e009_known_tag_is_silent(tmp_path):
    """A tag the list already carries is not flagged. Without this, a
    check that warned on everything would pass the test above."""
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "tags: [eos]", "tags: [eos, web]")
    fs = run_e(root)
    assert only(fs, "E009") == []


def test_e009_skipped_when_vocabulary_missing(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "GOVERNANCE.md", "## Tag vocabulary", "## Tags renamed")
    edit(root, "org/STATE.md", "tags: [eos]", "tags: [eos, nonsense]")
    fs = run_e(root)
    assert only(fs, "E009") == []


# --- E010, withdrawn ----------------------------------------------------


def test_the_state_view_cannot_emit_the_line_e010_watched():
    """E010 warned that `active_session` in org/STATE.md was stale.

    The generator has no such line to emit, which is why the check was
    withdrawn rather than kept as reassurance. If a state view ever
    grows one again, the withdrawal needs revisiting and this fails.
    """
    from tools.eos import taskops
    from tools.eos.checks import REGISTRY

    assert "E010" not in REGISTRY
    assert "active_session" not in taskops._state_view(
        [], None, None, None)


# --- E011 derived view drift --------------------------------------------


def make_view_repo(tmp_path):
    """The fixture repo plus the v2 record model, views freshly written."""
    from tools.eos import taskops

    root = make_repo(tmp_path)
    tasks = root / "org" / "tasks"
    tasks.mkdir(parents=True, exist_ok=True)
    (tasks / "T-0001.json").write_text(json.dumps({
        "id": "T-0001", "mode": "standard", "tier_ruled": "R0",
        "status": "blocked", "owner_session": "s1",
        "intent": "hold the fixture"}), encoding="utf-8", newline="\n")
    (root / "org" / "claims.json").write_text(json.dumps({
        "version": 1, "assigned": "2026-08-03",
        "lanes": [{"lane_id": "L1", "task_id": "T-0001", "session_id": "s1",
                   "expires": "2026-08-04T00:00:00Z",
                   "path_claims": ["packs/testmod/"]}]}),
        encoding="utf-8", newline="\n")
    taskops.render_views(root)
    return root


def test_e011_is_silent_when_the_views_match_their_generator(tmp_path):
    root = make_view_repo(tmp_path)
    assert only(run_e(root), "E011") == []


def test_e011_catches_a_hand_edited_view(tmp_path):
    """The two views were declared derived, given a generator and then
    compared by nothing, which is the hole packs/INDEX.md sat in."""
    root = make_view_repo(tmp_path)
    edit(root, "org/TASKS.md", "| T-0001 | standard | R0 | blocked | s1 |",
         "| T-0001 | standard | R3 | done | s1 |")
    assert only(run_e(root), "E011") == [
        ("error", "org/TASKS.md", "stale against its generator, run task views")]


def test_e011_catches_a_hand_edited_state_view(tmp_path):
    root = make_view_repo(tmp_path)
    edit(root, "org/STATE.md", "- T-0001 blocked: hold the fixture",
         "- T-0001 blocked: hold the fixture\n- T-0999 blocked: by hand")
    assert only(run_e(root), "E011") == [
        ("error", "org/STATE.md", "stale against its generator, run task views")]


def test_e011_leaves_the_machine_facts_block_to_s007(tmp_path):
    """A generated view records the commit it came from, and that commit
    is behind HEAD the moment the view is committed. S007 tests it by
    ancestry for that reason; equality here would overturn S007."""
    root = make_view_repo(tmp_path)
    edit(root, "org/STATE.md", "Git facts unavailable in this working copy.",
         "```facts\ncommit: 0123456789abcdef\n```")
    assert only(run_e(root), "E011") == []


def test_e011_still_reads_past_the_machine_facts_block(tmp_path):
    """Only the facts values are blanked. Cutting the file at the
    heading would have made the end of it a place edits could hide."""
    root = make_view_repo(tmp_path)
    state = root / "org" / "STATE.md"
    state.write_text(
        state.read_text(encoding="utf-8").replace(
            "Git facts unavailable in this working copy.",
            "```facts\ncommit: 0123456789abcdef\n```\n\n"
            "And a paragraph somebody added by hand."),
        encoding="utf-8", newline="\n")
    assert only(run_e(root), "E011") == [
        ("error", "org/STATE.md", "stale against its generator, run task views")]


def test_e011_reports_a_missing_view(tmp_path):
    root = make_view_repo(tmp_path)
    (root / "org" / "TASKS.md").unlink()
    assert only(run_e(root), "E011") == [
        ("error", "org/TASKS.md", "missing, run task views")]


def test_e011_says_nothing_without_the_record_model(tmp_path):
    """A repository with no org/tasks/ has no canonical records, so
    there is nothing for a view to be derived from."""
    root = make_repo(tmp_path)
    assert only(run_e(root), "E011") == []


def test_e011_reports_an_unreadable_record_rather_than_drift(tmp_path):
    root = make_view_repo(tmp_path)
    (root / "org" / "tasks" / "T-0002.json").write_text(
        "{not json", encoding="utf-8", newline="\n")
    findings = only(run_e(root), "E011")
    assert len(findings) == 1
    assert findings[0][1] == "org/tasks/T-0002.json"
    assert "cannot compare the derived views" in findings[0][2]


# --- the lessons view ---------------------------------------------------


LEDGER = {
    "version": 1,
    "note": "A test ledger",
    "preamble": ["The ledger's own history, emitted verbatim."],
    "rows": [
        {"id": "LES-0002", "origin": "harvest", "venture": "Venture C",
         "title": "A cold-start probe finds what a warm session cannot",
         "lesson": "A cold-start probe run before the rubric is signed "
                   "surfaces defects a warm session cannot see",
         "disposition": "estate-default", "scope": "estate",
         "decided": "2026-08-08", "reasoning": "It ran and it worked"},
        {"id": "LES-0001", "origin": "study", "sources": ["EV-0007"],
         "lens": "LENS-0001", "title": "Independence beats ordering",
         "lesson": "A test written from the implementation finds less",
         "disposition": "rejected", "scope": "estate",
         "reasoning": "Too narrow to bind"},
        {"id": "LES-0003", "origin": "harvest", "venture": "Venture A",
         "title": "A template that states history needs a slot",
         "lesson": "Boilerplate stating venture history must be a slot",
         "disposition": "deferred", "scope": "estate",
         "revisit_trigger": "The next reseed"},
        {"id": "LES-0004", "origin": "harvest", "venture": "Venture C",
         "title": "Ceremony budgets split by trigger",
         "lesson": "Doctrine-triggered rulings are counted separately",
         "disposition": "estate-default", "scope": "estate"},
        {"id": "LES-0005", "origin": "harvest", "venture": "Venture B",
         "title": "Cap urllib3 below 2.5", "lesson": "It breaks startup",
         "disposition": "dated-registry-fact", "scope": "estate",
         "pruned_on": "2026-08-03"},
    ],
}


def write_ledger(root, doc=None):
    (root / "registry").mkdir(exist_ok=True)
    (root / "registry" / "lessons.json").write_text(
        json.dumps(doc if doc is not None else LEDGER, indent=1) + "\n",
        encoding="utf-8", newline="\n")


def test_lessons_view_renders_every_row_and_sorts_by_id(tmp_path):
    from tools.eos.checks.structural import build_lessons

    root = make_repo(tmp_path)
    write_ledger(root)
    text = build_lessons(RepoModel.load(root, today=TODAY))
    assert "derived: true" in text
    # Rows sort by id inside their section, so regeneration is
    # byte-stable whatever order the ledger happens to hold them in.
    live = text.split("## Live", 1)[1].split("## Rejected", 1)[0]
    assert live.index("### LES-0002") < live.index("### LES-0004")
    assert "- **Lens**: LENS-0001" in text
    assert "- **Evidence**: EV-0007" in text
    assert "**Live: 2. Rejected: 1. Deferred: 1. Pruned: 1.**" in text
    # The ledger's own history is part of the record and lives in the
    # canonical file, or the view would be its only home.
    assert "The ledger's own history, emitted verbatim." in text
    # The rejected row keeps its reason: a decline that leaves no trace
    # can be re-proposed for ever.
    rejected = text.split("## Rejected", 1)[1].split("## Deferred", 1)[0]
    assert "Too narrow to bind" in rejected
    # A pruned row is provenance, listed apart from the live rules.
    pruned = text.split("## Pruned", 1)[1]
    assert "### LES-0005" in pruned
    assert "- **Pruned**: 2026-08-03" in pruned


def test_lessons_view_renders_a_field_it_did_not_expect(tmp_path):
    """A view that silently drops an unknown key is how a derived file
    starts lying about its source."""
    from tools.eos.checks.structural import build_lessons

    root = make_repo(tmp_path)
    write_ledger(root, {"version": 1, "rows": [
        {"id": "LES-0003", "lesson": "x", "invented_axis": "kept anyway"}]})
    text = build_lessons(RepoModel.load(root, today=TODAY))
    assert "- **invented_axis**: kept anyway" in text


def test_lessons_view_renders_a_conflict_and_how_it_was_settled(tmp_path):
    from tools.eos.checks.structural import build_lessons

    root = make_repo(tmp_path)
    write_ledger(root, {"version": 1, "rows": [
        {"id": "LES-0006", "title": "Platform-native beats containers",
         "lesson": "On a sovereign LAN", "disposition": "venture-ruling",
         "conflicts_with": ["WG-OPS-002"],
         "conflict_resolutions": {"WG-OPS-002": {
             "resolution": "scoped-differently",
             "note": "The container default holds where parity is in play"}}}]})
    text = build_lessons(RepoModel.load(root, today=TODAY))
    assert "- **Conflicts with**: WG-OPS-002" in text
    assert ("- **Conflict resolutions**: WG-OPS-002: resolution: "
            "scoped-differently; note: The container default holds where "
            "parity is in play") in text


def test_e001_compares_the_lessons_view_once_the_ledger_exists(tmp_path):
    root = make_repo(tmp_path)
    write_ledger(root)
    assert ("error", "registry/LESSONS.md", "missing, run --write-index") \
        in only(run_e(root), "E001")
    assert write_indexes(ctx_for(root)) == []
    assert only(run_e(root), "E001") == []
    (root / "registry" / "LESSONS.md").write_text(
        "hand-edited\n", encoding="utf-8", newline="\n")
    assert ("error", "registry/LESSONS.md", "stale, run --write-index") \
        in only(run_e(root), "E001")


def test_no_lessons_view_is_demanded_without_a_ledger(tmp_path):
    """registry/lessons.json is canonical from v2.1; with no ledger
    there is nothing to derive a view from."""
    root = make_repo(tmp_path)
    assert [f for f in only(run_e(root), "E001") if "LESSONS" in f[1]] == []


# --- retired ids --------------------------------------------------------


def test_retired_ids_resolve_but_do_not_duplicate(tmp_path):
    """ADR-0003 moved the archive of record to a pushed tag. An id whose
    defining file went with it is still defined and still locatable, so
    a provenance reference to it is not dangling. Retiring archive/v1
    without this turned 33 real ids into 79 findings overnight."""
    root = make_repo(tmp_path)
    (root / "archive").mkdir(exist_ok=True)
    (root / "archive" / "RETIRED_IDS.json").write_text(
        '{"version": 1, "tag": "archive/v1-final",'
        ' "ids": {"WG-GONE-001": "doctrine/gone/WG-GONE-001-x.md"}}\n',
        encoding="utf-8", newline="\n")
    write = root / "org" / "STATE.md"
    write.write_text(
        write.read_text(encoding="utf-8").replace(
            "The fixture repo is at rest.",
            "The fixture repo is at rest. See WG-GONE-001 for the v1 argument."),
        encoding="utf-8", newline="\n")
    fs = run_e(root)
    assert [f for f in fs if f.check_id == "E005"] == []


def test_a_genuinely_undefined_id_still_reports(tmp_path):
    """The exemption is for ids that moved, not for ids that never were."""
    root = make_repo(tmp_path)
    write = root / "org" / "STATE.md"
    write.write_text(
        write.read_text(encoding="utf-8").replace(
            "The fixture repo is at rest.",
            "The fixture repo is at rest. See WG-NEVER-001."),
        encoding="utf-8", newline="\n")
    fs = run_e(root)
    assert ("warn", "org/STATE.md",
            "reference to undefined wargame WG-NEVER-001") in only(fs, "E005")


# --- B001 benchmark freeze ----------------------------------------------


def test_b001_detects_a_changed_frozen_file(tmp_path):
    """The manifest said changes need an ADR amendment and nothing
    verified it, so it failed its own check on fifteen entries."""
    from tools.eos.checks import freeze

    root = make_repo(tmp_path)
    (root / "benchmark").mkdir(exist_ok=True)
    target = root / "benchmark" / "frozen.py"
    target.write_text("original\n", encoding="utf-8", newline="\n")
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    (root / "benchmark" / "FREEZE_MANIFEST.json").write_text(
        json.dumps({"version": 1, "files": {"benchmark/frozen.py": digest}}),
        encoding="utf-8", newline="\n")
    model = RepoModel.load(root, today=TODAY)
    assert freeze.verify(model) == []

    target.write_text("tampered\n", encoding="utf-8", newline="\n")
    model = RepoModel.load(root, today=TODAY)
    findings = freeze.verify(model)
    assert len(findings) == 1
    assert "does not match its recorded hash" in findings[0].message
    assert "unrecorded change" in findings[0].message


def test_b001_detects_two_spellings_of_one_path(tmp_path):
    """Thirty-four entries used Windows separators and duplicated a
    forward-slash entry, fourteen with a different hash. A manifest
    holding two hashes for one file verifies nothing."""
    from tools.eos.checks import freeze

    root = make_repo(tmp_path)
    (root / "benchmark").mkdir(exist_ok=True)
    target = root / "benchmark" / "frozen.py"
    target.write_text("original\n", encoding="utf-8", newline="\n")
    digest = hashlib.sha256(target.read_bytes()).hexdigest()
    windows_key = "benchmark" + chr(92) + "frozen.py"
    assert chr(92) in windows_key
    (root / "benchmark" / "FREEZE_MANIFEST.json").write_text(
        json.dumps({"version": 1, "files": {
            "benchmark/frozen.py": digest,
            windows_key: "0" * 64,
        }}), encoding="utf-8", newline="\n")
    model = RepoModel.load(root, today=TODAY)
    msgs = [f.message for f in freeze.verify(model)]
    assert any("duplicate entry" in m for m in msgs)


def test_b001_says_nothing_where_there_is_no_freeze(tmp_path):
    """A venture repository has no frozen suite, so there is no freeze
    to verify and no finding to make."""
    from tools.eos.checks import freeze

    model = RepoModel.load(make_repo(tmp_path), today=TODAY)
    assert freeze.verify(model) == []


def test_b001_reports_a_frozen_file_that_has_gone(tmp_path):
    """A deletion is the loudest change a freeze can suffer, and hashing
    only what is present would report it as nothing at all."""
    from tools.eos.checks import freeze

    root = make_repo(tmp_path)
    (root / "benchmark").mkdir(exist_ok=True)
    (root / "benchmark" / "FREEZE_MANIFEST.json").write_text(
        json.dumps({"version": 1, "files": {"benchmark/gone.py": "0" * 64}}),
        encoding="utf-8", newline="\n")
    model = RepoModel.load(root, today=TODAY)
    msgs = [f.message for f in freeze.verify(model)]
    assert msgs == ["frozen file is missing: benchmark/gone.py"]


def test_b001_names_an_amendment_rather_than_crying_tamper(tmp_path):
    """A recorded amendment is the sanctioned way to change frozen
    material. It still reports, because the manifest hash is now stale,
    but it tells the reader which of the two situations they are in."""
    from tools.eos.checks import freeze

    root = make_repo(tmp_path)
    (root / "benchmark").mkdir(exist_ok=True)
    target = root / "benchmark" / "frozen.py"
    target.write_text("original\n", encoding="utf-8", newline="\n")
    (root / "benchmark" / "FREEZE_MANIFEST.json").write_text(
        json.dumps({"version": 1,
                    "files": {"benchmark/frozen.py": "0" * 64},
                    "amendments": [{"adr": "ADR-0002",
                                    "files": ["benchmark/frozen.py"]}]}),
        encoding="utf-8", newline="\n")
    model = RepoModel.load(root, today=TODAY)
    findings = freeze.verify(model)
    assert len(findings) == 1
    assert "listed in an amendment" in findings[0].message
