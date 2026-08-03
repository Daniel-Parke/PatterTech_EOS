"""Tests for RepoModel loading, fixture flags and skip rules."""

from datetime import date

from conftest import make_repo
from tools.eos.repo import RepoModel

TODAY = date(2026, 8, 3)


def _write(root, rel, text="---\nsummary: X\ntype: org\ntags: [eos]\n---\nBody.\n"):
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def test_loads_minirepo_files(tmp_path):
    root = make_repo(tmp_path)
    model = RepoModel.load(root, today=TODAY)
    paths = [f.path for f in model.files]
    assert "AGENTS.md" in paths
    assert "packs/testmod/guides/WG-TST-001-sample.md" in paths
    # traversal order is deterministic: a reload sees the same order
    assert paths == [f.path for f in RepoModel.load(root, today=TODAY).files]


def test_paths_are_posix_relative(tmp_path):
    root = make_repo(tmp_path)
    model = RepoModel.load(root, today=TODAY)
    for f in model.files:
        assert "\\" not in f.path
        assert not f.path.startswith("/")


def test_fixture_flag_for_benchmark_paths(tmp_path):
    root = make_repo(tmp_path)
    _write(root, "benchmark/fixtures/seedling/NOTE.md")
    _write(root, "benchmark/holdout/secret/NOTE.md")
    _write(root, "benchmark/tasks/NOTE.md")
    model = RepoModel.load(root, today=TODAY)
    flags = {f.path: f.fixture for f in model.files}
    assert flags["benchmark/fixtures/seedling/NOTE.md"] is True
    assert flags["benchmark/holdout/secret/NOTE.md"] is True
    assert flags["benchmark/tasks/NOTE.md"] is False
    assert flags["AGENTS.md"] is False


def test_skip_dirs(tmp_path):
    root = make_repo(tmp_path)
    _write(root, ".git/objects/NOTE.md")
    _write(root, "__pycache__/NOTE.md")
    _write(root, ".pytest_cache/NOTE.md")
    _write(root, "node_modules/pkg/NOTE.md")
    model = RepoModel.load(root, today=TODAY)
    paths = {f.path for f in model.files}
    assert not any(".git" in p or "__pycache__" in p or ".pytest_cache" in p
                   or "node_modules" in p for p in paths)


def test_record_fields(tmp_path):
    root = make_repo(tmp_path)
    model = RepoModel.load(root, today=TODAY)
    rec = model.get("org/STATE.md")
    assert rec is not None
    assert rec.fm.present is True
    assert rec.fm.data["type"] == "org"
    assert rec.lines == len(rec.text.splitlines())


def test_get_read_exists(tmp_path):
    root = make_repo(tmp_path)
    model = RepoModel.load(root, today=TODAY)
    assert model.get("nope/MISSING.md") is None
    assert model.read("nope/MISSING.md") is None
    assert model.exists("GOVERNANCE.md") is True
    assert model.exists("nope") is False
    assert "Tag vocabulary" in model.read("GOVERNANCE.md")


def test_today_injected(tmp_path):
    root = make_repo(tmp_path)
    model = RepoModel.load(root, today=TODAY)
    assert model.today == TODAY
