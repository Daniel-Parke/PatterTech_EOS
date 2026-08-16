"""Reconstruct the frozen Doctrine source inventory from Git.

The inventory is deliberately derived from the pinned pre-migration tree,
never from the working tree.  It records where each normative source block
was and its digest, but it does not copy the source prose into the migration
ledger.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


BASELINE_COMMIT = "7f56e4e22378323cf58318fe051d26b5afa8c35f"
EXPECTED_INVENTORY_SHA256 = (
    "a7fcfb117a2e973a3cf6758c985cd35c3ba7a5730dccc8569ca7be326cfb646d"
)
EXPECTED_STANDARD_SHA256 = (
    "a2392764ea84c3876aacd99bc05069b22af904692682dbdcac6444ccbfc5db91"
)

_PACK_PATH_RE = re.compile(r"^packs/[^/]+/PACK\.md$")
_H2_RE = re.compile(r"^##\s+(.+?)\s*$")
_H3_RE = re.compile(r"^###(?:\s|$)")
_LABELLED_RE = re.compile(r"^\*\*((?:B\d+|D\d+|BR-\d+|H\d+))\.")
_REQUIREMENT_LABEL_RE = re.compile(r"^\*\*((?:B\d+|BR-\d+|H\d+))\.")
_NUMBERED_BOLD_RE = re.compile(r"^\d+\.\s+\*\*")
_LIST_ITEM_RE = re.compile(r"^-\s+")
_TABLE_ROW_RE = re.compile(r"^\|.*\|\s*$")

_REQUIREMENT_SECTIONS = {
    "Binding requirements",
    "Requirements",
    "House requirements",
}
_NORMATIVE_SECTIONS = _REQUIREMENT_SECTIONS | {"Defaults", "Preferences"}


class InventoryError(RuntimeError):
    """The pinned inventory cannot be reconstructed exactly."""


@dataclass(frozen=True, order=True)
class SourceBlock:
    """One baseline source block, with source text retained only in memory."""

    path: str
    family: str
    ordinal: int
    start: int
    end: int
    block_sha256: str
    text: str

    @property
    def source_key(self) -> str:
        return f"{self.path}:{self.family}:{self.ordinal:03d}"

    @property
    def canonical_row(self) -> str:
        return (
            f"{self.path}\t{self.family}\t{self.ordinal:03d}\t"
            f"{self.start:04d}-{self.end:04d}\t{self.block_sha256}"
        )

    @property
    def legacy_anchor(self) -> str | None:
        match = _LABELLED_RE.match(self.text)
        return match.group(1) if match else None


def _git(root: Path, *args: str) -> str:
    try:
        process = subprocess.run(
            ["git", "-C", str(root), *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="strict",
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise InventoryError(f"git {' '.join(args)} could not run") from exc
    if process.returncode:
        detail = process.stderr.strip() or "unknown git failure"
        raise InventoryError(f"git {' '.join(args)} failed: {detail}")
    return process.stdout


def _normalise_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _digest_block(lines: Sequence[str], start: int, end: int) -> tuple[str, str]:
    text = "\n".join(lines[start - 1 : end]) + "\n"
    return hashlib.sha256(text.encode("utf-8")).hexdigest(), text.rstrip("\n")


def _is_table_separator(line: str) -> bool:
    if not _TABLE_ROW_RE.match(line):
        return False
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def _first_table_cell(line: str) -> str:
    if not _TABLE_ROW_RE.match(line):
        return ""
    return line.strip().strip("|").split("|", 1)[0].strip()


def _prose_candidates(lines: Sequence[str], section: str, begin: int, end: int) -> list[int]:
    starts: list[int] = []
    family = "requirements" if section in _REQUIREMENT_SECTIONS else section.lower()
    for index in range(begin, end + 1):
        line = lines[index - 1]
        if family == "requirements":
            if _REQUIREMENT_LABEL_RE.match(line) or _NUMBERED_BOLD_RE.match(line):
                starts.append(index)
        elif family == "defaults":
            if _LABELLED_RE.match(line) or _LIST_ITEM_RE.match(line):
                starts.append(index)
        elif family == "preferences":
            if _LIST_ITEM_RE.match(line):
                starts.append(index)
    return starts


def _table_default_rows(lines: Sequence[str], begin: int, end: int) -> list[int]:
    starts: list[int] = []
    default_table = False
    for index in range(begin, end + 1):
        line = lines[index - 1]
        if not _TABLE_ROW_RE.match(line):
            default_table = False
            continue
        if _is_table_separator(line):
            continue
        first = _first_table_cell(line)
        if first == "Default":
            default_table = True
            continue
        if default_table:
            starts.append(index)
    return starts


def _block_end(lines: Sequence[str], start: int, candidates: set[int], limit: int) -> int:
    end = start
    for index in range(start + 1, limit + 1):
        line = lines[index - 1]
        if index in candidates or _H2_RE.match(line) or _H3_RE.match(line):
            break
        end = index
    while end > start and lines[end - 1] == "":
        end -= 1
    return end


def parse_pack(path: str, text: str) -> list[SourceBlock]:
    """Parse one baseline ``PACK.md`` according to the frozen grammar."""

    text = _normalise_lf(text)
    if text.endswith("\n"):
        text = text[:-1]
    lines = text.split("\n")
    section_starts: list[tuple[int, str]] = []
    for line_number, line in enumerate(lines, 1):
        match = _H2_RE.match(line)
        if match and match.group(1) in _NORMATIVE_SECTIONS:
            section_starts.append((line_number, match.group(1)))

    raw: list[tuple[str, int, int]] = []
    for heading_line, section in section_starts:
        section_end = len(lines)
        for index in range(heading_line + 1, len(lines) + 1):
            if _H2_RE.match(lines[index - 1]):
                section_end = index - 1
                break
        starts = _prose_candidates(lines, section, heading_line + 1, section_end)
        if section == "Defaults":
            starts.extend(_table_default_rows(lines, heading_line + 1, section_end))
        if (
            path == "packs/native-client/PACK.md"
            and section == "Preferences"
        ):
            starts.extend(
                index
                for index in range(heading_line + 1, section_end + 1)
                if lines[index - 1].startswith("Taste. Depart freely")
            )
        starts = sorted(set(starts))
        candidates = set(starts)
        family = (
            "requirements"
            if section in _REQUIREMENT_SECTIONS
            else section.lower()
        )
        for start in starts:
            if family == "defaults" and _TABLE_ROW_RE.match(lines[start - 1]):
                block_end = start
            else:
                block_end = _block_end(lines, start, candidates, section_end)
            raw.append((family, start, block_end))

    if path == "packs/writing-content/PACK.md":
        voice_heading = next(
            (
                index
                for index, line in enumerate(lines, 1)
                if line == "## The three voice scopes"
            ),
            None,
        )
        if voice_heading is not None:
            table_started = False
            for index in range(voice_heading + 1, len(lines) + 1):
                line = lines[index - 1]
                if _H2_RE.match(line):
                    break
                if not _TABLE_ROW_RE.match(line):
                    if table_started:
                        break
                    continue
                if _is_table_separator(line):
                    continue
                if _first_table_cell(line) == "Scope":
                    table_started = True
                    continue
                if table_started:
                    raw.append(("voice-scope", index, index))

    raw.sort(key=lambda item: (item[1], item[0], item[2]))
    ordinals: dict[str, int] = {}
    result: list[SourceBlock] = []
    for family, start, end in raw:
        ordinals[family] = ordinals.get(family, 0) + 1
        digest, block_text = _digest_block(lines, start, end)
        result.append(
            SourceBlock(
                path=path,
                family=family,
                ordinal=ordinals[family],
                start=start,
                end=end,
                block_sha256=digest,
                text=block_text,
            )
        )
    return result


def read_baseline(root: Path, commit: str = BASELINE_COMMIT) -> list[SourceBlock]:
    """Read and parse all one-segment pack bodies at ``commit``."""

    root = Path(root).resolve()
    resolved = _git(root, "rev-parse", "--verify", f"{commit}^{{commit}}").strip()
    if resolved != commit:
        raise InventoryError(
            f"baseline ref resolved to {resolved}, expected exact commit {commit}"
        )
    paths = sorted(
        path
        for path in _git(root, "ls-tree", "-r", "--name-only", commit).splitlines()
        if _PACK_PATH_RE.fullmatch(path)
    )
    blocks: list[SourceBlock] = []
    for path in paths:
        blocks.extend(parse_pack(path, _git(root, "show", f"{commit}:{path}")))
    return sorted(blocks, key=lambda block: block.canonical_row)


def inventory_sha256(blocks: Iterable[SourceBlock]) -> str:
    rows = sorted({block.canonical_row for block in blocks})
    payload = "\n".join(rows) + "\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def preliminary_authority(block: SourceBlock) -> str:
    """Return only authority already explicit in the frozen source."""

    if block.family == "defaults":
        return "default"
    if block.family == "preferences":
        return "preference"
    if block.family == "voice-scope":
        cells = [cell.strip() for cell in block.text.strip("|").split("|")]
        return cells[1].split(",", 1)[0].strip() if len(cells) > 1 else "default"
    if block.path == "packs/pattertech-house/PACK.md":
        return "preference"
    explicit = re.search(r"\bAuthority:\s*(binding|default)\b", block.text)
    if explicit:
        return explicit.group(1)
    return "binding"


def inventory_document(blocks: Sequence[SourceBlock]) -> dict:
    """Build the prose-free source freeze, not the final migration ledger."""

    rows = []
    for block in sorted(blocks, key=lambda item: item.canonical_row):
        row = {
            "source_key": block.source_key,
            "path": block.path,
            "family": block.family,
            "ordinal": block.ordinal,
            "start": block.start,
            "end": block.end,
            "block_sha256": block.block_sha256,
            "preliminary_authority": preliminary_authority(block),
        }
        if block.legacy_anchor:
            row["legacy_anchor"] = block.legacy_anchor
        rows.append(row)
    standard = [block for block in blocks if block.family != "voice-scope"]
    return {
        "version": 1,
        "kind": "doctrine-source-inventory",
        "schema_note": (
            "Inventory-only freeze. It is not the reviewed knowledge-migration "
            "ledger governed by knowledge-migration.schema.json."
        ),
        "authority_note": (
            "preliminary_authority records the frozen section, explicit "
            "Authority line and accepted house-scope overrides. It is a "
            "non-final migration hint, not a reviewed disposition."
        ),
        "baseline_commit": BASELINE_COMMIT,
        "inventory_sha256": inventory_sha256(blocks),
        "standard_inventory_sha256": inventory_sha256(standard),
        "rows": rows,
    }


def write_inventory(root: Path, destination: Path) -> dict:
    """Rebuild ``destination`` after verifying the frozen oracle values."""

    blocks = read_baseline(root)
    actual = inventory_sha256(blocks)
    standard = inventory_sha256(
        block for block in blocks if block.family != "voice-scope"
    )
    if len(blocks) != 501 or actual != EXPECTED_INVENTORY_SHA256:
        raise InventoryError(
            f"frozen inventory differs: rows={len(blocks)}, sha256={actual}"
        )
    if len([block for block in blocks if block.family != "voice-scope"]) != 498:
        raise InventoryError("standard inventory does not contain 498 rows")
    if standard != EXPECTED_STANDARD_SHA256:
        raise InventoryError(f"standard inventory differs: sha256={standard}")
    document = inventory_document(blocks)
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(document, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return document


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Rebuild the frozen Doctrine source inventory."
    )
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("org/migration/DOCTRINE_SOURCE_INVENTORY.json"),
    )
    args = parser.parse_args(argv)
    destination = args.out
    if not destination.is_absolute():
        destination = args.repo / destination
    document = write_inventory(args.repo, destination)
    print(
        f"wrote {len(document['rows'])} rows to {destination} "
        f"({document['inventory_sha256']})"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
