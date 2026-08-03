"""Semantic S-series tests: one defect per check, exact findings.

The series defaults to warn severity; ctx["strict_semantic"] flips it
to error. Both behaviours are asserted.
"""

import json
import shutil
from datetime import date

from conftest import git, make_git_repo, make_repo
from tools.eos.checks import run_all
from tools.eos.repo import RepoModel

TODAY = date(2026, 8, 3)


def run_s(root, today=TODAY, strict=False, offline=True):
    model = RepoModel.load(root, today=today)
    ctx = {"model": model, "root": model.root, "today": today,
           "offline": offline, "strict_semantic": strict}
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
    assert only(fs, "S001") == [("warn", "packs/testmod/guides/WG-TST-001-sample.md",
                                 "invalid status: bogus")]


def test_s001_strict_flag_flips_severity(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/guides/WG-TST-001-sample.md",
         "status: active", "status: bogus")
    fs = run_s(root, strict=True)
    assert only(fs, "S001") == [("error", "packs/testmod/guides/WG-TST-001-sample.md",
                                 "invalid status: bogus")]


def test_s001_invalid_v2_axis(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/RULE.md",
          "---\nsummary: A rule\ntype: org\ntags: [eos]\nkind: rule\n"
          "lifecycle: forever\nscope: galaxy\n---\n\nBody.\n")
    fs = run_s(root)
    assert ("warn", "org/RULE.md", "invalid lifecycle: forever") in only(fs, "S001")
    assert ("warn", "org/RULE.md", "invalid scope: galaxy") in only(fs, "S001")


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
    assert only(fs, "S002") == [("warn", "org/NEW.md",
                                 "supersedes reference does not resolve: org/GONE.md")]


def test_s002_missing_back_pointer(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/OLD.md",
          "---\nsummary: The predecessor\ntype: org\ntags: [eos]\n---\nBody.\n")
    write(root, "org/NEW.md",
          "---\nsummary: The successor\ntype: org\ntags: [eos]\n"
          "supersedes: org/OLD.md\n---\nBody.\n")
    fs = run_s(root)
    assert only(fs, "S002") == [("warn", "org/NEW.md",
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
         "See `docs/MISSING.md` for details.")
    fs = run_s(root)
    assert only(fs, "S003") == [("warn", "org/STATE.md",
                                 "path reference does not resolve: docs/MISSING.md")]


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
    assert only(fs, "S004") == [("warn", "org/STATE.md",
                                 "reference to undefined id ADR-0009")]


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
    assert only(fs, "S005") == [("warn", "org/VIEW.md",
                                 "derived file has no registered generator")]


def test_s005_registered_indexes_clean(tmp_path):
    assert only(run_s(make_repo(tmp_path)), "S005") == []


# --- S006 ---------------------------------------------------------------


def test_s006_missing_doctrine_organ(tmp_path):
    root = make_repo(tmp_path)
    (root / "packs" / "testmod" / "CHECKS.md").unlink()
    fs = run_s(root)
    assert only(fs, "S006") == [("warn", "packs/testmod", "pack missing CHECKS.md")]


def test_s006_missing_guides_dir(tmp_path):
    root = make_repo(tmp_path)
    shutil.rmtree(root / "packs" / "testmod" / "guides")
    fs = run_s(root)
    assert only(fs, "S006") == [("warn", "packs/testmod", "pack missing guides/")]


# --- S007 ---------------------------------------------------------------


def _gitify(root):
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.email", "suite@example.invalid")
    git(root, "config", "user.name", "Test Suite")
    git(root, "config", "commit.gpgsign", "false")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "fixture")


def test_s007_machine_facts_mismatch(tmp_path):
    root = make_repo(tmp_path)
    _gitify(root)
    edit(root, "org/STATE.md", "Nothing is in flight. The fixture repo is at rest.",
         "```facts\nbranch: release\ncommit: 0000000\n```\n")
    fs = run_s(root)
    got = only(fs, "S007")
    assert ("warn", "org/STATE.md",
            "machine fact branch: release but git says main") in got
    assert any(m.startswith("machine fact commit: 0000000 but HEAD is")
               for _, _, m in got)


def test_s007_matching_facts_clean(tmp_path):
    root = make_repo(tmp_path)
    _gitify(root)
    edit(root, "org/STATE.md", "Nothing is in flight. The fixture repo is at rest.",
         "```facts\nbranch: main\n```\n")
    assert only(run_s(root), "S007") == []


def test_s007_no_git_degrades_silently(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "Nothing is in flight. The fixture repo is at rest.",
         "```facts\nbranch: release\n```\n")
    assert only(run_s(root), "S007") == []


# --- S008 ---------------------------------------------------------------


def test_s008_canonical_fact_restated(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "type: org",
         "type: org\ncanonical_facts: [the cadence runs monthly]")
    edit(root, "GOVERNANCE.md", "Nothing in the fixture is protected.",
         "Nothing in the fixture is protected, and the cadence runs monthly.")
    fs = run_s(root)
    assert only(fs, "S008") == [("warn", "GOVERNANCE.md",
                                 "restates canonical fact owned by org/STATE.md: "
                                 "the cadence runs monthly")]


# --- S009 ---------------------------------------------------------------


def test_s009_cadence_table_overdue(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/CADENCE.md",
          "---\nsummary: Cadence table\ntype: org\ntags: [eos]\n---\n\n"
          "| Cadence | Playbook | Frequency | last_run | next_due |\n"
          "| --- | --- | --- | --- | --- |\n"
          "| Hygiene | PB-E09 | Monthly | 2026-06-01 | 2026-07 |\n")
    fs = run_s(root)
    assert ("warn", "org/CADENCE.md",
            "cadence 'Hygiene' overdue: next_due 2026-07") in only(fs, "S009")


def test_s009_machine_rows_overdue(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/cadence.json",
          json.dumps([{"name": "harvest", "next_due": "2026-07-15"}]))
    fs = run_s(root)
    assert only(fs, "S009") == [("warn", "org/cadence.json",
                                 "cadence 'harvest' overdue: next_due 2026-07-15")]


def test_s009_malformed_machine_rows(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/cadence.json", "not json")
    fs = run_s(root)
    assert only(fs, "S009") == [("error", "org/cadence.json", "malformed JSON")]


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
    assert only(fs, "S010") == [("warn", "registry/PROJECTS.md",
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
    assert only(fs, "S010") == [("warn", "registry/PROJECTS.md",
                                 "venture alpha pin abc1234 does not resolve")]


# --- S011 ---------------------------------------------------------------


def test_s011_heading_without_tag(tmp_path):
    root = make_git_repo(tmp_path)
    write(root, "CHANGELOG.md", "# Changelog\n\n## v9.9.9 · 2026-08-01\n\n- a change\n")
    fs = run_s(root)
    assert only(fs, "S011") == [("warn", "CHANGELOG.md",
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
    assert ("warn", "CHANGELOG.md", "git tag v0.2.0 has no CHANGELOG heading") in got
    assert ("warn", "CHANGELOG.md",
            "1 commits since v0.2.0 but the Unreleased section is empty") in got


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
    assert ("warn", "estate/repos.yaml", "missing top-level key: version") in got
    assert ("warn", "estate/repos.yaml", "repo alpha: missing role") in got
    assert ("warn", "estate/repos.yaml", "repo alpha: missing status") in got
    assert ("warn", "estate/repos.yaml", "repo alpha: unknown key bogus") in got


def test_s012_well_formed_manifest_clean(tmp_path):
    root = make_repo(tmp_path)
    write(root, "estate/repos.yaml", ESTATE_YAML)
    assert only(run_s(root), "S012") == []
