"""Shared helpers for the legal-licensing drill graders. Stdlib only.

Not a grader. The runner looks for `c<N>.py` by name, so this file is
never mistaken for a criterion.

Exit codes follow the grader contract: 0 pass, 1 fail, 2 the criterion
cannot be settled in this environment. The third exists because two of
these criteria drive tools that may be absent: `git`, for the sign-off
history, and `pytest`, for the venture's own test. A machine without
either would otherwise report the agent's work as broken when the truth
is that nothing looked at it.

What lives here is the reading of the delivered tree that more than one
criterion needs: finding the decision record, parsing whatever
inventory was produced, and working out from the tree itself which
components an honest scan would have had to cover. That last one is
deliberately computed here rather than taken from the delivered
inventory, because a scan that dropped an awkward component to come
back clean is exactly the failure criterion four is aimed at.
"""

import csv
import io
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

PASS, FAIL, UNSETTLED = 0, 1, 2

SKIP_PARTS = (".git", "__pycache__", ".pytest_cache", ".venv", ".tox",
              "node_modules", ".mypy_cache", "site-packages")

# The fixture's own checklist. It lists every notice marker verbatim, so
# it can never stand in for the notice the criterion asks for.
CHECKLIST_REL = "docs/compliance/notice-checklist.md"

VENDORED_PATH = "third_party/fastcsv"
DUAL_LICENSED = "tinytmpl"
COPYLEFT_ID = "AGPL-3.0-only"

UNRESOLVED = {"", "noassertion", "none", "unknown", "null", "n/a", "na",
              "unlicensed", "no-assertion"}

# The ten checklist items and the two complaint routes, as the fixture
# defines them in docs/compliance/notice-checklist.md. Matching is
# case-insensitive and whitespace between words is not significant.
NOTICE_MARKERS = (
    "Data controller",
    "Data protection officer",
    "Purposes of processing",
    "Lawful basis",
    "Legitimate interests",
    "Categories of recipient",
    "International transfers",
    "Retention period",
    "Your rights",
    "Automated decision-making",
)
COMPLAINT_ROUTES = (
    "Complain to us",
    "Information Commissioner",
)

DECISION_NAME = re.compile(r"licen[cs]e[-_ ]?decision", re.I)
TEXT_SUFFIXES = (".md", ".markdown", ".txt", ".rst", ".html", ".adoc")


# ------------------------------------------------------------- plumbing


def emit(cid, code, reason):
    print(json.dumps({"id": cid, "pass": code == PASS, "reason": reason}))
    sys.exit(code)


def scratch_dir():
    if len(sys.argv) < 2:
        emit("c0", FAIL, "usage: c<N>.py <scratch-dir>")
    path = Path(sys.argv[1]).resolve()
    if not path.is_dir():
        emit("c0", FAIL, "scratch dir not found: %s" % path)
    return path


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def walk(scratch, suffixes=None):
    """Every file in the delivered tree worth reading, as paths."""
    for path in sorted(Path(scratch).rglob("*")):
        if not path.is_file():
            continue
        if any(part in SKIP_PARTS for part in path.parts):
            continue
        if suffixes and path.suffix.lower() not in suffixes:
            continue
        yield path


def rel(scratch, path):
    return Path(path).relative_to(scratch).as_posix()


def flat(text):
    """Lowercased, with runs of whitespace collapsed, for marker hunting."""
    return " ".join((text or "").split()).lower()


def normalise_name(name):
    return re.sub(r"[-_.]+", "-", str(name or "").strip()).lower()


# ------------------------------------------------------ decision record


def decision_records(scratch):
    """[(rel, text)] for every file that reads as the decision record.

    The pack names `LICENCE_DECISION.md` at the venture root. Anything
    whose name carries the two words in either spelling counts, wherever
    it sits, so a venture that files its records under `docs/` is not
    failed for tidiness.
    """
    found = []
    for path in walk(scratch, suffixes=TEXT_SUFFIXES):
        if DECISION_NAME.search(path.stem):
            found.append((rel(scratch, path), read(path)))
    return found


def decision_text(scratch):
    """Every decision record joined, for a "is it named anywhere" check."""
    return "\n".join(text for _, text in decision_records(scratch))


# ----------------------------------------------------------- inventory


def _licence_from_cyclonedx(entry):
    licences = entry.get("licenses") or entry.get("licences")
    if not isinstance(licences, list):
        return None
    parts = []
    for item in licences:
        if not isinstance(item, dict):
            continue
        if isinstance(item.get("expression"), str):
            parts.append(item["expression"])
            continue
        lic = item.get("license") or item.get("licence")
        if isinstance(lic, dict):
            value = lic.get("id") or lic.get("name")
            if isinstance(value, str):
                parts.append(value)
        elif isinstance(lic, str):
            parts.append(lic)
    return " AND ".join(p.strip() for p in parts if p.strip()) or None


def _licence_of(entry):
    """The licence an inventory entry claims, whatever shape it came in."""
    for key in ("licence", "license", "licenceExpression",
                "licenseExpression", "licenseDeclared", "licenseConcluded",
                "spdx", "spdx_id", "spdxId"):
        value = entry.get(key)
        if isinstance(value, str):
            return value.strip()
    from_list = _licence_from_cyclonedx(entry)
    if from_list is not None:
        return from_list
    return ""


def _entries_from(doc):
    if isinstance(doc, list):
        return [e for e in doc if isinstance(e, dict)]
    if not isinstance(doc, dict):
        return []
    for key in ("components", "packages", "dependencies", "entries",
                "inventory"):
        value = doc.get(key)
        if isinstance(value, list):
            return [e for e in value if isinstance(e, dict)]
    return []


def parse_inventory(text):
    """[{name, licence, raw}] from a JSON inventory, or None if it is not one.

    CycloneDX, SPDX and a plain list of records all reduce to the same
    two facts, which are the only two any criterion here asks about.
    """
    try:
        doc = json.loads(text)
    except ValueError:
        return None
    entries = _entries_from(doc)
    if not entries:
        return None
    rows = []
    for entry in entries:
        name = entry.get("name") or entry.get("packageName") or \
            entry.get("component") or entry.get("id") or ""
        if not isinstance(name, str) or not name.strip():
            continue
        rows.append({"name": normalise_name(name),
                     "licence": _licence_of(entry),
                     "raw": entry})
    return rows or None


def inventories(scratch):
    """[(rel, rows)] for every parseable inventory in the delivered tree.

    JSON first, because that is what the repository's own scan writes,
    then CSV, because several scanners emit that instead and the
    criterion asks only that the inventory parses.
    """
    found = []
    for path in walk(scratch, suffixes=(".json", ".csv")):
        parts = Path(rel(scratch, path)).parts
        if parts and parts[0] in ("vendor", "third_party"):
            continue
        text = read(path)
        rows = (parse_inventory(text) if path.suffix.lower() == ".json"
                else parse_csv_inventory(text))
        if rows:
            found.append((rel(scratch, path), rows))
    found.sort(key=lambda item: (-len(item[1]), item[0]))
    return found


def best_inventory(scratch):
    """The fullest inventory in the tree, or (None, None)."""
    found = inventories(scratch)
    return found[0] if found else (None, None)


def json_files(scratch):
    return [rel(scratch, p) for p in walk(scratch, suffixes=(".json",))]


# --------------------------------------------- what a scan had to cover


_REQUIREMENT = re.compile(r"^([A-Za-z0-9._-]+)\s*(?:[=<>!~]=?|$)")
_REQUIRES_DIST = re.compile(r"^Requires-Dist:\s*([A-Za-z0-9._-]+)", re.M)


def _requirement_names(scratch):
    names = []
    for name in ("requirements.txt", "requirements.in",
                 "requirements-prod.txt"):
        path = Path(scratch) / name
        if not path.is_file():
            continue
        for line in read(path).splitlines():
            line = line.strip()
            if not line or line.startswith(("#", "-")):
                continue
            match = _REQUIREMENT.match(line)
            if match:
                names.append(match.group(1))
    pyproject = Path(scratch) / "pyproject.toml"
    if pyproject.is_file():
        text = read(pyproject)
        block = re.search(r"^dependencies\s*=\s*\[(.*?)\]", text,
                          re.S | re.M)
        if block:
            for item in re.findall(r"[\"']([^\"']+)[\"']", block.group(1)):
                match = _REQUIREMENT.match(item.strip())
                if match:
                    names.append(match.group(1))
    return names


def _vendor_requires(scratch, name):
    """Names that one vendored distribution declares it needs."""
    vendor = Path(scratch) / "vendor"
    if not vendor.is_dir():
        return []
    wanted = normalise_name(name)
    for path in sorted(vendor.glob("*.dist-info/METADATA")):
        stem = path.parent.name[: -len(".dist-info")]
        if normalise_name(stem.rsplit("-", 1)[0]) == wanted:
            return _REQUIRES_DIST.findall(read(path))
    return []


def expected_components(scratch):
    """Component names a scan over this tree could not honestly omit.

    The pinned requirements, everything they pull in through the
    metadata in `vendor/`, and one entry for each vendored directory
    under `third_party/`. Read from the tree rather than from the
    delivered inventory on purpose: an inventory that quietly lost the
    awkward component would otherwise agree with itself.
    """
    found = {}
    queue = list(_requirement_names(scratch))
    while queue:
        name = normalise_name(queue.pop(0))
        if not name or name in found:
            continue
        found[name] = "requirements"
        for other in _vendor_requires(scratch, name):
            if normalise_name(other) not in found:
                queue.append(other)
    base = Path(scratch) / "third_party"
    if base.is_dir():
        for path in sorted(p for p in base.iterdir() if p.is_dir()):
            if path.name in SKIP_PARTS:
                continue
            found[normalise_name(path.name)] = "third_party/%s" % path.name
    return found


# ------------------------------------------------------------ resolved


def is_unresolved(licence):
    value = (licence or "").strip().lower()
    if value in UNRESOLVED:
        return True
    return value.startswith("noassertion")


def named_in(text, name):
    """Is this component named anywhere in the decision record."""
    return normalise_name(name) in flat(text).replace("_", "-")


# ----------------------------------------------------------------- git


def git_available():
    return shutil.which("git") is not None


def git(cwd, *args):
    proc = subprocess.run(["git", "-C", str(cwd), *args],
                          capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def require_git(cid):
    if not git_available():
        emit(cid, UNSETTLED,
             "git is not on PATH here, so this criterion was not settled. "
             "That is a gap in the environment, not a finding against the "
             "delivered tree.")


def has_history(scratch):
    code, _ = git(scratch, "rev-parse", "--git-dir")
    if code != 0:
        return False
    code, _ = git(scratch, "rev-parse", "--verify", "HEAD")
    return code == 0


# -------------------------------------------------------------- pytest


def pytest_available():
    try:
        import importlib.util
        return importlib.util.find_spec("pytest") is not None
    except (ImportError, ValueError):
        return False


def test_env(tree):
    """Environment for running the venture's tests in the delivered tree.

    The repository puts `vendor/` and `third_party/` on `PYTHONPATH` in
    its own Makefile, so a grader that did not would fail work that runs
    perfectly well for the people who wrote it.
    """
    env = dict(os.environ)
    parts = [str(tree)]
    for extra in ("vendor", "third_party"):
        path = Path(tree) / extra
        if path.is_dir():
            parts.append(str(path))
    if env.get("PYTHONPATH"):
        parts.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(parts)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def run_tests(tree, target, timeout=300):
    """Run one test file. Returns (returncode, output, how)."""
    if pytest_available():
        cmd = [sys.executable, "-m", "pytest", "-q", "--tb=short",
               "-p", "no:cacheprovider", str(target)]
        how = "pytest"
    else:
        cmd = [sys.executable, "-m", "unittest", "-v",
               str(Path(target).as_posix()).replace("/", ".")[:-3]]
        how = "unittest"
    try:
        proc = subprocess.run(cmd, cwd=str(tree), capture_output=True,
                              text=True, encoding="utf-8", errors="replace",
                              timeout=timeout, env=test_env(tree))
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, str(exc), how
    return proc.returncode, (proc.stdout or "") + (proc.stderr or ""), how


def tail(output, limit=280):
    return " ".join((output or "").split())[-limit:]


def parse_csv_inventory(text):
    """[{name, licence}] from a CSV inventory, or None."""
    try:
        rows = list(csv.DictReader(io.StringIO(text)))
    except (ValueError, csv.Error):
        return None
    out = []
    for row in rows:
        keys = {(k or "").strip().lower(): v for k, v in row.items()}
        name = keys.get("name") or keys.get("component") or keys.get("package")
        if not name:
            continue
        licence = (keys.get("licence") or keys.get("license")
                   or keys.get("licence expression")
                   or keys.get("license expression") or "")
        out.append({"name": normalise_name(name),
                    "licence": (licence or "").strip(), "raw": row})
    return out or None
