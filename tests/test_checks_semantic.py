"""Semantic S-series tests: one defect per check, exact findings.

The series defaults to error severity; ctx["relax_semantic"] drops it
back to warnings for a caller that wants the work list rather than the
gate. Both behaviours are asserted, along with the exemptions that keep
verbatim history and out-of-tree material out of scope.
"""

import json
import shutil
from datetime import date

from conftest import REPO_ROOT, git, make_git_repo, make_repo
from tools.eos.checks import run_all
from tools.eos.repo import RepoModel

TODAY = date(2026, 8, 3)


def run_s(root, today=TODAY, strict=False, relax=False, offline=True):
    model = RepoModel.load(root, today=today)
    ctx = {"model": model, "root": model.root, "today": today,
           "offline": offline, "strict_semantic": strict,
           "relax_semantic": relax}
    return run_all(ctx, series="S")


def only(findings, check_id):
    return [(f.severity, f.path, f.message) for f in findings if f.check_id == check_id]


def edit(root, rel, old, new):
    p = root / rel
    text = p.read_text(encoding="utf-8")
    assert old in text, f"marker not found in {rel}: {old}"
    p.write_text(text.replace(old, new), encoding="utf-8")


def write(root, rel, text):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def test_minirepo_is_semantically_green(tmp_path):
    assert run_s(make_repo(tmp_path)) == []


# --- S001 ---------------------------------------------------------------


def test_s001_invalid_v1_status(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/guides/WG-TST-001-sample.md",
         "status: active", "status: bogus")
    fs = run_s(root)
    assert only(fs, "S001") == [("error", "packs/testmod/guides/WG-TST-001-sample.md",
                                 "invalid status: bogus")]


def test_s001_strict_flag_keeps_error_severity(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/guides/WG-TST-001-sample.md",
         "status: active", "status: bogus")
    fs = run_s(root, strict=True)
    assert only(fs, "S001") == [("error", "packs/testmod/guides/WG-TST-001-sample.md",
                                 "invalid status: bogus")]


def test_s001_relax_flag_drops_to_warning(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/guides/WG-TST-001-sample.md",
         "status: active", "status: bogus")
    fs = run_s(root, relax=True)
    assert only(fs, "S001") == [("warn", "packs/testmod/guides/WG-TST-001-sample.md",
                                 "invalid status: bogus")]


def test_s_series_defaults_to_error_with_no_flag_at_all(tmp_path):
    """No key in the context means the gate. A caller who says nothing
    gets the strict reading, not the soft one."""
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/guides/WG-TST-001-sample.md",
         "status: active", "status: bogus")
    model = RepoModel.load(root, today=TODAY)
    ctx = {"model": model, "root": model.root, "today": TODAY, "offline": True}
    assert only(run_all(ctx, series="S"), "S001") == [
        ("error", "packs/testmod/guides/WG-TST-001-sample.md",
         "invalid status: bogus")]


def test_strict_wins_over_relax_where_a_caller_passes_both(tmp_path):
    """Which is all --strict-semantic does now that error is the
    default. A command line assembled from parts can carry both, and it
    has to resolve to the gate rather than to the softer of the two."""
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/guides/WG-TST-001-sample.md",
         "status: active", "status: bogus")
    fs = run_s(root, strict=True, relax=True)
    assert [sev for sev, _p, _m in only(fs, "S001")] == ["error"]


def test_s001_invalid_v2_axis(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/RULE.md",
          "---\nsummary: A rule\ntype: org\ntags: [eos]\nkind: rule\n"
          "lifecycle: forever\nscope: galaxy\n---\n\nBody.\n")
    fs = run_s(root)
    assert ("error", "org/RULE.md", "invalid lifecycle: forever") in only(fs, "S001")
    assert ("error", "org/RULE.md", "invalid scope: galaxy") in only(fs, "S001")


def test_s001_brand_scope_legal(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/RULE.md",
          "---\nsummary: A rule\ntype: org\ntags: [eos]\nkind: guide\n"
          "scope: brand:pattertech\n---\n\nBody.\n")
    assert only(run_s(root), "S001") == []


def test_s001_fixture_files_exempt(tmp_path):
    root = make_repo(tmp_path)
    write(root, "benchmark/fixtures/old/OLD.md",
          "---\nsummary: Old fixture\ntype: org\ntags: [eos]\nstatus: retired\n---\nBody.\n")
    assert only(run_s(root), "S001") == []


# --- S002 ---------------------------------------------------------------


def test_s002_unresolvable_reference(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/NEW.md",
          "---\nsummary: The successor\ntype: org\ntags: [eos]\n"
          "supersedes: org/GONE.md\n---\nBody.\n")
    fs = run_s(root)
    assert only(fs, "S002") == [("error", "org/NEW.md",
                                 "supersedes reference does not resolve: org/GONE.md")]


def test_s002_missing_back_pointer(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/OLD.md",
          "---\nsummary: The predecessor\ntype: org\ntags: [eos]\n---\nBody.\n")
    write(root, "org/NEW.md",
          "---\nsummary: The successor\ntype: org\ntags: [eos]\n"
          "supersedes: org/OLD.md\n---\nBody.\n")
    fs = run_s(root)
    assert only(fs, "S002") == [("error", "org/NEW.md",
                                 "supersedes org/OLD.md does not point back via superseded_by")]


def test_s002_bidirectional_pair_is_clean(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/OLD.md",
          "---\nsummary: The predecessor\ntype: org\ntags: [eos]\n"
          "superseded_by: org/NEW.md\n---\nBody.\n")
    write(root, "org/NEW.md",
          "---\nsummary: The successor\ntype: org\ntags: [eos]\n"
          "supersedes: org/OLD.md\n---\nBody.\n")
    assert only(run_s(root), "S002") == []


# --- S003 ---------------------------------------------------------------


def test_s003_dangling_path_reference(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "See `org/MISSING.md` for details.")
    fs = run_s(root)
    assert only(fs, "S003") == [("error", "org/STATE.md",
                                 "path reference does not resolve: org/MISSING.md")]


def test_s003_path_outside_this_tree_is_not_a_reference(tmp_path):
    """A venture seed naming its own docs/ is not claiming ours."""
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "The venture writes `docs/COMPILE_REPORT.md` in its own repo.")
    assert only(run_s(root), "S003") == []


def test_s003_placeholder_path_is_a_pattern_not_a_reference(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "Updates land at `org/product/updates/SU-YYYY-WW.md`.")
    assert only(run_s(root), "S003") == []


def test_s003_resolvable_reference_clean(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "See `packs/testmod/PACK.md` for details.")
    assert only(run_s(root), "S003") == []


# --- S004 ---------------------------------------------------------------


def test_s004_undefined_adr_reference(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "Ruled by ADR-0009.")
    fs = run_s(root)
    assert only(fs, "S004") == [("error", "org/STATE.md",
                                 "reference to undefined id ADR-0009")]


def test_s004_venture_owned_id_is_not_ours(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "Venture A's ADR-0003 rules local-first, and its ADR-0011 the shape.")
    assert only(run_s(root), "S004") == []


def test_s004_same_id_unqualified_elsewhere_is_still_checked(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "Venture A's ADR-0003 rules local-first. We follow ADR-0003 too.")
    assert only(run_s(root), "S004") == [
        ("error", "org/STATE.md", "reference to undefined id ADR-0003")]


def test_s004_all_zero_id_is_the_placeholder_shape(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "Dates come from the S-0000 baseline, ids look like ADR-0000.")
    assert only(run_s(root), "S004") == []


def test_s004_fixture_wargame_still_defines_its_id(tmp_path):
    """Exemptions govern what is checked, never what exists."""
    root = make_repo(tmp_path)
    write(root, "benchmark/fixtures/mini/wargames/WG-BEN-001-sample.md",
          "---\nsummary: A fixture wargame\ntype: wargame\ntags: [eos]\n"
          "status: active\nreview_by: 2030-01\n---\nBody.\n")
    edit(root, "INDEX.md", "# INDEX", "# INDEX\n\nRow for WG-BEN-001.")
    assert only(run_s(root), "S004") == []


def test_s004_defined_adr_reference_clean(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/decisions/ADR-0009-sample.md",
          "---\nsummary: A ruling\ntype: decision\ntags: [eos]\nstatus: accepted\n---\nBody.\n")
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "Ruled by ADR-0009.")
    assert only(run_s(root), "S004") == []


# --- S005 ---------------------------------------------------------------


def test_s005_derived_without_generator(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/VIEW.md",
          "---\nsummary: A hand-derived view\ntype: org\ntags: [eos]\n"
          "derived: true\n---\nBody.\n")
    fs = run_s(root)
    assert only(fs, "S005") == [("error", "org/VIEW.md",
                                 "derived file has no registered generator")]


def test_s005_registered_indexes_clean(tmp_path):
    assert only(run_s(make_repo(tmp_path)), "S005") == []


# --- S006 ---------------------------------------------------------------


def test_s006_missing_doctrine_organ(tmp_path):
    root = make_repo(tmp_path)
    (root / "packs" / "testmod" / "CHECKS.md").unlink()
    fs = run_s(root)
    assert only(fs, "S006") == [("error", "packs/testmod", "pack missing CHECKS.md")]


def test_s006_missing_guides_dir(tmp_path):
    root = make_repo(tmp_path)
    shutil.rmtree(root / "packs" / "testmod" / "guides")
    fs = run_s(root)
    assert only(fs, "S006") == [("error", "packs/testmod", "pack missing guides/")]


def test_s006_a_complete_pack_is_silent(tmp_path):
    """The fixture pack has all three organs, so nothing is reported.
    Named here so the silence is attributable to S006 rather than to
    the whole-series green."""
    assert only(run_s(make_repo(tmp_path)), "S006") == []


def test_s006_research_fragments_are_not_yet_a_pack(tmp_path):
    """A directory holding only imported fragments is a pack that has
    not been authored, not a pack missing its organs."""
    root = make_repo(tmp_path)
    write(root, "packs/incoming/research/sources.md",
          "---\nsummary: Fragments waiting on an author\ntype: org\n"
          "tags: [eos]\n---\n\nNotes.\n")
    assert only(run_s(root), "S006") == []


# --- S007 ---------------------------------------------------------------


def _gitify(root):
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.email", "suite@example.invalid")
    git(root, "config", "user.name", "Test Suite")
    git(root, "config", "commit.gpgsign", "false")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "fixture")


def test_s007_reports_a_commit_that_does_not_resolve(tmp_path):
    root = make_repo(tmp_path)
    _gitify(root)
    edit(root, "org/STATE.md", "Nothing is in flight. The fixture repo is at rest.",
         "```facts\ncommit: 0000000\n```\n")
    assert only(run_s(root), "S007") == [
        ("error", "org/STATE.md",
         "machine fact commit: 0000000 does not resolve")]


def test_s007_ignores_a_recorded_branch(tmp_path):
    """There is no branch arm, and a stale branch name is not a finding.

    A branch name written into a committed file is correct until the
    branch merges and wrong the moment it does, with no input having
    changed, so checking it turned the merge commit's own run red. The
    generator stopped recording it and this stopped checking it.
    """
    root = make_repo(tmp_path)
    _gitify(root)
    edit(root, "org/STATE.md", "Nothing is in flight. The fixture repo is at rest.",
         "```facts\nbranch: some-feature-branch\n```\n")
    assert only(run_s(root), "S007") == []


def test_s007_commit_behind_head_is_clean(tmp_path):
    """A view records the commit it was built from, so it is always behind.

    Ancestry is also what carries the fact through a merge, which is why
    the commit is the one machine fact worth committing to a file.
    """
    root = make_repo(tmp_path)
    _gitify(root)
    head = git(root, "rev-parse", "HEAD").strip()
    (root / "later.txt").write_text("later\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "moves on")
    edit(root, "org/STATE.md", "Nothing is in flight. The fixture repo is at rest.",
         f"```facts\ncommit: {head[:12]}\n```\n")
    assert only(run_s(root), "S007") == []


def test_s007_commit_off_the_current_history_is_drift(tmp_path):
    """A recorded commit that HEAD cannot reach is the real drift."""
    root = make_repo(tmp_path)
    _gitify(root)
    git(root, "checkout", "-q", "-b", "sidetrack")
    (root / "aside.txt").write_text("aside\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "off to one side")
    aside = git(root, "rev-parse", "HEAD").strip()
    git(root, "checkout", "-q", "main")
    edit(root, "org/STATE.md", "Nothing is in flight. The fixture repo is at rest.",
         f"```facts\ncommit: {aside}\n```\n")
    got = only(run_s(root), "S007")
    assert len(got) == 1
    assert got[0][:2] == ("error", "org/STATE.md")
    assert got[0][2].startswith(f"machine fact commit: {aside} is not an ancestor")


def test_s007_reports_a_recorded_tag_git_does_not_have(tmp_path):
    root = make_repo(tmp_path)
    _gitify(root)
    git(root, "tag", "v0.1.0")
    edit(root, "org/STATE.md", "Nothing is in flight. The fixture repo is at rest.",
         "```facts\ntag: v9.9.9\n```\n")
    assert only(run_s(root), "S007") == [
        ("error", "org/STATE.md", "machine fact tag: v9.9.9 is not a git tag")]


def test_s007_no_git_degrades_silently(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "Nothing is in flight. The fixture repo is at rest.",
         "```facts\ncommit: 0000000\n```\n")
    assert only(run_s(root), "S007") == []


# --- S008, withdrawn ----------------------------------------------------


def test_nothing_opts_into_the_key_s008_watched(tmp_path):
    """S008 held one writer per fact, for facts that opted in through a
    canonical_facts key. Nothing ever opted in, so it never fired once
    and was withdrawn; the id is not reused. If a file starts declaring
    the key, the withdrawal needs revisiting and this fails."""
    from tools.eos.checks import REGISTRY

    assert "S008" not in REGISTRY
    root = make_repo(tmp_path)
    model = RepoModel.load(root, today=TODAY)
    assert not [r for r in model.files if "canonical_facts" in r.fm.data]


# --- S009 ---------------------------------------------------------------


def test_s009_month_only_next_due_is_late_once_the_month_has_passed(tmp_path):
    """A month-only next_due is a window, and a window closes. This case
    used to be read out of a Markdown table in org/CADENCE.md; that file
    was cut at release, so the only cadence surface is the JSON."""
    root = make_repo(tmp_path)
    write(root, "org/cadence.json",
          json.dumps([{"id": "hygiene", "next_due": "2026-07",
                       "procedure": "org/PLAYBOOKS.md#pb-e09-hygiene"}]))
    fs = run_s(root)
    assert ("error", "org/cadence.json",
            "cadence 'hygiene' overdue: next_due 2026-07, "
            "procedure org/PLAYBOOKS.md#pb-e09-hygiene") in only(fs, "S009")


def test_s009_machine_rows_overdue(tmp_path):
    """The row key is id, as org/cadence.json actually writes it. The
    check read 'name' and so reported every overdue cadence as '?',
    which told the operator a cadence was late but never which one."""
    root = make_repo(tmp_path)
    write(root, "org/cadence.json",
          json.dumps([{"id": "harvest", "next_due": "2026-07-15",
                       "procedure": "org/PLAYBOOKS.md#pb-e02-harvest"}]))
    fs = run_s(root)
    assert only(fs, "S009") == [
        ("error", "org/cadence.json",
         "cadence 'harvest' overdue: next_due 2026-07-15, "
         "procedure org/PLAYBOOKS.md#pb-e02-harvest")]


def test_s009_malformed_machine_rows(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/cadence.json", "not json")
    fs = run_s(root)
    assert only(fs, "S009") == [("error", "org/cadence.json", "malformed JSON")]


def test_s009_a_cadence_still_in_its_window_is_not_overdue(tmp_path):
    """A month-only next_due names a window, so a cadence due this
    month is on time all month. Read as the first of the month it
    reported every monthly row late from the second day onward, and a
    list that is always red is a list nobody reads."""
    root = make_repo(tmp_path)
    write(root, "org/cadence.json",
          json.dumps([{"id": "hygiene", "next_due": "2026-08",
                       "procedure": "org/PLAYBOOKS.md#pb-e09-hygiene"},
                      {"id": "harvest", "next_due": "2026-08-03",
                       "procedure": "org/PLAYBOOKS.md#pb-e02-harvest"}]))
    assert only(run_s(root), "S009") == []


def test_s009_ignores_a_next_due_it_cannot_read(tmp_path):
    """A malformed date is not a late cadence. Guessing at one would
    put an overdue row on the operator's desk with no date behind it."""
    root = make_repo(tmp_path)
    write(root, "org/cadence.json",
          json.dumps([{"id": "harvest", "next_due": "whenever"}]))
    assert only(run_s(root), "S009") == []


# --- S010 ---------------------------------------------------------------


ESTATE_YAML = (
    "version: 1\n"
    "updated: 2026-08-03\n"
    "root: C:/ventures\n"
    "repos:\n"
    "  alpha:\n"
    "    path: ventures/alpha\n"
    "    role: venture\n"
    "    status: active\n"
)


def test_s010_venture_missing_from_estate(tmp_path):
    root = make_repo(tmp_path)
    write(root, "estate/repos.yaml", ESTATE_YAML)
    write(root, "registry/PROJECTS.md",
          "---\nsummary: Ventures registry\ntype: registry\ntags: [eos]\n"
          "status: active\n---\n\n"
          "| Venture | Path | Status | Pin |\n"
          "| --- | --- | --- | --- |\n"
          "| ghost | `ventures/ghost` | active | none |\n")
    fs = run_s(root)
    assert only(fs, "S010") == [("error", "registry/PROJECTS.md",
                                 "venture ghost not in the estate manifest (estate/repos.yaml)")]


def test_s010_unresolvable_pin(tmp_path):
    root = make_repo(tmp_path)
    write(root, "estate/repos.yaml", ESTATE_YAML)
    write(root, "registry/PROJECTS.md",
          "---\nsummary: Ventures registry\ntype: registry\ntags: [eos]\n"
          "status: active\n---\n\n"
          "| Venture | Path | Status | Pin |\n"
          "| --- | --- | --- | --- |\n"
          "| alpha | `ventures/alpha` | active | v1 @ abc1234 |\n")
    fs = run_s(root)
    assert only(fs, "S010") == [("error", "registry/PROJECTS.md",
                                 "venture alpha pin abc1234 does not resolve")]


def test_s010_a_venture_in_the_manifest_with_no_pin_is_clean(tmp_path):
    """The registry and the manifest agree and nothing claims a commit,
    so there is nothing to resolve and nothing to report."""
    root = make_repo(tmp_path)
    write(root, "estate/repos.yaml", ESTATE_YAML)
    write(root, "registry/PROJECTS.md",
          "---\nsummary: Ventures registry\ntype: registry\ntags: [eos]\n"
          "status: active\n---\n\n"
          "| Venture | Path | Status | Pin |\n"
          "| --- | --- | --- | --- |\n"
          "| alpha | `ventures/alpha` | active | none |\n")
    assert only(run_s(root), "S010") == []


def test_s010_says_nothing_without_both_registries(tmp_path):
    """One half of a cross-check is not a cross-check. A repository with
    no estate manifest is not making a claim S010 can test."""
    root = make_repo(tmp_path)
    write(root, "registry/PROJECTS.md",
          "---\nsummary: Ventures registry\ntype: registry\ntags: [eos]\n"
          "status: active\n---\n\n"
          "| Venture | Path | Status | Pin |\n"
          "| --- | --- | --- | --- |\n"
          "| ghost | `ventures/ghost` | active | none |\n")
    assert only(run_s(root), "S010") == []


# --- S011 ---------------------------------------------------------------


def test_s011_heading_without_tag(tmp_path):
    root = make_git_repo(tmp_path)
    write(root, "CHANGELOG.md", "# Changelog\n\n## v9.9.9 · 2026-08-01\n\n- a change\n")
    fs = run_s(root)
    assert only(fs, "S011") == [("error", "CHANGELOG.md",
                                 "heading v9.9.9 has no matching git tag")]


def test_s011_tag_without_heading_and_empty_unreleased(tmp_path):
    root = make_git_repo(tmp_path)
    write(root, "CHANGELOG.md",
          "# Changelog\n\n## Unreleased\n\n## v0.1.0 · 2026-08-01\n\n- first cut\n")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "changelog")
    git(root, "tag", "v0.1.0")
    git(root, "tag", "v0.2.0")
    (root / "b.txt").write_text("two\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "post-release work")
    fs = run_s(root)
    got = only(fs, "S011")
    assert ("error", "CHANGELOG.md", "git tag v0.2.0 has no CHANGELOG heading") in got
    assert ("error", "CHANGELOG.md",
            "1 commits since v0.2.0 but the Unreleased section is empty") in got


def test_s011_a_tagged_changelog_with_work_written_up_is_clean(tmp_path):
    """Every heading has a tag, every tag has a heading, and the commits
    since the last tag are written up. Nothing to report."""
    root = make_git_repo(tmp_path)
    write(root, "CHANGELOG.md",
          "# Changelog\n\n## Unreleased\n\n- the work since v0.1.0\n\n"
          "## v0.1.0 · 2026-08-01\n\n- first cut\n")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "changelog")
    git(root, "tag", "v0.1.0")
    (root / "b.txt").write_text("two\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "the work")
    assert only(run_s(root), "S011") == []


def test_s011_reports_entries_written_up_against_no_commits(tmp_path):
    """The other direction, and the one a release pass trips: an
    Unreleased section carrying entries with nothing behind them means
    the tag was cut and the section was never emptied."""
    root = make_git_repo(tmp_path)
    write(root, "CHANGELOG.md",
          "# Changelog\n\n## Unreleased\n\n- a change nobody committed\n\n"
          "## v0.1.0 · 2026-08-01\n\n- first cut\n")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "changelog")
    git(root, "tag", "v0.1.0")
    assert only(run_s(root), "S011") == [
        ("error", "CHANGELOG.md",
         "Unreleased section has entries but no commits since v0.1.0")]


def test_s011_runs_on_a_detached_head(tmp_path):
    """The environment CI actually runs it in.

    actions/checkout builds the merge commit and leaves the tree
    detached, so a check that asks for a branch name before it will run
    is a check that never runs on a pull request. This one asks whether
    git answers at all, and a detached checkout still has the tags.
    """
    root = make_git_repo(tmp_path)
    git(root, "checkout", "--detach", "HEAD")
    write(root, "CHANGELOG.md", "# Changelog\n\n## v9.9.9 · 2026-08-01\n\n- a change\n")
    assert only(run_s(root), "S011") == [("error", "CHANGELOG.md",
                                          "heading v9.9.9 has no matching git tag")]


def test_s011_is_silent_outside_a_repository(tmp_path):
    """No git means no tags, and every heading would read as missing one."""
    root = make_repo(tmp_path)
    write(root, "CHANGELOG.md", "# Changelog\n\n## v9.9.9 · 2026-08-01\n\n- a change\n")
    assert only(run_s(root), "S011") == []


# --- S012 ---------------------------------------------------------------


def test_s012_missing_top_key_and_row_keys(tmp_path):
    root = make_repo(tmp_path)
    write(root, "estate/repos.yaml",
          "updated: 2026-08-03\n"
          "root: C:/ventures\n"
          "repos:\n"
          "  alpha:\n"
          "    path: ventures/alpha\n"
          "    bogus: value\n")
    fs = run_s(root)
    got = only(fs, "S012")
    assert ("error", "estate/repos.yaml", "missing top-level key: version") in got
    assert ("error", "estate/repos.yaml", "repo alpha: missing role") in got
    assert ("error", "estate/repos.yaml", "repo alpha: missing status") in got
    assert ("error", "estate/repos.yaml", "repo alpha: unknown key bogus") in got


def test_s012_well_formed_manifest_clean(tmp_path):
    root = make_repo(tmp_path)
    write(root, "estate/repos.yaml", ESTATE_YAML)
    assert only(run_s(root), "S012") == []


# --- exemptions: verbatim history and out-of-tree material --------------


BROKEN = ("---\nsummary: A file with a dead reference\ntype: org\n"
          "tags: [eos]\n---\n\nSee `org/GONE.md` and ADR-0099.\n")


def test_archive_is_verbatim_history_and_exempt(tmp_path):
    root = make_repo(tmp_path)
    write(root, "archive/v1/doctrine/OLD.md", BROKEN)
    assert run_s(root) == []


def test_session_logs_are_append_only_and_exempt(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/logs/2026-07/S-0019.md", BROKEN)
    assert run_s(root) == []


def test_pack_research_fragments_are_exempt(tmp_path):
    root = make_repo(tmp_path)
    write(root, "packs/testmod/research/DRILL_PROPOSAL.md", BROKEN)
    assert run_s(root) == []


def test_the_same_defect_in_a_live_file_is_an_error(tmp_path):
    """The exemptions are about where, not about what."""
    root = make_repo(tmp_path)
    write(root, "org/LIVE.md", BROKEN)
    got = only(run_s(root), "S003") + only(run_s(root), "S004")
    assert ("error", "org/LIVE.md",
            "path reference does not resolve: org/GONE.md") in got
    assert ("error", "org/LIVE.md", "reference to undefined id ADR-0099") in got


# --- S013 domain coverage matrix ---------------------------------------

REPO_ROOT_COV = "registry/coverage.json"


def _matrix(root, rows):
    """Give the fixture a coverage matrix and the schema that governs it."""
    write(root, REPO_ROOT_COV, json.dumps({"version": 1, "rows": rows}, indent=1) + "\n")
    src = (RepoModel.load(root, today=TODAY).root)
    schema = shutil.copy(
        str(__import__("conftest").REPO_ROOT / "kernel" / "schemas" / "coverage.schema.json"),
        str(src / "kernel" / "schemas" / "coverage.schema.json"))
    return schema


def _built_row(**over):
    row = {
        "capability": "testing-things",
        "status": "built",
        "pack": "packs/testmod/",
        "activation": "Any test. Predicates: does_a_thing.",
        "evidence_sources": ["EV-0001", "EV-0002", "EV-0003"],
        "worked_example": ["packs/testmod/PACK.md"],
        "evaluation_method": "packs/testmod/CHECKS.md",
        "estate_relevance": "The fixture needs one.",
        "owner": "EOS integrator",
        "review_trigger": "2030-01",
    }
    row.update(over)
    return row


def _prepare(root):
    (root / "kernel" / "schemas").mkdir(parents=True, exist_ok=True)
    write(root, "registry/evidence.json", json.dumps(
        {"version": 1, "records": [{"id": f"EV-{n:04d}"} for n in (1, 2, 3)]}, indent=1) + "\n")


def test_s013_clean_matrix(tmp_path):
    root = make_repo(tmp_path)
    _prepare(root)
    _matrix(root, [_built_row()])
    assert only(run_s(root), "S013") == []


def test_s013_built_row_without_a_worked_example(tmp_path):
    """The defect that shipped: twelve rows said built and carried no
    worked_example key at all."""
    root = make_repo(tmp_path)
    _prepare(root)
    row = _built_row()
    del row["worked_example"]
    _matrix(root, [row])
    assert any("worked_example" in m for _, _, m in only(run_s(root), "S013"))


def test_s013_prose_where_evidence_ids_belong(tmp_path):
    """'18 records in registry/evidence.json' is not a source list."""
    root = make_repo(tmp_path)
    _prepare(root)
    _matrix(root, [_built_row(evidence_sources=["18 records in registry/evidence.json"])])
    msgs = " ".join(m for _, _, m in only(run_s(root), "S013"))
    assert "EV-" in msgs


def test_s013_worked_example_must_resolve(tmp_path):
    root = make_repo(tmp_path)
    _prepare(root)
    _matrix(root, [_built_row(worked_example=["packs/testmod/exemplars/GONE.md"])])
    assert any("does not resolve" in m for _, _, m in only(run_s(root), "S013"))


def test_s013_a_pack_with_no_row_is_a_finding(tmp_path):
    """Omissions are rows, never silence."""
    root = make_repo(tmp_path)
    _prepare(root)
    _matrix(root, [])
    assert any("no coverage row" in m for _, _, m in only(run_s(root), "S013"))


def test_s013_unknown_evidence_id(tmp_path):
    root = make_repo(tmp_path)
    _prepare(root)
    _matrix(root, [_built_row(evidence_sources=["EV-0001", "EV-0002", "EV-9999"])])
    assert any("not in the ledger: EV-9999" in m for _, _, m in only(run_s(root), "S013"))


# --- S014 pack-local fragment ids --------------------------------------


def test_s014_fragment_id_in_the_read_surface(tmp_path):
    """1,035 citations pointed at a namespace that existed only inside
    one file per pack, after the import had assigned real EV ids."""
    root = make_repo(tmp_path)
    write(root, "packs/testmod/PACK.md",
          "---\nsummary: A pack citing its own fragment namespace\n"
          "type: doctrine\ntags: [eos]\nreview_by: 2030-01\n---\n\n"
          "# Testmod\n\nThe rule rests on FRAG-TESTMOD-01.\n")
    assert only(run_s(root), "S014") == [
        ("error", "packs/testmod/PACK.md",
         "pack-local fragment id in the read surface: FRAG-TESTMOD-01; "
         "cite the EV id the import assigned")]


def test_s014_research_is_the_pre_import_record(tmp_path):
    """research/ keeps its fragment ids: sources.fragment.json still
    uses them, and rewriting one without the other desyncs the pair."""
    root = make_repo(tmp_path)
    write(root, "packs/testmod/research/NOTES.md",
          "---\nsummary: Research notes before import\ntype: org\n"
          "tags: [eos]\n---\n\nFRAG-TESTMOD-01 says so.\n")
    assert only(run_s(root), "S014") == []


# --- S015 pack activation triggers --------------------------------------

PACK_HEAD = ("---\nsummary: Testmod doctrine, one plain principle\n"
             "type: doctrine\ntags: [eos]\nreview: 2030-01\n")


def test_s015_is_quiet_when_a_pack_declares_both_triggers(tmp_path):
    """The fixture pack carries both, so the whole S-series is green on
    it. This names the check so the silence is attributable."""
    root = make_repo(tmp_path)
    assert only(run_s(root), "S015") == []


def test_s015_a_pack_without_activation_paths_cannot_be_reached(tmp_path):
    root = make_repo(tmp_path)
    write(root, "packs/testmod/PACK.md",
          PACK_HEAD + "applies_when: [does_a_fixture_thing]\n---\n\n"
          "# Testmod\n\nBody.\n")
    msgs = [m for _, _, m in only(run_s(root), "S015")]
    assert msgs == ["no activation_paths: the pack cannot be reached "
                    "deterministically, so it will never activate"]


def test_s015_a_pack_without_predicates_has_no_real_gate(tmp_path):
    root = make_repo(tmp_path)
    write(root, "packs/testmod/PACK.md",
          PACK_HEAD + "activation_paths: [**/testmod/**]\n---\n\n"
          "# Testmod\n\nBody.\n")
    msgs = [m for _, _, m in only(run_s(root), "S015")]
    assert msgs == ["no applies_when: predicates are the real gate "
                    "under packs/PACK_SHAPE.md"]


def test_s015_judges_pack_md_and_nothing_else_under_a_pack(tmp_path):
    """A guide or a checks file is not an activation surface, so it is
    never asked for triggers it has no business carrying."""
    root = make_repo(tmp_path)
    write(root, "packs/testmod/CHECKS.md",
          "---\nsummary: Testmod acceptance checks\ntype: doctrine\n"
          "tags: [eos]\nreview: 2030-01\n---\n\n# Checks\n\nBody.\n")
    assert only(run_s(root), "S015") == []


# --- S016 cited_by is derived, not typed in ------------------------------


def _ledger(root, records, cutoff="2026-08-01"):
    doc = {"version": 1, "generated": "2026-08-01",
           "note": "Fixture ledger.", "records": records}
    if cutoff:
        doc["research_cutoff"] = cutoff
    write(root, "registry/evidence.json", json.dumps(doc, indent=1) + "\n")


def test_s016_is_quiet_when_cited_by_matches_the_tree(tmp_path):
    root = make_repo(tmp_path)
    write(root, "packs/testmod/CITES.md",
          "---\nsummary: A pack file citing one evidence row\n"
          "type: doctrine\ntags: [eos]\nreview: 2030-01\n---\n\n"
          "# Cites\n\nThe rule rests on EV-0001.\n")
    _ledger(root, [{"id": "EV-0001", "cited_by": ["testmod"]}])
    assert only(run_s(root), "S016") == []


def test_s016_reports_a_record_that_claims_a_citation_it_has_not(tmp_path):
    """cited_by is derived. Typed in, it says a dead record is load
    bearing, which is the shape that hid 107 uncited rows."""
    root = make_repo(tmp_path)
    _ledger(root, [{"id": "EV-0001", "cited_by": ["testmod"]}])
    msgs = [m for _, _, m in only(run_s(root), "S016")]
    assert len(msgs) == 1
    assert "cited_by is stale for 1 record(s) (EV-0001)" in msgs[0]
    assert "python tools/import_fragments.py" in msgs[0]


def test_s016_wants_the_ledger_to_date_its_own_reading(tmp_path):
    root = make_repo(tmp_path)
    _ledger(root, [{"id": "EV-0001", "cited_by": []}], cutoff=None)
    msgs = [m for _, _, m in only(run_s(root), "S016")]
    assert msgs == ["no research_cutoff: the ledger cannot say how old "
                    "its own reading is"]


def test_s016_says_nothing_without_a_ledger(tmp_path):
    assert only(run_s(make_repo(tmp_path)), "S016") == []


# --- S017 the evidence ledger against its schema ------------------------


def _evidence_schema(root):
    (root / "kernel" / "schemas").mkdir(parents=True, exist_ok=True)
    shutil.copy(
        str(REPO_ROOT / "kernel" / "schemas" / "evidence.schema.json"),
        str(root / "kernel" / "schemas" / "evidence.schema.json"))


def _record(**over):
    row = {
        "id": "EV-0001",
        "source": "A source the fixture cites",
        "url": "https://example.invalid/a",
        "kind": "maintainer",
        "publication_status": "blog",
        "study_design": None,
        "population": None,
        "model": None,
        "benchmark": None,
        "version_or_commit": "2026-08-01",
        "licence": "CC-BY-4.0",
        "access_date": "2026-08-01",
        "maintenance": "active",
        "finding": "The fixture needs one finding.",
        "applicability_limits": "It is a fixture.",
        "counter_evidence": None,
        "cited_by": [],
        "review": "2030-01",
    }
    row.update(over)
    return row


def test_s017_is_quiet_on_a_ledger_that_matches_its_schema(tmp_path):
    root = make_repo(tmp_path)
    _evidence_schema(root)
    _ledger(root, [_record()])
    assert only(run_s(root), "S017") == []


def test_s017_reports_a_value_outside_the_schema_enum(tmp_path):
    """A schema nobody validates against is a comment."""
    root = make_repo(tmp_path)
    _evidence_schema(root)
    _ledger(root, [_record(publication_status="probably-out-by-now")])
    msgs = [m for _, _, m in only(run_s(root), "S017")]
    assert msgs and all(m.startswith("schema: ") for m in msgs)
    assert any("publication_status" in m for m in msgs)


def test_s017_holds_the_licence_floor(tmp_path):
    """PACK_SHAPE item 11 wants a fact. A record may say the source
    states no licence; 'unknown' means nobody looked."""
    root = make_repo(tmp_path)
    _evidence_schema(root)
    _ledger(root, [_record(licence="unknown")])
    msgs = [m for _, _, m in only(run_s(root), "S017")]
    assert len(msgs) == 1
    assert "licence 'unknown' (EV-0001)" in msgs[0]


def test_s017_says_nothing_without_a_ledger_or_a_schema(tmp_path):
    root = make_repo(tmp_path)
    _ledger(root, [_record(licence="unknown")])
    assert only(run_s(root), "S017") == []


# --- retired trees ------------------------------------------------------


def test_s003_reference_into_a_retired_tree(tmp_path):
    """The exemption for out-of-tree paths also hid every reference into
    a tree we deleted, which is how GOVERNANCE.md pointed at
    doctrine/WARGAME_INDEX.md unseen."""
    root = make_repo(tmp_path)
    write(root, "archive/RETIRED_IDS.json",
          json.dumps({"version": 1, "ids": {}, "retired_paths": ["doctrine/"]}))
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "See `doctrine/WARGAME_INDEX.md` for the index.")
    msgs = [m for _, _, m in only(run_s(root), "S003")]
    assert any("retired tree doctrine/" in m for m in msgs)


def test_s003_venture_paths_stay_exempt(tmp_path):
    """Prose about another workspace was never a claim about this tree."""
    root = make_repo(tmp_path)
    write(root, "archive/RETIRED_IDS.json",
          json.dumps({"version": 1, "ids": {}, "retired_paths": ["doctrine/"]}))
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "The venture writes `docs/COMPILE_REPORT.md` in its own repo.")
    assert only(run_s(root), "S003") == []


# --- S018 lesson conflicts ----------------------------------------------


def lessons(root, rows, **top):
    doc = {"version": 1, "note": "a test ledger", "rows": rows}
    doc.update(top)
    write(root, "registry/lessons.json", json.dumps(doc, indent=1) + "\n")


# A row that validates against the shipped schema. S018 reads shapes out
# of a lesson row, so a test asserting that a shape is accepted has to
# run against the real schema and a row that satisfies it: with a stub
# schema, or none at all, S018 will happily accept shapes S019 rejects,
# which is exactly how the two drifted apart.
VALID_LESSON_ROW = {
    "id": "LES-0001", "origin": "harvest", "venture": "Venture C",
    "title": "A short scannable label",
    "lesson": "The lesson itself, one paragraph.",
    "evidence_class": "observational", "disposition": "estate-default",
    "outcome": "Folded into a pack.", "scope": "estate",
    "applicability_conditions": "Where the conditions held.",
    "decided": "2026-08",
}


def with_kernel_schema(root):
    """Install the lesson schema the repository actually ships."""
    from conftest import REPO_ROOT

    (root / "kernel" / "schemas").mkdir(parents=True, exist_ok=True)
    shutil.copy(REPO_ROOT / "kernel" / "schemas" / "lesson.schema.json",
                root / "kernel" / "schemas" / "lesson.schema.json")


def test_s018_says_nothing_without_a_ledger(tmp_path):
    """registry/lessons.json is new in v2.1. A repository without one
    has no lessons, which is not a finding."""
    assert only(run_s(make_repo(tmp_path)), "S018") == []


def test_s018_fires_on_an_unresolved_conflict(tmp_path):
    root = make_repo(tmp_path)
    lessons(root, [{"id": "LES-0001", "lesson": "x",
                    "conflicts_with": ["packs/coding/PACK.md#B1"]}])
    msgs = [m for _, _, m in only(run_s(root), "S018")]
    assert msgs == ["LES-0001: conflicts_with packs/coding/PACK.md#B1 is "
                    "unresolved; record it in conflict_resolutions as "
                    "{resolution, note}, the resolution being one of "
                    "stricter-applies, scoped-differently, superseded, "
                    "operator-ruling"]


def test_s018_accepts_the_shape_the_schema_permits(tmp_path):
    """One shape: a ref string in conflicts_with, and an object under
    conflict_resolutions carrying the resolution and the note."""
    root = make_repo(tmp_path)
    with_kernel_schema(root)
    lessons(root, [dict(
        VALID_LESSON_ROW,
        conflicts_with=["LES-0000"],
        conflict_resolutions={"LES-0000": {
            "resolution": "stricter-applies",
            "note": "the older rule is the tighter one"}})])
    assert only(run_s(root), "S018") == []
    assert only(run_s(root), "S019") == []


def test_s018_does_not_accept_a_bare_string_resolution(tmp_path):
    """The schema wants an object under each ref. A bare string reads as
    no resolution here rather than as a resolution in the wrong wrapper,
    and S019 reports the shape, which is its job and not this check's."""
    root = make_repo(tmp_path)
    with_kernel_schema(root)
    lessons(root, [dict(VALID_LESSON_ROW, conflicts_with=["LES-0000"],
                        conflict_resolutions={"LES-0000": "stricter-applies"})])
    assert [m for _, _, m in only(run_s(root), "S018")] == [
        "LES-0001: conflicts_with LES-0000 is unresolved; record it in "
        "conflict_resolutions as {resolution, note}, the resolution being "
        "one of stricter-applies, scoped-differently, superseded, "
        "operator-ruling"]
    assert any("is not of type 'object'" in m
               for _, _, m in only(run_s(root), "S019"))


def test_s018_does_not_accept_a_resolution_written_inside_the_link(tmp_path):
    """conflicts_with holds ref strings. An object written in there is
    not a second sanctioned shape: the schema rejects it, so S018 must
    not report it settled."""
    root = make_repo(tmp_path)
    with_kernel_schema(root)
    lessons(root, [dict(VALID_LESSON_ROW, conflicts_with=[
        {"ref": "LES-0000", "resolution": "scoped-differently",
         "note": "one is estate scope, one is venture"}])])
    assert [m for _, _, m in only(run_s(root), "S018")] == [
        "LES-0001: conflicts_with (not a ref string) is unresolved; record "
        "it in conflict_resolutions as {resolution, note}, the resolution "
        "being one of stricter-applies, scoped-differently, superseded, "
        "operator-ruling"]
    assert only(run_s(root), "S019") != []


def test_s018_rejects_a_resolution_outside_the_vocabulary(tmp_path):
    root = make_repo(tmp_path)
    with_kernel_schema(root)
    lessons(root, [dict(VALID_LESSON_ROW, conflicts_with=["LES-0000"],
                        conflict_resolutions={"LES-0000": {
                            "resolution": "we talked about it",
                            "note": "at some point"}})])
    msgs = [m for _, _, m in only(run_s(root), "S018")]
    assert msgs == ["LES-0001: unknown conflict resolution for LES-0000: "
                    "we talked about it; expected one of stricter-applies, "
                    "scoped-differently, superseded, operator-ruling"]


def test_s018_wants_a_note_on_every_resolution(tmp_path):
    """The schema requires a note for every resolution, not only for an
    operator ruling: a resolution nobody can read cannot be reviewed."""
    root = make_repo(tmp_path)
    with_kernel_schema(root)
    for resolution in ("operator-ruling", "superseded"):
        lessons(root, [dict(VALID_LESSON_ROW, conflicts_with=["LES-0000"],
                            conflict_resolutions={"LES-0000": {
                                "resolution": resolution, "note": ""}})])
        msgs = [m for _, _, m in only(run_s(root), "S018")]
        assert msgs == ["LES-0001: conflict with LES-0000 is resolved %s "
                        "with nothing recorded; note the condition, the "
                        "ruling or the successor that settles it"
                        % resolution]
    lessons(root, [dict(VALID_LESSON_ROW, conflicts_with=["LES-0000"],
                        conflict_resolutions={"LES-0000": {
                            "resolution": "operator-ruling",
                            "note": "Daniel kept the older rule"}})])
    assert only(run_s(root), "S018") == []
    assert only(run_s(root), "S019") == []


def test_s018_leaves_a_row_with_no_conflicts_alone(tmp_path):
    root = make_repo(tmp_path)
    lessons(root, [{"id": "LES-0001", "lesson": "x", "informs": ["packs/coding"]}])
    assert only(run_s(root), "S018") == []


# --- S019 the lessons ledger against its schema -------------------------


LESSON_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "required": ["version", "rows"],
    "properties": {"version": {"type": "integer"}, "rows": {
        "type": "array",
        "items": {"type": "object", "required": ["id", "lesson"],
                  "properties": {"id": {"type": "string",
                                        "pattern": "^LES-\\d{4}$"}}}}},
}


def with_schema(root, schema=None):
    write(root, "kernel/schemas/lesson.schema.json",
          json.dumps(schema if schema is not None else LESSON_SCHEMA))


def test_s019_validates_the_ledger_against_its_schema(tmp_path):
    root = make_repo(tmp_path)
    with_schema(root)
    lessons(root, [{"id": "nonsense", "lesson": "x"}])
    msgs = [m for _, _, m in only(run_s(root), "S019")]
    assert any("schema: rows/0/id" in m for m in msgs)


def test_s019_runs_against_the_real_kernel_schema(tmp_path):
    """The stub above exercises the plumbing; this runs the schema the
    repository actually ships, so the check and the schema cannot drift
    apart unnoticed."""
    import shutil

    from conftest import REPO_ROOT

    root = make_repo(tmp_path)
    (root / "kernel" / "schemas").mkdir(parents=True, exist_ok=True)
    shutil.copy(REPO_ROOT / "kernel" / "schemas" / "lesson.schema.json",
                root / "kernel" / "schemas" / "lesson.schema.json")
    row = {
        "id": "LES-0001", "origin": "harvest", "venture": "Venture C",
        "title": "A short scannable label",
        "lesson": "The lesson itself, one paragraph.",
        "evidence_class": "observational", "disposition": "estate-default",
        "outcome": "Folded into a pack.", "scope": "estate",
        "applicability_conditions": "Where the conditions held.",
        "decided": "2026-08",
    }
    lessons(root, [row])
    assert only(run_s(root), "S019") == []
    assert only(run_s(root), "S018") == []

    # The schema requires a resolution once a conflict is named, and
    # S018 requires it to be one the vocabulary knows.
    lessons(root, [dict(row, conflicts_with=["WG-OPS-002"])])
    assert [m for _, _, m in only(run_s(root), "S018")] == [
        "LES-0001: conflicts_with WG-OPS-002 is unresolved; record it in "
        "conflict_resolutions as {resolution, note}, the resolution being "
        "one of stricter-applies, scoped-differently, superseded, "
        "operator-ruling"]
    assert any("conflict_resolutions" in m
               for _, _, m in only(run_s(root), "S019"))


def test_s019_is_quiet_on_a_clean_ledger(tmp_path):
    root = make_repo(tmp_path)
    with_schema(root)
    lessons(root, [{"id": "LES-0001", "lesson": "x"}])
    assert only(run_s(root), "S019") == []


def test_s019_reports_a_duplicate_id(tmp_path):
    """informs, conflicts_with and supersedes all address a row by id,
    so a duplicate makes every link into it ambiguous."""
    root = make_repo(tmp_path)
    with_schema(root)
    lessons(root, [{"id": "LES-0001", "lesson": "x"},
                   {"id": "LES-0001", "lesson": "y"}])
    msgs = [m for _, _, m in only(run_s(root), "S019")]
    assert msgs == ["duplicate lesson id LES-0001: every link into it is "
                    "ambiguous"]


def test_s019_reports_an_evidence_id_the_ledger_does_not_hold(tmp_path):
    root = make_repo(tmp_path)
    with_schema(root)
    write(root, "registry/evidence.json",
          json.dumps({"version": 1, "generated": "2026-08-03", "note": "n",
                      "records": [{"id": "EV-0001"}]}))
    lessons(root, [{"id": "LES-0001", "lesson": "x", "evidence": ["EV-9999"]}])
    msgs = [m for _, _, m in only(run_s(root), "S019")]
    assert msgs == ["LES-0001: cites EV-9999, which is not in "
                    "registry/evidence.json"]
    lessons(root, [{"id": "LES-0001", "lesson": "x", "evidence": ["EV-0001"]}])
    assert only(run_s(root), "S019") == []


def test_s019_says_the_schema_is_missing_rather_than_passing_quietly(tmp_path):
    root = make_repo(tmp_path)
    lessons(root, [{"id": "LES-0001", "lesson": "x"}])
    msgs = [m for _, _, m in only(run_s(root), "S019")]
    assert any("lesson.schema.json is missing" in m for m in msgs)


def test_s019_reports_a_malformed_ledger(tmp_path):
    root = make_repo(tmp_path)
    write(root, "registry/lessons.json", "{not json")
    msgs = [m for _, _, m in only(run_s(root), "S019")]
    assert any("not valid JSON" in m for m in msgs)
