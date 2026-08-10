#!/usr/bin/env python3
"""Criterion 4: the scanner report and the manual verdict file agree.

This criterion is graded in one direction only, and the reason is
worth stating plainly.

Half of it is a browser fact: axe-core, driven over every route in a
real engine, returning nothing at the pinned WCAG 2.2 A and AA tags. No
stdlib Python script can produce that fact, and no machine without a
browser driver and an axe build can either. This grader does not
re-execute the scan and does not pretend to.

The other half is an evidence fact, and it is fully settleable: is
there a report, is it axe-shaped, are the tags actually pinned to WCAG
2.2 A and AA, does it cover every route the tree builds, does it record
zero violations, and does `A11Y_MANUAL.md` carry one written verdict
for each incomplete result and no more. Every one of those can fail
here, and each failure is a real finding.

So: absence, malformation, loose tags, missing routes, recorded
violations and a count mismatch are failures. Complete and consistent
evidence is reported as unsettled, exit 2, which the runner records as
manual. That is the honest verdict when the scan itself was not
re-run, and it keeps the drill from going green on a file an agent
could have typed.
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, SURFACES, UNSETTLED, built_pages, emit,  # noqa: E402
                     html_pages, iter_files, read, rel, scratch_dir)

CID = "c4"

MANUAL_FILE = "A11Y_MANUAL.md"
REQUIRED_TAGS = ("wcag2a", "wcag2aa", "wcag22aa")


def find_reports(scratch):
    """Every axe-shaped JSON document in the tree, with its path."""
    out = []
    for path in iter_files(scratch, exts={".json"}):
        text = read(path)
        if "violations" not in text or "incomplete" not in text:
            continue
        try:
            doc = json.loads(text)
        except ValueError:
            continue
        for result in flatten(doc):
            out.append((path, result))
    return out


def flatten(doc):
    if isinstance(doc, list):
        out = []
        for item in doc:
            out += flatten(item)
        return out
    if not isinstance(doc, dict):
        return []
    if "violations" in doc and "incomplete" in doc:
        return [doc]
    out = []
    for key in ("results", "routes", "pages", "runs"):
        if key in doc:
            out += flatten(doc[key])
    return out


def tags_of(result):
    found = set()
    options = result.get("toolOptions") or {}
    run_only = options.get("runOnly") or {}
    values = run_only.get("values") or run_only.get("value") or []
    if isinstance(values, str):
        values = [values]
    found.update(str(v).lower() for v in values)
    for value in (options.get("runOnly"), result.get("tags")):
        if isinstance(value, list):
            found.update(str(v).lower() for v in value)
    return found


def route_of(result):
    return str(result.get("url") or result.get("route")
               or result.get("page") or "")


def expected_routes(scratch):
    routes = []
    for name in SURFACES:
        pages = built_pages(scratch, name) or html_pages(scratch, name)
        routes += [rel(scratch, p) for p in pages]
    return routes


def manual_entries(text):
    """Rule ids named in the verdict file, with the prose under each."""
    entries = {}
    current, buffer = None, []
    for line in text.splitlines():
        found = re.findall(r"\b([a-z][a-z0-9]+(?:-[a-z0-9]+){1,4})\b", line)
        ids = [f for f in found if "-" in f and not f.endswith(".md")]
        stripped = line.lstrip()
        heading = (stripped.startswith(("#", "-", "*", "|"))
                   or re.match(r"^[a-z][\w-]*\s*:", stripped) is not None)
        if ids and heading:
            if current:
                entries[current] = " ".join(buffer).strip()
            current, buffer = ids[0], [line]
            continue
        if current:
            buffer.append(line)
    if current:
        entries[current] = " ".join(buffer).strip()
    return entries


def main():
    scratch = scratch_dir()
    manual_path = Path(scratch) / MANUAL_FILE
    reports = find_reports(scratch)

    if not reports and not manual_path.is_file():
        emit(CID, FAIL,
             "no scanner report and no %s: nothing in the tree records an "
             "accessibility scan of the routes" % MANUAL_FILE)
    if not reports:
        emit(CID, FAIL,
             "%s is present but there is no axe report anywhere in the tree, "
             "so its entries answer to nothing" % MANUAL_FILE)
    if not manual_path.is_file():
        emit(CID, FAIL,
             "an axe report is present but %s is not, so the incomplete "
             "results carry no written verdict" % MANUAL_FILE)

    where = sorted({rel(scratch, p) for p, _ in reports})
    results = [r for _, r in reports]

    loose = [route_of(r) or "(unnamed route)" for r in results
             if not set(REQUIRED_TAGS) <= tags_of(r)]
    if loose:
        sample = tags_of(results[0])
        emit(CID, FAIL,
             "the report does not pin WCAG 2.2 A and AA rule tags on %d of "
             "%d route(s); %s wants %s and carries %s"
             % (len(loose), len(results), loose[0], ", ".join(REQUIRED_TAGS),
                ", ".join(sorted(sample)) or "no runOnly tags"))

    scanned = [route_of(r) for r in results]
    wanted = expected_routes(scratch)
    if not wanted:
        emit(CID, FAIL,
             "neither surface has any page to scan, so a clean report "
             "describes nothing")
    uncovered = [w for w in wanted
                 if not any(Path(w).name and Path(w).name in s
                            for s in scanned)]
    if uncovered:
        emit(CID, FAIL,
             "%d of %d route(s) never appear in the report: %s. The scan has "
             "to cover every route"
             % (len(uncovered), len(wanted), ", ".join(uncovered[:4])))

    violations = []
    for result in results:
        for item in result.get("violations") or []:
            violations.append("%s on %s" % (item.get("id", "?"),
                                            route_of(result) or "?"))
    if violations:
        emit(CID, FAIL,
             "the report records %d violation(s) at the pinned tags: %s"
             % (len(violations), "; ".join(violations[:4])))

    incomplete = {}
    for result in results:
        for item in result.get("incomplete") or []:
            key = str(item.get("id", "")).strip()
            if key:
                incomplete.setdefault(key, []).append(route_of(result))
    entries = manual_entries(read(manual_path))
    named = {k: v for k, v in entries.items() if k in incomplete}

    if not incomplete:
        emit(CID, FAIL,
             "the report records no incomplete results at all across %d "
             "route(s), so %s has nothing to answer for. A scan of custom "
             "interactive components that reports zero incompletes is the "
             "failure signal this criterion exists to catch"
             % (len(results), MANUAL_FILE))
    missing = sorted(set(incomplete) - set(named))
    if missing:
        emit(CID, FAIL,
             "%d incomplete result(s) carry no verdict in %s: %s"
             % (len(missing), MANUAL_FILE, ", ".join(missing[:4])))
    thin = sorted(k for k, v in named.items() if len(v.strip()) < 60)
    if thin:
        emit(CID, FAIL,
             "%s names %s but writes no verdict against %s: an entry is a "
             "sentence saying what was checked and what was concluded"
             % (MANUAL_FILE, ", ".join(thin[:3]), thin[0]))
    if len(named) != len(incomplete):
        emit(CID, FAIL,
             "%s carries %d entries against %d incomplete results in the "
             "report; the counts have to match"
             % (MANUAL_FILE, len(named), len(incomplete)))

    emit(CID, UNSETTLED,
         "the evidence is complete and consistent: %s pins %s, covers all %d "
         "route(s), records no violations and %d incomplete result(s), and "
         "%s carries a written verdict for each. The scan itself was not "
         "re-executed here, because no browser-driving axe run is available "
         "to this grader, so the zero-violations half rests on the committed "
         "report and is left for a human."
         % (", ".join(where), ", ".join(REQUIRED_TAGS), len(wanted),
            len(incomplete), MANUAL_FILE))


if __name__ == "__main__":
    main()
