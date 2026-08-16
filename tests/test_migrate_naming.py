from __future__ import annotations

import hashlib
import json
from pathlib import Path, PurePosixPath

import pytest

from tools.eos.migrate_naming import (
    BASELINE_PATH,
    LEDGER_PATH,
    NamingMigrationError,
    _replace_text,
    _source_wargames,
    apply,
    check,
    expected_ledger,
    main,
    plan,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def _write(root: Path, relative: str, data: str | bytes) -> None:
    path = root.joinpath(*PurePosixPath(relative).parts)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data.encode("utf-8") if isinstance(data, str) else data)


def _tree(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def _fixture_repo(tmp_path: Path) -> tuple[Path, dict, bytes]:
    root = tmp_path / "repo"
    root.mkdir()
    baseline_bytes = (REPO_ROOT / BASELINE_PATH).read_bytes()
    baseline = json.loads(baseline_bytes)
    _write(root, BASELINE_PATH, baseline_bytes)

    inverse = {new: old for old, new in baseline["identifier_migration"].items()}
    sources = _source_wargames(baseline)
    for source, target in sources.items():
        target_id = PurePosixPath(target).name.split("-", 3)
        if target_id[0] == "WG":
            target_id = "-".join(target_id[:3])
        else:  # pragma: no cover - the frozen target contract rejects this shape
            raise AssertionError(target)
        source_id = inverse.get(target_id, target_id)
        _write(
            root,
            source,
            "---\n"
            f"id: {source_id}\n"
            "kind: wargame\n"
            "type: wargame\n"
            "---\n"
            f"# {source_id}\n\n"
            f"See [evidence](packs/agentic-development/refs/source.md).\n",
        )

    first_old = next(iter(baseline["identifier_migration"]))
    for identifier, row in baseline["relations"].items():
        document = {
            "id": identifier,
            "kind": "record",
            "type": "doctrine-relation",
            "covering_wargame": first_old,
        }
        _write(root, row["baseline_path"], json.dumps(document, indent=2) + "\n")

    for number in range(1, baseline["counts"]["doctrine_records"] + 1):
        identifier = f"DOC-TST-{number:03d}"
        _write(
            root,
            "packs/agentic-development/doctrines/"
            f"{identifier}-this-basename-breaks-midworddeliberately.md",
            "---\n"
            f"id: {identifier}\n"
            "kind: record\n"
            "type: doctrine\n"
            "statement: This basename ends only at a complete word boundary when shortened\n"
            "---\n"
            f"# {identifier}\n",
        )

    for number in range(1, baseline["counts"]["pack_exemplar_files"] + 1):
        _write(
            root,
            f"packs/agentic-development/exemplars/EX-{number:03d}.md",
            "---\nkind: exemplar\ntype: example\n---\n# Example\n",
        )
    binary_reference = b"\xff\x00unchanged\r\n"
    _write(root, "packs/agentic-development/refs/REF-001.bin", binary_reference)
    for number in range(2, baseline["counts"]["pack_reference_files"] + 1):
        _write(
            root,
            f"packs/agentic-development/refs/REF-{number:03d}.md",
            f"reference {number}\r\n".encode("utf-8"),
        )
    for number in range(1, baseline["counts"]["pack_research_files"] + 1):
        _write(
            root,
            f"packs/agentic-development/research/RES-{number:03d}.md",
            f"research {number}\n",
        )
    _write(
        root,
        "packs/agentic-development/research/RES-001.md",
        "Read PACK.md, guides/, refs/, exemplars/. "
        "Keep https://example.test/guides/topic, refs/heads/main and "
        "refs/notes/review unchanged.\n",
    )

    for slug in baseline["packs"]:
        _write(
            root,
            f"packs/{slug}/PACK.md",
            "---\nkind: record\ntype: guide\n---\n# Pack\n",
        )
        _write(
            root,
            f"packs/{slug}/CHECKS.md",
            "---\nkind: guide\ntype: guide\n---\n# Checks\n",
        )

    public_sources = baseline["public_file_migration"]
    for source in public_sources:
        _write(root, source, f"# {PurePosixPath(source).name}\n")
    _write(root, "packs/GUIDE_INDEX.md", "# Compatibility pointer\n")
    _write(root, "packs/WARGAME_INDEX.md", "# Canonical index\n")
    _write(root, ".venv/lib/tool.py", 'path = "guides/topic"\n')
    _write(
        root,
        "registry/identifier-aliases.json",
        json.dumps({"schema_version": 1, "aliases": {"B1": "DOC-TST-001"}}, indent=1)
        + "\n",
    )
    _write(
        root,
        "registry/lessons.json",
        json.dumps({"lessons": [{"disposition": "decision-guide"}]}, indent=2) + "\n",
    )
    _write(
        root,
        "kernel/schemas/lesson.schema.json",
        json.dumps({"enum": ["decision-guide", "deferred"]}, indent=2) + "\n",
    )
    current = (
        f"Use {first_old} and "
        "[the procedure](packs/agentic-development/guides/"
        f"{first_old}-topology-selection.md), plus `refs/source.md`.\n"
        f"A compound path also names archive/example/{first_old}-historical.md.\n"
    )
    _write(root, "docs/current.md", current)

    frozen = (
        f"Historical {first_old} at "
        f"packs/agentic-development/guides/{first_old}-topology-selection.md\n"
    ).encode("utf-8")
    for relative in (
        "archive/snapshot.md",
        "benchmark/snapshot.md",
        "org/decisions/ADR-0001-historical.md",
        "org/reports/HISTORICAL.md",
        "org/migration/WARGAME_MIGRATION.json",
        "tests/test_historical.py",
    ):
        _write(root, relative, frozen)
    return root, baseline, binary_reference


def test_checked_in_ledger_is_exactly_derived_from_frozen_baseline() -> None:
    baseline_file = REPO_ROOT / BASELINE_PATH
    baseline_bytes = baseline_file.read_bytes()
    baseline = json.loads(baseline_bytes)
    expected = expected_ledger(baseline, hashlib.sha256(baseline_bytes).hexdigest())
    actual = json.loads((REPO_ROOT / LEDGER_PATH).read_text(encoding="utf-8"))

    assert actual == expected
    assert len(actual["identity_migration"]) == 103
    assert actual["identity_migration"] == baseline["identifier_migration"]


def test_plan_apply_and_check_are_safe_exact_and_idempotent(tmp_path: Path) -> None:
    root, baseline, binary_reference = _fixture_repo(tmp_path)
    before_plan = _tree(root)

    reviewed = plan(root)

    assert _tree(root) == before_plan
    assert reviewed["contract"]["identity_mappings"] == 103
    assert reviewed["state"] == "pending"

    # A target collision is rejected while the tree remains byte-identical.
    first_source, first_target = next(iter(_source_wargames(baseline).items()))
    first_old = "-".join(PurePosixPath(first_source).name.split("-", 3)[:3])
    collision_path = root.joinpath(*PurePosixPath(first_target).parts)
    collision_path.parent.mkdir(parents=True, exist_ok=True)
    collision_path.write_bytes(b"collision\n")
    collided = _tree(root)
    with pytest.raises(NamingMigrationError, match="target collision"):
        plan(root)
    assert _tree(root) == collided
    collision_path.unlink()

    # A reviewed plan is invalidated by any intervening source change.
    current_path = root / "docs" / "current.md"
    current = current_path.read_bytes()
    reviewed = plan(root)
    current_path.write_bytes(current + b"changed after review\n")
    with pytest.raises(NamingMigrationError, match="no longer matches"):
        apply(root, reviewed)
    assert root.joinpath(*PurePosixPath(first_source).parts).is_file()
    current_path.write_bytes(current)

    assert main(["apply", "--repo", str(root)]) == 2
    reviewed = plan(root)
    result = apply(root, reviewed)

    assert result["state"] == "applied"
    assert not root.joinpath(*PurePosixPath(first_source).parts).exists()
    first_new = baseline["identifier_migration"][first_old]
    migrated = root.joinpath(*PurePosixPath(first_target).parts).read_text(
        encoding="utf-8"
    )
    assert f"id: {first_new}" in migrated
    assert first_source not in migrated
    assert f"{first_old}-historical.md" not in (
        root / "docs" / "current.md"
    ).read_text(encoding="utf-8")

    assert not (root / "packs" / "GUIDE_INDEX.md").exists()
    assert (root / "packs" / "PACK_CONTRACT.md").is_file()
    assert (root / "registry" / "IDENTIFIER_ALIASES.md").is_file()
    assert (
        root / "packs" / "agentic-development" / "references" / "REF-001.bin"
    ).read_bytes() == binary_reference

    pack_text = (root / "packs" / "agentic-development" / "PACK.md").read_text(
        encoding="utf-8"
    )
    assert "kind: record" in pack_text
    assert "type: pack" in pack_text
    assert "display_name: Agent Systems" in pack_text
    assert "category: data-ai" in pack_text
    assert "id_namespace: AGENT" in pack_text
    example_text = (
        root / "packs" / "agentic-development" / "examples" / "EX-001.md"
    ).read_text(encoding="utf-8")
    assert "kind: example" in example_text
    assert "type: example" in example_text
    research_text = (
        root / "packs" / "agentic-development" / "research" / "RES-001.md"
    ).read_text(encoding="utf-8")
    assert "wargames/, references/, examples/" in research_text
    assert "https://example.test/guides/topic" in research_text
    assert "refs/heads/main" in research_text
    assert "refs/notes/review" in research_text
    assert (root / ".venv" / "lib" / "tool.py").read_text(encoding="utf-8") == (
        'path = "guides/topic"\n'
    )

    aliases = json.loads(
        (root / "registry" / "identifier-aliases.json").read_text(encoding="utf-8")
    )["aliases"]
    assert {old: aliases[old] for old in baseline["identifier_migration"]} == baseline[
        "identifier_migration"
    ]
    assert (
        json.loads((root / "registry" / "lessons.json").read_text(encoding="utf-8"))[
            "lessons"
        ][0]["disposition"]
        == "wargame"
    )

    for relative in (
        "archive/snapshot.md",
        "benchmark/snapshot.md",
        "org/decisions/ADR-0001-historical.md",
        "org/reports/HISTORICAL.md",
        "org/migration/WARGAME_MIGRATION.json",
        "tests/test_historical.py",
    ):
        assert first_source.split("/", 3)[2] in root.joinpath(
            *PurePosixPath(relative).parts
        ).read_text(encoding="utf-8")

    doctrine_paths = list(
        (root / "packs" / "agentic-development" / "doctrines").glob("*.md")
    )
    assert len(doctrine_paths) == baseline["counts"]["doctrine_records"]
    assert all(
        len(path.stem) <= baseline["doctrine_basename_max"] for path in doctrine_paths
    )
    assert not any(
        (root / "packs" / slug / "guides").exists() for slug in baseline["packs"]
    )
    assert not any(
        (root / "packs" / slug / "exemplars").exists() for slug in baseline["packs"]
    )
    assert not any(
        (root / "packs" / slug / "refs").exists() for slug in baseline["packs"]
    )

    assert check(root) == []
    assert plan(root)["state"] == "fixpoint"
    assert apply(root) == {"state": "fixpoint", "moves": 0, "rewrites": 0, "deletes": 0}


def test_path_escape_is_rejected_before_mutation(tmp_path: Path) -> None:
    root, _, _ = _fixture_repo(tmp_path)
    baseline_path = root / BASELINE_PATH
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    first = next(iter(baseline["target_wargames"]))
    baseline["target_wargames"][first] = "../outside.md"
    baseline_path.write_text(json.dumps(baseline, indent=2) + "\n", encoding="utf-8")
    before = _tree(root)

    with pytest.raises(NamingMigrationError, match="escapes the repository"):
        plan(root)

    assert _tree(root) == before
    assert not (tmp_path / "outside.md").exists()


def test_current_repository_contract_can_be_planned_without_writing() -> None:
    before = {
        path: (REPO_ROOT / path).read_bytes() for path in (BASELINE_PATH, LEDGER_PATH)
    }

    current = plan(REPO_ROOT)

    assert current["contract"]["identity_mappings"] == 103
    assert current["state"] in {"pending", "fixpoint"}
    assert {path: (REPO_ROOT / path).read_bytes() for path in before} == before


def test_reviewed_live_prose_uses_entity_names_without_touching_source_titles() -> None:
    baseline = json.loads((REPO_ROOT / BASELINE_PATH).read_text(encoding="utf-8"))
    source = (
        b'"method": "(PACK.md, CHECKS.md, guides, refs, exemplars)", '
        b'"source": "An external style guide"\n'
    )

    rendered, labels = _replace_text(
        source,
        "packs/agentic-development/research/provenance.fragment.json",
        baseline,
        {},
    )

    assert b"PACK.md, CHECKS.md, Wargames, references, examples" in rendered
    assert b"An external style guide" in rendered
    assert "reviewed live prose" in labels
