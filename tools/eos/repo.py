"""RepoModel: read the repository once, hand every check the same view.

The model collects every markdown file (sorted, matching the v1
checker's traversal so derived-index bytes stay identical), parses its
front-matter with the hardened parser, and flags fixture files: paths
under benchmark/fixtures/ or benchmark/holdout/ keep v1-era metadata,
are exempt from v2 metadata semantics, but are still indexed and still
run the structural E-series.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path

from .frontmatter import FrontMatter, parse

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules"}
FIXTURE_PREFIXES = ("benchmark/fixtures/", "benchmark/holdout/")
# Drill scenarios are read past entirely rather than treated as lenient
# fixtures. A scenario is a toy repository a cold agent is dropped into
# and works inside, so it has to read as an ordinary project: EOS
# front-matter in one of its files is a tell that the run is a test,
# and the marketing scenario ships a client's pricing page and support
# tickets, which are exactly the kind of file that must not carry our
# metadata. They are still hashed and still version controlled.
#
# benchmark/surfaces/ is read past for a different reason: those files
# are the process surface a benchmark run copies onto a fixture, and
# they deliberately carry an unfilled {{VENTURE_NAME}} slot that the
# harness fills per run. Held to the repository's own law they would
# fail E008 for being what they are meant to be.
SKIP_PREFIXES = ("benchmark/drills/scenarios/", "benchmark/surfaces/")


@dataclass
class FileRecord:
    path: str  # repo-relative posix path
    fm: FrontMatter | None
    text: str
    lines: int
    fixture: bool


class RepoModel:
    def __init__(self, root: Path, today: date, files: list[FileRecord]) -> None:
        self.root = Path(root)
        self.today = today
        self.files = files
        self._by_path = {f.path: f for f in files}

    @classmethod
    def load(cls, root, *, today: date) -> "RepoModel":
        root = Path(root).resolve()
        files: list[FileRecord] = []
        for p in sorted(root.rglob("*.md")):
            if SKIP_DIRS.intersection(p.parts):
                continue
            rel = p.relative_to(root).as_posix()
            if rel.startswith(SKIP_PREFIXES):
                continue
            text = p.read_text(encoding="utf-8", errors="replace")
            files.append(
                FileRecord(
                    path=rel,
                    fm=parse(text),
                    text=text,
                    lines=len(text.splitlines()),
                    fixture=rel.startswith(FIXTURE_PREFIXES),
                )
            )
        return cls(root, today, files)

    def get(self, rel_path: str) -> FileRecord | None:
        return self._by_path.get(rel_path)

    def read(self, rel_path: str) -> str | None:
        """Read any repo file (markdown or not); None when absent."""
        p = self.root / rel_path
        if not p.is_file():
            return None
        return p.read_text(encoding="utf-8", errors="replace")

    def exists(self, rel_path: str) -> bool:
        return (self.root / rel_path).exists()
