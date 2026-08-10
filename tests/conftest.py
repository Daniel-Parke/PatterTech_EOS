"""Shared test helpers for the EOS tooling suite.

make_repo builds the minimal green fixture repo from tests/fixtures/
minirepo into tmp_path; make_seed copies a frozen v1 seed fixture;
make_git_repo builds a small real git repository. Tests mutate the
copies, never the sources, and every date-sensitive check receives an
injected today.

The minirepo sources are stored with a .mdt extension so the real
repository's checkers and derived indexes never see them; make_repo
renames them to .md while copying. The pytest cache plugin is blocked
for the same reason: .pytest_cache/README.md at the repo root would be
a v1-checker finding.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MINIREPO = Path(__file__).resolve().parent / "fixtures" / "minirepo"

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def pytest_configure(config):
    pm = config.pluginmanager
    for name in ("cacheprovider", "lfplugin", "lfplugin-collwrapper",
                 "nfplugin", "stepwiseplugin"):
        plugin = pm.get_plugin(name)
        if plugin is not None:
            pm.unregister(plugin)
    pm.set_blocked("cacheprovider")


def make_repo(tmp_path) -> Path:
    """Build the minimal green fixture repo in tmp_path and return it."""
    dst = Path(tmp_path) / "minirepo"
    shutil.copytree(MINIREPO, dst)
    for p in sorted(dst.rglob("*.mdt")):
        p.rename(p.with_suffix(".md"))
    return dst


def make_seed(tmp_path, scale: str) -> Path:
    """Copy the frozen v1 seed fixture for a scale into tmp_path."""
    src = REPO_ROOT / "benchmark" / "fixtures" / f"seed-v1-{scale}"
    dst = Path(tmp_path) / f"seed-{scale}"
    shutil.copytree(src, dst)
    return dst


def git(root, *args: str) -> str:
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    return proc.stdout


def make_git_repo(tmp_path) -> Path:
    """A real git repository with one committed file on branch main."""
    root = Path(tmp_path) / "gitrepo"
    root.mkdir()
    git(root, "init", "-q", "-b", "main")
    git(root, "config", "user.email", "suite@example.invalid")
    git(root, "config", "user.name", "Test Suite")
    git(root, "config", "commit.gpgsign", "false")
    (root / "a.txt").write_text("one\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "first")
    return root
