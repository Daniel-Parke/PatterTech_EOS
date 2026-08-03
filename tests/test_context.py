"""Context packet tests: changed surface, summaries, references, routing."""

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools.eos import contextgen  # noqa: E402


def _git(root, *args):
    subprocess.run(["git", "-C", str(root), *args], check=True,
                   capture_output=True, text=True)


@pytest.fixture
def git_repo(tmp_path):
    root = tmp_path / "repo"
    (root / "docs").mkdir(parents=True)
    _git(root, "init", "-b", "main")
    _git(root, "config", "user.email", "test@example.invalid")
    _git(root, "config", "user.name", "Test")
    (root / "docs" / "guide.md").write_text(
        "---\nsummary: How the widget works\nkind: guide\n---\n\n# Guide\n",
        encoding="utf-8")
    (root / "docs" / "index.md").write_text(
        "# Index\n\nSee docs/guide.md for the widget guide.\n",
        encoding="utf-8")
    (root / "docs" / "unrelated.md").write_text(
        "# Unrelated\n\nNothing to see.\n", encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-m", "base")
    (root / "docs" / "guide.md").write_text(
        "---\nsummary: How the widget works\nkind: guide\n---\n\n# Guide\n\nMore.\n",
        encoding="utf-8")
    _git(root, "add", "-A")
    _git(root, "commit", "-m", "edit guide")
    return root


def test_packet_shape_and_changed_set(git_repo):
    packet = contextgen.build_packet(git_repo, base_ref="HEAD~1")
    assert set(packet) == {"changed", "summaries", "referencing_files",
                           "activated_packs", "routed"}
    assert packet["changed"] == ["docs/guide.md"]
    assert packet["activated_packs"] == []


def test_front_matter_summaries(git_repo):
    packet = contextgen.build_packet(git_repo, base_ref="HEAD~1")
    assert packet["summaries"]["docs/guide.md"] == "How the widget works"


def test_reverse_reference_scan(git_repo):
    packet = contextgen.build_packet(git_repo, base_ref="HEAD~1")
    refs = packet["referencing_files"].get("docs/guide.md", [])
    assert "docs/index.md" in refs
    assert "docs/unrelated.md" not in refs


def test_routed_tier_present(git_repo):
    packet = contextgen.build_packet(git_repo, base_ref="HEAD~1")
    assert packet["routed"]["tier"] in ("R0", "R1", "R2", "R3")
    assert isinstance(packet["routed"]["reasons"], list)


def test_explicit_files_mode_needs_no_git(tmp_path):
    root = tmp_path / "plain"
    root.mkdir()
    (root / "a.md").write_text(
        "---\nsummary: A file\nkind: record\n---\n", encoding="utf-8")
    (root / "b.md").write_text("mentions a.md here\n", encoding="utf-8")
    packet = contextgen.build_packet(root, files=["a.md"])
    assert packet["changed"] == ["a.md"]
    assert packet["summaries"]["a.md"] == "A file"
    assert "b.md" in packet["referencing_files"].get("a.md", [])
    assert packet["routed"]["tier"] == "R0"


def test_deleted_and_missing_files_are_marked(tmp_path):
    root = tmp_path / "plain"
    root.mkdir()
    packet = contextgen.build_packet(root, files=["gone.md"])
    assert packet["summaries"]["gone.md"] == "(deleted)"


def test_no_front_matter_is_named_not_invented(tmp_path):
    root = tmp_path / "plain"
    root.mkdir()
    (root / "plain.md").write_text("# Plain\n", encoding="utf-8")
    packet = contextgen.build_packet(root, files=["plain.md"])
    assert packet["summaries"]["plain.md"] == "(no front matter)"
