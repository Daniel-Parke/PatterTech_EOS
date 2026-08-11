"""Finding and Findings: the one result type every check returns.

A Finding is one observation: check id, severity, path, message.
to_dict is the machine shape tools/CLI_CONTRACTS.md documents for the
check command, and the CLI prints it rather than building the same
dict a second time.

The Findings collection aggregates them, splits them by severity and
renders text for a human. It does not rule the exit code: that rule
lives once, in the CLI, where the exit code is actually returned.
Stdlib only.
"""

from __future__ import annotations

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
        """The machine shape, in the order CLI_CONTRACTS.md prints it."""
        return {
            "check": self.check_id,
            "path": self.path,
            "message": self.message,
            "severity": self.severity,
        }


class Findings:
    """Ordered collection of Finding rows with the uniform exit rule."""

    def __init__(self, initial: Iterable[Finding] = ()) -> None:
        self._items: list[Finding] = list(initial)

    def add(self, finding: Finding) -> None:
        self._items.append(finding)

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

    def to_text(self) -> str:
        """Errors first, then warnings, then the summary line.

        Used where a Findings collection has to become an exception
        message. The check command orders its output by check id
        instead, because a reader working down a list wants the ids in
        the order the registry ran them.
        """
        lines = []
        for f in self.errors:
            lines.append(f"ERROR {f.check_id} {f.path}: {f.message}")
        for f in self.warns:
            lines.append(f"warn  {f.check_id} {f.path}: {f.message}")
        lines.append(f"{len(self.errors)} errors, {len(self.warns)} warnings")
        return "\n".join(lines)
