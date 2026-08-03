"""Benchcli tests: subprocess pass-through, no reimplementation, drills stub."""

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools.eos import benchcli  # noqa: E402

# A stand-in script that records exactly what it was invoked with, so
# the pass-through contract is observable without ever running the
# frozen suite inside a test.
_ECHO_SCRIPT = (
    "import json, sys\n"
    "print(json.dumps({'argv': sys.argv[1:]}))\n"
    "sys.exit(0)\n"
)

_FAIL_SCRIPT = (
    "import sys\n"
    "sys.stderr.write('criterion failed\\n')\n"
    "sys.exit(1)\n"
)


@pytest.fixture
def bench_root(tmp_path):
    root = tmp_path / "repo"
    (root / "benchmark").mkdir(parents=True)
    (root / "benchmark" / "runner.py").write_text(_ECHO_SCRIPT, encoding="utf-8")
    (root / "benchmark" / "score.py").write_text(_ECHO_SCRIPT, encoding="utf-8")
    return root


def test_runner_passes_args_through_verbatim(bench_root):
    proc = benchcli.runner(
        bench_root, ["run", "--task", "tasks/T1", "--variant", "v2"])
    assert proc.returncode == 0
    argv = json.loads(proc.stdout)["argv"]
    assert argv == ["run", "--task", "tasks/T1", "--variant", "v2"]


def test_score_passes_args_through_verbatim(bench_root):
    proc = benchcli.score(
        bench_root,
        ["--task", "tasks/T1", "--scratch", "s", "--transcript", "t.md",
         "--variant", "v1", "--run-id", "run-7"])
    assert proc.returncode == 0
    argv = json.loads(proc.stdout)["argv"]
    assert argv[-2:] == ["--run-id", "run-7"]
    assert "--transcript" in argv


def test_wrapper_surfaces_the_scripts_exit_code(bench_root):
    (bench_root / "benchmark" / "score.py").write_text(
        _FAIL_SCRIPT, encoding="utf-8")
    proc = benchcli.score(bench_root, ["--task", "tasks/T1"])
    assert proc.returncode == 1
    assert "criterion failed" in proc.stderr


def test_missing_frozen_script_raises(tmp_path):
    root = tmp_path / "empty"
    (root / "benchmark").mkdir(parents=True)
    with pytest.raises(FileNotFoundError):
        benchcli.runner(root, ["run"])


def test_benchcli_never_imports_the_frozen_suite():
    # Contract: subprocess only. The module must not import or exec the
    # frozen runner or scorer, in any form.
    source = (REPO / "tools" / "eos" / "benchcli.py").read_text(encoding="utf-8")
    assert "import runner" not in source
    assert "import score" not in source
    assert "from benchmark" not in source
    assert "importlib" not in source
    assert "exec(" not in source


def test_real_frozen_scripts_are_present_and_untouched_by_this_lane():
    # The wrappers point at benchmark/runner.py and benchmark/score.py;
    # both must exist in the real repo for the CLI to be wireable.
    assert (REPO / "benchmark" / "runner.py").is_file()
    assert (REPO / "benchmark" / "score.py").is_file()


# The drills command is no longer a stub. Its behaviour is covered in
# tests/test_drills.py; these two only hold the wiring contract that the
# CLI depends on.
def test_drills_list_reads_the_frozen_manifest():
    payload, code = benchcli.drills(REPO, "list")
    assert code == 0
    assert payload["count"] == len(payload["drills"])
    assert payload["drills"][0]["sha256"]


def test_drills_rejects_unknown_action():
    with pytest.raises(ValueError):
        benchcli.drills(REPO, "frobnicate")
