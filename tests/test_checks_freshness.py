"""Freshness F-series tests: one defect per check, exact findings."""

import json
from datetime import date

from conftest import make_repo
from tools.eos.checks import run_all
from tools.eos.repo import RepoModel

TODAY = date(2026, 8, 3)


def run_f(root, today=TODAY):
    model = RepoModel.load(root, today=today)
    ctx = {"model": model, "root": model.root, "today": today, "offline": True}
    return run_all(ctx, series="F")


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


def test_minirepo_is_fresh(tmp_path):
    assert run_f(make_repo(tmp_path)) == []


# --- F001 ---------------------------------------------------------------


def test_f001_past_review(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/README.md", "review: 2030-01", "review: 2020-01")
    fs = run_f(root)
    assert only(fs, "F001") == [("warn", "packs/testmod/README.md",
                                 "review 2020-01 has passed, verify before relying")]


def test_f001_malformed_review(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/README.md", "review: 2030-01", "review: whenever")
    fs = run_f(root)
    assert only(fs, "F001") == [
        ("error", "packs/testmod/README.md",
         "review must be YYYY-MM, on-change-of:<source> or none: whenever")]


def test_f001_v1_review_by_still_checked(tmp_path):
    """The frozen seed fixtures carry review_by and must not be edited
    to suit a checker, so the v1 spelling stays under F001."""
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/README.md", "review: 2030-01", "review_by: 2020-01")
    fs = run_f(root)
    assert only(fs, "F001") == [("warn", "packs/testmod/README.md",
                                 "review_by 2020-01 has passed, verify before relying")]


def test_f001_v2_review_none_illegal_outside_records(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/GUIDE.md",
          "---\nsummary: A guide\ntype: org\ntags: [eos]\nkind: guide\n"
          "review: none\n---\nBody.\n")
    fs = run_f(root)
    assert only(fs, "F001") == [("error", "org/GUIDE.md",
                                 "review: none is legal only for records and archived items")]


def test_f001_v2_review_none_legal_for_records_and_archived(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/REC.md",
          "---\nsummary: A record\ntype: org\ntags: [eos]\nkind: record\n"
          "review: none\n---\nBody.\n")
    write(root, "org/ARCHIVED.md",
          "---\nsummary: An archived guide\ntype: org\ntags: [eos]\nkind: guide\n"
          "lifecycle: archived\nreview: none\n---\nBody.\n")
    assert only(run_f(root), "F001") == []


def test_f001_v2_review_on_change_of_clean(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/RULE.md",
          "---\nsummary: A rule\ntype: org\ntags: [eos]\nkind: rule\n"
          "review: on-change-of:WCAG-2.2\n---\nBody.\n")
    assert only(run_f(root), "F001") == []


def test_f001_v2_review_past_and_malformed(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/PAST.md",
          "---\nsummary: Past review\ntype: org\ntags: [eos]\nkind: guide\n"
          "review: 2020-01\n---\nBody.\n")
    write(root, "org/BAD.md",
          "---\nsummary: Bad review\ntype: org\ntags: [eos]\nkind: guide\n"
          "review: eventually\n---\nBody.\n")
    fs = run_f(root)
    got = only(fs, "F001")
    assert ("warn", "org/PAST.md", "review 2020-01 has passed, verify before relying") in got
    assert ("error", "org/BAD.md",
            "review must be YYYY-MM, on-change-of:<source> or none: eventually") in got


# --- F002 ---------------------------------------------------------------


def test_f002_evidence_review_passed(tmp_path):
    root = make_repo(tmp_path)
    write(root, "registry/evidence.json", json.dumps(
        {"version": 1, "generated": "2026-08-01", "note": "",
         "records": [{"id": "EV-0001", "review": "2020-01"},
                     {"id": "EV-0002", "review": "2030-01"}]}))
    fs = run_f(root)
    assert only(fs, "F002") == [("warn", "registry/evidence.json",
                                 "EV-0001: review 2020-01 has passed")]


def test_f002_malformed_review(tmp_path):
    root = make_repo(tmp_path)
    write(root, "registry/evidence.json", json.dumps(
        {"records": [{"id": "EV-0003", "review": "soon"}]}))
    fs = run_f(root)
    assert only(fs, "F002") == [("error", "registry/evidence.json",
                                 "EV-0003: review must be YYYY-MM, on-change-of:<source> or none: soon")]


def test_f002_malformed_json(tmp_path):
    root = make_repo(tmp_path)
    write(root, "registry/evidence.json", "{broken")
    fs = run_f(root)
    assert only(fs, "F002") == [("error", "registry/evidence.json", "malformed JSON")]


def test_f002_leaves_the_three_legal_review_policies_alone(tmp_path):
    """METADATA_SPEC allows a month, an event trigger and none. Only the
    month can expire; an event-triggered row fires on its source moving
    and has no date to compare against."""
    root = make_repo(tmp_path)
    write(root, "registry/evidence.json", json.dumps(
        {"version": 1, "generated": "2026-08-01", "note": "",
         "records": [{"id": "EV-0001", "review": "2030-01"},
                     {"id": "EV-0002", "review": "on-change-of:the source"},
                     {"id": "EV-0003", "review": "none"},
                     {"id": "EV-0004", "review": "2026-08"}]}))
    assert only(run_f(root), "F002") == []


# --- F003 ---------------------------------------------------------------


def test_f003_bulk_identical_review_dates(tmp_path):
    root = make_repo(tmp_path)
    for i in range(11):
        write(root, f"bulk/f{i:02d}.md",
              "---\nsummary: Bulk file\ntype: org\ntags: [eos]\n"
              "review_by: 2029-01\n---\nBody.\n")
    fs = run_f(root)
    assert only(fs, "F003") == [("warn", "bulk/f00.md",
                                 "review date 2029-01 shared by 11 files, bulk-set smell")]


def test_f003_ten_files_is_not_a_smell(tmp_path):
    root = make_repo(tmp_path)
    for i in range(10):
        write(root, f"bulk/f{i:02d}.md",
              "---\nsummary: Bulk file\ntype: org\ntags: [eos]\n"
              "review_by: 2029-01\n---\nBody.\n")
    assert only(run_f(root), "F003") == []


# --- F004 ---------------------------------------------------------------


def test_f004_previously_exempt_type_without_review(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/README.md", "review: 2030-01\n", "")
    fs = run_f(root)
    assert only(fs, "F004") == [("warn", "packs/testmod/README.md",
                                 "type doctrine carries no review_by or review date")]


def test_f004_v2_review_field_counts_as_coverage(tmp_path):
    root = make_repo(tmp_path)
    edit(root, "packs/testmod/README.md", "review: 2030-01", "review: 2030-01")
    assert only(run_f(root), "F004") == []


def test_f003_counts_a_file_once_not_once_per_key(tmp_path):
    """review and review_by on one file is one re-read, not two."""
    root = make_repo(tmp_path)
    for i in range(8):
        write(root, f"bulk/f{i:02d}.md",
              "---\nsummary: Bulk file\ntype: org\ntags: [eos]\n"
              "kind: guide\nreview: 2029-01\nreview_by: 2029-01\n---\nBody.\n")
    assert only(run_f(root), "F003") == []


# --- exemptions: verbatim history ---------------------------------------


STALE = ("---\nsummary: A stale record\ntype: doctrine\ntags: [eos]\n"
         "review_by: 2020-01\n---\n\nBody.\n")


def test_archive_keeps_its_dates_unjudged(tmp_path):
    root = make_repo(tmp_path)
    write(root, "archive/v1/doctrine/OLD.md", STALE)
    assert run_f(root) == []


def test_session_logs_keep_their_dates_unjudged(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/logs/2026-07/S-0001.md", STALE)
    assert run_f(root) == []


def test_the_same_stale_date_in_a_live_file_is_reported(tmp_path):
    root = make_repo(tmp_path)
    write(root, "org/LIVE.md", STALE)
    assert ("warn", "org/LIVE.md",
            "review_by 2020-01 has passed, verify before relying") in only(
                run_f(root), "F001")
