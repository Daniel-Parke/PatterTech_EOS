"""Semantic checks S001-S007 and S009-S019.

S008 checked that a fact declared canonical in one file was not
restated in another. No file ever declared canonical_facts, so it had
no subscribers and never fired once; it was withdrawn in v2.1 with the
rest of the dead weight (ADR-0006 decision 8). The id is not reused.
Exact-string ownership over teaching prose was the reason nothing
subscribed: it would flag every deliberate restatement in TOUR.md and
OPERATORS_GUIDE.md.

Severity: the S-series lands as ERRORS. The repository is clean under
the series, so the P4 flip has happened: a new semantic defect is a
build failure, not an item on a list nobody reads. ctx["strict_semantic"]
still forces strict, and ctx["relax_semantic"] = True drops the series
back to warnings for a caller that wants the work list rather than the
gate. The CLI exposes the relaxed form as `--relax-semantic`, and
`--strict-semantic` pins the strict form against a future relaxation.

Exemptions, applied uniformly unless a check says otherwise:

- benchmark/** is the frozen suite (fixtures, holdout, tasks): v1-era
  metadata by design, exempt from v2 semantics, still indexed and
  still under the structural E-series.
- archive/** is verbatim v1 history. It is kept exactly as it was
  written and must not be edited, so a finding against it has no legal
  fix. With the series at error severity an unfixable finding would
  fail every build for ever, which is why archive/** is exempt rather
  than tidied.
- org/logs/** is the append-only session log, and carries the same
  argument as archive/**: a log records what was true when the session
  ran, and rewriting one to satisfy a checker destroys the audit
  trail. Its references are history, not claims about the tree today.
- packs/*/research/** holds imported fragments and drill proposals
  written before a pack was authored. They describe workspaces that
  are not this repository, so their paths and ids are not references
  into it. S006 already treats a directory of research fragments as
  not yet a pack.
- template: true files document syntax (placeholder enums, slot
  values) and are exempt from value-level semantic checks.

WG id references are checked by both E005 (the v1 parity port, which
also covers fixtures) and S004 (the generalised scheme table), so an
undefined WG reference reports twice by design until E005 retires.
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import PurePosixPath

from .. import gitfacts
from ..findings import Finding
from ..repo import RepoModel
from . import register
from .structural import strip_code

V1_STATUS = {"draft", "active", "contested", "superseded", "accepted",
             "proposed", "archived"}

V2_AXES = {
    "kind": {"rule", "guide", "recipe", "exemplar", "stack-profile", "fact", "record"},
    "authority": {"binding", "default", "advisory", "preference", "none"},
    "lifecycle": {"draft", "experimental", "active", "contested", "superseded", "archived"},
    "basis": {"decision", "law", "standard", "empirical-evidence", "local-observation"},
    "evidence_grade": {"controlled", "observational", "anecdotal", "asserted", "not-applicable"},
    "volatility": {"stable", "slow", "fast", "event-driven"},
}
V2_SCOPES = {"estate", "venture", "eos-internal"}

DERIVED_GENERATED = {"INDEX.md",
                     "packs/GUIDE_INDEX.md", "packs/INDEX.md",
                     "registry/CAPABILITIES.md", "registry/LESSONS.md",
                     "org/TASKS.md", "org/STATE.md"}

PATH_EXTS = (".md", ".py", ".json", ".yaml")
PATH_BAD_CHARS = set("*<>{}$#()\\ \t")
# Naming patterns, not references: SU-YYYY-WW.md, report-MM.json.
PLACEHOLDER_SEGMENT = re.compile(r"(?<![A-Za-z0-9])(YYYY|MM|DD|WW|HH|NNN?N?)(?![A-Za-z0-9])")

ID_SCHEMES = {
    "WG": re.compile(r"\bWG-[A-Z]+-\d{3}\b"),
    "ADR": re.compile(r"\bADR-\d{4}\b"),
    "PB": re.compile(r"\bPB-E\d{2}\b"),
    "S": re.compile(r"\bS-\d{4}\b"),
}

# An id whose number is all zeros is the documented placeholder shape.
ZERO_ID = re.compile(r"-0+$")
# A possessive immediately before an id gives it to another venture.
OWNED_ELSEWHERE = re.compile(r"(?:\w+'s|\bits|\btheir)\s+$", re.I)

ESTATE_ROW_REQUIRED = ("role", "status")
ESTATE_ROW_ALLOWED = {
    "governed",
    "path", "remote", "role", "status", "stack", "owns", "does_not_own",
    "commands", "agent_files", "eos_pin", "interacts_with", "notes", "built",
}
ESTATE_TOP_REQUIRED = ("version", "updated", "root", "repos")


STRICT_DEFAULT = True

# Verbatim material and out-of-tree material: see the module docstring.
EXEMPT_PREFIXES = ("benchmark/", "archive/", "org/logs/")
RESEARCH_SEGMENT = re.compile(r"^packs/[^/]+/research/")


def _sev(ctx: dict) -> str:
    if ctx.get("strict_semantic"):
        return "error"
    if ctx.get("relax_semantic"):
        return "warn"
    return "error" if STRICT_DEFAULT else "warn"


def _f(ctx, check, path, msg):
    return Finding(check, _sev(ctx), path, msg)


def _semantic_scope(rec) -> bool:
    """True when the record is inside the v2 semantic contract."""
    if rec.path.startswith(EXEMPT_PREFIXES):
        return False
    if RESEARCH_SEGMENT.match(rec.path):
        return False
    if not rec.fm.present:
        return False
    if rec.fm.data.get("template"):
        return False
    return True


def _past_month(value: str, today: date) -> bool:
    m = re.match(r"^(\d{4})-(\d{2})$", value.strip())
    if not m:
        return False
    y, mo = int(m.group(1)), int(m.group(2))
    if not 1 <= mo <= 12:
        return False
    return (y, mo) < (today.year, today.month)


# --- S001 status and axis enums ----------------------------------------


@register("S001")
def check_s001_enums(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    out = []
    for rec in model.files:
        if not _semantic_scope(rec):
            continue
        fm = rec.fm.data
        if "kind" in fm:
            for axis, allowed in V2_AXES.items():
                value = fm.get(axis)
                if isinstance(value, str) and value and value not in allowed:
                    out.append(_f(ctx, "S001", rec.path, f"invalid {axis}: {value}"))
            scope = fm.get("scope")
            if isinstance(scope, str) and scope \
                    and scope not in V2_SCOPES and not scope.startswith("brand:"):
                out.append(_f(ctx, "S001", rec.path, f"invalid scope: {scope}"))
        elif "status" in fm:
            status = fm.get("status")
            if isinstance(status, str) and status and status not in V1_STATUS:
                out.append(_f(ctx, "S001", rec.path, f"invalid status: {status}"))
    return out


# --- S002 supersession bidirectionality --------------------------------


def _lineage_values(fm: dict, key: str) -> list:
    raw = fm.get(key)
    values = raw if isinstance(raw, list) else [raw] if raw else []
    return [v for v in values
            if isinstance(v, str) and v.strip().lower() not in ("", "null", "none")]


def _resolve_ref(model: RepoModel, value: str):
    value = value.strip()
    rec = model.get(value.lstrip("./"))
    if rec is not None:
        return rec
    for cand in model.files:
        stem = PurePosixPath(cand.path).stem
        if stem == value or stem.startswith(value + "-") or stem.startswith(value + "."):
            return cand
    return None


def _points_back(model: RepoModel, target, back_key: str, origin) -> bool:
    if not target.fm.present:
        return False
    for back in _lineage_values(target.fm.data, back_key):
        resolved = _resolve_ref(model, back)
        if resolved is not None and resolved.path == origin.path:
            return True
    return False


# A lineage reference into a git tag, for example
# archive/v1-final:GUIDE.md. ADR-0003 moved the archive of record from a
# directory to a pushed tag, and a tag is immutable: the superseded file
# cannot be edited to point back, so bidirectionality is impossible by
# construction rather than by omission. Such a reference is terminal.
TAG_REF = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]*:[A-Za-z0-9][A-Za-z0-9._/-]*$")


@register("S002")
def check_s002_supersession(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    out = []
    pairs = (("supersedes", "superseded_by"), ("superseded_by", "supersedes"))
    for rec in model.files:
        if not _semantic_scope(rec):
            continue
        for key, back_key in pairs:
            for value in _lineage_values(rec.fm.data, key):
                if TAG_REF.match(value.strip()):
                    continue
                target = _resolve_ref(model, value)
                if target is None:
                    out.append(_f(ctx, "S002", rec.path,
                                  f"{key} reference does not resolve: {value}"))
                elif not _points_back(model, target, back_key, rec):
                    out.append(_f(ctx, "S002", rec.path,
                                  f"{key} {value} does not point back via {back_key}"))
    return out


# --- S003 backtick path references -------------------------------------


def _fenceless(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def _path_tokens(text: str):
    for token in re.findall(r"`([^`\n]+)`", _fenceless(text)):
        token = token.strip()
        if "/" not in token or ":" in token:
            continue
        if not token.endswith(PATH_EXTS):
            continue
        if PATH_BAD_CHARS.intersection(token):
            continue
        if PLACEHOLDER_SEGMENT.search(token):
            continue
        yield token.lstrip("./")


@register("S003")
def check_s003_path_references(ctx: dict) -> list:
    """Backticked paths must resolve, where they claim this repository.

    Two narrowings keep the check honest now that it fails a build.
    A token carrying a placeholder run (SU-YYYY-WW.md) is a naming
    pattern, not a reference. And a token is a reference into this tree
    only when its leading segment is a directory of this repository:
    prose that documents another workspace, a venture repo or a drill
    scratch directory is not making a claim about this one.

    The second rule used to hide a whole class: a reference into a tree
    this repository no longer has resolved to nothing and was not
    reported, so a moved file was caught and a deleted tree was not.
    That is exactly the staleness a migration produces, and it is how
    GOVERNANCE.md sat pointing at doctrine/WARGAME_INDEX.md unseen.
    Trees we deliberately retired are named in
    archive/RETIRED_IDS.json and a reference into one is a finding
    again. Prose about a venture repo stays exempt, because that was
    never a claim about this tree.
    """
    model: RepoModel = ctx["model"]
    retired = retired_paths(model)
    out = []
    for rec in model.files:
        if not _semantic_scope(rec):
            continue
        for token in sorted(set(_path_tokens(rec.text))):
            gone = next((r for r in retired if token.startswith(r)), None)
            if gone:
                out.append(_f(ctx, "S003", rec.path,
                              f"reference into the retired tree {gone}: "
                              f"{token}; it is at the archive/v1-final tag"))
                continue
            if not _anchored(model, token):
                continue
            if not model.exists(token):
                out.append(_f(ctx, "S003", rec.path,
                              f"path reference does not resolve: {token}"))
    return out


def retired_paths(model: RepoModel) -> list:
    """Prefixes this repository deliberately no longer has."""
    raw = model.read("archive/RETIRED_IDS.json")
    if not raw:
        return []
    try:
        return list(json.loads(raw).get("retired_paths") or [])
    except ValueError:
        return []


def _anchored(model: RepoModel, token: str) -> bool:
    """True when the token's leading segment is a tree of this repo."""
    head = token.split("/", 1)[0]
    if not head or head in (".", ".."):
        return False
    return (model.root / head).is_dir()


# --- S004 generalised id references ------------------------------------


def _id_definitions(model: RepoModel) -> dict:
    """Every id the repository defines, wherever the defining file sits.

    Exemptions govern what gets checked, never what exists: a wargame
    under benchmark/fixtures/ still defines its id, and the derived
    indexes reference it, so excluding it here would report the index
    as broken when it is exactly right.
    """
    defs: dict = {"WG": set(), "ADR": set(), "PB": set(), "S": set()}
    for rec in model.files:
        stem = PurePosixPath(rec.path).stem
        # The filename carries the id. Keying on type: wargame missed
        # every v1 wargame migrated into a pack, because those carry
        # type: guide, so their ids read as undefined the moment the
        # archived originals left the tree.
        if rec.fm.present:
            m = re.match(r"WG-[A-Z]+-\d{3}", stem)
            if m:
                defs["WG"].add(m.group(0))
        if rec.path.startswith("org/decisions/"):
            m = re.match(r"ADR-\d{4}", stem)
            if m:
                defs["ADR"].add(m.group(0))
        if re.match(r"S-\d{4}$", stem) and "/logs/" in rec.path:
            defs["S"].add(stem)
    playbooks = model.read("org/PLAYBOOKS.md")
    if playbooks:
        defs["PB"] = set(ID_SCHEMES["PB"].findall(playbooks))
    return defs


@register("S004")
def check_s004_id_references(ctx: dict) -> list:
    """Ids cited in prose must be defined here, where they claim to be.

    Two references are not claims about this repository's id space. An
    all-zero id (WG-MOD-000, S-0000, ADR-0000) is the documented
    placeholder for the shape of an id. And an id carrying a possessive
    ("Venture A's ADR-0003", "its ADR-0011") belongs to the venture named
    beside it: ADR numbering is per repository, and the estate cites
    venture rulings by owner. An id that also appears unqualified
    somewhere is still checked.

    A third case is an id whose defining file was retired to a pushed
    tag under ADR-0003. It is still defined and still locatable, so
    archive/RETIRED_IDS.json counts as a definition. Without that,
    moving the v1 tree to a tag would have turned 33 real ids into 79
    dangling references, and the only fix would have been rewording
    every provenance line in the repository.
    """
    from .structural import retired_ids

    model: RepoModel = ctx["model"]
    defs = _id_definitions(model)
    defs["WG"] = set(defs.get("WG") or set()) | retired_ids(model)
    out = []
    for rec in model.files:
        if not _semantic_scope(rec):
            continue
        prose = strip_code(rec.text)
        for scheme, pattern in ID_SCHEMES.items():
            if scheme == "PB" and rec.path == "org/PLAYBOOKS.md":
                continue
            for ref in sorted(_unqualified_refs(prose, pattern)):
                if ZERO_ID.search(ref):
                    continue
                if ref not in defs[scheme]:
                    out.append(_f(ctx, "S004", rec.path,
                                  f"reference to undefined id {ref}"))
    return out


def _unqualified_refs(prose: str, pattern) -> set:
    """Ids cited without a possessive naming another venture as owner."""
    found = set()
    for m in pattern.finditer(prose):
        if OWNED_ELSEWHERE.search(prose[:m.start()]):
            continue
        found.add(m.group(0))
    return found


# --- S005 derived files need a registered generator --------------------


@register("S005")
def check_s005_derived(ctx: dict) -> list:
    """Every derived:true file must come from a registered generator.

    Drift for the two index generators is E001's finding; S005 catches
    derived-flagged files nothing regenerates, which can only be
    hand-maintained and therefore drift silently.
    """
    model: RepoModel = ctx["model"]
    out = []
    for rec in model.files:
        if not _semantic_scope(rec):
            continue
        if rec.fm.data.get("derived") and rec.path not in DERIVED_GENERATED:
            out.append(_f(ctx, "S005", rec.path,
                          "derived file has no registered generator"))
    return out


# --- S006 pack organ completeness --------------------------------------


@register("S006")
def check_s006_module_organs(ctx: dict) -> list:
    """Every built pack carries its invariant organs.

    packs/PACK_SHAPE.md fixes the contract: PACK.md (whose first
    paragraph is the always-loaded metadata), guides/ for the decision
    guides, and CHECKS.md for the evaluation criteria. Archived v1
    modules under archive/ are history and are not held to it.
    """
    model: RepoModel = ctx["model"]
    packs: dict = {}
    for rec in model.files:
        parts = rec.path.split("/")
        if parts[0] == "packs" and len(parts) >= 3:
            packs.setdefault(parts[1], set()).add(rec.path)
    out = []
    for pack in sorted(packs):
        base = f"packs/{pack}"
        paths = packs[pack]
        # A directory holding only research fragments is not yet a pack.
        if all(p.startswith(f"{base}/research/") for p in paths):
            continue
        for organ in ("PACK.md", "CHECKS.md"):
            if f"{base}/{organ}" not in paths:
                out.append(_f(ctx, "S006", base, f"pack missing {organ}"))
        if not any(p.startswith(f"{base}/guides/") for p in paths):
            out.append(_f(ctx, "S006", base, "pack missing guides/"))
    return out


# --- S007 machine facts vs git reality ---------------------------------


FACTS_BLOCK = re.compile(r"```facts\n(.*?)```", re.S)


@register("S007")
def check_s007_machine_facts(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    out = []
    for rec in model.files:
        if not _semantic_scope(rec):
            continue
        if not rec.path.endswith("org/STATE.md") and rec.path != "org/STATE.md":
            continue
        m = FACTS_BLOCK.search(rec.text)
        if not m:
            continue
        facts = {}
        for line in m.group(1).splitlines():
            km = re.match(r"^([a-z_]+):\s*(.+)$", line.strip())
            if km:
                facts[km.group(1)] = km.group(2).strip()
        if "branch" in facts:
            actual = gitfacts.current_branch(model.root)
            if actual is not None and actual != facts["branch"]:
                out.append(_f(ctx, "S007", rec.path,
                              f"machine fact branch: {facts['branch']} but git says {actual}"))
        if "commit" in facts:
            # A derived view records the commit it was generated from,
            # and that commit is behind HEAD the moment the view is
            # committed. Equality can never hold in a repository that
            # keeps moving, so the honest invariant is ancestry: the
            # recorded commit must exist and must be reachable from
            # HEAD. A commit that does not resolve, or that sits on a
            # branch HEAD does not contain, is the real drift.
            head = gitfacts.rev_parse(model.root, "HEAD")
            fact = facts["commit"]
            if head is not None:
                if not gitfacts.object_exists(model.root, f"{fact}^{{commit}}"):
                    out.append(_f(ctx, "S007", rec.path,
                                  f"machine fact commit: {fact} does not resolve"))
                elif not gitfacts.is_ancestor(model.root, fact, head):
                    out.append(_f(ctx, "S007", rec.path,
                                  f"machine fact commit: {fact} is not an ancestor of HEAD {head[:12]}"))
        if "tag" in facts:
            known = gitfacts.tags(model.root)
            if known and facts["tag"] not in known:
                out.append(_f(ctx, "S007", rec.path,
                              f"machine fact tag: {facts['tag']} is not a git tag"))
    return out


# --- S009 cadence overdue ----------------------------------------------


def _table_rows(text: str) -> list:
    rows = []
    for line in text.splitlines():
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            rows.append(cells)
    return rows


def _parse_due(value: str):
    m = re.match(r"^(\d{4})-(\d{2})(?:-(\d{2}))?$", value.strip())
    if not m:
        return None
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3) or 1))
    except ValueError:
        return None


@register("S009")
def check_s009_cadence_overdue(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    today = ctx["today"]
    out = []
    cadence = model.read("org/CADENCE.md")
    if cadence:
        for cells in _table_rows(cadence):
            if len(cells) >= 5 and cells[0] not in ("Cadence", "---") \
                    and not cells[0].startswith("-"):
                due = _parse_due(cells[4])
                if due and due < today:
                    out.append(_f(ctx, "S009", "org/CADENCE.md",
                                  f"cadence '{cells[0]}' overdue: next_due {cells[4]}"))
    machine = model.read("org/cadence.json")
    if machine:
        try:
            rows = json.loads(machine)
        except ValueError:
            return out + [Finding("S009", "error", "org/cadence.json", "malformed JSON")]
        for row in rows if isinstance(rows, list) else []:
            due = _parse_due(str(row.get("next_due", "")))
            if due and due < today:
                out.append(_f(ctx, "S009", "org/cadence.json",
                              f"cadence '{row.get('id', '?')}' overdue: "
                              f"next_due {row.get('next_due')}, "
                              f"procedure {row.get('procedure', 'unrecorded')}"))
    return out


# --- estate manifest narrow reader (shared by S010 and S012) -----------


def read_repos_yaml(text: str):
    """Narrow reader for estate/repos.yaml until the JSON migration lands.

    Handles exactly the manifest's shape: top-level scalars, a repos:
    map of repo blocks, scalar keys, dash lists, nested command maps
    and indented continuation lines. Returns (top, repos, errors).
    """
    top: dict = {}
    repos: dict = {}
    errors: list = []
    current_repo = None
    current_key = None
    in_repos = False
    for lineno, raw in enumerate(text.splitlines(), start=1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        if indent == 0:
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
            if not m:
                errors.append((lineno, f"unparseable line: {line}"))
                continue
            key, value = m.group(1), m.group(2).strip().strip('"')
            if key == "repos":
                in_repos = True
            else:
                top[key] = value
            current_repo, current_key = None, None
        elif in_repos and indent == 2:
            m = re.match(r"^([A-Za-z0-9_.-]+):\s*$", line)
            if not m:
                errors.append((lineno, f"unparseable repo row: {line}"))
                continue
            current_repo = m.group(1)
            repos[current_repo] = {}
            current_key = None
        elif current_repo and indent == 4:
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", line)
            if not m:
                errors.append((lineno, f"unparseable repo key: {line}"))
                continue
            current_key = m.group(1)
            repos[current_repo][current_key] = m.group(2).strip()
        elif current_repo and current_key and indent >= 6:
            entry = repos[current_repo]
            if line.startswith("- "):
                if not isinstance(entry[current_key], list):
                    entry[current_key] = []
                entry[current_key].append(line[2:].strip())
            elif isinstance(entry[current_key], list):
                entry[current_key][-1] = f"{entry[current_key][-1]} {line}"
            elif re.match(r"^[A-Za-z_][A-Za-z0-9_-]*:\s", line):
                if not isinstance(entry[current_key], dict):
                    entry[current_key] = {}
                k, v = line.split(":", 1)
                entry[current_key][k.strip()] = v.strip()
            else:
                entry[current_key] = f"{entry[current_key]} {line}".strip()
        else:
            errors.append((lineno, f"unexpected indentation: {line}"))
    return top, repos, errors


def _load_estate(model: RepoModel):
    """Prefer estate/repos.json once the migration lands; fall back to YAML."""
    as_json = model.read("estate/repos.json")
    if as_json is not None:
        try:
            doc = json.loads(as_json)
        except ValueError:
            return None, None, "estate/repos.json", [(0, "malformed JSON")]
        return doc, doc.get("repos", {}), "estate/repos.json", []
    as_yaml = model.read("estate/repos.yaml")
    if as_yaml is None:
        return None, None, None, []
    top, repos, errors = read_repos_yaml(as_yaml)
    return top, repos, "estate/repos.yaml", errors


# --- S010 cross-registry consistency -----------------------------------


PIN_SHA = re.compile(r"@\s*([0-9a-f]{7,40})\b")


@register("S010")
def check_s010_cross_registry(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    offline = ctx.get("offline", True)
    out = []
    projects = model.read("registry/PROJECTS.md")
    _, repos, manifest_path, _ = _load_estate(model)
    if not projects or repos is None:
        return out
    known_names = set(repos)
    known_dirs = {PurePosixPath(str(row.get("path", "")).replace("\\", "/")).name
                  for row in repos.values() if isinstance(row, dict)}
    reach_targets = list(gitfacts.tags(model.root).values())
    reach_targets += list(gitfacts.remote_tracking_heads(model.root).values())
    remote = gitfacts.remote_heads(model.root, offline)
    if remote:
        reach_targets += list(remote.values())
    for cells in _table_rows(projects):
        if len(cells) < 4 or cells[0] in ("Venture", "---") or cells[0].startswith("-"):
            continue
        venture = cells[0]
        path_dir = PurePosixPath(cells[1].strip("`").replace("\\", "/")).name
        if venture not in known_names and path_dir not in known_names \
                and path_dir not in known_dirs:
            out.append(_f(ctx, "S010", "registry/PROJECTS.md",
                          f"venture {venture} not in the estate manifest ({manifest_path})"))
        for sha in PIN_SHA.findall(cells[3]):
            if not gitfacts.object_exists(model.root, f"{sha}^{{commit}}"):
                out.append(_f(ctx, "S010", "registry/PROJECTS.md",
                              f"venture {venture} pin {sha} does not resolve"))
            elif reach_targets and not any(
                    gitfacts.is_ancestor(model.root, sha, t) for t in reach_targets):
                out.append(_f(ctx, "S010", "registry/PROJECTS.md",
                              f"venture {venture} pin {sha} not reachable from a pushed tag or origin head"))
    return out


# --- S011 CHANGELOG vs tags --------------------------------------------


SEMVER_TAG = re.compile(r"^v\d+\.\d+\.\d+$")
CHANGELOG_HEADING = re.compile(r"^## v(\d+\.\d+\.\d+)", re.M)


@register("S011")
def check_s011_changelog_tags(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    out = []
    text = model.read("CHANGELOG.md")
    if text is None:
        return out
    versions = CHANGELOG_HEADING.findall(text)
    known = {name: sha for name, sha in gitfacts.tags(model.root).items()
             if SEMVER_TAG.match(name)}
    if gitfacts.current_branch(model.root) is None:
        return out
    for v in versions:
        if f"v{v}" not in known:
            out.append(_f(ctx, "S011", "CHANGELOG.md",
                          f"heading v{v} has no matching git tag"))
    for name in sorted(known):
        if name[1:] not in versions:
            out.append(_f(ctx, "S011", "CHANGELOG.md",
                          f"git tag {name} has no CHANGELOG heading"))
    if known:
        latest = max(known, key=lambda n: tuple(int(x) for x in n[1:].split(".")))
        count = gitfacts.commit_count(model.root, f"{latest}..HEAD")
        um = re.search(r"^## Unreleased.*?$(.*?)(?=^## |\Z)", text, re.M | re.S)
        has_entries = bool(um and re.search(r"^- ", um.group(1), re.M))
        if count and count > 0 and not has_entries:
            out.append(_f(ctx, "S011", "CHANGELOG.md",
                          f"{count} commits since {latest} but the Unreleased section is empty"))
        if count == 0 and has_entries:
            out.append(_f(ctx, "S011", "CHANGELOG.md",
                          f"Unreleased section has entries but no commits since {latest}"))
    return out


# --- S012 estate manifest schema ---------------------------------------


@register("S012")
def check_s012_estate_schema(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    top, repos, manifest_path, errors = _load_estate(model)
    if manifest_path is None:
        return []
    out = []
    for lineno, msg in errors:
        out.append(_f(ctx, "S012", manifest_path, f"line {lineno}: {msg}"))
    if top is None or repos is None:
        return out
    for key in ESTATE_TOP_REQUIRED:
        if key == "repos":
            if not repos:
                out.append(_f(ctx, "S012", manifest_path, "no repos rows"))
        elif key not in top:
            out.append(_f(ctx, "S012", manifest_path, f"missing top-level key: {key}"))
    for name, row in repos.items():
        if not isinstance(row, dict):
            out.append(_f(ctx, "S012", manifest_path, f"repo {name}: not a mapping"))
            continue
        for key in ESTATE_ROW_REQUIRED:
            if not row.get(key):
                out.append(_f(ctx, "S012", manifest_path, f"repo {name}: missing {key}"))
        for key in sorted(set(row) - ESTATE_ROW_ALLOWED):
            out.append(_f(ctx, "S012", manifest_path, f"repo {name}: unknown key {key}"))
    return out


# --- S013 domain coverage matrix ----------------------------------------

COVERAGE_PATH = "registry/coverage.json"
COVERAGE_SCHEMA = "kernel/schemas/coverage.schema.json"


@register("S013")
def check_s013_coverage_matrix(ctx: dict) -> list:
    """The coverage matrix agrees with its schema and with the packs.

    The matrix exists to make omissions visible. It did the opposite:
    twelve rows read status built beside evaluation_method "None yet",
    carried no worked_example key at all, and listed evidence as the
    prose string "18 records in registry/evidence.json". Nothing
    validated the file, so none of that was a finding.

    Four things are checked here, because each of them failed:
    the file matches its schema; every built row's pack directory
    exists and every pack directory has a row; every cited path
    resolves; and every EV id resolves in the evidence ledger.
    """
    model: RepoModel = ctx["model"]
    raw = model.read(COVERAGE_PATH)
    if raw is None:
        return []
    out = []
    try:
        cov = json.loads(raw)
    except ValueError as exc:
        return [_f(ctx, "S013", COVERAGE_PATH, f"not valid JSON: {exc}")]

    schema_raw = model.read(COVERAGE_SCHEMA)
    if schema_raw is not None:
        try:
            import jsonschema
        except ImportError:
            out.append(_f(ctx, "S013", COVERAGE_PATH,
                          "jsonschema missing, matrix not validated against "
                          "its schema; install tools/requirements.txt"))
        else:
            validator = jsonschema.Draft202012Validator(json.loads(schema_raw))
            for err in sorted(validator.iter_errors(cov), key=lambda e: list(e.path)):
                where = "/".join(str(p) for p in err.path) or "(root)"
                out.append(_f(ctx, "S013", COVERAGE_PATH, f"{where}: {err.message}"))

    rows = cov.get("rows") or []
    ledger_raw = model.read("registry/evidence.json")
    known_ev = set()
    if ledger_raw:
        try:
            known_ev = {r["id"] for r in json.loads(ledger_raw).get("records", [])}
        except (ValueError, KeyError, TypeError):
            known_ev = set()

    charted = set()
    for row in rows:
        cap = row.get("capability", "(unnamed)")
        if row.get("status") != "built":
            continue
        pack = (row.get("pack") or "").rstrip("/")
        if not pack:
            continue
        charted.add(pack)
        if not model.exists(pack):
            out.append(_f(ctx, "S013", COVERAGE_PATH,
                          f"{cap}: built but {pack}/ does not exist"))
            continue
        for cited in row.get("worked_example") or []:
            if not model.exists(cited):
                out.append(_f(ctx, "S013", COVERAGE_PATH,
                              f"{cap}: worked_example does not resolve: {cited}"))
        if known_ev:
            for ev in row.get("evidence_sources") or []:
                if ev not in known_ev:
                    out.append(_f(ctx, "S013", COVERAGE_PATH,
                                  f"{cap}: evidence id not in the ledger: {ev}"))

    # The other direction. A pack with no row is a silent omission, and
    # silence is the one thing the matrix is not allowed to do.
    for rec in model.files:
        parts = rec.path.split("/")
        if len(parts) == 3 and parts[0] == "packs" and parts[2] == "PACK.md":
            base = f"packs/{parts[1]}"
            if base not in charted:
                out.append(_f(ctx, "S013", COVERAGE_PATH,
                              f"{base}/ is a built pack with no coverage row"))
    return out


# --- S014 pack-local fragment ids in the read surface --------------------

FRAG_ID = re.compile(r"\bFRAG-[A-Z0-9-]+-\d{2}\b")


@register("S014")
def check_s014_fragment_citations(ctx: dict) -> list:
    """A pack cites evidence ids, never its own fragment namespace.

    Ten packs kept citing FRAG-* ids in prose after the integrator had
    imported those fragments and assigned real EV ids. 1,035 citations
    pointed at a namespace that existed only inside one file per pack,
    against the rule the agentic-development pack states plainly: cite
    ids, never re-record sources.

    research/ is exempt. It is the pre-import record, and its fragment
    ids are the local namespace sources.fragment.json still uses;
    rewriting one without the other would desync the pair.
    """
    model: RepoModel = ctx["model"]
    out = []
    for rec in model.files:
        if not rec.path.startswith("packs/") or RESEARCH_SEGMENT.match(rec.path):
            continue
        hits = sorted(set(FRAG_ID.findall(strip_code(rec.text))))
        for hit in hits:
            out.append(_f(ctx, "S014", rec.path,
                          f"pack-local fragment id in the read surface: {hit}; "
                          f"cite the EV id the import assigned"))
    return out


# --- S015 pack activation triggers --------------------------------------


@register("S015")
def check_s015_activation_triggers(ctx: dict) -> list:
    """Every built pack carries a machine-readable, non-keyword trigger.

    packs/PACK_SHAPE.md requires it, because routing has to be
    deterministic given the same inputs. Twenty packs stated their
    triggers in prose only, so nothing could evaluate them, and
    contextgen returned a hardcoded empty list: progressive disclosure,
    the whole reason twenty dense packs should cost less than five thin
    modules, was never wired up.
    """
    model: RepoModel = ctx["model"]
    out = []
    for rec in model.files:
        parts = rec.path.split("/")
        if len(parts) != 3 or parts[0] != "packs" or parts[2] != "PACK.md":
            continue
        if not rec.fm.present:
            continue
        fm = rec.fm.data
        if not fm.get("activation_paths"):
            out.append(_f(ctx, "S015", rec.path,
                          "no activation_paths: the pack cannot be reached "
                          "deterministically, so it will never activate"))
        if not fm.get("applies_when"):
            out.append(_f(ctx, "S015", rec.path,
                          "no applies_when: predicates are the real gate "
                          "under packs/PACK_SHAPE.md"))
    return out


@register("S016")
def check_s016_cited_by_is_derived(ctx: dict) -> list:
    """registry/evidence.json's cited_by matches the citations that exist.

    The field used to be written by the fragment importer and meant
    "a pack fragment contributed this record", which is a different
    fact from "a pack cites this record" recorded under the citing
    name. Every record imported from estate-wide research carried an
    empty list while being cited by id in pack prose, so 107 of 448
    read as uncited when 12 actually were.

    The scan is imported from the generator rather than reimplemented
    here. A checker with its own copy of the rule is how the two come
    to disagree, which is the defect this field already had once.

    Regenerate with `python tools/import_fragments.py`.
    """
    import json

    model: RepoModel = ctx["model"]
    raw = model.read("registry/evidence.json")
    if raw is None:
        return []
    try:
        ledger = json.loads(raw)
    except ValueError as exc:
        return [_f(ctx, "S016", "registry/evidence.json",
                   f"not valid JSON: {exc}")]

    try:
        import sys
        root = str(model.root)
        if root not in sys.path:
            sys.path.insert(0, root)
        from tools.import_fragments import scan_citations
    except ImportError as exc:
        return [_f(ctx, "S016", "registry/evidence.json",
                   f"cannot load the citation scanner: {exc}")]

    actual = scan_citations(model.root)

    out = []
    stale = []
    for record in ledger.get("records", []):
        rid = record.get("id")
        recorded = set(record.get("cited_by") or ())
        if actual.get(rid, set()) != recorded:
            stale.append(rid)
    if stale:
        out.append(_f(ctx, "S016", "registry/evidence.json",
                      "cited_by is stale for %d record(s) (%s%s): it is "
                      "derived, so regenerate with "
                      "python tools/import_fragments.py"
                      % (len(stale), ", ".join(stale[:5]),
                         ", ..." if len(stale) > 5 else "")))
    if not ledger.get("research_cutoff"):
        out.append(_f(ctx, "S016", "registry/evidence.json",
                      "no research_cutoff: the ledger cannot say how old "
                      "its own reading is"))
    return out


@register("S017")
def check_s017_evidence_matches_its_schema(ctx: dict) -> list:
    """registry/evidence.json validates against kernel/schemas/evidence.schema.json.

    The schema existed and nothing read it. Two violations had
    accumulated by the time anyone ran it, and both were introduced
    during this review: a derived `research_cutoff` at the top level
    that the schema forbade, and a record whose publication_status was
    outside the enum. A schema nobody validates against is a comment.

    Also holds the licence floor of packs/PACK_SHAPE.md item 11. A
    record may say what the source states, including that the source
    states nothing, but "unknown" means nobody looked and is a gap
    rather than a value.
    """
    import json

    model: RepoModel = ctx["model"]
    raw = model.read("registry/evidence.json")
    schema_raw = model.read("kernel/schemas/evidence.schema.json")
    if raw is None or schema_raw is None:
        return []
    try:
        doc = json.loads(raw)
        schema = json.loads(schema_raw)
    except ValueError as exc:
        return [_f(ctx, "S017", "registry/evidence.json",
                   f"not valid JSON: {exc}")]

    out = []
    try:
        import jsonschema
    except ImportError:
        out.append(_f(ctx, "S017", "registry/evidence.json",
                      "jsonschema is not installed, so the ledger was not "
                      "validated against its schema on this run"))
    else:
        errors = sorted(jsonschema.Draft202012Validator(schema).iter_errors(doc),
                        key=lambda e: list(e.path))
        for err in errors[:10]:
            where = "/".join(str(p) for p in err.path) or "(root)"
            out.append(_f(ctx, "S017", "registry/evidence.json",
                          f"schema: {where}: {err.message}"))

    unknown = [r.get("id") for r in doc.get("records", [])
               if str(r.get("licence", "")).strip().lower() == "unknown"]
    if unknown:
        out.append(_f(ctx, "S017", "registry/evidence.json",
                      "%d record(s) carry licence 'unknown' (%s%s): read the "
                      "licence off the source, or record that the source "
                      "states none. PACK_SHAPE item 11 wants a fact here."
                      % (len(unknown), ", ".join(unknown[:5]),
                         ", ..." if len(unknown) > 5 else "")))
    return out


# --- the lessons ledger: S018 conflicts, S019 schema --------------------

LESSONS_PATH = "registry/lessons.json"
LESSON_SCHEMA = "kernel/schemas/lesson.schema.json"

# How a lesson row may record that it has settled a contradiction it
# names. GOVERNANCE's five precedence rules decide which of the first
# three applies; the fourth is Daniel ruling in the room, which is
# authority rather than derivation and therefore has to say what he
# ruled.
CONFLICT_RESOLUTIONS = ("stricter-applies", "scoped-differently",
                        "superseded", "operator-ruling")
_RESOLUTION_LIST = ", ".join(CONFLICT_RESOLUTIONS)
_LESSON_EV = re.compile(r"\bEV-\d{4}\b")


def _lesson_rows(model: RepoModel):
    """(rows, problem): the ledger's lesson rows, or why they are absent.

    Absent is not a problem: registry/lessons.json is new in v2.1 and a
    repository without one simply has no lessons to check.
    """
    raw = model.read(LESSONS_PATH)
    if raw is None:
        return [], None
    try:
        doc = json.loads(raw)
    except ValueError as exc:
        return [], "not valid JSON: %s" % exc
    if isinstance(doc, list):
        rows = doc
    elif isinstance(doc, dict):
        rows = doc.get("lessons") or doc.get("rows") or doc.get("records") or []
    else:
        return [], "the ledger is neither an object nor a list"
    return [r for r in rows if isinstance(r, dict)], None


def _conflict_entries(row: dict):
    """(ref, resolution, note) per entry in the row's conflicts_with.

    One shape is read, because one shape is what
    kernel/schemas/lesson.schema.json permits: conflicts_with holds ref
    strings, and conflict_resolutions maps a ref to an object carrying a
    resolution and a note. This used to read two more shapes, an object
    inside conflicts_with and a bare string resolution, and its docstring
    said either satisfied the rule. Neither validates, so S018 was
    accepting rows S019 rejects and the tests that proved otherwise ran
    without the real schema installed.

    Anything the schema does not permit yields no resolution here, which
    reports as unresolved: the shape itself is S019's finding to make,
    and this check does not restate it.
    """
    raw = row.get("conflicts_with")
    entries = raw if isinstance(raw, list) else [raw] if raw else []
    resolutions = row.get("conflict_resolutions")
    resolutions = resolutions if isinstance(resolutions, dict) else {}
    for entry in entries:
        if not isinstance(entry, str):
            yield "(not a ref string)", "", ""
            continue
        ref = entry.strip()
        recorded = resolutions.get(ref)
        if isinstance(recorded, dict):
            yield (ref, str(recorded.get("resolution") or "").strip(),
                   str(recorded.get("note") or "").strip())
        else:
            yield ref, "", ""


@register("S018")
def check_s018_lesson_conflicts(ctx: dict) -> list:
    """A lesson naming a contradiction must say how it was settled.

    ADR-0006 decision 2: the conflict pass runs before Daniel sees a
    finding, and the resolution is recorded on the row it belongs to.
    Without this check the contradiction is caught later, by whoever
    next reads two rules that disagree, which is how a ledger of
    decisions turns into a ledger of arguments nobody had.

    So: every entry in a row's conflicts_with carries a resolution, one
    of stricter-applies, scoped-differently, superseded or
    operator-ruling, and every resolution carries a note saying what
    settled it. The note rule is the schema's rule, not a stricter one
    invented here: a resolution nobody can read cannot be reviewed, and
    a row that says Daniel decided without saying what cannot be argued
    with later.

    What this does not do: it does not check that the thing a row
    conflicts with exists. Conflicts are named against packs, guides,
    policies and prior lessons, which live in four different id spaces,
    and a reference check across all four is a different check from
    this one.
    """
    model: RepoModel = ctx["model"]
    rows, problem = _lesson_rows(model)
    if problem:
        return [_f(ctx, "S018", LESSONS_PATH, problem)]
    out = []
    for row in rows:
        rid = row.get("id") or "(row with no id)"
        for ref, resolution, note in _conflict_entries(row):
            if not resolution:
                out.append(_f(ctx, "S018", LESSONS_PATH,
                              "%s: conflicts_with %s is unresolved; record it "
                              "in conflict_resolutions as {resolution, note}, "
                              "the resolution being one of %s"
                              % (rid, ref, _RESOLUTION_LIST)))
            elif resolution not in CONFLICT_RESOLUTIONS:
                out.append(_f(ctx, "S018", LESSONS_PATH,
                              "%s: unknown conflict resolution for %s: %s; "
                              "expected one of %s"
                              % (rid, ref, resolution, _RESOLUTION_LIST)))
            elif not note:
                out.append(_f(ctx, "S018", LESSONS_PATH,
                              "%s: conflict with %s is resolved %s with "
                              "nothing recorded; note the condition, the "
                              "ruling or the successor that settles it"
                              % (rid, ref, resolution)))
    return out


@register("S019")
def check_s019_lessons_match_the_schema(ctx: dict) -> list:
    """registry/lessons.json validates, and its ids resolve.

    The same rule evidence.json gets from S017: a schema nobody
    validates against is a comment. Three things are checked here.

    The ledger matches kernel/schemas/lesson.schema.json. Ids are
    unique, which the schema cannot express and which matters because
    informs, conflicts_with and supersedes all address a row by id, so
    a duplicate makes every link into it ambiguous. And every EV id a
    row cites resolves in registry/evidence.json, because a study row
    whose source is not in the ledger cannot be re-read.
    """
    model: RepoModel = ctx["model"]
    rows, problem = _lesson_rows(model)
    if problem:
        return [_f(ctx, "S019", LESSONS_PATH, problem)]
    raw = model.read(LESSONS_PATH)
    if raw is None:
        return []

    out = []
    schema_raw = model.read(LESSON_SCHEMA)
    if schema_raw is None:
        out.append(_f(ctx, "S019", LESSONS_PATH,
                      "%s is missing, so the ledger was not validated "
                      "against a schema on this run" % LESSON_SCHEMA))
    else:
        try:
            import jsonschema
        except ImportError:
            out.append(_f(ctx, "S019", LESSONS_PATH,
                          "jsonschema is not installed, so the ledger was not "
                          "validated against its schema on this run"))
        else:
            schema = json.loads(schema_raw)
            doc = json.loads(raw)
            errors = sorted(
                jsonschema.Draft202012Validator(schema).iter_errors(doc),
                key=lambda e: list(e.path))
            for err in errors[:10]:
                where = "/".join(str(p) for p in err.path) or "(root)"
                out.append(_f(ctx, "S019", LESSONS_PATH,
                              "schema: %s: %s" % (where, err.message)))

    seen = set()
    for row in rows:
        rid = row.get("id")
        if not rid:
            out.append(_f(ctx, "S019", LESSONS_PATH, "a row carries no id"))
            continue
        if rid in seen:
            out.append(_f(ctx, "S019", LESSONS_PATH,
                          "duplicate lesson id %s: every link into it is "
                          "ambiguous" % rid))
        seen.add(rid)

    ledger_raw = model.read("registry/evidence.json")
    known_ev = set()
    if ledger_raw:
        try:
            known_ev = {r.get("id") for r
                        in json.loads(ledger_raw).get("records", [])}
        except (ValueError, AttributeError, TypeError):
            known_ev = set()
    if known_ev:
        for row in rows:
            rid = row.get("id") or "(row with no id)"
            for ev in sorted(set(_LESSON_EV.findall(json.dumps(row)))):
                if ev not in known_ev:
                    out.append(_f(ctx, "S019", LESSONS_PATH,
                                  "%s: cites %s, which is not in "
                                  "registry/evidence.json" % (rid, ev)))
    return out
