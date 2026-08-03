"""CLI tests for the routed task record.

task new routes as it creates and prints the ruling, so no session
needs a second command to learn its tier. route stays for the two
recomputations that remain: a facts file before any record exists, and
gate-time recomputation against the actual diff, which resolves upward
only and is what keeps routing-once honest.
"""

import json
import shutil
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from conftest import git  # noqa: E402
from tools.eos import cli  # noqa: E402

SCHEMA = "task-record.schema.json"


def _record(side_effects=None, task_id="T-0001"):
    return {
        "id": task_id,
        "intent": "wire the quote endpoint",
        "declared": {"capabilities": [], "side_effects": side_effects or []},
        "mode": "standard",
        "tier_proposed": "R0",
        "tier_ruled": "R0",
        "reasons": [],
        "status": "proposed",
        "owner_session": "lane/test",
        "claims": ["app/"],
        "timestamps": {"opened": "2026-08-03T10:00",
                       "updated": "2026-08-03T10:00"},
    }


@pytest.fixture
def venture(tmp_path, monkeypatch):
    """A tmp venture the CLI treats as its repo root."""
    root = tmp_path / "venture"
    (root / "kernel" / "schemas").mkdir(parents=True)
    shutil.copy(REPO / "kernel" / "schemas" / SCHEMA,
                root / "kernel" / "schemas" / SCHEMA)
    monkeypatch.setattr(cli, "REPO", root)
    return root


def _record_file(root, **kwargs):
    path = root / "proposed.json"
    path.write_text(json.dumps(_record(**kwargs)), encoding="utf-8")
    return str(path)


def test_task_new_prints_the_ruling_without_a_second_command(venture, capsys):
    code = cli.main(["task", "new", "--record",
                     _record_file(venture, side_effects=["handles-pii"])])
    captured = capsys.readouterr()
    assert code == 0
    out = json.loads(captured.out)
    assert out["tier_ruled"] == "R2"
    assert [r["factor"] for r in out["reasons"]] == ["pii-handling"]
    assert out["reasons"][0]["source"] == "declared"
    # The ruling is on the record too, which is where sessions read it.
    written = json.loads(
        (venture / "org" / "tasks" / "T-0001.json").read_text(encoding="utf-8"))
    assert written["tier_ruled"] == "R2"
    assert written["reasons"] == out["reasons"]
    # And the human sees it without asking again.
    assert "ruled R2" in captured.err
    assert "pii-handling" in captured.err
    assert "read the ruling off the record" in captured.err


def test_task_new_says_when_the_ruling_is_a_clean_r0(venture, capsys):
    code = cli.main(["task", "new", "--record", _record_file(venture)])
    captured = capsys.readouterr()
    assert code == 0
    out = json.loads(captured.out)
    assert out["tier_ruled"] == "R0"
    assert out["reasons"] == []
    assert "no factor active, a clean R0" in captured.err


def test_task_new_refuses_an_invalid_record(venture):
    bad = venture / "bad.json"
    record = _record()
    del record["intent"]
    bad.write_text(json.dumps(record), encoding="utf-8")
    with pytest.raises(ValueError):
        cli.main(["task", "new", "--record", str(bad)])
    assert not (venture / "org" / "tasks" / "T-0001.json").exists()


def test_route_still_rules_a_facts_file(venture, capsys):
    facts = venture / "facts.json"
    facts.write_text(json.dumps({"capabilities": [],
                                 "side_effects": ["financial-impact"]}),
                     encoding="utf-8")
    assert cli.main(["route", "--facts", str(facts)]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["tier"] == "R2"
    assert [r["factor"] for r in out["reasons"]] == ["money"]


def test_the_gate_raises_a_stored_ruling_the_diff_contradicts(venture, capsys):
    # The loophole test. A record declares nothing and is stored as a
    # clean R0. The diff migrates a schema. Gate-time recomputation
    # rules R2, reports the discrepancy and exits 1, so under-declaring
    # buys a session nothing at the merge.
    assert cli.main(["task", "new", "--record", _record_file(venture)]) == 0
    stored = json.loads(
        (venture / "org" / "tasks" / "T-0001.json").read_text(encoding="utf-8"))
    assert stored["tier_ruled"] == "R0"
    capsys.readouterr()

    git(venture, "init", "-q", "-b", "main")
    git(venture, "config", "user.email", "suite@example.invalid")
    git(venture, "config", "user.name", "Test Suite")
    git(venture, "config", "commit.gpgsign", "false")
    git(venture, "add", ".")
    git(venture, "commit", "-q", "-m", "the record lands")
    (venture / "migrations").mkdir()
    (venture / "migrations" / "001_add.sql").write_text(
        "ALTER TABLE quote ADD COLUMN note text;\n", encoding="utf-8")
    git(venture, "add", "-A")

    code = cli.main(["route", "--task", "T-0001", "--diff", "HEAD"])
    out = json.loads(capsys.readouterr().out)
    assert code == 1
    assert out["tier"] == "R2"
    assert "schema-change" in out["discrepancies"]


def test_the_gate_reads_the_records_declared_facts(venture, capsys):
    # The record's declared block is the fact set at the gate, so a
    # declared floor survives a diff that shows nothing.
    assert cli.main(["task", "new", "--record",
                     _record_file(venture, side_effects=["touches-auth"])]) == 0
    capsys.readouterr()
    assert cli.main(["route", "--task", "T-0001"]) == 0
    out = json.loads(capsys.readouterr().out)
    assert out["tier"] == "R2"
    assert [r["factor"] for r in out["reasons"]] == ["auth-surface"]


def test_the_gate_never_lowers_the_ruling_on_the_record(venture, capsys):
    # Someone edits the declaration down after creation. Recomputation
    # resolves upward only, so the stored ruling holds.
    assert cli.main(["task", "new", "--record",
                     _record_file(venture, side_effects=["touches-auth"])]) == 0
    capsys.readouterr()
    rec = venture / "org" / "tasks" / "T-0001.json"
    record = json.loads(rec.read_text(encoding="utf-8"))
    record["declared"]["side_effects"] = []
    rec.write_text(json.dumps(record), encoding="utf-8")

    assert cli.main(["route", "--task", "T-0001"]) == 0
    captured = capsys.readouterr()
    assert json.loads(captured.out)["tier"] == "R2"
    assert "resolves upward only" in captured.err
