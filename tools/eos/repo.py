"""RepoModel: read the repository once, hand every check the same view.

The model collects every markdown file (sorted, matching the v1
checker's traversal so derived-index bytes stay identical) and parses
its front-matter with the hardened parser. Which files a check judges
is the check's business: the semantic and freshness series exempt the
frozen and verbatim trees by path prefix, and say why there.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from .frontmatter import FrontMatter, parse

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", "node_modules"}
# Drill scenarios are read past entirely rather than loaded and exempted.
# A scenario is a toy repository a cold agent is dropped into
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


def content_sha256(path) -> str:
    """Hash what a file says, not the newline convention it arrived in.

    The freeze manifest and the drill manifest both record hashes of LF
    content, because that is what git stores and what the tools that
    wrote them emitted. Git's `core.autocrlf=true`, the default on a
    Windows install, rewrites those files to CRLF on checkout. Hashing
    the raw bytes then reports every frozen text file as modified on a
    machine that has changed nothing.

    That is not a hypothetical. Checking out `main` after the v2 merge
    turned a clean tree into 108 B001 errors, all of them false, and a
    fresh clone on Windows would have shown a new reader the same thing
    on their first command. A freeze check that fails on an intact
    repository is worse than no freeze check, because it teaches people
    to ignore it.

    So: undo the checkout transform before hashing. Only CRLF becomes
    LF, which is exactly what autocrlf did on the way out; a lone CR is
    left alone because it is content rather than a line ending git ever
    writes. Binary files are hashed byte for byte, detected the way git
    detects them, by a NUL in the buffer.
    """
    data = Path(path).read_bytes()
    if b"\x00" not in data:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


@dataclass
class FileRecord:
    path: str  # repo-relative posix path
    fm: FrontMatter | None
    text: str
    lines: int


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
        # Sort on the POSIX string, never on the Path. Path comparison
        # is case-insensitive on Windows and case-sensitive on POSIX, so
        # sorting Path objects orders packs/INDEX.md before or after
        # packs/agentic-swarm/PACK.md depending on the machine. Every
        # derived index is written in this order, so the same tree
        # generated an INDEX.md that was clean on Windows and stale on
        # Linux, and CI caught it only because CI runs both.
        for p in sorted(root.rglob("*.md"), key=lambda q: q.as_posix()):
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
