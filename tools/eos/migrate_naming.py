"""Plan, apply and verify the reviewed T-0028 naming migration.

The frozen baseline owns identity decisions.  This module only turns that
reviewed contract into deterministic file moves and byte substitutions.  A
plan is read-only, apply re-plans before writing, and check is empty only at a
fixpoint.
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shutil
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any, Mapping, Sequence

from tools.eos.frontmatter import parse as parse_frontmatter

BASELINE_PATH = "org/migration/NAMING_BASELINE.json"
LEDGER_PATH = "org/migration/NAMING_MIGRATION.json"
GENERATOR = "tools.eos.migrate_naming"
TASK = "T-0028"
PLAN_VERSION = 1

_SKIP_DIRS = {".git", ".mypy_cache", ".pytest_cache", "__pycache__"}
_SELF_PATH = "tools/eos/migrate_naming.py"
_IDENTIFIER_BOUNDARY = r"[A-Z0-9]"


class NamingMigrationError(RuntimeError):
    """The reviewed naming migration cannot proceed safely."""


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")


def _json_hash(value: object) -> str:
    return _sha256(_canonical_json(value))


def _normalise_root(repo: str | Path) -> Path:
    root = Path(repo).resolve()
    if not root.is_dir():
        raise NamingMigrationError(f"repository root is not a directory: {root}")
    return root


def _safe_path(root: Path, relative: str) -> Path:
    if not isinstance(relative, str) or not relative:
        raise NamingMigrationError("migration paths must be non-empty strings")
    if "\\" in relative:
        raise NamingMigrationError(
            f"migration path is not POSIX-normalised: {relative}"
        )
    pure = PurePosixPath(relative)
    if (
        pure.is_absolute()
        or relative != pure.as_posix()
        or ".." in pure.parts
        or any(":" in part or part in _SKIP_DIRS for part in pure.parts)
    ):
        raise NamingMigrationError(f"migration path escapes the repository: {relative}")
    candidate = root.joinpath(*pure.parts).resolve(strict=False)
    if candidate != root and root not in candidate.parents:
        raise NamingMigrationError(f"migration path escapes the repository: {relative}")
    return candidate


def _read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise NamingMigrationError(f"cannot read {label} at {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise NamingMigrationError(f"{label} must contain a JSON object")
    return value


def _load_baseline(
    root: Path, baseline_path: str | Path | None
) -> tuple[dict[str, Any], str, str]:
    if baseline_path is None:
        relative = BASELINE_PATH
        path = _safe_path(root, relative)
    else:
        raw = Path(baseline_path)
        path = raw.resolve() if raw.is_absolute() else _safe_path(root, raw.as_posix())
        if path != root and root not in path.parents:
            raise NamingMigrationError(f"baseline escapes the repository: {path}")
        relative = path.relative_to(root).as_posix()
    data = path.read_bytes()
    baseline = _read_json(path, "naming baseline")
    _validate_baseline(baseline)
    return baseline, relative, _sha256(data)


def _mapping(value: object, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise NamingMigrationError(f"baseline field {name} must be an object")
    if not all(isinstance(key, str) for key in value):
        raise NamingMigrationError(f"baseline field {name} has a non-string key")
    return dict(value)


def _string_list(value: object, name: str) -> list[str]:
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise NamingMigrationError(f"baseline field {name} must be a string list")
    return list(value)


def _validate_baseline(baseline: Mapping[str, Any]) -> None:
    if baseline.get("schema_version") != 1 or baseline.get("task") != TASK:
        raise NamingMigrationError("unsupported naming baseline contract")
    identifiers = _mapping(baseline.get("identifier_migration"), "identifier_migration")
    targets = _mapping(baseline.get("target_wargames"), "target_wargames")
    relations = _mapping(baseline.get("relations"), "relations")
    packs = _mapping(baseline.get("packs"), "packs")
    counts = _mapping(baseline.get("counts"), "counts")
    if len(identifiers) != int(counts.get("wargames_with_gd_id", -1)) + 3:
        raise NamingMigrationError(
            "identity migration count does not match the baseline"
        )
    if len(identifiers) != 103:
        raise NamingMigrationError(
            "the reviewed identity migration must contain 103 rows"
        )
    if len(targets) != int(counts.get("wargames", -1)):
        raise NamingMigrationError("Wargame target count does not match the baseline")
    if len(relations) != int(counts.get("relations", -1)):
        raise NamingMigrationError("relation count does not match the baseline")
    if len(packs) != int(counts.get("packs", -1)):
        raise NamingMigrationError("pack count does not match the baseline")
    if len(set(identifiers.values())) != len(identifiers):
        raise NamingMigrationError("identity migration targets are not unique")
    if set(identifiers.values()) - set(targets):
        raise NamingMigrationError("an identity target has no canonical Wargame path")
    for name in (
        "canonical_collections",
        "optional_collections",
        "retired_collection_paths",
        "allowed_legacy_surfaces",
        "pre_t0028_snapshot_surfaces",
    ):
        _string_list(baseline.get(name), name)
    for relative in targets.values():
        if not isinstance(relative, str):
            raise NamingMigrationError("a Wargame target path is not a string")
    for relation in relations.values():
        row = _mapping(relation, "relations row")
        if not isinstance(row.get("baseline_path"), str) or not isinstance(
            row.get("target_path"), str
        ):
            raise NamingMigrationError("a relation row is missing its paths")


def expected_ledger(
    baseline: Mapping[str, Any], baseline_sha256: str
) -> dict[str, Any]:
    """Return the compact, reviewable ledger derived from the frozen baseline."""

    _validate_baseline(baseline)
    identifiers = _mapping(baseline["identifier_migration"], "identifier_migration")
    targets = _mapping(baseline["target_wargames"], "target_wargames")
    relations = _mapping(baseline["relations"], "relations")
    retired = _string_list(baseline["retired_collection_paths"], "retired paths")
    canonical = _string_list(baseline["canonical_collections"], "collections")
    optional = _string_list(baseline["optional_collections"], "optional collections")
    public = _mapping(baseline["public_file_migration"], "public_file_migration")
    collection_migration = {
        retired[0]: canonical[1],
        retired[1]: canonical[2],
        retired[2]: canonical[3],
        retired[3]: optional[0],
    }
    old_index = "packs/" + "GUIDE" + "_INDEX.md"
    sources = _source_wargames(baseline)
    source_for_target = {target: source for source, target in sources.items()}
    identity_paths = {
        old: {
            "target_id": new,
            "baseline_path": source_for_target[str(targets[new])],
            "target_path": str(targets[new]),
        }
        for old, new in sorted(identifiers.items())
    }
    return {
        "schema_version": PLAN_VERSION,
        "kind": "naming-migration",
        "task": TASK,
        "status": "reviewed-contract",
        "application_state": "verified by tools.eos.migrate_naming check",
        "generator": GENERATOR,
        "baseline": {
            "path": BASELINE_PATH,
            "sha256": baseline_sha256,
            "frozen_from": baseline["frozen_from"],
        },
        "counts": {
            "identity_mappings": len(identifiers),
            "target_wargames": len(targets),
            "relations": len(relations),
            "packs": len(_mapping(baseline["packs"], "packs")),
            "doctrines": int(
                _mapping(baseline["counts"], "counts")["doctrine_records"]
            ),
        },
        "identity_migration": dict(sorted(identifiers.items())),
        "identity_path_migration": identity_paths,
        "contract_hashes": {
            "identity_migration": _json_hash(identifiers),
            "target_wargames": _json_hash(targets),
            "relations": _json_hash(relations),
        },
        "collection_migration": collection_migration,
        "public_file_migration": dict(sorted(public.items())),
        "removed_compatibility_files": [old_index],
        "doctrine_basename": {
            "maximum_characters": int(baseline["doctrine_basename_max"]),
            "truncation": "whole-word",
        },
        "excluded_surfaces": sorted(
            set(_string_list(baseline["allowed_legacy_surfaces"], "allowed surfaces"))
            | set(
                _string_list(
                    baseline["pre_t0028_snapshot_surfaces"], "snapshot surfaces"
                )
            )
        ),
    }


def _all_files(root: Path) -> dict[str, bytes]:
    files: dict[str, bytes] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if any(
            part in _SKIP_DIRS or part.startswith(".naming-migration-")
            for part in relative.parts
        ):
            continue
        if path.is_symlink():
            resolved = path.resolve(strict=False)
            if resolved != root and root not in resolved.parents:
                raise NamingMigrationError(
                    f"repository symlink escapes the root: {relative}"
                )
            raise NamingMigrationError(
                f"repository symlinks are not migration inputs: {relative}"
            )
        if path.is_file():
            files[relative.as_posix()] = path.read_bytes()
    return files


def _replace_part(relative: str, old: str, new: str) -> str:
    parts = list(PurePosixPath(relative).parts)
    old_parts = PurePosixPath(old).parts
    for index in range(len(parts) - len(old_parts) + 1):
        if tuple(parts[index : index + len(old_parts)]) == old_parts:
            parts[index : index + len(old_parts)] = PurePosixPath(new).parts
            return PurePosixPath(*parts).as_posix()
    raise NamingMigrationError(
        f"path does not contain expected collection {old}: {relative}"
    )


def _source_wargames(baseline: Mapping[str, Any]) -> dict[str, str]:
    identities = _mapping(baseline["identifier_migration"], "identifier_migration")
    inverse = {new: old for old, new in identities.items()}
    targets = _mapping(baseline["target_wargames"], "target_wargames")
    retired = _string_list(baseline["retired_collection_paths"], "retired paths")[0]
    canonical = _string_list(baseline["canonical_collections"], "collections")[1]
    result: dict[str, str] = {}
    for target_id, target_path in targets.items():
        source_id = inverse.get(target_id, target_id)
        pure = PurePosixPath(target_path)
        if canonical in pure.parts and pure.parts[0] == "packs":
            source_path = _replace_part(target_path, canonical, retired)
            name = PurePosixPath(source_path).name
            if not name.startswith(target_id + "-"):
                raise NamingMigrationError(
                    f"Wargame target filename does not begin with its ID: {target_path}"
                )
            source_path = str(
                PurePosixPath(source_path).with_name(source_id + name[len(target_id) :])
            )
        else:
            source_path = target_path
        result[source_path] = target_path
    if len(result) != len(targets):
        raise NamingMigrationError("derived Wargame source paths are not unique")
    return result


def _register_move(
    files: Mapping[str, bytes],
    moves: dict[str, tuple[str, str]],
    source: str,
    target: str,
    reason: str,
    *,
    required: bool = True,
) -> None:
    if source == target:
        if required and source not in files:
            raise NamingMigrationError(f"required canonical file is missing: {source}")
        return
    source_exists = source in files
    target_exists = target in files
    if source_exists and target_exists:
        raise NamingMigrationError(f"migration target collision: {source} -> {target}")
    if not source_exists:
        if required and not target_exists:
            raise NamingMigrationError(
                f"migration source and target are missing: {source}"
            )
        return
    previous = moves.get(source)
    if previous and previous[0] != target:
        raise NamingMigrationError(f"one source has two migration targets: {source}")
    for other_source, (other_target, _) in moves.items():
        if other_source != source and other_target == target:
            raise NamingMigrationError(f"two sources have migration target {target}")
    moves[source] = (target, reason)


def _collection_files(files: Mapping[str, bytes], collection: str) -> list[str]:
    old_parts = PurePosixPath(collection).parts
    found: list[str] = []
    for relative in files:
        parts = PurePosixPath(relative).parts
        if len(parts) < 3 or parts[0] != "packs":
            continue
        for index in range(2, len(parts) - len(old_parts) + 1):
            if tuple(parts[index : index + len(old_parts)]) == old_parts:
                found.append(relative)
                break
    return sorted(found)


def _slug(value: str) -> str:
    value = value.replace("'", "").replace("’", "")
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")


def _doctrine_target(relative: str, data: bytes, maximum: int) -> str:
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise NamingMigrationError(f"Doctrine is not UTF-8: {relative}") from exc
    parsed = parse_frontmatter(text)
    identifier = parsed.data.get("id")
    statement = parsed.data.get("statement")
    if (
        parsed.errors
        or not isinstance(identifier, str)
        or not isinstance(statement, str)
    ):
        raise NamingMigrationError(
            f"Doctrine metadata cannot drive its basename: {relative}"
        )
    words = _slug(statement).split("-")
    available = maximum - len(identifier) - 1
    selected: list[str] = []
    for word in words:
        candidate = "-".join([*selected, word])
        if len(candidate) > available:
            break
        selected.append(word)
    if not selected:
        raise NamingMigrationError(
            f"Doctrine has no whole-word basename within {maximum}: {identifier}"
        )
    name = identifier + "-" + "-".join(selected) + ".md"
    return str(PurePosixPath(relative).with_name(name))


def _is_excluded(relative: str, baseline: Mapping[str, Any]) -> bool:
    if relative == _SELF_PATH:
        return True
    patterns = _string_list(baseline["allowed_legacy_surfaces"], "allowed surfaces")
    patterns += _string_list(
        baseline["pre_t0028_snapshot_surfaces"], "snapshot surfaces"
    )
    return any(fnmatch.fnmatchcase(relative, pattern) for pattern in patterns)


def _replace_text(
    data: bytes,
    relative: str,
    baseline: Mapping[str, Any],
    path_moves: Mapping[str, str],
) -> tuple[bytes, list[str]]:
    if _is_excluded(relative, baseline):
        return data, []
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError:
        return data, []
    labels: list[str] = []

    def literal(old: str, new: str, label: str) -> None:
        nonlocal text
        if old and old in text:
            text = text.replace(old, new)
            labels.append(label)

    for old, new in sorted(
        path_moves.items(), key=lambda item: (-len(item[0]), item[0])
    ):
        literal(old, new, "canonical path")

    identities = _mapping(baseline["identifier_migration"], "identifier_migration")
    for old, new in sorted(identities.items()):
        pattern = re.compile(
            rf"(?<!{_IDENTIFIER_BOUNDARY}){re.escape(old)}(?!{_IDENTIFIER_BOUNDARY})"
        )
        text, count = pattern.subn(new, text)
        if count:
            labels.append("Wargame identity")

    retired = _string_list(baseline["retired_collection_paths"], "retired paths")
    canonical = _string_list(baseline["canonical_collections"], "collections")
    optional = _string_list(baseline["optional_collections"], "optional collections")
    collection_pairs = (
        (retired[0], canonical[1]),
        (retired[1], canonical[2]),
        (retired[2], canonical[3]),
        (retired[3], optional[0]),
    )
    for old, new in collection_pairs:
        for prefix in ("(", "`"):
            literal(prefix + old + "/", prefix + new + "/", "relative collection path")
        for pack in _mapping(baseline["packs"], "packs"):
            literal(
                f"packs/{pack}/{old}/",
                f"packs/{pack}/{new}/",
                "pack collection path",
            )

    for old, new in _mapping(
        baseline["public_file_migration"], "public_file_migration"
    ).items():
        literal(PurePosixPath(old).name, PurePosixPath(new).name, "public filename")
    old_index = "GUIDE" + "_INDEX.md"
    literal(old_index, "WARGAME_INDEX.md", "retired index")
    for old, new in _mapping(
        baseline["lesson_disposition_migration"], "lesson_disposition_migration"
    ).items():
        pattern = re.compile(rf"(?<![a-z-]){re.escape(old)}(?![a-z-])")
        text, count = pattern.subn(new, text)
        if count:
            labels.append("lesson disposition")
    result = text.encode("utf-8")
    return result, sorted(set(labels))


def _frontmatter_update(
    data: bytes, relative: str, updates: Mapping[str, str]
) -> tuple[bytes, list[str]]:
    if not updates:
        return data, []
    try:
        text = data.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise NamingMigrationError(f"front matter is not UTF-8: {relative}") from exc
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise NamingMigrationError(f"front matter is missing: {relative}")
    end = next(
        (index for index, line in enumerate(lines[1:60], 1) if line.strip() == "---"),
        None,
    )
    if end is None:
        raise NamingMigrationError(f"front matter is unterminated: {relative}")
    newline = "\r\n" if "\r\n" in text else "\n"
    changed: list[str] = []
    for key, value in updates.items():
        matches = [
            index
            for index in range(1, end)
            if re.match(rf"^{re.escape(key)}\s*:", lines[index])
        ]
        if len(matches) > 1:
            raise NamingMigrationError(f"duplicate front-matter key {key}: {relative}")
        rendered = f"{key}: {value}{newline}"
        if matches:
            index = matches[0]
            suffix = (
                "\r\n"
                if lines[index].endswith("\r\n")
                else "\n" if lines[index].endswith("\n") else ""
            )
            rendered = f"{key}: {value}{suffix}"
            if lines[index] != rendered:
                lines[index] = rendered
                changed.append(key)
        else:
            lines.insert(end, rendered)
            end += 1
            changed.append(key)
    return "".join(lines).encode("utf-8"), ["front matter: " + key for key in changed]


def _rewrite_alias_registry(
    data: bytes, baseline: Mapping[str, Any]
) -> tuple[bytes, list[str]]:
    try:
        text = data.decode("utf-8")
        document = json.loads(text)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise NamingMigrationError("identifier alias registry is invalid") from exc
    aliases = document.get("aliases") if isinstance(document, dict) else None
    if not isinstance(aliases, dict):
        raise NamingMigrationError("identifier alias registry has no aliases object")
    migration = _mapping(baseline["identifier_migration"], "identifier_migration")
    updated = dict(aliases)
    replacements: dict[str, str] = {}
    for alias, target in list(updated.items()):
        if isinstance(target, str) and target in migration:
            updated[alias] = migration[target]
            replacements[target] = migration[target]
    for old, new in migration.items():
        existing = updated.get(old)
        if existing is not None and existing != new:
            raise NamingMigrationError(f"identifier alias collision for {old}")
        updated[old] = new
    if updated == aliases:
        return data, []

    # Existing bytes, indentation and key order are retained.  Only reviewed
    # target substitutions and missing alias rows are inserted.
    for old, new in sorted(replacements.items()):
        pattern = re.compile(rf"(:\s*){re.escape(json.dumps(old))}(?=\s*[,}}])")
        text = pattern.sub(lambda match: match.group(1) + json.dumps(new), text)

    reparsed = json.loads(text)
    current = reparsed.get("aliases")
    if not isinstance(current, dict):
        raise NamingMigrationError("identifier alias registry changed while rendering")
    missing = [
        (old, new) for old, new in sorted(migration.items()) if old not in current
    ]
    if missing:
        match = re.search(r'"aliases"\s*:\s*\{', text)
        if match is None:
            raise NamingMigrationError("cannot locate the aliases object")
        open_brace = text.find("{", match.start())
        depth = 0
        in_string = False
        escaped = False
        close_brace: int | None = None
        for index in range(open_brace, len(text)):
            character = text[index]
            if in_string:
                if escaped:
                    escaped = False
                elif character == "\\":
                    escaped = True
                elif character == '"':
                    in_string = False
                continue
            if character == '"':
                in_string = True
            elif character == "{":
                depth += 1
            elif character == "}":
                depth -= 1
                if depth == 0:
                    close_brace = index
                    break
        if close_brace is None:
            raise NamingMigrationError("cannot find the end of the aliases object")
        before = text[:close_brace]
        trailing_match = re.search(r"\s*$", before)
        trailing = trailing_match.group(0) if trailing_match else ""
        core = before[: len(before) - len(trailing)] if trailing else before
        newline = "\r\n" if "\r\n" in text else "\n"
        entry_match = re.search(
            r'\r?\n([ \t]+)"[^"\r\n]+"\s*:', text[open_brace:close_brace]
        )
        entry_indent = entry_match.group(1) if entry_match else "    "
        rendered_rows = ("," + newline).join(
            entry_indent
            + json.dumps(old, ensure_ascii=False)
            + ": "
            + json.dumps(new, ensure_ascii=False)
            for old, new in missing
        )
        separator = "," if current else ""
        if not trailing:
            trailing = newline + entry_indent[:-2]
        text = (
            core + separator + newline + rendered_rows + trailing + text[close_brace:]
        )

    rendered = text.encode("utf-8")
    final = json.loads(text)
    final_aliases = final.get("aliases") if isinstance(final, dict) else None
    if not isinstance(final_aliases, dict) or any(
        final_aliases.get(old) != new for old, new in migration.items()
    ):
        raise NamingMigrationError("rendered identifier aliases failed verification")
    return rendered, ["identifier aliases"]


def _metadata_updates(relative: str, baseline: Mapping[str, Any]) -> dict[str, str]:
    parts = PurePosixPath(relative).parts
    target_metadata = _mapping(baseline["target_metadata"], "target_metadata")
    if len(parts) == 3 and parts[0] == "packs" and parts[2] == "PACK.md":
        pack = _mapping(baseline["packs"], "packs").get(parts[1])
        if not isinstance(pack, dict):
            raise NamingMigrationError(f"unknown pack metadata target: {relative}")
        return {
            **_mapping(target_metadata["pack"], "pack target metadata"),
            "display_name": str(pack["display_name"]),
            "category": str(pack["category"]),
            "id_namespace": str(pack["id_namespace"]),
        }
    if len(parts) == 3 and parts[0] == "packs" and parts[2] == "CHECKS.md":
        return {
            key: str(value)
            for key, value in _mapping(
                target_metadata["checks"], "checks target metadata"
            ).items()
        }
    canonical = _string_list(baseline["canonical_collections"], "collections")
    if len(parts) >= 4 and parts[0] == "packs" and parts[2] == canonical[2]:
        return {
            key: str(value)
            for key, value in _mapping(
                target_metadata["example"], "example target metadata"
            ).items()
        }
    return {}


def _build_plan(
    repo: str | Path, baseline_path: str | Path | None
) -> tuple[dict[str, Any], dict[str, bytes], set[str], set[str]]:
    root = _normalise_root(repo)
    baseline, baseline_relative, baseline_sha = _load_baseline(root, baseline_path)
    files = _all_files(root)
    ledger_file = _safe_path(root, LEDGER_PATH)
    if baseline_relative == BASELINE_PATH and ledger_file.is_file():
        ledger = _read_json(ledger_file, "naming migration ledger")
        if ledger != expected_ledger(baseline, baseline_sha):
            raise NamingMigrationError(
                "naming baseline and reviewed migration ledger do not match"
            )
    moves: dict[str, tuple[str, str]] = {}

    wargame_sources = _source_wargames(baseline)
    for source, target in wargame_sources.items():
        _safe_path(root, source)
        _safe_path(root, target)
        _register_move(files, moves, source, target, "Wargame canonical path")

    retired = _string_list(baseline["retired_collection_paths"], "retired paths")
    canonical = _string_list(baseline["canonical_collections"], "collections")
    current_pack_wargames = set(_collection_files(files, retired[0]))
    current_pack_wargames |= set(_collection_files(files, canonical[1]))
    logical_pack_wargames = {
        wargame_sources.get(path, path) for path in current_pack_wargames
    }
    target_pack_wargames = {
        target
        for target in wargame_sources.values()
        if PurePosixPath(target).parts[0] == "packs"
    }
    if logical_pack_wargames != target_pack_wargames:
        raise NamingMigrationError(
            "pack Wargame inventory differs from the frozen contract"
        )

    relations = _mapping(baseline["relations"], "relations")
    relation_paths: dict[str, str] = {}
    for row in relations.values():
        relation = _mapping(row, "relation row")
        source, target = str(relation["baseline_path"]), str(relation["target_path"])
        relation_paths[source] = target
        _safe_path(root, source)
        _safe_path(root, target)
        _register_move(files, moves, source, target, "relation collection")
    current_relations = set(_collection_files(files, retired[3]))
    current_relations |= {
        path
        for path in files
        if len(PurePosixPath(path).parts) >= 4
        and PurePosixPath(path).parts[0] == "packs"
        and PurePosixPath(path).parts[2]
        == _string_list(baseline["optional_collections"], "optional collections")[0]
    }
    if {relation_paths.get(path, path) for path in current_relations} != set(
        relation_paths.values()
    ):
        raise NamingMigrationError(
            "relation inventory differs from the frozen contract"
        )

    counts = _mapping(baseline["counts"], "counts")
    for old, new, expected, reason in (
        (
            retired[1],
            canonical[2],
            int(counts["pack_exemplar_files"]),
            "example collection",
        ),
        (
            retired[2],
            canonical[3],
            int(counts["pack_reference_files"]),
            "reference collection",
        ),
    ):
        old_files = _collection_files(files, old)
        new_files = _collection_files(files, new)
        logical_targets = {_replace_part(path, old, new) for path in old_files} | set(
            new_files
        )
        if len(logical_targets) != expected:
            raise NamingMigrationError(
                f"{reason} inventory is {len(logical_targets)}, expected {expected}"
            )
        for source in old_files:
            target = _replace_part(source, old, new)
            _safe_path(root, target)
            _register_move(files, moves, source, target, reason)

    research_files = _collection_files(files, canonical[4])
    if len(research_files) != int(counts["pack_research_files"]):
        raise NamingMigrationError(
            f"research inventory is {len(research_files)}, expected {counts['pack_research_files']}"
        )

    for source, target in _mapping(
        baseline["public_file_migration"], "public_file_migration"
    ).items():
        _safe_path(root, source)
        _safe_path(root, target)
        _register_move(files, moves, source, target, "public contract filename")

    doctrine_sources = [
        path
        for path in files
        if len(PurePosixPath(path).parts) >= 4
        and PurePosixPath(path).parts[0] == "packs"
        and PurePosixPath(path).parts[2] == canonical[0]
        and PurePosixPath(path).suffix == ".md"
    ]
    if len(doctrine_sources) != int(counts["doctrine_records"]):
        raise NamingMigrationError(
            f"Doctrine inventory is {len(doctrine_sources)}, expected {counts['doctrine_records']}"
        )
    for source in doctrine_sources:
        target = _doctrine_target(
            source, files[source], int(baseline["doctrine_basename_max"])
        )
        _safe_path(root, target)
        _register_move(files, moves, source, target, "Doctrine whole-word basename")

    for slug in _mapping(baseline["packs"], "packs"):
        for name in ("PACK.md", "CHECKS.md"):
            relative = f"packs/{slug}/{name}"
            if relative not in files:
                raise NamingMigrationError(
                    f"required pack surface is missing: {relative}"
                )
    for relative in (
        "registry/identifier-aliases.json",
        "registry/lessons.json",
        "kernel/schemas/lesson.schema.json",
    ):
        if relative not in files:
            raise NamingMigrationError(
                f"required naming surface is missing: {relative}"
            )

    delete_name = "packs/" + "GUIDE" + "_INDEX.md"
    deletes = {delete_name} if delete_name in files else set()

    move_targets = {source: target for source, (target, _) in moves.items()}
    target_owners: dict[str, str] = {}
    for source, target in move_targets.items():
        owner = target_owners.setdefault(target, source)
        if owner != source:
            raise NamingMigrationError(f"two sources own target {target}")
        _safe_path(root, source)
        _safe_path(root, target)
    for deleted in deletes:
        _safe_path(root, deleted)

    logical_files: dict[str, tuple[str, bytes]] = {}
    for source, data in files.items():
        if source in deletes:
            continue
        target = move_targets.get(source, source)
        if target in logical_files:
            raise NamingMigrationError(f"logical file collision at {target}")
        logical_files[target] = (source, data)

    rewrites: list[dict[str, Any]] = []
    desired: dict[str, bytes] = {}
    alias_path = "registry/identifier-aliases.json"
    for target, (source, original) in sorted(logical_files.items()):
        data = original
        labels: list[str] = []
        if target == alias_path:
            data, alias_labels = _rewrite_alias_registry(data, baseline)
            labels.extend(alias_labels)
        else:
            data, text_labels = _replace_text(data, source, baseline, move_targets)
            labels.extend(text_labels)
        data, metadata_labels = _frontmatter_update(
            data, target, _metadata_updates(target, baseline)
        )
        labels.extend(metadata_labels)
        if source != target or data != original:
            desired[target] = data
        if data != original:
            rewrites.append(
                {
                    "path": target,
                    "source": source,
                    "before_sha256": _sha256(original),
                    "after_sha256": _sha256(data),
                    "substitutions": sorted(set(labels)),
                }
            )

    for identifier, relative in _mapping(
        baseline["target_wargames"], "target_wargames"
    ).items():
        if relative not in logical_files:
            raise NamingMigrationError(f"canonical Wargame is missing: {identifier}")
        data = desired.get(relative, logical_files[relative][1])
        try:
            parsed = parse_frontmatter(data.decode("utf-8"))
        except UnicodeDecodeError as exc:
            raise NamingMigrationError(f"Wargame is not UTF-8: {relative}") from exc
        if parsed.errors or parsed.data.get("id") != identifier:
            raise NamingMigrationError(
                f"Wargame identity does not match its canonical path: {relative}"
            )
        if parsed.data.get("kind") != "wargame" or parsed.data.get("type") != "wargame":
            raise NamingMigrationError(f"Wargame metadata is not canonical: {relative}")

    move_rows = [
        {
            "source": source,
            "target": target,
            "reason": reason,
            "source_sha256": _sha256(files[source]),
            "target_sha256": _sha256(desired.get(target, files[source])),
        }
        for source, (target, reason) in sorted(moves.items())
    ]
    delete_rows = [
        {
            "path": path,
            "sha256": _sha256(files[path]),
            "reason": "retired compatibility index",
        }
        for path in sorted(deletes)
    ]
    identifiers = _mapping(baseline["identifier_migration"], "identifier_migration")
    source_for_target = {target: source for source, target in wargame_sources.items()}
    identity_path_migration = {
        old: {
            "target_id": new,
            "baseline_path": source_for_target[str(baseline["target_wargames"][new])],
            "target_path": str(baseline["target_wargames"][new]),
        }
        for old, new in sorted(identifiers.items())
    }
    document: dict[str, Any] = {
        "schema_version": PLAN_VERSION,
        "kind": "naming-migration-plan",
        "task": TASK,
        "generator": GENERATOR,
        "baseline": {"path": baseline_relative, "sha256": baseline_sha},
        "contract": {
            "identity_mappings": len(identifiers),
            "identity_path_migration": identity_path_migration,
            "identity_migration_sha256": _json_hash(identifiers),
            "target_wargames_sha256": _json_hash(baseline["target_wargames"]),
            "relations_sha256": _json_hash(relations),
        },
        "state": "pending" if move_rows or rewrites or delete_rows else "fixpoint",
        "operations": {
            "moves": move_rows,
            "rewrites": rewrites,
            "deletes": delete_rows,
        },
        "counts": {
            "moves": len(move_rows),
            "rewrites": len(rewrites),
            "deletes": len(delete_rows),
        },
    }
    removals = set(move_targets) | deletes
    retired_dirs = {str(PurePosixPath(path).parent) for path in removals}
    return document, desired, removals, retired_dirs


def plan(
    repo: str | Path = ".", *, baseline_path: str | Path | None = None
) -> dict[str, Any]:
    """Return a JSON-safe, read-only migration plan for ``repo``."""

    document, _, _, _ = _build_plan(repo, baseline_path)
    return document


def check(
    repo: str | Path = ".", *, baseline_path: str | Path | None = None
) -> list[str]:
    """Return migration work still required; an empty list is the fixpoint."""

    document = plan(repo, baseline_path=baseline_path)
    findings: list[str] = []
    for row in document["operations"]["moves"]:
        findings.append(f"move {row['source']} -> {row['target']}")
    for row in document["operations"]["rewrites"]:
        findings.append(f"rewrite {row['path']}")
    for row in document["operations"]["deletes"]:
        findings.append(f"delete {row['path']}")
    return findings


def apply(
    repo: str | Path = ".",
    reviewed_plan: Mapping[str, Any] | None = None,
    *,
    baseline_path: str | Path | None = None,
) -> dict[str, Any]:
    """Apply the current reviewed plan after all safety checks have passed."""

    root = _normalise_root(repo)
    document, desired, removals, retired_dirs = _build_plan(root, baseline_path)
    if reviewed_plan is not None and dict(reviewed_plan) != document:
        raise NamingMigrationError("reviewed plan no longer matches repository state")
    if document["state"] == "fixpoint":
        return {"state": "fixpoint", "moves": 0, "rewrites": 0, "deletes": 0}

    stage = Path(tempfile.mkdtemp(prefix=".naming-migration-", dir=root)).resolve()
    if stage.parent != root:
        raise NamingMigrationError("migration staging directory escaped the repository")
    try:
        staged: dict[str, Path] = {}
        for index, (target, data) in enumerate(sorted(desired.items())):
            _safe_path(root, target)
            staged_path = stage / f"{index:06d}"
            staged_path.write_bytes(data)
            if _sha256(staged_path.read_bytes()) != _sha256(data):
                raise NamingMigrationError(
                    f"staged bytes failed verification: {target}"
                )
            staged[target] = staged_path

        # Re-plan before the first repository mutation to close the review-to-write gap.
        current, _, _, _ = _build_plan(root, baseline_path)
        if current != document:
            raise NamingMigrationError(
                "repository changed while the migration was staged"
            )

        for target, staged_path in sorted(staged.items()):
            destination = _safe_path(root, target)
            destination.parent.mkdir(parents=True, exist_ok=True)
            os.replace(staged_path, destination)
        for relative in sorted(
            removals, key=lambda value: (-len(PurePosixPath(value).parts), value)
        ):
            path = _safe_path(root, relative)
            target = next(
                (
                    row["target"]
                    for row in document["operations"]["moves"]
                    if row["source"] == relative
                ),
                None,
            )
            if target == relative:
                continue
            if path.exists():
                path.unlink()
        for relative in sorted(
            retired_dirs, key=lambda value: -len(PurePosixPath(value).parts)
        ):
            directory = _safe_path(root, relative)
            if directory.is_dir():
                try:
                    directory.rmdir()
                except OSError:
                    pass
    finally:
        if stage.exists():
            shutil.rmtree(stage)

    remaining = check(root, baseline_path=baseline_path)
    if remaining:
        raise NamingMigrationError(
            "migration did not reach a fixpoint: " + "; ".join(remaining[:5])
        )
    return {
        "state": "applied",
        "moves": document["counts"]["moves"],
        "rewrites": document["counts"]["rewrites"],
        "deletes": document["counts"]["deletes"],
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("plan", "apply", "check"))
    parser.add_argument("--repo", default=".", help="repository root")
    parser.add_argument("--baseline", help="baseline path within the repository")
    parser.add_argument(
        "--confirm",
        help=f"required for CLI apply; pass {TASK}",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.action == "plan":
            print(
                json.dumps(
                    plan(args.repo, baseline_path=args.baseline),
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0
        if args.action == "check":
            findings = check(args.repo, baseline_path=args.baseline)
            for finding in findings:
                print(finding)
            return 1 if findings else 0
        if args.confirm != TASK:
            raise NamingMigrationError(f"CLI apply requires --confirm {TASK}")
        result = apply(args.repo, baseline_path=args.baseline)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    except NamingMigrationError as exc:
        print(f"naming migration error: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
