"""Taskops tests: record ops, atomic writes, assigned-claims verification."""

import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

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
    assert findings.exit_code() == 1
    assert len(findings.errors) == 1
    assert "refused" in findings.errors[0].message


def test_diff_inside_claims_is_clean(tmp_path):
    findings = taskops.verify_claims(
        tmp_path, _claims_doc(), "lane/t2",
        ["tools/eos/router.py", "tests/test_router.py"], now=NOW)
    assert findings.exit_code() == 0
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
    assert findings.exit_code() == 1
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
    assert findings.exit_code() == 1
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
    assert findings.exit_code() == 1
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
    assert findings.exit_code() == 1
    assert "pip install" in findings.errors[0].message
