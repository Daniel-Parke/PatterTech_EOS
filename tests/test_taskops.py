"""Taskops tests: record ops, atomic writes, assigned-claims
verification, and the derived view generator."""

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from conftest import git  # noqa: E402
from tools.eos import taskops  # noqa: E402

NOW = datetime(2026, 8, 3, 12, 0, tzinfo=timezone.utc)


def _record(task_id="T-0001"):
    return {
        "id": task_id,
        "intent": "test task",
        "declared": {"capabilities": [], "side_effects": []},
        "mode": "standard",
        "tier_proposed": "R1",
        "tier_ruled": "R1",
        "reasons": [],
        "status": "proposed",
        "owner_session": "lane/test",
        "claims": ["tools/eos/"],
        "timestamps": {"opened": "2026-08-03T10:00", "updated": "2026-08-03T10:00"},
    }


@pytest.fixture
def repo_root(tmp_path):
    # The schema is read from the real kernel; copy it into the tmp repo.
    root = tmp_path / "repo"
    (root / "kernel" / "schemas").mkdir(parents=True)
    shutil.copy(REPO / "kernel" / "schemas" / "task-record.schema.json",
                root / "kernel" / "schemas" / "task-record.schema.json")
    return root


def _claims_doc(**lane_overrides):
    lane = {
        "lane_id": "lane/t2",
        "task_id": "T-0001",
        "session_id": "sess-1",
        "host": "box-1",
        "pid": 4242,
        "path_claims": ["tools/eos/", "tests/test_router.py"],
        "acquired": "2026-08-03T09:00",
        "expires": "2026-08-04T09:00",
    }
    lane.update(lane_overrides)
    return {"version": 1, "assigned": "2026-08-03", "lanes": [lane]}


def test_next_task_id_starts_at_one(tmp_path):
    assert taskops.next_task_id(tmp_path) == "T-0001"


def test_next_task_id_increments(tmp_path):
    tasks = tmp_path / "org" / "tasks"
    tasks.mkdir(parents=True)
    (tasks / "T-0007.json").write_text("{}", encoding="utf-8")
    (tasks / "T-0003.json").write_text("{}", encoding="utf-8")
    assert taskops.next_task_id(tmp_path) == "T-0008"


def test_create_task_writes_valid_record(repo_root):
    path = taskops.create_task(repo_root, _record())
    assert Path(path) == repo_root / "org" / "tasks" / "T-0001.json"
    loaded = json.loads(Path(path).read_text(encoding="utf-8"))
    assert loaded["intent"] == "test task"
    # No temp files left behind by the atomic write.
    leftovers = [p for p in Path(path).parent.iterdir() if p.suffix == ".tmp"]
    assert leftovers == []


def test_create_task_rejects_invalid_record(repo_root):
    bad = _record()
    del bad["intent"]
    with pytest.raises(ValueError):
        taskops.create_task(repo_root, bad)
    assert not (repo_root / "org" / "tasks" / "T-0001.json").exists()


def test_create_task_rejects_bad_id(repo_root):
    with pytest.raises(ValueError):
        taskops.create_task(repo_root, _record(task_id="TASK-1"))


def test_create_task_routes_once_at_creation(repo_root):
    # Routing is paid here, not per session: the record carries the
    # ruled tier and the machine-readable reasons from creation on.
    rec = _record()
    rec["tier_proposed"] = "R0"
    rec["declared"]["side_effects"] = ["touches-auth"]
    path = taskops.create_task(repo_root, rec)
    loaded = json.loads(Path(path).read_text(encoding="utf-8"))
    assert loaded["tier_ruled"] == "R2"
    # The agent proposes and the router rules; the proposal stands.
    assert loaded["tier_proposed"] == "R0"
    assert [r["factor"] for r in loaded["reasons"]] == ["auth-surface"]
    reason = loaded["reasons"][0]
    assert reason["tier_floor"] == "R2"
    assert reason["source"] == "declared"
    assert "touches-auth" in reason["evidence"]
    # Stamped in place, so the caller reads the ruling back without a
    # second command.
    assert rec["tier_ruled"] == "R2"
    assert rec["reasons"] == loaded["reasons"]


def test_create_task_without_declared_facts_rules_a_clean_r0(repo_root):
    rec = _record()
    path = taskops.create_task(repo_root, rec)
    loaded = json.loads(Path(path).read_text(encoding="utf-8"))
    assert loaded["tier_ruled"] == "R0"
    # An empty reasons list is how the record says no factor is active.
    assert loaded["reasons"] == []


def test_create_task_ruling_overrides_an_optimistic_claim(repo_root):
    rec = _record()
    rec["tier_ruled"] = "R0"
    rec["declared"]["side_effects"] = ["migrates-schema", "irreversible-action"]
    taskops.create_task(repo_root, rec)
    assert rec["tier_ruled"] == "R3"
    factors = {r["factor"] for r in rec["reasons"]}
    assert factors == {"irreversible-action", "schema-change"}


def test_create_task_routing_reads_no_diff(repo_root, monkeypatch):
    # Creation-time routing is declaration-only: no git, no diff, which
    # is what makes it cheap enough to pay once and read thereafter.
    from tools.eos import router

    def boom(*args, **kwargs):
        raise AssertionError("creation-time routing must not read a diff")

    monkeypatch.setattr(router, "derive_signals", boom)
    monkeypatch.setattr(router, "_git", boom)
    path = taskops.create_task(repo_root, _record())
    assert Path(path).is_file()


def test_load_policy_reads_either_home_and_degrades_quietly(repo_root):
    assert taskops.load_policy(repo_root) == {}
    (repo_root / "docs").mkdir(parents=True, exist_ok=True)
    (repo_root / "docs" / "policy.json").write_text(
        json.dumps({"express": {"max_files": 3}}), encoding="utf-8")
    assert taskops.load_policy(repo_root)["express"]["max_files"] == 3
    # The org home wins, and a malformed policy never breaks creation.
    (repo_root / "org").mkdir(parents=True, exist_ok=True)
    (repo_root / "org" / "policy.json").write_text("{broken", encoding="utf-8")
    assert taskops.load_policy(repo_root) == {}
    assert taskops.create_task(repo_root, _record())


def test_update_task_merges_and_rewrites(repo_root):
    taskops.create_task(repo_root, _record())
    taskops.update_task(repo_root, "T-0001", {
        "status": "active",
        "timestamps": {"updated": "2026-08-03T11:00"},
    })
    loaded = json.loads(
        (repo_root / "org" / "tasks" / "T-0001.json").read_text(encoding="utf-8"))
    assert loaded["status"] == "active"
    assert loaded["timestamps"]["updated"] == "2026-08-03T11:00"
    assert loaded["timestamps"]["opened"] == "2026-08-03T10:00"


def test_update_task_rejects_invalid_patch(repo_root):
    taskops.create_task(repo_root, _record())
    with pytest.raises(ValueError):
        taskops.update_task(repo_root, "T-0001", {"status": "not-a-status"})
    loaded = json.loads(
        (repo_root / "org" / "tasks" / "T-0001.json").read_text(encoding="utf-8"))
    assert loaded["status"] == "proposed"


def test_update_task_missing_record(repo_root):
    with pytest.raises(FileNotFoundError):
        taskops.update_task(repo_root, "T-0099", {"status": "active"})


# Assigned-claims verification.

def test_refusal_when_actor_not_named(tmp_path):
    findings = taskops.verify_claims(
        tmp_path, _claims_doc(), "lane/unknown", ["tools/eos/router.py"], now=NOW)
    assert len(findings.errors) == 1
    assert "refused" in findings.errors[0].message


def test_diff_inside_claims_is_clean(tmp_path):
    findings = taskops.verify_claims(
        tmp_path, _claims_doc(), "lane/t2",
        ["tools/eos/router.py", "tests/test_router.py"], now=NOW)
    assert findings.errors == []


def test_case_folded_posix_compare(tmp_path):
    doc = _claims_doc(path_claims=["Tools/EOS/"])
    findings = taskops.verify_claims(
        tmp_path, doc, "lane/t2", ["tools\\eos\\router.py"], now=NOW)
    assert findings.errors == []


def test_prefix_needs_trailing_slash(tmp_path):
    doc = _claims_doc(path_claims=["tools/eos"])
    findings = taskops.verify_claims(
        tmp_path, doc, "lane/t2", ["tools/eos/router.py"], now=NOW)
    assert len(findings.errors) == 1
    assert "outside" in findings.errors[0].message


def test_file_outside_claims_is_an_error(tmp_path):
    findings = taskops.verify_claims(
        tmp_path, _claims_doc(), "lane/t2", ["kernel/POLICY_SPEC.md"], now=NOW)
    assert findings.errors[0].path == "kernel/POLICY_SPEC.md"


def test_rename_needs_both_paths_covered(tmp_path):
    # A rename touches both paths; the old path outside claims fails.
    findings = taskops.verify_claims(
        tmp_path, _claims_doc(), "lane/t2",
        ["tools/eos/router.py", "legacy/router.py"], now=NOW)
    assert len(findings.errors) == 1
    assert findings.errors[0].path == "legacy/router.py"


def test_expired_claim_surfaces_liveness_never_takeover(tmp_path):
    doc = _claims_doc(expires="2026-08-03T09:00")
    findings = taskops.verify_claims(
        tmp_path, doc, "lane/t2", ["tools/eos/router.py"], now=NOW)
    message = findings.errors[0].message
    assert "host=box-1" in message
    assert "pid=4242" in message
    assert "operator" in message
    assert "never authorises takeover" in message


def test_unexpired_claim_is_quiet(tmp_path):
    doc = _claims_doc(expires="2026-08-03T14:00")
    findings = taskops.verify_claims(
        tmp_path, doc, "lane/t2", ["tools/eos/router.py"], now=NOW)
    assert findings.errors == []


def test_derived_files_are_integrator_only(tmp_path):
    doc = _claims_doc(path_claims=["INDEX.md", "tools/eos/"])
    findings = taskops.verify_claims(
        tmp_path, doc, "lane/t2", ["INDEX.md"], now=NOW)
    assert "integrator" in findings.errors[0].message


@pytest.mark.parametrize(
    "path",
    [
        "packs/DOCTRINE_INDEX.md",
        "packs/WARGAME_INDEX.md",
        "registry/DOCTRINE_PRESSURE_MATRIX.md",
        "registry/IDENTIFIER_ALIASES.md",
    ],
)
def test_current_knowledge_views_are_integrator_only(tmp_path, path):
    doc = _claims_doc(path_claims=[path])
    findings = taskops.verify_claims(
        tmp_path, doc, "lane/t2", [path], now=NOW,
    )
    assert "integrator" in findings.errors[0].message


def test_integrator_may_touch_derived_files(tmp_path):
    doc = _claims_doc(lane_id="integrator", path_claims=["INDEX.md"])
    findings = taskops.verify_claims(
        tmp_path, doc, "integrator", ["INDEX.md"], now=NOW)
    assert findings.errors == []


def test_missing_jsonschema_degrades_with_install_command(repo_root, monkeypatch):
    import builtins
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "jsonschema":
            raise ImportError("no jsonschema")
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    findings = taskops.validate_task_record(repo_root, _record())
    assert "pip install" in findings.errors[0].message


# Derived views.

def _write_record(root, task_id, status="proposed", **overrides):
    rec = _record(task_id)
    rec["status"] = status
    rec.update(overrides)
    tasks = root / "org" / "tasks"
    tasks.mkdir(parents=True, exist_ok=True)
    (tasks / ("%s.json" % task_id)).write_text(
        json.dumps(rec, indent=2) + "\n", encoding="utf-8")
    return rec


def _view_root(tmp_path):
    root = tmp_path / "venture"
    _write_record(root, "T-0002", status="blocked",
                  intent="wire the deploy runbook")
    _write_record(root, "T-0001", status="active", mode="express")
    (root / "org" / "claims.json").write_text(json.dumps(
        _claims_doc(), indent=2) + "\n", encoding="utf-8")
    (root / "org" / "cadence.json").write_text(json.dumps([
        {"id": "upkeep", "frequency": "fortnightly", "last_run": None,
         "next_due": "2026-08-15", "procedure": "org/PLAYBOOKS.md#upkeep"},
        {"id": "retro", "frequency": "monthly", "last_run": None,
         "next_due": "2026-08-31", "procedure": "org/PLAYBOOKS.md#retro"},
    ], indent=2) + "\n", encoding="utf-8")
    return root


def test_render_views_writes_both_derived_views(tmp_path):
    root = _view_root(tmp_path)
    findings = taskops.render_views(root)
    assert findings == []
    tasks_view = (root / "org" / "TASKS.md").read_text(encoding="utf-8")
    state_view = (root / "org" / "STATE.md").read_text(encoding="utf-8")
    for view in (tasks_view, state_view):
        assert view.startswith("---\nsummary: ")
        assert "\ntype: org\n" in view
        assert "\ntags: [eos]\n" in view
        assert "\nderived: true\n" in view
    # One table row per record, sorted by id, records being canonical.
    assert tasks_view.index("| T-0001 |") < tasks_view.index("| T-0002 |")
    assert "| T-0001 | express | R1 | active | lane/test |" in tasks_view
    assert "| T-0002 | standard | R1 | blocked | lane/test |" in tasks_view
    # The claim set, the operator flag and the cadence rows all render.
    assert "| lane/t2 | T-0001 | sess-1 | 2026-08-04T09:00 | " \
           "tools/eos/, tests/test_router.py |" in state_view
    assert "- T-0002 blocked: wire the deploy runbook" in state_view
    assert "- T-0001" not in state_view
    assert "| upkeep | fortnightly | 2026-08-15 |" in state_view
    assert "| retro | monthly | 2026-08-31 |" in state_view


def test_render_views_regeneration_is_byte_stable(tmp_path):
    root = _view_root(tmp_path)
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.email", "suite@example.invalid")
    git(root, "config", "user.name", "Test Suite")
    git(root, "config", "commit.gpgsign", "false")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "records land")
    assert taskops.render_views(root) == []
    first_tasks = (root / "org" / "TASKS.md").read_bytes()
    first_state = (root / "org" / "STATE.md").read_bytes()
    assert taskops.render_views(root) == []
    assert (root / "org" / "TASKS.md").read_bytes() == first_tasks
    assert (root / "org" / "STATE.md").read_bytes() == first_state


def test_render_views_machine_facts_track_git(tmp_path):
    root = _view_root(tmp_path)
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.email", "suite@example.invalid")
    git(root, "config", "user.name", "Test Suite")
    git(root, "config", "commit.gpgsign", "false")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "records land")
    head = git(root, "rev-parse", "HEAD").strip()
    taskops.render_views(root)
    state_view = (root / "org" / "STATE.md").read_text(encoding="utf-8")
    # The exact shape the S007 check parses and verifies.
    assert "```facts\ncommit: %s\n```" % head in state_view


def test_render_views_records_no_branch_name(tmp_path):
    """The commit is the only machine fact written down.

    A branch name in a committed file is correct on the branch it was
    generated on and wrong the moment that branch merges, with no input
    having changed, so a check on it goes red on the merge commit's own
    run. The commit survives the merge by ancestry, which is what S007
    tests it for.
    """
    root = _view_root(tmp_path)
    git(root, "init", "-q", "-b", "some-feature-branch")
    git(root, "config", "user.email", "suite@example.invalid")
    git(root, "config", "user.name", "Test Suite")
    git(root, "config", "commit.gpgsign", "false")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "records land")
    taskops.render_views(root)
    state_view = (root / "org" / "STATE.md").read_text(encoding="utf-8")
    assert "branch" not in state_view
    assert "some-feature-branch" not in state_view


def test_render_views_without_git_omits_the_facts_block(tmp_path):
    root = _view_root(tmp_path)
    taskops.render_views(root)
    state_view = (root / "org" / "STATE.md").read_text(encoding="utf-8")
    assert "```facts" not in state_view
    assert "Git facts unavailable" in state_view


def test_render_views_empty_venture_still_renders(tmp_path):
    root = tmp_path / "bare"
    root.mkdir()
    assert taskops.render_views(root) == []
    tasks_view = (root / "org" / "TASKS.md").read_text(encoding="utf-8")
    state_view = (root / "org" / "STATE.md").read_text(encoding="utf-8")
    assert "(no task records yet)" in tasks_view
    assert "No lanes hold claims." in state_view
    assert "Nothing waits on the operator." in state_view
    assert "No cadence rows recorded." in state_view


def test_render_views_reports_and_skips_malformed_records(tmp_path):
    root = _view_root(tmp_path)
    (root / "org" / "tasks" / "T-0003.json").write_text("{broken",
                                                        encoding="utf-8")
    findings = taskops.render_views(root)
    assert [(f.severity, f.path) for f in findings] == [
        ("error", "org/tasks/T-0003.json")]
    assert "malformed JSON" in findings[0].message
    tasks_view = (root / "org" / "TASKS.md").read_text(encoding="utf-8")
    assert "| T-0001 |" in tasks_view and "| T-0002 |" in tasks_view
    assert "T-0003" not in tasks_view


def test_render_views_in_review_is_an_operator_flag(tmp_path):
    root = tmp_path / "venture"
    _write_record(root, "T-0001", status="in-review",
                  intent="awaiting the approval verdict")
    taskops.render_views(root)
    state_view = (root / "org" / "STATE.md").read_text(encoding="utf-8")
    assert "- T-0001 in-review: awaiting the approval verdict" in state_view


# --- claim refusal ------------------------------------------------------


def _claim_set(root, lane_id="integrator", session="s1", paths=("org/",)):
    (root / "org").mkdir(parents=True, exist_ok=True)
    (root / "org" / "claims.json").write_text(json.dumps({
        "version": 1, "assigned": "2026-08-08",
        "lanes": [{"lane_id": lane_id, "task_id": "T-0001",
                   "session_id": session, "host": "h",
                   "harness_task_id": session,
                   "path_claims": list(paths),
                   "acquired": "2026-08-08T09:00:00Z",
                   "expires": "2026-08-15T09:00:00Z"}],
    }, indent=1), encoding="utf-8")


def _claim_record(task_id="T-0042"):
    return {
        "id": task_id,
        "intent": "A record written to test the claim control.",
        "declared": {"capabilities": [], "side_effects": []},
        "mode": "standard", "tier_proposed": "R1", "tier_ruled": "R1",
        "reasons": [], "status": "proposed", "owner_session": "s1",
        "claims": ["org/"],
        "timestamps": {"opened": "2026-08-08T09:00:00Z",
                       "updated": "2026-08-08T09:00:00Z"},
        "hypothesis_ledger": [],
    }


def test_create_task_refuses_an_unclaimed_session(repo_root):
    """AGENTS.md, TOUR.md and CLI_CONTRACTS.md all stated this control.
    create_task did no claim check at all."""
    root = repo_root
    _claim_set(root)
    with pytest.raises(taskops.ClaimRefused) as exc:
        taskops.create_task(root, _claim_record(), session="drive-by")
    assert exc.value.payload["refused"] is True
    assert "not named in the committed claim set" in exc.value.payload["reason"]
    assert exc.value.payload["claim_set_ref"] == "org/claims.json"
    assert not (root / "org" / "tasks" / "T-0042.json").exists()


def test_create_task_allows_the_claimed_session(repo_root):
    root = repo_root
    _claim_set(root)
    path = taskops.create_task(root, _claim_record(), session="s1")
    assert Path(path).is_file()


def test_create_task_refuses_a_lane_without_the_path(repo_root):
    """Being named is not enough; the claim has to cover the write."""
    root = repo_root
    _claim_set(root, paths=("packs/",))
    with pytest.raises(taskops.ClaimRefused) as exc:
        taskops.create_task(root, _claim_record(), session="s1")
    assert "holds no claim covering" in exc.value.payload["reason"]


def test_update_task_is_guarded_too(repo_root):
    root = repo_root
    _claim_set(root)
    taskops.create_task(root, _claim_record(), session="s1")
    with pytest.raises(taskops.ClaimRefused):
        taskops.update_task(root, "T-0042", {"status": "active"}, session="drive-by")


def test_no_claims_file_means_the_model_is_not_running(repo_root):
    """A repo with no claim set is not using assigned claims, and the
    control does not apply to it."""
    assert not (repo_root / "org" / "claims.json").exists()
    assert taskops.create_task(repo_root, _claim_record(), session="anyone")


def _empty_claim_set(root):
    (root / "org").mkdir(parents=True, exist_ok=True)
    (root / "org" / "claims.json").write_text(json.dumps(
        {"version": 1, "assigned": "2026-08-11", "lanes": []}, indent=1),
        encoding="utf-8")


def test_an_empty_lanes_list_is_not_a_claim_model(repo_root):
    """ADR-0008 decision 1: a claim is required only where more than one
    session may write at once, and a session working alone is implicitly
    claimed. The check keyed on the file existing rather than on it
    holding a lane, so it refused the lone operator, whose released
    claim set is committed empty rather than deleted. It would also have
    refused a venture's very first task new: check D009 requires a
    compiled ORG seed to ship org/claims.json with an empty lanes list.
    No session identity is supplied here, because a solo operator has
    none to supply."""
    root = repo_root
    _empty_claim_set(root)
    assert taskops.require_claim(
        root, root / "org" / "tasks" / "T-0042.json") is None
    assert Path(taskops.create_task(root, _claim_record(),
                                    session="solo")).is_file()


def test_a_populated_claim_set_still_refuses_an_unnamed_session(repo_root):
    """The other direction, and the one that matters. What releases the
    control is the integrator emptying the list, never a session reading
    it. With lanes present the refusal is unchanged, and being named is
    still not enough on its own."""
    root = repo_root
    _claim_set(root)
    record_path = root / "org" / "tasks" / "T-0042.json"
    with pytest.raises(taskops.ClaimRefused) as exc:
        taskops.require_claim(root, record_path, session="drive-by")
    assert "not named in the committed claim set" in exc.value.payload["reason"]
    lane = taskops.require_claim(root, record_path, session="s1")
    assert lane["lane_id"] == "integrator"
