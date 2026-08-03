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
            text = p.read_text(encoding="utf-8", errors="replace")
            rel = p.relative_to(root).as_posix()
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
