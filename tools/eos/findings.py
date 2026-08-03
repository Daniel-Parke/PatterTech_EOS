"""Finding and Findings: the one result type every check returns.

A Finding is one observation: check id, severity, path, message. The
Findings collection aggregates them, renders text for humans and JSON
for machines (per tools/CLI_CONTRACTS.md the JSON keys are check,
severity, path, message), and rules the exit code: 0 for clean or
warnings only, 1 when any error-severity finding exists. Stdlib only.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Iterable, Iterator

SEVERITIES = ("error", "warn")


@dataclass(frozen=True)
class Finding:
    check_id: str
    severity: str  # 'error' | 'warn'
    path: str
    message: str

    def __post_init__(self) -> None:
        if self.severity not in SEVERITIES:
            raise ValueError(f"severity must be one of {SEVERITIES}: {self.severity}")

    def to_dict(self) -> dict:
        return {
            "check": self.check_id,
            "severity": self.severity,
            "path": self.path,
            "message": self.message,
        }


class Findings:
    """Ordered collection of Finding rows with the uniform exit rule."""

    def __init__(self, initial: Iterable[Finding] = ()) -> None:
        self._items: list[Finding] = list(initial)

    def add(self, finding: Finding) -> None:
        self._items.append(finding)

    def extend(self, findings: Iterable[Finding]) -> None:
        self._items.extend(findings)

    def __iter__(self) -> Iterator[Finding]:
        return iter(self._items)

    def __len__(self) -> int:
        return len(self._items)

    @property
    def errors(self) -> list[Finding]:
        return [f for f in self._items if f.severity == "error"]

    @property
    def warns(self) -> list[Finding]:
        return [f for f in self._items if f.severity == "warn"]

    def to_json(self) -> str:
        return json.dumps([f.to_dict() for f in self._items], indent=2)

    def to_text(self) -> str:
        """Human lines in the v1 eos_check format plus the summary line."""
        lines = []
        for f in self.errors:
            lines.append(f"ERROR {f.check_id} {f.path}: {f.message}")
        for f in self.warns:
            lines.append(f"warn  {f.check_id} {f.path}: {f.message}")
        lines.append(f"{len(self.errors)} errors, {len(self.warns)} warnings")
        return "\n".join(lines)

    def exit_code(self) -> int:
        return 1 if self.errors else 0
