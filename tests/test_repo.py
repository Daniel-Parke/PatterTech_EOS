"""Tests for RepoModel loading, skip rules and content hashing."""

from datetime import date

from conftest import make_repo
from tools.eos.repo import RepoModel, content_sha256

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
    assert "packs/testmod/wargames/WG-TST-001-sample.md" in paths
    # traversal order is deterministic: a reload sees the same order
    assert paths == [f.path for f in RepoModel.load(root, today=TODAY).files]


def test_paths_are_posix_relative(tmp_path):
    root = make_repo(tmp_path)
    model = RepoModel.load(root, today=TODAY)
    for f in model.files:
        assert "\\" not in f.path
        assert not f.path.startswith("/")


def test_file_order_is_the_same_on_every_platform(tmp_path):
    """Records come back in POSIX byte order, not the platform's order.

    Path comparison is case-insensitive on Windows and case-sensitive on
    POSIX, so sorting Path objects put UPPER.md before lower/ on Linux
    and after it on Windows. Every derived index is written in this
    order, so one tree produced an INDEX.md that was clean on the
    machine that generated it and stale on the machine that checked it.
    """
    root = make_repo(tmp_path)
    (root / "packs").mkdir(parents=True, exist_ok=True)
    (root / "packs" / "INDEX.md").write_text(
        "---\nsummary: s\ntype: index\ntags: [eos]\n---\n", encoding="utf-8")
    (root / "packs" / "agentic-swarm").mkdir(parents=True, exist_ok=True)
    (root / "packs" / "agentic-swarm" / "PACK.md").write_text(
        "---\nsummary: s\nkind: record\ntype: pack\ntags: [eos]\n"
        "display_name: Agentic Swarm\ncategory: engineering\n"
        "id_namespace: AGENT\n---\n", encoding="utf-8")
    paths = [f.path for f in RepoModel.load(root, today=TODAY).files]
    assert paths == sorted(paths), "records must come back in POSIX byte order"
    assert paths.index("packs/INDEX.md") < paths.index(
        "packs/agentic-swarm/PACK.md")


def test_benchmark_files_are_loaded_not_skipped(tmp_path):
    """Fixtures and holdouts are read: the E-series still judges them.

    Only the drill scenarios and the benchmark surfaces are read past,
    and for reasons repo.py states. Which of the loaded files a check
    then judges is the check's own exemption list.
    """
    root = make_repo(tmp_path)
    _write(root, "benchmark/fixtures/seedling/NOTE.md")
    _write(root, "benchmark/holdout/secret/NOTE.md")
    _write(root, "benchmark/drills/scenarios/toy/README.md")
    _write(root, "benchmark/surfaces/v2/AGENTS.md")
    model = RepoModel.load(root, today=TODAY)
    paths = {f.path for f in model.files}
    assert "benchmark/fixtures/seedling/NOTE.md" in paths
    assert "benchmark/holdout/secret/NOTE.md" in paths
    assert "benchmark/drills/scenarios/toy/README.md" not in paths
    assert "benchmark/surfaces/v2/AGENTS.md" not in paths


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


# --- content_sha256: a checkout must not read as a modification --------


def test_content_sha256_ignores_the_checkout_line_ending(tmp_path):
    """CRLF and LF spellings of one text file hash the same.

    core.autocrlf=true, the Windows default, rewrites LF to CRLF on
    checkout. Hashing raw bytes made every frozen text file report as
    an unrecorded change on a tree where nothing had been edited.
    """
    lf = tmp_path / "lf.py"
    crlf = tmp_path / "crlf.py"
    lf.write_bytes(b"def f():\n    return 1\n")
    crlf.write_bytes(b"def f():\r\n    return 1\r\n")
    assert content_sha256(lf) == content_sha256(crlf)


def test_content_sha256_still_sees_a_real_edit(tmp_path):
    """Normalising newlines must not blind the hash to content."""
    a, b = tmp_path / "a.py", tmp_path / "b.py"
    a.write_bytes(b"return 1\n")
    b.write_bytes(b"return 2\n")
    assert content_sha256(a) != content_sha256(b)


def test_content_sha256_leaves_binary_alone(tmp_path):
    """A NUL means binary: CRLF in it is data, not a line ending."""
    p, q = tmp_path / "p.bin", tmp_path / "q.bin"
    p.write_bytes(b"\x00\r\nx")
    q.write_bytes(b"\x00\nx")
    assert content_sha256(p) != content_sha256(q)


def test_freeze_manifest_records_content_hashes():
    """Every recorded hash is the LF form, so the set is one convention.

    Twenty-one entries were once recorded from a CRLF working tree,
    which is invisible until someone checks out on the other platform.
    """
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parent.parent
    doc = json.loads((root / "benchmark" / "FREEZE_MANIFEST.json")
                     .read_text(encoding="utf-8"))
    wrong = []
    for key, want in doc["files"].items():
        path = root / key.replace("\\", "/")
        if path.is_file() and content_sha256(path) != want:
            wrong.append(key)
    assert wrong == []
