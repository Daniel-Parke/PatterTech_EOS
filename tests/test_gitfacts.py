"""Tests for the read-only git helpers, against a real tmp repository."""

import re

import pytest

from conftest import git, make_git_repo
from tools.eos import gitfacts


def test_current_branch(tmp_path):
    root = make_git_repo(tmp_path)
    assert gitfacts.current_branch(root) == "main"


def test_current_branch_degrades_outside_a_repo(tmp_path):
    assert gitfacts.current_branch(tmp_path) is None


def test_remote_tracking_heads_skip_the_symbolic_head(tmp_path):
    root = make_git_repo(tmp_path)
    head = gitfacts.rev_parse(root, "HEAD")
    git(root, "update-ref", "refs/remotes/origin/main", head)
    git(root, "symbolic-ref", "refs/remotes/origin/HEAD",
        "refs/remotes/origin/main")
    heads = gitfacts.remote_tracking_heads(root)
    assert set(heads) == {"origin/main"}
    assert all(re.fullmatch(r"[0-9a-f]{40}", sha) for sha in heads.values())


def test_remote_tracking_heads_degrade(tmp_path):
    assert gitfacts.remote_tracking_heads(tmp_path) == {}


def test_output_returns_stdout(tmp_path):
    root = make_git_repo(tmp_path)
    assert gitfacts.output(root, "rev-parse", "--abbrev-ref", "HEAD").strip() \
        == "main"


def test_output_raises_where_the_fact_helpers_degrade(tmp_path):
    """The strict helper is strict on purpose.

    A base ref that does not resolve must stop the router and the
    context packet. Degraded to an empty diff it reads as a change with
    nothing in it, which routes a clean R0.
    """
    root = make_git_repo(tmp_path)
    assert gitfacts.rev_parse(root, "no-such-ref") is None
    with pytest.raises(RuntimeError) as excinfo:
        gitfacts.output(root, "rev-parse", "--verify", "no-such-ref")
    assert "git rev-parse" in str(excinfo.value)


def test_tags_peel_annotated(tmp_path):
    root = make_git_repo(tmp_path)
    git(root, "tag", "light")
    git(root, "tag", "-a", "v1.0.0", "-m", "release")
    head = gitfacts.rev_parse(root, "HEAD")
    tags = gitfacts.tags(root)
    assert tags == {"light": head, "v1.0.0": head}


def test_remote_heads_offline_is_none(tmp_path):
    root = make_git_repo(tmp_path)
    assert gitfacts.remote_heads(root, offline=True) is None


def test_remote_heads_no_remote_is_none(tmp_path):
    root = make_git_repo(tmp_path)
    assert gitfacts.remote_heads(root, offline=False) is None


def test_is_ancestor(tmp_path):
    root = make_git_repo(tmp_path)
    first = gitfacts.rev_parse(root, "HEAD")
    (root / "b.txt").write_text("two\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "second")
    second = gitfacts.rev_parse(root, "HEAD")
    assert gitfacts.is_ancestor(root, first, second) is True
    assert gitfacts.is_ancestor(root, second, first) is False


def test_commit_count(tmp_path):
    root = make_git_repo(tmp_path)
    git(root, "tag", "v0.1.0")
    (root / "b.txt").write_text("two\n", encoding="utf-8")
    git(root, "add", ".")
    git(root, "commit", "-q", "-m", "second")
    assert gitfacts.commit_count(root, "v0.1.0..HEAD") == 1
    assert gitfacts.commit_count(root, "HEAD..HEAD") == 0
    assert gitfacts.commit_count(root, "nonsense..HEAD") is None


def test_object_exists_and_ls_tree(tmp_path):
    root = make_git_repo(tmp_path)
    head = gitfacts.rev_parse(root, "HEAD")
    assert gitfacts.object_exists(root, f"{head}:a.txt") is True
    assert gitfacts.object_exists(root, f"{head}:missing.txt") is False
    assert gitfacts.ls_tree(root, "HEAD") == ["a.txt"]
    assert gitfacts.ls_tree(root, "no-such-ref") == []


def test_rev_parse(tmp_path):
    root = make_git_repo(tmp_path)
    assert re.fullmatch(r"[0-9a-f]{40}", gitfacts.rev_parse(root, "HEAD"))
    assert gitfacts.rev_parse(root, "no-such-ref") is None
