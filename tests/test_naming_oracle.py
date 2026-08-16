"""Independent acceptance oracle for the T-0028 naming migration.

The baseline test proves the supplied inventory against the immutable pre-task
commit. The remaining tests describe the target and are expected to be red
until the implementation lands. This file does not use migration helpers.
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import re
import subprocess
from collections import Counter
from functools import lru_cache
from pathlib import Path, PurePosixPath

from tools.eos.frontmatter import parse as parse_frontmatter
from tools.eos.ontology import KnowledgeResolver


REPO = Path(__file__).resolve().parents[1]
BASELINE_PATH = REPO / "org/migration/NAMING_BASELINE.json"
WG_ID = re.compile(r"^WG-[A-Z0-9]+-\d{3}$")
ANY_WARGAME_ID = re.compile(r"^(?:GD|WG)-[A-Z0-9]+-\d{3}$")
DEFINITION_ID = re.compile(r"((?:DOC|DREL|GD|WG)-[A-Z0-9]+-\d{3})")
IGNORED_WORKTREE_PARTS = {".git", ".pytest_cache", "__pycache__", ".venv"}


def _load_baseline() -> dict:
    return json.loads(BASELINE_PATH.read_text(encoding="utf-8"))


def _git(*args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(REPO), *args],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert result.returncode == 0, result.stderr or result.stdout
    return result.stdout


def _tree_paths(commit: str) -> tuple[str, ...]:
    return tuple(sorted(_git("ls-tree", "-r", "--name-only", commit).splitlines()))


def _tree_text(commit: str, path: str) -> str:
    return _git("show", f"{commit}:{path}")


def _worktree_paths() -> tuple[str, ...]:
    rows = []
    for path in REPO.rglob("*"):
        if not path.is_file() or IGNORED_WORKTREE_PARTS.intersection(path.parts):
            continue
        rows.append(path.relative_to(REPO).as_posix())
    return tuple(sorted(rows))


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _id_from_path(path: str) -> str:
    match = DEFINITION_ID.search(PurePosixPath(path).name)
    assert match, f"definition path has no identity: {path}"
    return match.group(1)


def _baseline_wargames(commit: str, paths: tuple[str, ...]) -> dict[str, str]:
    rows = {}
    for path in paths:
        is_pack = re.fullmatch(r"packs/[^/]+/guides/(?:GD|WG)-[^/]+\.md", path)
        is_inception = re.fullmatch(r"inception/wargames/WG-[^/]+\.md", path)
        if is_pack or is_inception:
            identifier = _id_from_path(path)
            assert identifier not in rows, f"duplicate baseline Wargame {identifier}"
            parsed = parse_frontmatter(_tree_text(commit, path))
            assert parsed.data.get("id") == identifier
            rows[identifier] = path
    return rows


def _baseline_relations(commit: str, paths: tuple[str, ...]) -> dict[str, str]:
    rows = {}
    for path in paths:
        if not re.fullmatch(
            r"packs/[^/]+/doctrines/relations/DREL-[^/]+\.json", path
        ):
            continue
        record = json.loads(_tree_text(commit, path))
        identifier = str(record.get("id") or _id_from_path(path))
        assert identifier == _id_from_path(path)
        assert identifier not in rows, f"duplicate baseline relation {identifier}"
        rows[identifier] = path
    return rows


def _row_hash(kind: str, rows: dict[str, str]) -> str:
    if kind:
        text = "".join(
            f"{kind}\t{identifier}\t{path}\n"
            for identifier, path in sorted(rows.items())
        )
    else:
        text = "".join(
            f"{identifier}\t{path}\n" for identifier, path in sorted(rows.items())
        )
    return _sha256(text)


def _metadata_counts(commit: str, paths: tuple[str, ...], pattern: str) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for path in paths:
        if not re.fullmatch(pattern, path):
            continue
        data = parse_frontmatter(_tree_text(commit, path)).data
        counts[f"{data.get('kind')}|{data.get('type')}"] += 1
    return dict(sorted(counts.items()))


def _frontmatter(path: Path) -> dict:
    parsed = parse_frontmatter(path.read_text(encoding="utf-8"))
    assert parsed.present, f"missing front matter: {path.relative_to(REPO)}"
    assert not parsed.errors, f"bad front matter in {path.relative_to(REPO)}: {parsed.errors}"
    return dict(parsed.data)


@lru_cache(maxsize=1)
def _source_to_target_paths() -> dict[str, str]:
    baseline = _load_baseline()
    resolver = KnowledgeResolver.open(REPO, baseline["frozen_from"]["commit"])
    migration = baseline["identifier_migration"]
    targets = baseline["target_wargames"]
    result = {}
    for row in resolver.list("wargame"):
        target_id = migration.get(row.canonical_id, row.canonical_id)
        result[row.path] = targets[target_id]
    return result


def _normalise_naming_text(text: str, baseline: dict) -> str:
    text = text.replace("\r\n", "\n")
    for old, new in sorted(
        _source_to_target_paths().items(), key=lambda item: -len(item[0])
    ):
        text = text.replace(old, new)
    for old, new in sorted(
        baseline["identifier_migration"].items(), key=lambda item: -len(item[0])
    ):
        text = re.sub(rf"\b{re.escape(old)}\b", new, text)
    replacements = {
        "/guides/": "/wargames/",
        "/exemplars/": "/examples/",
        "/refs/": "/references/",
        "/doctrines/relations/": "/relations/",
        "PACK_SHAPE.md": "PACK_CONTRACT.md",
        "ID_ALIASES.md": "IDENTIFIER_ALIASES.md",
        "GUIDE_INDEX.md": "WARGAME_INDEX.md",
        "decision-guide": "wargame",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    text = re.sub(r"\bguides\b", "wargames", text, flags=re.IGNORECASE)
    text = re.sub(r"\bguide\b", "wargame", text, flags=re.IGNORECASE)
    text = re.sub(r"\bexemplars\b", "examples", text, flags=re.IGNORECASE)
    text = re.sub(r"\bexemplar\b", "example", text, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", text).strip().casefold()


def _normalise_json(value, baseline: dict):
    if isinstance(value, dict):
        return {key: _normalise_json(item, baseline) for key, item in value.items()}
    if isinstance(value, list):
        return [_normalise_json(item, baseline) for item in value]
    if isinstance(value, str):
        return _normalise_naming_text(value, baseline)
    return value


def test_naming_baseline_matches_frozen_commit() -> None:
    baseline = _load_baseline()
    commit = baseline["frozen_from"]["commit"]
    assert _git("rev-parse", f"{commit}^{{commit}}").strip() == commit
    assert baseline["frozen_from"]["claims_commit"] == (
        "ca1a2d2e86bc98f1810bf68a6889eef37b5cadc0"
    )

    paths = _tree_paths(commit)
    wargames = _baseline_wargames(commit, paths)
    relations = _baseline_relations(commit, paths)
    counts = baseline["counts"]
    assert len(paths) == counts["tracked_files"] == 1985
    assert len(wargames) == counts["wargames"] == 127
    assert sum(identifier.startswith("GD-") for identifier in wargames) == 100
    assert sum(identifier.startswith("WG-") for identifier in wargames) == 27
    assert len(relations) == counts["relations"] == 19
    assert sum(re.fullmatch(r"packs/[^/]+/doctrines/DOC-[^/]+\.md", p) is not None for p in paths) == 516

    hashes = baseline["current_path_id_hashes"]
    assert _row_hash("", wargames) == hashes["wargames"]
    assert _row_hash("", relations) == hashes["relations"]
    combined = {
        f"wargame\t{identifier}": path for identifier, path in wargames.items()
    } | {f"relation\t{identifier}": path for identifier, path in relations.items()}
    assert _row_hash("", combined) == hashes["wargames_and_relations"]

    pack_slugs = {
        match.group(1)
        for path in paths
        if (match := re.fullmatch(r"packs/([^/]+)/PACK\.md", path))
    }
    assert pack_slugs == set(baseline["packs"])
    assert len(pack_slugs) == counts["packs"] == 25
    for spec in baseline["packs"].values():
        assert set(spec) == {"display_name", "category", "id_namespace"}
        assert spec["category"] in baseline["categories"]

    migration = baseline["identifier_migration"]
    targets = baseline["target_wargames"]
    assert len(migration) == len(set(migration.values())) == 103
    assert set(migration).issubset(wargames)
    assert set(targets) == {migration.get(identifier, identifier) for identifier in wargames}
    assert len(targets) == len(set(targets.values())) == 127
    retired = set(
        re.findall(r"\bWG-[A-Z0-9]+-\d{3}\b", _tree_text(commit, "archive/RETIRED_IDS.json"))
    )
    assert not retired.intersection(targets), "target map reuses a retired Wargame identity"
    for old_id, old_path in wargames.items():
        new_id = migration.get(old_id, old_id)
        new_path = targets[new_id]
        assert WG_ID.fullmatch(new_id)
        assert PurePosixPath(new_path).stem.startswith(f"{new_id}-")
        old_suffix = PurePosixPath(old_path).stem.removeprefix(f"{old_id}-")
        assert PurePosixPath(new_path).stem == f"{new_id}-{old_suffix}"

    assert baseline["relations"] == {
        identifier: {
            "baseline_path": path,
            "target_path": path.replace("/doctrines/relations/", "/relations/"),
        }
        for identifier, path in relations.items()
    }
    assert _metadata_counts(commit, paths, r"packs/[^/]+/PACK\.md") == baseline[
        "baseline_metadata"
    ]["pack_kind_type"]
    assert _metadata_counts(commit, paths, r"packs/[^/]+/CHECKS\.md") == baseline[
        "baseline_metadata"
    ]["checks_kind_type"]
    assert _metadata_counts(commit, paths, r"packs/[^/]+/exemplars/[^/]+\.md") == baseline[
        "baseline_metadata"
    ]["example_kind_type"]
    lesson_rows = json.loads(_tree_text(commit, "registry/lessons.json"))["rows"]
    lesson_counts = dict(sorted(Counter(row["disposition"] for row in lesson_rows).items()))
    assert lesson_counts == baseline["baseline_metadata"]["lesson_dispositions"]


def test_target_pack_namespaces_and_record_taxonomy() -> None:
    baseline = _load_baseline()
    pack_paths = {path.parent.name: path for path in REPO.glob("packs/*/PACK.md")}
    assert set(pack_paths) == set(baseline["packs"]), "pack slugs changed or disappeared"
    errors = []
    for slug, expected in baseline["packs"].items():
        data = _frontmatter(pack_paths[slug])
        actual = {key: data.get(key) for key in expected}
        if actual != expected:
            errors.append(f"{slug}: {actual!r} != {expected!r}")
        record = baseline["target_metadata"]["pack"]
        if {key: data.get(key) for key in record} != record:
            errors.append(f"{slug}/PACK.md is not record|pack")
    assert not errors, "pack naming contract is not implemented:\n" + "\n".join(errors[:25])

    checks_expected = baseline["target_metadata"]["checks"]
    for path in sorted(REPO.glob("packs/*/CHECKS.md")):
        data = _frontmatter(path)
        assert {key: data.get(key) for key in checks_expected} == checks_expected, path
    examples = sorted(REPO.glob("packs/*/examples/*.md"))
    assert len(examples) == baseline["counts"]["pack_exemplar_files"]
    example_expected = baseline["target_metadata"]["example"]
    for path in examples:
        data = _frontmatter(path)
        assert {key: data.get(key) for key in example_expected} == example_expected, path


def test_target_collection_layout_and_public_names() -> None:
    baseline = _load_baseline()
    required = set(baseline["canonical_collections"])
    optional = set(baseline["optional_collections"])
    errors = []
    for slug in baseline["packs"]:
        pack = REPO / "packs" / slug
        actual = {path.name for path in pack.iterdir() if path.is_dir()}
        if not required.issubset(actual) or not actual.issubset(required | optional):
            errors.append(f"{slug}: directories are {sorted(actual)}")
        if (pack / "doctrines" / "relations").exists():
            errors.append(f"{slug}: nested doctrines/relations remains live")
    assert not errors, "collection layout is not canonical:\n" + "\n".join(errors[:25])

    for old, new in baseline["public_file_migration"].items():
        assert not (REPO / old).exists(), f"retired public name remains: {old}"
        assert (REPO / new).is_file(), f"canonical public name is missing: {new}"
    live_indexes = {
        path.relative_to(REPO).as_posix()
        for path in REPO.rglob("WARGAME_INDEX.md")
        if not {"archive", "benchmark"}.intersection(path.parts)
    }
    assert live_indexes == {"packs/WARGAME_INDEX.md"}
    assert not (REPO / "packs/GUIDE_INDEX.md").exists()


def test_target_wargames_aliases_and_old_pin_resolution() -> None:
    baseline = _load_baseline()
    expected = baseline["target_wargames"]
    actual = {}
    paths = list(REPO.glob("packs/*/wargames/*.md")) + list(
        REPO.glob("inception/wargames/*.md")
    )
    for path in paths:
        data = _frontmatter(path)
        identifier = str(data.get("id") or "")
        assert WG_ID.fullmatch(identifier), f"non-WG live Wargame: {path}"
        assert data.get("kind") == data.get("type") == "wargame", path
        assert identifier not in actual, f"duplicate live Wargame: {identifier}"
        actual[identifier] = path.relative_to(REPO).as_posix()
    assert actual == expected, "the 127-record target Wargame map is not implemented"

    aliases = json.loads(
        (REPO / "registry/identifier-aliases.json").read_text(encoding="utf-8")
    )["aliases"]
    identity_aliases = {
        key: value for key, value in aliases.items() if ANY_WARGAME_ID.fullmatch(key)
    }
    assert identity_aliases == baseline["identifier_migration"], (
        "the Wargame alias map is not the exact frozen 103-entry mapping"
    )

    current = KnowledgeResolver.open(REPO)
    assert {row.canonical_id: row.path for row in current.list("wargame")} == expected
    for old_id, new_id in baseline["identifier_migration"].items():
        resolved = current.require_live(old_id, {"wargame"})
        assert resolved.canonical_id == new_id
        assert resolved.requested_id == old_id

    old = KnowledgeResolver.open(REPO, baseline["frozen_from"]["commit"])
    old_rows = {row.canonical_id: row.path for row in old.list("wargame")}
    assert len(old_rows) == baseline["counts"]["wargames"]
    for old_id in baseline["identifier_migration"]:
        resolved = old.require_live(old_id, {"wargame"})
        assert resolved.canonical_id == old_id
        assert resolved.path == old_rows[old_id]


def test_target_wargames_and_relations_preserve_semantics() -> None:
    baseline = _load_baseline()
    commit = baseline["frozen_from"]["commit"]
    old = KnowledgeResolver.open(REPO, commit)
    migration = baseline["identifier_migration"]
    for row in old.list("wargame"):
        target_id = migration.get(row.canonical_id, row.canonical_id)
        target_path = baseline["target_wargames"][target_id]
        assert (REPO / target_path).is_file(), f"missing migrated Wargame: {target_path}"
        before = _normalise_naming_text(_tree_text(commit, row.path), baseline)
        after = _normalise_naming_text(
            (REPO / target_path).read_text(encoding="utf-8"), baseline
        )
        assert after == before, f"semantic Wargame content changed: {row.canonical_id}"

    for identifier, paths in baseline["relations"].items():
        target = REPO / paths["target_path"]
        assert target.is_file(), f"missing migrated relation: {identifier}"
        before = json.loads(_tree_text(commit, paths["baseline_path"]))
        after = json.loads(target.read_text(encoding="utf-8"))
        assert _normalise_json(after, baseline) == _normalise_json(before, baseline), (
            f"semantic relation content changed: {identifier}"
        )


def test_target_lesson_disposition_is_wargame() -> None:
    baseline = _load_baseline()
    old_counts = Counter(baseline["baseline_metadata"]["lesson_dispositions"])
    migration = baseline["lesson_disposition_migration"]
    expected = Counter(old_counts)
    for old, new in migration.items():
        expected[new] += expected.pop(old, 0)
    lessons = json.loads((REPO / "registry/lessons.json").read_text(encoding="utf-8"))
    actual = Counter(row["disposition"] for row in lessons["rows"])
    assert actual == expected
    schema = json.loads(
        (REPO / "kernel/schemas/lesson.schema.json").read_text(encoding="utf-8")
    )
    enum = schema["$defs"]["row"]["properties"]["disposition"]["enum"]
    assert "wargame" in enum
    assert "decision-guide" not in enum


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower().replace("'", "")).strip("-")


def test_target_doctrine_basenames_end_on_word_boundaries() -> None:
    baseline = _load_baseline()
    maximum = baseline["doctrine_basename_max"]
    doctrines = sorted(REPO.glob("packs/*/doctrines/DOC-*.md"))
    assert len(doctrines) == baseline["counts"]["doctrine_records"]
    errors = []
    for path in doctrines:
        data = _frontmatter(path)
        identifier = str(data.get("id") or "")
        stem = path.stem
        prefix = f"{identifier}-"
        filename_slug = stem.removeprefix(prefix)
        statement_slug = _slug(str(data.get("statement") or ""))
        if len(stem) > maximum:
            errors.append(f"{path.name}: {len(stem)} > {maximum}")
        if not stem.startswith(prefix) or not filename_slug:
            errors.append(f"{path.name}: missing descriptive slug")
        elif not (
            statement_slug == filename_slug
            or statement_slug.startswith(f"{filename_slug}-")
        ):
            errors.append(f"{path.name}: slug ends inside a word")
    assert not errors, "Doctrine basenames are not bounded whole-word prefixes:\n" + "\n".join(
        errors[:30]
    )


def _legacy_allowed(path: str, baseline: dict, baseline_paths: set[str]) -> bool:
    if any(fnmatch.fnmatch(path, pattern) for pattern in baseline["allowed_legacy_surfaces"]):
        return True
    return path in baseline_paths and any(
        fnmatch.fnmatch(path, pattern)
        for pattern in baseline["pre_t0028_snapshot_surfaces"]
    )


def test_target_has_no_unapproved_legacy_surface() -> None:
    baseline = _load_baseline()
    baseline_paths = set(_tree_paths(baseline["frozen_from"]["commit"]))
    legacy_patterns = [
        re.compile(r"packs/[a-z0-9-]+/(?:guides|exemplars|refs)/"),
        re.compile(r"(?:\(|`)(?:guides|exemplars|refs)/"),
        re.compile(r"packs/[a-z0-9-]+/doctrines/relations/"),
        re.compile(r"(?:PACK_SHAPE|ID_ALIASES|GUIDE_INDEX)\.md"),
        re.compile(r"\bdecision-guide\b"),
        re.compile(r"\bGD-[A-Z0-9]+-(?:\d{3}|NNN)\b"),
        re.compile(r"\bWG-OPS-(?:003|005|006)\b"),
    ]
    violations = []
    for path in _worktree_paths():
        if _legacy_allowed(path, baseline, baseline_paths):
            continue
        if re.fullmatch(
            r"packs/[^/]+/(?:guides|exemplars|refs)/.*"
            r"|packs/[^/]+/doctrines/relations/.*",
            path,
        ):
            violations.append(f"{path}: retired collection path")
            continue
        try:
            text = (REPO / path).read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        matches = sorted(
            {match.group(0) for pattern in legacy_patterns for match in pattern.finditer(text)}
        )
        if matches:
            violations.append(f"{path}: {', '.join(matches[:5])}")
    assert not violations, (
        f"{len(violations)} live files retain unapproved legacy naming:\n"
        + "\n".join(violations[:40])
    )
