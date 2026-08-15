"""Canonical Doctrine, Wargame, relation and Ruling semantics.

One resolver is shared by repository checks, generated views, the CLI and
seed validation.  Existing ``GD-*`` and ``WG-*`` values are identities.  The
prefix never decides the semantic kind and a historical lookup never falls
back to the worktree.
"""

from __future__ import annotations

import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Iterable, Mapping

from .frontmatter import parse as parse_frontmatter


DOC_ID = re.compile(r"^DOC-[A-Z0-9]+-\d{3}$")
WARGAME_ID = re.compile(r"^(?:GD|WG)-[A-Z0-9]+-\d{3}$")
RELATION_ID = re.compile(r"^DREL-[A-Z0-9]+-\d{3}$")
RULING_ID = re.compile(r"^RUL-[A-Z0-9]+-\d{3}$")
DEFINITION_FROM_STEM = re.compile(
    r"^((?:DOC|DREL|GD|WG)-[A-Z0-9]+-\d{3})(?:-|\.|$)"
)
RELATION_TYPES = {
    "depends_on", "supports", "tensions_with", "conflicts_with",
    "exception_to", "supersedes", "covers_gap",
}
ACYCLIC_RELATIONS = {"depends_on", "supersedes"}
TRI_STATES = {"true", "false", "unknown"}


@dataclass(frozen=True)
class KnowledgeProblem:
    code: str
    path: str
    identifier: str
    message: str


@dataclass(frozen=True)
class Resolution:
    canonical_id: str
    kind: str
    path: str
    state: str = "live"
    summary: str = ""
    metadata: Mapping[str, object] = field(default_factory=dict)
    requested_id: str | None = None

    @property
    def identifier(self) -> str:
        return self.canonical_id

    @property
    def id(self) -> str:
        return self.canonical_id


class TreeView:
    """A worktree or one immutable Git tree.

    Paths and blobs are cached on the instance.  A requested ref is resolved
    once to a full commit SHA; failure is a cannot-run error rather than an
    empty view which a caller might mistake for a clean result.
    """

    def __init__(self, root: Path, commit: str | None) -> None:
        self.root = Path(root).resolve()
        self.commit = commit
        self._paths: tuple[str, ...] | None = None
        self._texts: dict[str, str | None] = {}
        self._tag_paths: dict[str, frozenset[str]] = {}

    @classmethod
    def open(cls, root: Path, ref: str | None = None) -> "TreeView":
        root = Path(root).resolve()
        if ref is None or str(ref).upper() == "WORKTREE":
            return cls(root, None)
        proc = subprocess.run(
            ["git", "-C", str(root), "rev-parse", "--verify",
             f"{ref}^{{commit}}"],
            capture_output=True, text=True, encoding="utf-8",
        )
        if proc.returncode:
            detail = (proc.stderr or proc.stdout).strip()
            raise ValueError(f"cannot resolve Git ref or commit {ref}: {detail}")
        return cls(root, proc.stdout.strip())

    def paths(self) -> tuple[str, ...]:
        if self._paths is not None:
            return self._paths
        if self.commit is None:
            skip = {".git", "__pycache__", ".pytest_cache", "node_modules"}
            rows = []
            for path in self.root.rglob("*"):
                if not path.is_file() or skip.intersection(path.parts):
                    continue
                rows.append(path.relative_to(self.root).as_posix())
            self._paths = tuple(sorted(rows))
        else:
            proc = subprocess.run(
                ["git", "-C", str(self.root), "ls-tree", "-r",
                 "--name-only", self.commit],
                capture_output=True, text=True, encoding="utf-8",
            )
            if proc.returncode:
                raise ValueError(
                    f"cannot list Git commit {self.commit}: "
                    f"{(proc.stderr or proc.stdout).strip()}"
                )
            self._paths = tuple(sorted(p for p in proc.stdout.splitlines() if p))
        return self._paths

    def read_text(self, path: str) -> str | None:
        path = str(PurePosixPath(path))
        if path in self._texts:
            return self._texts[path]
        if self.commit is None:
            target = self.root / Path(path)
            text = target.read_text(encoding="utf-8", errors="replace") \
                if target.is_file() else None
        else:
            proc = subprocess.run(
                ["git", "-C", str(self.root), "show",
                 f"{self.commit}:{path}"],
                capture_output=True, text=True, encoding="utf-8",
            )
            text = proc.stdout if proc.returncode == 0 else None
        self._texts[path] = text
        return text

    def exists(self, path: str) -> bool:
        return str(PurePosixPath(path)) in set(self.paths())

    def knowledge_paths(self) -> tuple[str, ...]:
        """The small canonical surface from which identities may be defined."""
        if self.commit is not None:
            paths = self.paths()
        else:
            candidates = []
            patterns = (
                "packs/*/PACK.md",
                "packs/*/doctrines/**/*.md",
                "packs/*/doctrines/**/*.json",
                "packs/*/guides/*.md",
                "packs/*/wargames/*.md",
                "inception/wargames/*.md",
            )
            for pattern in patterns:
                candidates.extend(self.root.glob(pattern))
            for rel in ("archive/RETIRED_IDS.json",
                        "registry/identifier-aliases.json",
                        "registry/pressure-dispositions.json"):
                path = self.root / rel
                if path.is_file():
                    candidates.append(path)
            return tuple(sorted({
                path.relative_to(self.root).as_posix()
                for path in candidates if path.is_file()
            }))
        return tuple(path for path in paths if (
            _is_pack(path) or _is_doctrine(path) or _is_wargame(path) or
            _is_relation(path) or path in {
                "archive/RETIRED_IDS.json",
                "registry/identifier-aliases.json",
                "registry/pressure-dispositions.json",
            }
        ))

    def read_tag_text(self, tag: str, path: str) -> str | None:
        proc = subprocess.run(
            ["git", "-C", str(self.root), "show", f"{tag}:{path}"],
            capture_output=True, text=True, encoding="utf-8",
        )
        return proc.stdout if proc.returncode == 0 else None

    def tag_paths(self, tag: str) -> frozenset[str]:
        """All paths at a tag, fetched once for retired-ID verification."""
        if tag in self._tag_paths:
            return self._tag_paths[tag]
        proc = subprocess.run(
            ["git", "-C", str(self.root), "ls-tree", "-r", "--name-only", tag],
            capture_output=True, text=True, encoding="utf-8",
        )
        if proc.returncode:
            paths = frozenset()
        else:
            paths = frozenset(p for p in proc.stdout.splitlines() if p)
        self._tag_paths[tag] = paths
        return paths


def _values(value: object) -> list[str]:
    if isinstance(value, list):
        return [str(v).strip() for v in value if str(v).strip()]
    if value is None or str(value).strip() in {"", "none", "null"}:
        return []
    return [str(value).strip()]


def _definition_id(path: str, metadata: Mapping[str, object]) -> str | None:
    stated = str(metadata.get("id") or "").strip()
    stem = PurePosixPath(path).stem
    match = DEFINITION_FROM_STEM.match(stem)
    from_name = match.group(1) if match else None
    return stated or from_name


def _is_pack(path: str) -> bool:
    parts = PurePosixPath(path).parts
    return len(parts) == 3 and parts[0] == "packs" and parts[2] == "PACK.md"


def _is_doctrine(path: str) -> bool:
    parts = PurePosixPath(path).parts
    return (len(parts) >= 4 and parts[0] == "packs" and
            parts[2] == "doctrines" and parts[-1].endswith(".md") and
            parts[-1].startswith("DOC-"))


def _is_wargame(path: str) -> bool:
    parts = PurePosixPath(path).parts
    if not path.endswith(".md"):
        return False
    in_pack = (len(parts) >= 4 and parts[0] == "packs" and
               parts[2] in {"guides", "wargames"})
    in_inception = (len(parts) >= 3 and parts[0] == "inception" and
                    parts[1] == "wargames")
    return (in_pack or in_inception) and bool(
        re.match(r"^(?:GD|WG)-", parts[-1]))


def _is_relation(path: str) -> bool:
    parts = PurePosixPath(path).parts
    return (path.endswith(".json") and len(parts) >= 5 and
            parts[0] == "packs" and parts[2:4] == ("doctrines", "relations")
            and parts[-1].startswith("DREL-"))


class KnowledgeResolver:
    """Resolve every knowledge identity from one tree view."""

    def __init__(self, view: TreeView) -> None:
        self.view = view
        self._definitions: dict[str, Resolution] = {}
        self._retired: dict[str, Resolution] = {}
        self._aliases: dict[str, str] = {}
        self._problems: list[KnowledgeProblem] = []
        self._relations: list[dict] = []
        self._pressure_dispositions: list[dict] = []
        self._packs: dict[str, dict] = {}
        self._bodies: dict[str, str] = {}
        self._load()

    @classmethod
    def open(cls, root: Path, ref: str | None = None) -> "KnowledgeResolver":
        return cls(TreeView.open(root, ref))

    @property
    def problems(self) -> tuple[KnowledgeProblem, ...]:
        return tuple(self._problems)

    @property
    def relations(self) -> tuple[dict, ...]:
        return tuple(self._relations)

    @property
    def packs(self) -> Mapping[str, dict]:
        return self._packs

    @property
    def pressure_dispositions(self) -> tuple[dict, ...]:
        return tuple(self._pressure_dispositions)

    def _problem(self, code: str, path: str, identifier: str,
                 message: str) -> None:
        self._problems.append(KnowledgeProblem(code, path, identifier, message))

    def _add_definition(self, identifier: str, kind: str, path: str,
                        metadata: dict, body: str = "") -> None:
        if identifier in self._definitions:
            first = self._definitions[identifier]
            self._problem(
                "duplicate-definition", path, identifier,
                f"duplicate live definition for {identifier}; first at {first.path}",
            )
            return
        expected = PurePosixPath(path).stem
        if not expected.startswith(identifier):
            self._problem(
                "id-path-mismatch", path, identifier,
                f"front-matter id {identifier} does not match filename {expected}",
            )
        summary = str(metadata.get("summary") or metadata.get("statement") or "")
        self._definitions[identifier] = Resolution(
            identifier, kind, path, "live", summary, dict(metadata), identifier,
        )
        self._bodies[identifier] = body

    def _load_markdown(self, path: str, kind: str) -> None:
        text = self.view.read_text(path)
        if text is None:
            return
        parsed = parse_frontmatter(text)
        identifier = _definition_id(path, parsed.data)
        if not identifier:
            self._problem("missing-id", path, "", "definition has no id")
            return
        pattern = DOC_ID if kind == "doctrine" else WARGAME_ID
        if not pattern.match(identifier):
            self._problem("invalid-id", path, identifier,
                          f"invalid {kind} identifier {identifier}")
            return
        self._add_definition(identifier, kind, path, parsed.data, parsed.body)

    def _load_relation(self, path: str) -> None:
        raw = self.view.read_text(path)
        if raw is None:
            return
        try:
            row = json.loads(raw)
        except (ValueError, TypeError) as exc:
            self._problem("relation-json", path, "", f"invalid relation JSON: {exc}")
            return
        if not isinstance(row, dict):
            self._problem("relation-shape", path, "", "relation is not an object")
            return
        identifier = str(row.get("id") or "")
        if not RELATION_ID.match(identifier):
            self._problem("invalid-id", path, identifier,
                          f"invalid relation identifier {identifier}")
            return
        self._relations.append(dict(row, _path=path))
        self._add_definition(identifier, "relation", path, row)

    def _load_pack(self, path: str) -> None:
        text = self.view.read_text(path)
        if text is None:
            return
        parsed = parse_frontmatter(text)
        name = PurePosixPath(path).parent.name
        self._packs[name] = {
            "path": path,
            "summary": str(parsed.data.get("summary") or ""),
            "applies_when": _values(parsed.data.get("applies_when")),
            "depends_on": _values(parsed.data.get("depends_on")),
        }

    def _load_aliases(self) -> None:
        path = "registry/identifier-aliases.json"
        raw = self.view.read_text(path)
        if raw is None:
            return
        try:
            doc = json.loads(raw)
        except ValueError as exc:
            self._problem("alias-json", path, "", f"invalid alias JSON: {exc}")
            return
        aliases = doc.get("aliases") if isinstance(doc, dict) else None
        if not isinstance(aliases, dict):
            self._problem("alias-shape", path, "", "aliases must be an object")
            return
        self._aliases = {str(k): str(v) for k, v in aliases.items()}
        for start in sorted(self._aliases):
            seen: list[str] = []
            current = start
            while current in self._aliases:
                if current in seen:
                    chain = " -> ".join(seen + [current])
                    self._problem("alias-cycle", path, start,
                                  f"alias cycle: {chain}")
                    break
                seen.append(current)
                current = self._aliases[current]
            else:
                if current not in self._definitions and current not in self._retired:
                    self._problem("alias-target", path, start,
                                  f"alias target does not resolve: {current}")

    def _load_retired(self) -> None:
        path = "archive/RETIRED_IDS.json"
        raw = self.view.read_text(path)
        if raw is None:
            return
        try:
            doc = json.loads(raw)
        except ValueError as exc:
            self._problem("retired-json", path, "", f"invalid retired JSON: {exc}")
            return
        tag = str(doc.get("tag") or "") if isinstance(doc, dict) else ""
        ids = doc.get("ids") if isinstance(doc, dict) else None
        if not tag or not isinstance(ids, dict):
            self._problem("retired-shape", path, "",
                          "retired manifest needs tag and ids object")
            return
        archived_paths = self.view.tag_paths(tag)
        if not archived_paths:
            self._problem("retired-tag", path, "",
                          f"retired tag does not resolve: {tag}")
        for identifier, archived_path in sorted(ids.items()):
            identifier, archived_path = str(identifier), str(archived_path)
            if archived_path not in archived_paths:
                self._problem("retired-missing", path, identifier,
                              f"retired location missing at {tag}:{archived_path}")
            else:
                match = DEFINITION_FROM_STEM.match(PurePosixPath(archived_path).stem)
                found = match.group(1) if match else None
                if found != identifier:
                    self._problem(
                        "retired-id-mismatch", path, identifier,
                        f"retired location defines {found or 'no id'} not {identifier}",
                    )
            kind = "wargame" if WARGAME_ID.match(identifier) else "doctrine"
            self._retired[identifier] = Resolution(
                identifier, kind, f"{tag}:{archived_path}", "retired", "", {}, identifier,
            )
            if identifier in self._definitions:
                self._problem("live-retired-collision", path, identifier,
                              f"{identifier} is both live and retired")

    def _validate_relations(self) -> None:
        graphs: dict[str, dict[str, set[str]]] = {
            name: {} for name in ACYCLIC_RELATIONS
        }
        for row in self._relations:
            path = str(row.get("_path") or "")
            identifier = str(row.get("id") or "")
            relation = str(row.get("relation") or "")
            owner = str(row.get("owner_doctrine") or row.get("owner") or "")
            target = str(row.get("target") or "")
            if relation not in RELATION_TYPES:
                self._problem("relation-type", path, identifier,
                              f"unknown relation type {relation}")
            endpoints = [("owner", owner, {"doctrine"})]
            if relation != "covers_gap":
                endpoints.append(("target", target, {"doctrine"}))
            elif not target:
                self._problem("relation-target", path, identifier,
                              "covers_gap needs a named gap target")
            for role, value, kinds in endpoints:
                resolved = self.resolve(value) if value else None
                if resolved is None or resolved.state != "live" or resolved.kind not in kinds:
                    self._problem("relation-target", path, identifier,
                                  f"{role} {value or '(missing)'} does not resolve live")
            if owner and owner == target:
                self._problem("self-relation", path, identifier,
                              f"relation {identifier} points {owner} to itself")
            wargame = str(row.get("wargame") or "")
            if wargame:
                resolved = self.resolve(wargame)
                if resolved is None or resolved.state != "live" or resolved.kind != "wargame":
                    self._problem("relation-wargame", path, identifier,
                                  f"wargame {wargame} does not resolve live")
                elif relation == "covers_gap" and str(
                    resolved.metadata.get("gap_domain") or ""
                ) != target:
                    self._problem(
                        "relation-gap", path, identifier,
                        f"covers_gap target {target} does not match "
                        f"{wargame} gap_domain",
                    )
            elif relation == "covers_gap":
                self._problem("relation-wargame", path, identifier,
                              "covers_gap needs a live covering Wargame")
            if relation in graphs and owner and target:
                graphs[relation].setdefault(owner, set()).add(target)
        for relation, graph in graphs.items():
            for cycle in _cycles(graph):
                self._problem("relation-cycle", "", cycle[0],
                              f"{relation} cycle: {' -> '.join(cycle)}")

    def _validate_packs(self) -> None:
        graph: dict[str, set[str]] = {}
        for name, row in sorted(self._packs.items()):
            graph[name] = set()
            for dep in row.get("depends_on") or []:
                if dep not in self._packs:
                    self._problem("pack-dependency", row["path"], name,
                                  f"pack dependency missing: {dep}")
                else:
                    graph[name].add(dep)
        # Edges point from consumer to prerequisite.  Cycle detection is
        # direction-independent, so the ordinary helper is sufficient.
        for cycle in _cycles(graph):
            self._problem("pack-cycle", "packs", cycle[0],
                          f"pack dependency cycle: {' -> '.join(cycle)}")

    def _load_pressure_dispositions(self) -> None:
        path = "registry/pressure-dispositions.json"
        raw = self.view.read_text(path)
        if raw is None:
            return
        try:
            document = json.loads(raw)
        except ValueError as exc:
            self._problem("pressure-json", path, "", f"invalid JSON: {exc}")
            return
        rows = document.get("rows") if isinstance(document, dict) else None
        if not isinstance(rows, list):
            self._problem("pressure-shape", path, "", "rows must be an array")
            return
        seen_cases: set[int] = set()
        seen_pressures: set[str] = set()
        for row in rows:
            if not isinstance(row, dict):
                self._problem("pressure-shape", path, "", "row must be an object")
                continue
            case = row.get("case")
            pressure = str(row.get("pressure") or "")
            if case in seen_cases:
                self._problem("pressure-case", path, pressure,
                              f"duplicate pressure case {case}")
            if pressure in seen_pressures:
                self._problem("pressure-name", path, pressure,
                              f"duplicate pressure {pressure}")
            if isinstance(case, int):
                seen_cases.add(case)
            seen_pressures.add(pressure)
            for identifier in _values(row.get("wargames")):
                target = self.resolve(identifier)
                if target is None or target.state != "live" or target.kind != "wargame":
                    self._problem("pressure-wargame", path, pressure,
                                  f"Wargame {identifier} does not resolve live")
            for identifier in _values(row.get("relations")):
                target = self.resolve(identifier)
                if target is None or target.state != "live" or target.kind != "relation":
                    self._problem("pressure-relation", path, pressure,
                                  f"relation {identifier} does not resolve live")
            self._pressure_dispositions.append(dict(row))

    def _load(self) -> None:
        paths = self.view.knowledge_paths()
        for path in paths:
            if _is_pack(path):
                self._load_pack(path)
            elif _is_doctrine(path):
                self._load_markdown(path, "doctrine")
            elif _is_wargame(path):
                self._load_markdown(path, "wargame")
            elif _is_relation(path):
                self._load_relation(path)
        # Retired definitions precede aliases so an alias may explicitly
        # terminate at provenance.  Active consumers still use require_live.
        self._load_retired()
        self._load_aliases()
        self._validate_relations()
        self._validate_packs()
        self._load_pressure_dispositions()

    def resolve(self, identifier: str) -> Resolution | None:
        requested = str(identifier).strip()
        current = requested
        seen: set[str] = set()
        while current in self._aliases:
            if current in seen:
                return None
            seen.add(current)
            current = self._aliases[current]
        found = self._definitions.get(current) or self._retired.get(current)
        if found is None:
            return None
        if requested == found.canonical_id:
            return found
        return Resolution(
            found.canonical_id, found.kind, found.path, found.state,
            found.summary, found.metadata, requested,
        )

    def require_live(self, identifier: str,
                     kinds: set[str] | None = None) -> Resolution:
        found = self.resolve(identifier)
        if found is None:
            raise ValueError(f"knowledge id does not resolve: {identifier}")
        if found.state != "live":
            raise ValueError(f"knowledge id is retired, not live: {identifier}")
        if kinds and found.kind not in kinds:
            raise ValueError(
                f"knowledge id {identifier} is {found.kind}, expected "
                f"{', '.join(sorted(kinds))}"
            )
        return found

    def list(self, kind: str | None = None) -> tuple[Resolution, ...]:
        rows = [row for row in self._definitions.values()
                if kind is None or row.kind == kind]
        return tuple(sorted(rows, key=lambda row: row.canonical_id))

    def pack_order(self, active: Iterable[str] | None = None) -> list[str]:
        wanted = set(active or self._packs)
        # Include prerequisites even when the caller named only a child.
        pending = list(wanted)
        while pending:
            name = pending.pop()
            for dep in self._packs.get(name, {}).get("depends_on") or []:
                if dep in self._packs and dep not in wanted:
                    wanted.add(dep)
                    pending.append(dep)
        indegree = {name: 0 for name in wanted}
        outgoing = {name: set() for name in wanted}
        for name in wanted:
            for dep in self._packs.get(name, {}).get("depends_on") or []:
                if dep in wanted:
                    outgoing[dep].add(name)
                    indegree[name] += 1
        ready = sorted(name for name, degree in indegree.items() if degree == 0)
        ordered: list[str] = []
        while ready:
            name = ready.pop(0)
            ordered.append(name)
            for child in sorted(outgoing[name]):
                indegree[child] -= 1
                if indegree[child] == 0:
                    ready.append(child)
                    ready.sort()
        if len(ordered) != len(wanted):
            # Problems already record the cycle.  Returning the stable lexical
            # remainder keeps diagnostic callers deterministic.
            ordered.extend(sorted(wanted - set(ordered)))
        return ordered


def _cycles(graph: Mapping[str, set[str]]) -> list[list[str]]:
    found: list[list[str]] = []
    visiting: list[str] = []
    visited: set[str] = set()

    def walk(node: str) -> None:
        if node in visiting:
            start = visiting.index(node)
            cycle = visiting[start:] + [node]
            key = tuple(cycle)
            if key not in {tuple(c) for c in found}:
                found.append(cycle)
            return
        if node in visited:
            return
        visiting.append(node)
        for child in sorted(graph.get(node, set())):
            walk(child)
        visiting.pop()
        visited.add(node)

    for node in sorted(graph):
        walk(node)
    return found


def _truth(facts: Mapping[str, str], predicates: list[str]) -> tuple[str, list[str]]:
    if not predicates:
        return "true", []
    values = [str(facts.get(name, "unknown")).lower() for name in predicates]
    unknown = [name for name, value in zip(predicates, values) if value == "unknown"]
    # Applicability is conjunctive.  One false fact makes it inapplicable;
    # otherwise uncertainty remains uncertainty.
    if "false" in values:
        return "false", unknown
    if unknown:
        return "unknown", unknown
    return "true", []


def _pressure_truth(facts: Mapping[str, str], predicates: list[str]) -> tuple[str, list[str]]:
    if not predicates:
        return "false", []
    values = [str(facts.get(name, "unknown")).lower() for name in predicates]
    unknown = [name for name, value in zip(predicates, values) if value == "unknown"]
    # Engagement predicates are alternatives: any true pressure engages.
    if "true" in values:
        return "true", unknown
    if unknown:
        return "unknown", unknown
    return "false", []


def _summary(row: Resolution) -> dict:
    data = row.metadata
    result = {
        "id": row.canonical_id,
        "kind": row.kind,
        "path": row.path,
        "summary": row.summary,
        "state": row.state,
    }
    for key in ("authority", "scenario_modes", "consequence"):
        if data.get(key):
            result[key] = data[key]
    return result


def match_knowledge(
    resolver: KnowledgeResolver,
    facts: Mapping[str, str],
    *,
    include: Mapping[str, str] | None = None,
    omit: Mapping[str, str] | None = None,
) -> dict:
    """Return applicable standing rules and pressure-selected procedures.

    The matcher classifies.  It never chooses an option or outcome.
    """

    normalised = {str(k): str(v).lower() for k, v in facts.items()}
    bad = sorted(f"{k}={v}" for k, v in normalised.items() if v not in TRI_STATES)
    if bad:
        raise ValueError("facts must be true, false or unknown: " + ", ".join(bad))
    include = dict(include or {})
    omit = dict(omit or {})
    for action, rows in (("include", include), ("omit", omit)):
        for identifier, reason in rows.items():
            if not str(reason).strip():
                raise ValueError(f"operator {action} of {identifier} needs a reason")
            resolver.require_live(identifier, {"wargame"})

    doctrines = []
    active_packs: set[str] = set()
    unresolved: set[str] = set()
    for row in resolver.list("doctrine"):
        state, unknown = _truth(normalised, _values(row.metadata.get("applies_when")))
        unresolved.update(unknown)
        if state == "true":
            doctrines.append(_summary(row))
            parts = PurePosixPath(row.path).parts
            if len(parts) > 1 and parts[0] == "packs":
                active_packs.add(parts[1])

    required: dict[str, dict] = {}
    candidates: dict[str, dict] = {}
    omitted_rows: dict[str, dict] = {}
    reasons: dict[str, list[str]] = {}
    covered_pressures: set[str] = set()
    for row in resolver.list("wargame"):
        data = row.metadata
        applies, apply_unknown = _truth(
            normalised, _values(data.get("applies_when")))
        unresolved.update(apply_unknown)
        engages = _values(data.get("engages_when") or data.get("engage_when"))
        pressure, pressure_unknown = _pressure_truth(normalised, engages)
        unresolved.update(pressure_unknown)
        covered_pressures.update(engages)
        identifier = row.canonical_id
        summary = _summary(row)
        if applies == "false":
            omitted_rows[identifier] = summary
            reasons[identifier] = ["applicability is false"]
        elif pressure == "true" or str(data.get("always_walk", "")).lower() == "true":
            required[identifier] = summary
            reasons[identifier] = ["engagement pressure is true"]
        elif pressure == "unknown" or applies == "unknown":
            if str(data.get("consequence") or "routine").lower() == "high":
                required[identifier] = summary
                reasons[identifier] = [
                    "high-consequence pressure is unknown; ask or include"
                ]
            else:
                candidates[identifier] = summary
                reasons[identifier] = ["routine pressure is unknown"]
        else:
            omitted_rows[identifier] = summary
            reasons[identifier] = ["engagement pressure is false"]

        parts = PurePosixPath(row.path).parts
        if applies != "false" and len(parts) > 1 and parts[0] == "packs":
            active_packs.add(parts[1])

    dispositions = {
        str(row.get("pressure")): row
        for row in resolver.pressure_dispositions
        if row.get("pressure")
    }
    covered_pressures.update(dispositions)
    pressure_rows = []
    for pressure_name in sorted(set(normalised) & set(dispositions)):
        row = dispositions[pressure_name]
        truth = normalised[pressure_name]
        disposition = str(row.get("disposition"))
        consequence = str(row.get("consequence") or "routine")
        if truth == "false":
            state = "omitted"
            reason = "pressure is false"
        elif disposition == "rejected":
            state = "deferred"
            reason = "admission is rejected until the recorded reopen trigger"
        elif truth == "true" and disposition == "relation-only":
            state = "fallback-required"
            reason = "relation fallback covers this pressure without a Wargame"
        elif truth == "true":
            state = "engaged"
            reason = "pressure is true"
        elif consequence == "high":
            state = "ask-or-fallback"
            reason = "high-consequence pressure is unknown"
        else:
            state = "candidate"
            reason = "routine pressure is unknown"
        pressure_rows.append({
            "case": row.get("case"),
            "pressure": pressure_name,
            "disposition": disposition,
            "state": state,
            "wargames": list(row.get("wargames") or []),
            "relations": list(row.get("relations") or []),
            "fallback": row.get("fallback"),
            "reopen_trigger": row.get("reopen_trigger"),
            "reason": reason,
        })

    for identifier, reason in include.items():
        row = resolver.require_live(identifier, {"wargame"})
        required[identifier] = _summary(row)
        candidates.pop(identifier, None)
        omitted_rows.pop(identifier, None)
        reasons[identifier] = [f"operator include: {reason}"]
    for identifier, reason in omit.items():
        row = resolver.require_live(identifier, {"wargame"})
        omitted_rows[identifier] = _summary(row)
        required.pop(identifier, None)
        candidates.pop(identifier, None)
        reasons[identifier] = [f"operator omit: {reason}"]

    # A declared true/unknown pressure with no Wargame engagement edge is
    # coverage debt. Applicability predicates are excluded because they say
    # where a rule applies rather than what decision is under pressure.
    uncovered = sorted(
        name for name, value in normalised.items()
        if value in {"true", "unknown"} and name not in covered_pressures
        and name not in {
            p for row in resolver.list("doctrine")
            for p in _values(row.metadata.get("applies_when"))
        }
    )
    return {
        "applicable_doctrines": sorted(doctrines, key=lambda row: row["id"]),
        "required_wargames": [required[k] for k in sorted(required)],
        "candidate_wargames": [candidates[k] for k in sorted(candidates)],
        "omitted_wargames": [omitted_rows[k] for k in sorted(omitted_rows)],
        "unresolved_facts": sorted(unresolved),
        "uncovered_pressures": uncovered,
        "pressure_dispositions": pressure_rows,
        "selection_reasons": {k: reasons[k] for k in sorted(reasons)},
        "pack_order": resolver.pack_order(active_packs or None),
    }


def validate_rulings(document: dict, resolver: KnowledgeResolver) \
        -> tuple[KnowledgeProblem, ...]:
    """Validate a venture-owned structured Rulings document."""

    problems: list[KnowledgeProblem] = []

    def add(code: str, identifier: str, message: str) -> None:
        problems.append(KnowledgeProblem(code, "docs/RULINGS.json",
                                         identifier, message))

    if not isinstance(document, dict):
        return (KnowledgeProblem("rulings-shape", "docs/RULINGS.json", "",
                                 "Rulings document must be an object"),)
    rows = document.get("rulings") or []
    if not isinstance(rows, list):
        return (KnowledgeProblem("rulings-shape", "docs/RULINGS.json", "",
                                 "rulings must be a list"),)
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            add("ruling-shape", "", "ruling is not an object")
            continue
        identifier = str(row.get("id") or "")
        if not RULING_ID.match(identifier):
            add("ruling-id", identifier, f"invalid Ruling id {identifier}")
        if identifier in seen:
            add("duplicate-ruling", identifier,
                f"duplicate Ruling id {identifier}")
        seen.add(identifier)
        wid = str(row.get("wargame") or "")
        resolved = resolver.resolve(wid)
        if resolved is None:
            add("ruling-wargame", wid, f"Wargame {wid} does not resolve")
        elif resolved.state != "live":
            add("ruling-wargame", wid,
                f"Wargame {wid} is retired and cannot receive a live Ruling")
        elif resolved.kind != "wargame":
            add("ruling-wargame", wid, f"{wid} is not a Wargame")
        for doctrine in _values(row.get("doctrines")):
            target = resolver.resolve(doctrine)
            if target is None or target.state != "live" or target.kind != "doctrine":
                add("ruling-doctrine", doctrine,
                    f"Doctrine {doctrine} does not resolve live")
        departures = row.get("departures") or []
        if isinstance(departures, list):
            for departure in departures:
                if not isinstance(departure, dict):
                    add("departure-shape", identifier,
                        "departure must be an object")
                    continue
                doctrine = str(departure.get("doctrine") or "")
                if not str(departure.get("reason") or "").strip():
                    add("departure-reason", doctrine,
                        f"departure from {doctrine} needs a reason")
                target = resolver.resolve(doctrine)
                if target is None or target.state != "live" or target.kind != "doctrine":
                    add("departure-doctrine", doctrine,
                        f"departure Doctrine {doctrine} does not resolve live")
        changes = row.get("binding_scope_changes") or []
        if isinstance(changes, list):
            for change in changes:
                if not isinstance(change, dict):
                    add("binding-change-shape", identifier,
                        "binding scope change must be an object")
                    continue
                doctrine = str(change.get("doctrine") or "")
                refs = ("adr", "adr_ref", "operator", "operator_ref",
                        "approval_ref")
                if not any(str(change.get(key) or "").strip() for key in refs):
                    add("binding-change-approval", doctrine,
                        f"binding scope change for {doctrine} needs an ADR or operator reference")
    selection = document.get("selection_log") or []
    if isinstance(selection, list):
        for row in selection:
            if not isinstance(row, dict):
                add("selection-shape", "", "selection row must be an object")
                continue
            wid = str(row.get("wargame") or "")
            target = resolver.resolve(wid)
            if target is None or target.state != "live" or target.kind != "wargame":
                state = "retired" if target and target.state == "retired" else "unresolved"
                add("selection-wargame", wid,
                    f"selection Wargame {wid} is {state}")
            if not str(row.get("reason") or "").strip():
                add("selection-reason", wid,
                    f"selection or omission of {wid} needs a reason")
    return tuple(problems)
