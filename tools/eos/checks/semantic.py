"""Semantic checks S001-S012.

Severity: the S-series lands as ERRORS. The repository is clean under
the series, so the P4 flip has happened: a new semantic defect is a
build failure, not an item on a list nobody reads. ctx["strict_semantic"]
still forces strict, and ctx["relax_semantic"] = True drops the series
back to warnings for a caller that wants the work list rather than the
gate. There is no CLI flag for the relaxed form yet; wiring one is a
one-line change in tools/eos/cli.py.

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
                     "registry/CAPABILITIES.md",
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

    The cost of the second rule is stated plainly: a reference into a
    whole tree this repository no longer has resolves to nothing and is
    no longer reported. A moved file is caught; a deleted tree is not.
    """
    model: RepoModel = ctx["model"]
    out = []
    for rec in model.files:
        if not _semantic_scope(rec):
            continue
        for token in sorted(set(_path_tokens(rec.text))):
            if not _anchored(model, token):
                continue
            if not model.exists(token):
                out.append(_f(ctx, "S003", rec.path,
                              f"path reference does not resolve: {token}"))
    return out


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
        if rec.fm.present and rec.fm.data.get("type") == "wargame":
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
    """
    model: RepoModel = ctx["model"]
    defs = _id_definitions(model)
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


# --- S008 canonical-fact duplication -----------------------------------


@register("S008")
def check_s008_canonical_facts(ctx: dict) -> list:
    model: RepoModel = ctx["model"]
    owners = []
    for rec in model.files:
        if not _semantic_scope(rec):
            continue
        facts = rec.fm.data.get("canonical_facts")
        if isinstance(facts, list):
            owners.append((rec, [x for x in facts if len(x) >= 8]))
    out = []
    for owner, facts in owners:
        for fact in facts:
            for rec in model.files:
                if rec.path == owner.path or not _semantic_scope(rec):
                    continue
                if rec.fm.data.get("derived"):
                    continue
                if fact in rec.text:
                    out.append(_f(ctx, "S008", rec.path,
                                  f"restates canonical fact owned by {owner.path}: {fact}"))
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
                              f"cadence '{row.get('name', '?')}' overdue: next_due {row.get('next_due')}"))
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
