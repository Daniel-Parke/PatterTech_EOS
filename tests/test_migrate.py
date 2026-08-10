"""Migrate tests: read-only planning, fixture-only apply transforms."""

import json
import shutil
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools.eos import migrate  # noqa: E402


def _copy_seed(name, tmp_path):
    src = REPO / "benchmark" / "fixtures" / name
    dest = tmp_path / name
    shutil.copytree(src, dest)
    # Task records need the schema reachable from the seed root.
    (dest / "kernel" / "schemas").mkdir(parents=True)
    shutil.copy(REPO / "kernel" / "schemas" / "task-record.schema.json",
                dest / "kernel" / "schemas" / "task-record.schema.json")
    return dest


def _snapshot(root):
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


def test_plan_reads_scale_and_pin_from_lockbook(tmp_path):
    seed = _copy_seed("seed-v1-M", tmp_path)
    plan = migrate.plan(seed)
    assert plan["venture"] == "FieldKit"
    assert plan["pin_current"] == "1.0.0@6590a82"
    assert plan["route"] == "apply"
    step_ids = [s["id"] for s in plan["steps"]]
    assert "pin-policy" in step_ids
    assert "roles-to-tier-note" in step_ids
    assert "queue-to-tasks" in step_ids
    assert "worklog-note" not in step_ids  # M logs per session, no WORKLOG


def test_plan_validates_against_migration_state_schema(tmp_path):
    jsonschema = pytest.importorskip("jsonschema")
    seed = _copy_seed("seed-v1-M", tmp_path)
    plan = migrate.plan(seed)
    schema = json.loads(
        (REPO / "kernel" / "schemas" / "migration-state.schema.json")
        .read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(plan)


def test_plan_is_read_only(tmp_path):
    seed = _copy_seed("seed-v1-S", tmp_path)
    before = _snapshot(seed)
    migrate.plan(seed)
    assert _snapshot(seed) == before


def test_plan_without_lockbook_routes_fresh_inception(tmp_path):
    bare = tmp_path / "bare"
    bare.mkdir()
    plan = migrate.plan(bare)
    assert plan["route"] == "fresh-inception"


def test_plan_prev_kernel_pin_routes_recompile(tmp_path):
    seed = _copy_seed("seed-v1-S", tmp_path)
    lockbook = seed / "docs" / "LOCKBOOK.md"
    text = lockbook.read_text(encoding="utf-8").replace(
        "eos_version: 1.0.0", "eos_version: 0.9.0")
    lockbook.write_text(text, encoding="utf-8")
    assert migrate.plan(seed)["route"] == "recompile"


def test_apply_dry_run_by_default_writes_nothing(tmp_path):
    seed = _copy_seed("seed-v1-M", tmp_path)
    plan = migrate.plan(seed)
    before = _snapshot(seed)
    result = migrate.apply(seed, plan)
    assert result["dry_run"] is True
    assert result["changes"]
    assert _snapshot(seed) == before
    assert all(s["status"] == "pending" for s in result["state"]["steps"])


def test_apply_transforms_fixture_seed(tmp_path):
    seed = _copy_seed("seed-v1-M", tmp_path)
    logs_before = _snapshot(seed / "org" / "logs")
    plan = migrate.plan(seed)
    result = migrate.apply(seed, plan, dry_run=False, today="2026-08-03")

    # Lock-book header gains the policy pin.
    lockbook = (seed / "docs" / "LOCKBOOK.md").read_text(encoding="utf-8")
    header = lockbook.split("\n---", 2)[0]
    assert "policy_pin:" in header

    # Role charters swap for the tier policy note.
    for name in ("PLAN.md", "WORK.md", "VERIFY.md"):
        text = (seed / "org" / "roles" / name).read_text(encoding="utf-8")
        assert "superseded" in text
        assert "POLICY_SPEC" in text

    # Queue rows became schema-valid task records.
    task = seed / "org" / "tasks" / "T-0001.json"
    assert task.is_file()
    record = json.loads(task.read_text(encoding="utf-8"))
    assert "WO-0001" in record["intent"]
    assert record["status"] == "proposed"

    # org/logs untouched.
    assert _snapshot(seed / "org" / "logs") == logs_before

    done = {s["id"] for s in result["state"]["steps"] if s["status"] == "done"}
    assert {"pin-policy", "roles-to-tier-note", "queue-to-tasks"} <= done


def test_apply_appends_worklog_note_at_s_scale(tmp_path):
    seed = _copy_seed("seed-v1-S", tmp_path)
    plan = migrate.plan(seed)
    migrate.apply(seed, plan, dry_run=False, today="2026-08-03")
    worklog = (seed / "docs" / "WORKLOG.md").read_text(encoding="utf-8")
    assert "migrated to EOS v2" in worklog


def test_apply_is_idempotent_on_the_pin(tmp_path):
    seed = _copy_seed("seed-v1-S", tmp_path)
    plan = migrate.plan(seed)
    migrate.apply(seed, plan, dry_run=False, today="2026-08-03")
    lockbook = (seed / "docs" / "LOCKBOOK.md").read_text(encoding="utf-8")
    result = migrate.apply(seed, plan, dry_run=False, today="2026-08-03")
    lockbook_after = (seed / "docs" / "LOCKBOOK.md").read_text(encoding="utf-8")
    assert lockbook.count("policy_pin:") == 1
    assert lockbook_after.count("policy_pin:") == 1
    assert not any("policy_pin" in c for c in result["changes"])


def test_apply_refuses_a_git_repository(tmp_path):
    trap = tmp_path / "sibling"
    (trap / ".git").mkdir(parents=True)
    with pytest.raises(ValueError):
        migrate.apply(trap, {"steps": []}, dry_run=False)


def test_v1_matrix_matches_scale_counts():
    # SCALE_MATRIX.md: S is eight files, M about eighteen with the
    # queue, L swaps the queue for the work-order system.
    s_files = [p for p, scales in migrate.V1_MATRIX.items() if "S" in scales]
    m_files = [p for p, scales in migrate.V1_MATRIX.items() if "M" in scales]
    l_files = [p for p, scales in migrate.V1_MATRIX.items() if "L" in scales]
    assert len(s_files) == 8
    assert "org/QUEUE.md" in m_files and "org/QUEUE.md" not in l_files
    assert "org/work/NEXT.md" in l_files and "org/work/NEXT.md" not in m_files
    assert "docs/WORKLOG.md" not in m_files
