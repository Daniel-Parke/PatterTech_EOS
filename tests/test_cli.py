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


def test_task_new_calls_an_empty_fact_set_what_it_is(venture, capsys):
    """R0 from nothing declared is not the same as R0 from nothing found.

    This printed "no factor active, a clean R0", which reads as though
    the thirteen factors examined the work. Routing here reads
    declarations and no diff, so on a record declaring nothing they had
    nothing to examine, and on 21 of the first 25 records that is what
    happened.
    """
    code = cli.main(["task", "new", "--record", _record_file(venture)])
    captured = capsys.readouterr()
    assert code == 0
    out = json.loads(captured.out)
    assert out["tier_ruled"] == "R0"
    assert out["reasons"] == []
    assert "empty fact set" in captured.err
    assert "no diff is read here" in captured.err
    assert "absence of evidence, not evidence of low risk" in captured.err
    # And the gate that would catch it is named as somebody's job.
    assert "Nothing runs that gate for you" in captured.err


def test_task_new_separates_declared_but_inert_from_declared_nothing(
        venture, capsys):
    """A side effect that reaches no factor is a different sentence."""
    code = cli.main(["task", "new", "--record",
                     _record_file(venture, side_effects=["sends-external"])])
    captured = capsys.readouterr()
    assert code == 0
    assert "empty fact set" not in captured.err


def test_task_new_surfaces_a_proposal_the_facts_do_not_carry(venture, capsys):
    """T-0013 proposed R3 and was ruled R0, and nothing said so."""
    record = _record()
    record["tier_proposed"] = "R3"
    path = venture / "proposed.json"
    path.write_text(json.dumps(record), encoding="utf-8")
    code = cli.main(["task", "new", "--record", str(path)])
    captured = capsys.readouterr()
    assert code == 0
    assert json.loads(captured.out)["tier_ruled"] == "R0"
    assert "you proposed R3" in captured.err
    assert "the facts behind it are not on this record" in captured.err


def test_task_new_is_quiet_when_the_proposal_matches(venture, capsys):
    code = cli.main(["task", "new", "--record",
                     _record_file(venture, side_effects=["handles-pii"])])
    captured = capsys.readouterr()
    assert code == 0
    assert "you proposed" not in captured.err


def test_task_new_refuses_an_invalid_record(venture, capsys):
    """A record the schema rejects is a run that could not happen.

    It used to raise out of main, print a traceback and exit 1, and 1
    is the code for findings, so a caller read a malformed record as a
    failing check.
    """
    bad = venture / "bad.json"
    record = _record()
    del record["intent"]
    bad.write_text(json.dumps(record), encoding="utf-8")
    assert cli.main(["task", "new", "--record", str(bad)]) == 2
    assert "task record invalid" in capsys.readouterr().err
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


def test_the_package_and_its_metadata_report_one_version():
    """Two version strings that can disagree will, and the one a reader
    trusts is whichever they happened to look at."""
    import re

    import tools.eos

    text = (REPO / "tools" / "pyproject.toml").read_text(encoding="utf-8")
    declared = re.search(r'(?m)^version\s*=\s*"([^"]+)"', text).group(1)
    assert tools.eos.__version__ == declared


def test_knowledge_list_is_a_summary_and_show_is_full(monkeypatch, capsys):
    monkeypatch.setattr(cli, "REPO", REPO)
    assert cli.main(["doctrine", "list"]) == 0
    listed = json.loads(capsys.readouterr().out)
    assert listed["count"] >= 513
    assert "metadata" not in listed["records"][0]
    assert "body" not in listed["records"][0]
    identifier = listed["records"][0]["id"]

    assert cli.main(["doctrine", "show", identifier]) == 0
    shown = json.loads(capsys.readouterr().out)
    assert shown["metadata"]["id"] == identifier
    assert shown["body"]


def test_a_closed_output_pipe_is_a_successful_short_read(monkeypatch):
    def closed_pipe(_args):
        raise BrokenPipeError

    monkeypatch.setattr(cli, "cmd_knowledge", closed_pipe)
    assert cli.main(["doctrine", "list"]) == 0


def _subcommands(parser):
    import argparse

    for action in parser._actions:
        if isinstance(action, argparse._SubParsersAction):
            return dict(action.choices)
    return {}


def test_cli_contracts_documents_every_subcommand():
    """The contract file is the CLI's law, and a command it does not
    mention is a command nobody agreed to."""
    commands = set(_subcommands(cli.build_parser()))
    text = (REPO / "tools" / "CLI_CONTRACTS.md").read_text(encoding="utf-8")
    headings = {line[3:].strip() for line in text.splitlines()
                if line.startswith("## ")}
    documented = {h.split()[0] for h in headings}
    assert commands <= documented, sorted(commands - documented)
    # And nothing documented as a command has quietly disappeared.
    assert (documented - commands - {"Shared", "Exit"}) == set()


def test_cli_contracts_documents_every_flag():
    """Every flag the parser accepts appears in the contract, so the
    file cannot describe a command it no longer matches."""
    text = (REPO / "tools" / "CLI_CONTRACTS.md").read_text(encoding="utf-8")
    for name, parser in _subcommands(cli.build_parser()).items():
        for action in parser._actions:
            for flag in action.option_strings:
                if flag in ("-h", "--help"):
                    continue
                assert flag in text, "%s %s is undocumented" % (name, flag)


def test_cli_contracts_documents_every_task_op():
    """The op is positional, so the flag test above never sees it, and
    a documented op that no longer exists reads as a command a session
    can run."""
    text = (REPO / "tools" / "CLI_CONTRACTS.md").read_text(encoding="utf-8")
    for name in ("task", "migrate", "benchmark"):
        parser = _subcommands(cli.build_parser())[name]
        for action in parser._actions:
            for choice in action.choices or ():
                assert "`%s" % choice in text or "%s " % choice in text, \
                    "%s %s is undocumented" % (name, choice)


def test_the_series_flag_takes_only_the_series_that_exist(capsys):
    """A typo used to read as a clean run.

    `--series` is a prefix match over the check ids, so any other value
    selected nothing and reported "0 errors, 0 warnings", exit 0. The
    choices are held against the registry here so the flag cannot drift
    from the checks that exist.
    """
    from tools.eos import checks

    series = None
    for action in _subcommands(cli.build_parser())["check"]._actions:
        if "--series" in action.option_strings:
            series = set(action.choices or ())
    assert series == {check_id[0] for check_id in checks.REGISTRY}

    with pytest.raises(SystemExit) as exit_code:
        cli.main(["check", "--series", "Z"])
    assert exit_code.value.code == 2
    assert "invalid choice" in capsys.readouterr().err


# --- the documented exit codes, exercised ------------------------------


def test_cannot_run_is_two_and_findings_are_one(venture, capsys, tmp_path):
    """Exit 2 says the run could not happen; exit 1 says it happened and
    found something. A caller that cannot tell them apart retries a
    broken invocation as though it were a failing check.
    """
    assert cli.main(["check", "--repo", "--seed", str(tmp_path)]) == 2
    assert "different runs" in capsys.readouterr().err

    assert cli.main(["route", "--task", "T-9999"]) == 2
    assert "no task record" in capsys.readouterr().err

    assert cli.main(["context", "--task", "T-9999"]) == 2
    assert "no task record" in capsys.readouterr().err

    assert cli.main(["task", "show", "--id", "T-9999"]) == 2
    assert "no task record" in capsys.readouterr().err

    assert cli.main(["route", "--facts", str(tmp_path / "nothing.json")]) == 2
    assert "No such file" in capsys.readouterr().err


def test_malformed_input_is_two_rather_than_a_traceback(venture, capsys):
    """Malformed input is the other half of "cannot run".

    Each of these raised out of main, printed a traceback and exited 1.
    A caller reads 1 as findings, so a broken invocation looked like a
    failing check, and the message a caller got was a stack trace.
    """
    facts = venture / "facts.json"
    facts.write_text("not json at all\n", encoding="utf-8")
    assert cli.main(["route", "--facts", str(facts)]) == 2
    err = capsys.readouterr().err
    assert "declared facts file" in err and "is not JSON" in err
    assert "Traceback" not in err

    # Valid JSON of the wrong shape is malformed for this purpose too:
    # it used to reach the reader as a list and fail there.
    facts.write_text(json.dumps(["capabilities"]), encoding="utf-8")
    assert cli.main(["route", "--facts", str(facts)]) == 2
    assert "not a JSON object" in capsys.readouterr().err

    assert cli.main(["task", "new", "--record",
                     _record_file(venture)]) == 0
    capsys.readouterr()
    assert cli.main(["task", "update", "--id", "T-0001",
                     "--patch", "status: done"]) == 2
    assert "--patch is not JSON" in capsys.readouterr().err


def test_a_diff_ref_git_cannot_resolve_is_a_cannot_run(venture, capsys):
    """The portable one. The merge gate wraps `route --diff BASE...HEAD`
    and a CI checkout often has only origin/main, so a base ref that
    does not resolve has to be distinguishable from discrepancies
    found."""
    facts = venture / "facts.json"
    facts.write_text(json.dumps({"capabilities": [], "side_effects": []}),
                     encoding="utf-8")
    git(venture, "init", "-q", "-b", "main")
    git(venture, "config", "user.email", "suite@example.invalid")
    git(venture, "config", "user.name", "Test Suite")
    git(venture, "config", "commit.gpgsign", "false")
    git(venture, "add", ".")
    git(venture, "commit", "-q", "-m", "base")

    assert cli.main(["route", "--facts", str(facts),
                     "--diff", "nosuchref...HEAD"]) == 2
    err = capsys.readouterr().err
    assert "failed" in err and "Traceback" not in err

    assert cli.main(["context", "--diff", "nosuchref...HEAD"]) == 2
    assert "failed" in capsys.readouterr().err


def test_guard_rules_allow_block_and_cannot_judge_apart(venture, capsys):
    """Exit 0 allow, 1 any blocking verdict, 2 when the guard cannot
    judge the action at all. Without a validated adapter every guarded
    class is manual-only, so 1 is the answer a repository with no
    adapter gets."""
    assert cli.main(["guard", "eval", "--class", "deletion",
                     "--payload", "delete the production bucket"]) == 1
    verdict = json.loads(capsys.readouterr().out)
    assert verdict["verdict"] in ("manual-only", "deny")
    assert verdict["adapter_validated"] is False

    assert cli.main(["guard", "eval", "--class", "deletion"]) == 2
    assert "cannot evaluate" in capsys.readouterr().err


def test_migrate_apply_needs_the_seed_the_state_cannot_name(venture, capsys):
    """The documented `apply --state FILE` could never run.

    `plan` cannot write the seed path into its state document, because
    `migration-state.schema.json` fixes the key set and has no room for
    one, so apply read a key that is never there, fell back to an empty
    string and refused every invocation as out of tree.
    """
    seed = venture / "seed"
    (seed / "docs").mkdir(parents=True)
    (seed / "docs" / "LOCKBOOK.md").write_text(
        "---\nsummary: A v1 lock-book\ntype: template\ntags: [eos]\n"
        "eos_version: 1.0.0\neos_commit: ba34d01\nscale: S\n"
        "stack: STACK-test\n---\n\n# Fieldwork lock-book\n",
        encoding="utf-8")
    state_path = venture / "state.json"

    assert cli.main(["migrate", "plan", "--seed", str(seed)]) == 0
    state = json.loads(capsys.readouterr().out)
    assert "seed_root" not in state
    state_path.write_text(json.dumps(state), encoding="utf-8")

    assert cli.main(["migrate", "apply", "--state", str(state_path)]) == 2
    assert "needs --seed" in capsys.readouterr().err

    before = (seed / "docs" / "LOCKBOOK.md").read_bytes()
    assert cli.main(["migrate", "apply", "--seed", str(seed),
                     "--state", str(state_path)]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["dry_run"] is True
    assert report["changes"]
    assert (seed / "docs" / "LOCKBOOK.md").read_bytes() == before


def test_migrate_apply_refuses_a_seed_outside_this_repository(
        venture, capsys, tmp_path):
    """The fixture-only guard. Pointed at a sibling tree it exits 2."""
    outside = tmp_path / "elsewhere"
    outside.mkdir()
    state = venture / "state.json"
    state.write_text(json.dumps({"version": 1, "steps": []}), encoding="utf-8")
    assert cli.main(["migrate", "apply", "--seed", str(outside),
                     "--state", str(state)]) == 2
    assert "only in this build" in capsys.readouterr().err


def test_migrate_apply_refuses_a_sibling_whose_name_extends_the_repo(
        venture, capsys, tmp_path):
    """The guard was a string prefix, so any sibling directory whose
    name merely extended this one passed it: a PatterTech_EOS_backup
    beside PatterTech_EOS. With --no-dry-run apply rewrites the
    lock-book header and every file under org/roles/, so what got
    through was a destructive write into another repository."""
    sibling = tmp_path / (venture.name + "_backup")
    (sibling / "docs").mkdir(parents=True)
    state = venture / "state.json"
    state.write_text(json.dumps({"version": 1, "steps": []}), encoding="utf-8")
    assert str(sibling).startswith(str(venture)), \
        "the fixture has to reproduce the prefix that used to pass"
    assert cli.main(["migrate", "apply", "--seed", str(sibling),
                     "--state", str(state), "--no-dry-run"]) == 2
    assert "only in this build" in capsys.readouterr().err


def test_route_exits_three_on_an_unacknowledged_protected_touch(
        venture, capsys, tmp_path):
    """Exit 3 is the only enforcement of the protected set the tooling
    has. The factor id has to match router.FACTOR_TABLE exactly, and a
    near miss switches the whole control off silently."""
    facts = venture / "facts.json"
    facts.write_text(json.dumps({"capabilities": [], "side_effects": []}),
                     encoding="utf-8")
    (venture / "org").mkdir(exist_ok=True)
    (venture / "org" / "policy.json").write_text(json.dumps(
        {"risk": {"path_patterns": {"protected": ["GOVERNANCE.md"]}}}),
        encoding="utf-8")

    git(venture, "init", "-q", "-b", "main")
    git(venture, "config", "user.email", "suite@example.invalid")
    git(venture, "config", "user.name", "Test Suite")
    git(venture, "config", "commit.gpgsign", "false")
    git(venture, "add", ".")
    git(venture, "commit", "-q", "-m", "base")
    (venture / "GOVERNANCE.md").write_text("changed\n", encoding="utf-8")
    git(venture, "add", "-A")

    assert cli.main(["route", "--facts", str(facts), "--diff", "HEAD"]) == 3
    captured = capsys.readouterr()
    assert "protected-set touch without --adr" in captured.err
    assert "GOVERNANCE.md" in captured.err

    # Acknowledged, the same touch is no longer a refusal.
    assert cli.main(["route", "--facts", str(facts), "--diff", "HEAD",
                     "--adr", "ADR-0005"]) == 0


def test_study_scaffolds_a_lens_contract(venture, capsys, tmp_path):
    """The name goes into the filename as given.

    The id form is `LENS-NNNN`, four digits, because that is what
    `kernel/schemas/lesson.schema.json` enforces on the `lens` field a
    study lesson carries, so that is what this passes.
    """
    (venture / "kernel" / "templates").mkdir(parents=True)
    (venture / "kernel" / "templates" / "LENS.tpl.md").write_text(
        "---\nsummary: Lens contract template\ntype: template\ntags: [eos]\n"
        "template: true\n---\n\n# LENS · {{SOURCE_NAME}}\n",
        encoding="utf-8")
    out_dir = tmp_path / "lenses"
    assert cli.main(["study", "--out", str(out_dir), "--name", "0002"]) == 0
    payload = json.loads(capsys.readouterr().out)
    written = Path(payload["created"])
    assert written.name == "LENS-0002.md"
    assert payload["slots"] == ["{{SOURCE_NAME}}"]
    text = written.read_text(encoding="utf-8")
    # A scaffolded contract is a working file, so it must not claim the
    # template exemption that keeps unfilled slots out of the checker.
    assert "template: true" not in text
    assert "{{SOURCE_NAME}}" in text


def test_study_refuses_to_overwrite_a_contract(venture, capsys, tmp_path):
    (venture / "kernel" / "templates").mkdir(parents=True)
    (venture / "kernel" / "templates" / "LENS.tpl.md").write_text(
        "---\nsummary: t\ntype: template\ntags: [eos]\n---\nbody\n",
        encoding="utf-8")
    out_dir = tmp_path / "lenses"
    assert cli.main(["study", "--out", str(out_dir)]) == 0
    capsys.readouterr()
    (out_dir / "LENS.md").write_text("filled in by hand\n", encoding="utf-8")
    assert cli.main(["study", "--out", str(out_dir)]) == 1
    assert "refused" in capsys.readouterr().err
    assert (out_dir / "LENS.md").read_text(encoding="utf-8") == \
        "filled in by hand\n"


def test_study_cannot_run_without_the_kernel_template(venture, capsys, tmp_path):
    assert cli.main(["study", "--out", str(tmp_path / "lenses")]) == 2
    assert "no lens template" in capsys.readouterr().err


def test_a_seed_that_is_not_there_is_a_cannot_run(venture, capsys, tmp_path):
    """Exit 2 means the run could not happen; exit 1 means findings. The
    branch that told them apart looked for the words "cannot run" in a
    message, which neither message says, so it never ran."""
    assert cli.main(["check", "--seed", str(tmp_path / "nowhere")]) == 2
    assert "seed path not found" in capsys.readouterr().err


def test_a_seed_that_fails_its_rubric_is_exit_one(capsys):
    fixture = REPO / "benchmark" / "fixtures" / "seed-v1-M"
    assert cli.main(["check", "--seed", str(fixture)]) == 1
    assert "D004" in capsys.readouterr().err


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
