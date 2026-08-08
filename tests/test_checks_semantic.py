"""Semantic S-series tests: one defect per check, exact findings.

The series defaults to error severity; ctx["relax_semantic"] drops it
back to warnings for a caller that wants the work list rather than the
gate. Both behaviours are asserted, along with the exemptions that keep
verbatim history and out-of-tree material out of scope.
"""

import json
import shutil
from datetime import date

from conftest import git, make_git_repo, make_repo
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
    """No key in the context means strict: the P4 flip, defaulted."""
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/guides/WG-TST-001-sample.md",
         "status: active", "status: bogus")
    model = RepoModel.load(root, today=TODAY)
    ctx = {"model": model, "root": model.root, "today": TODAY, "offline": True}
    assert only(run_all(ctx, series="S"), "S001") == [
        ("error", "packs/testmod/guides/WG-TST-001-sample.md",
         "invalid status: bogus")]


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
         "AutoWatt's ADR-0003 rules local-first, and its ADR-0011 the shape.")
    assert only(run_s(root), "S004") == []


def test_s004_same_id_unqualified_elsewhere_is_still_checked(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "org/STATE.md", "The fixture repo is at rest.",
         "AutoWatt's ADR-0003 rules local-first. We follow ADR-0003 too.")
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
    assert ("error", "org/STATE.md",
            "machine fact branch: release but git says main") in got
    assert ("error", "org/STATE.md",
            "machine fact commit: 0000000 does not resolve") in got


def test_s007_commit_behind_head_is_clean(tmp_path):
    """A view records the commit it was built from, so it is always behind."""
    root = make_repo(tmp_path)
    _gitify(root)
    head = git(root, "rev-parse", "HEAD").strip()
    (root / "later.txt").write_text("later\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "moves on")
    edit(root, "org/STATE.md", "Nothing is in flight. The fixture repo is at rest.",
         f"```facts\nbranch: main\ncommit: {head[:12]}\n```\n")
    assert only(run_s(root), "S007") == []


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
    assert only(fs, "S008") == [("error", "GOVERNANCE.md",
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
    assert ("error", "org/CADENCE.md",
            "cadence 'Hygiene' overdue: next_due 2026-07") in only(fs, "S009")


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
