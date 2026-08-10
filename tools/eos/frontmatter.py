"""Hardened front-matter parser for the EOS markdown contract.

Grammar (a deliberate YAML subset, no coercion, values stay strings):

- The block opens when line 1 is exactly ``---`` (stripped) and closes
  at the next ``---`` line. An opener with no terminator within the
  first 60 lines is an error and the block is treated as absent.
- Keys match ``[A-Za-z_][A-Za-z0-9_-]*`` at column zero.
- Values: plain strings (stripped), inline lists ``[a, b]``, or block
  lists (a bare ``key:`` followed by ``- item`` lines).
- Blank lines and ``#`` comments are legal and ignored.
- Any other non-blank, non-comment line inside the block is an error,
  never a silent skip.

Errors are (line_number, message) tuples, 1-indexed against the file.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

MAX_SCAN_LINES = 60
KEY_RE = re.compile(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$")
DASH_RE = re.compile(r"^\s*-\s+(.*)$")


@dataclass
class FrontMatter:
    data: dict = field(default_factory=dict)
    errors: list = field(default_factory=list)  # list[tuple[int, str]]
    present: bool = False
    body: str = ""


def _inline_list(raw: str) -> list:
    return [v.strip() for v in raw[1:-1].split(",") if v.strip()]


def parse(text: str) -> FrontMatter:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return FrontMatter(data={}, errors=[], present=False, body=text)

    end = None
    for i in range(1, min(len(lines), MAX_SCAN_LINES)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return FrontMatter(
            data={},
            errors=[(1, "unterminated front-matter block")],
            present=False,
            body=text,
        )

    data: dict = {}
    errors: list = []
    pending_list_key: str | None = None

    for i in range(1, end):
        line = lines[i]
        lineno = i + 1
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue

        m = KEY_RE.match(line)
        if m:
            key, raw = m.group(1), m.group(2).strip()
            if raw.startswith("[") and raw.endswith("]"):
                data[key] = _inline_list(raw)
                pending_list_key = None
            elif raw == "":
                data[key] = ""
                pending_list_key = key
            else:
                data[key] = raw
                pending_list_key = None
            continue

        dm = DASH_RE.match(line)
        if dm:
            if pending_list_key is None:
                errors.append((lineno, f"list item without a list key: {stripped}"))
            else:
                if not isinstance(data[pending_list_key], list):
                    data[pending_list_key] = []
                data[pending_list_key].append(dm.group(1).strip())
            continue

        errors.append((lineno, f"unparseable front-matter line: {stripped}"))
        pending_list_key = None

    body = "\n".join(lines[end + 1:])
    return FrontMatter(data=data, errors=errors, present=True, body=body)
