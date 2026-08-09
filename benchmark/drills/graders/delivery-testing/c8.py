#!/usr/bin/env python3
"""Criterion 8: a quarantine, if there is one, names an owner and expires.

The spec is explicit that no quarantine passes and a bare quarantine
fails, so this criterion is vacuous on a tree where nothing was
quarantined. It says so in its reason rather than reporting a green it
did not earn.

What counts as a quarantine record: a `skip`, `xfail` or `skipif`
marker on a test, any marker whose name mentions quarantine or flake,
and any file whose name mentions quarantine. A `skipif` guarded by
platform or version is a portability guard rather than a quarantine and
is not counted.

What counts as owned and expiring: an owner, written as `owner:`, an
`@handle` or an email address, and an ISO date that has not already
passed and is no more than thirty days out. The text searched is the
marker itself plus the comment lines immediately above it, because that
is where people put this in practice.
"""

import ast
import datetime as dt
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, dotted, emit, parse, read,  # noqa: E402
                     relative, scratch_dir, test_files)

CID = "c8"
WINDOW_DAYS = 30

MARKERS = ("skip", "skipif", "xfail")
FUZZY = ("quarantine", "flaky", "flake")
PORTABILITY = ("sys.platform", "sys.version_info", "os.name", "shutil.which",
               "importlib", "platform.system")

OWNER = re.compile(
    r"owner\s*[:=]\s*\S+|@[A-Za-z][\w.\-]{2,}|[\w.+\-]+@[\w\-]+\.[\w.]+",
    re.I)
ISO = re.compile(r"\b(\d{4}-\d{2}-\d{2})\b")


def comments_above(lines, lineno):
    """The contiguous comment block sitting above a 1-based line number."""
    out = []
    i = lineno - 2
    while i >= 0 and lines[i].strip().startswith("#"):
        out.append(lines[i].strip())
        i -= 1
    return "\n".join(reversed(out))


def marker_records(path, rel):
    text = read(path)
    lines = text.splitlines()
    node = parse(path)
    if node is None:
        return []
    out = []
    for sub in ast.walk(node):
        if not isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef,
                                ast.ClassDef)):
            continue
        for deco in sub.decorator_list:
            call = deco.func if isinstance(deco, ast.Call) else deco
            name = dotted(call)
            short = name.split(".")[-1].lower()
            fuzzy = any(word in name.lower() for word in FUZZY)
            if short not in MARKERS and not fuzzy:
                continue
            if short == "skipif" and isinstance(deco, ast.Call) and \
                    deco.args and any(
                        guard in (ast.unparse(deco.args[0]) or "")
                        for guard in PORTABILITY):
                continue
            segment = ast.get_source_segment(text, deco) or name
            body = comments_above(lines, deco.lineno) + "\n" + segment
            out.append(("%s::%s (%s)" % (rel, sub.name, short), body))
    return out


def file_records(path, rel):
    out = []
    blocks = re.split(r"\n\s*\n", read(path))
    for i, block in enumerate(blocks, 1):
        low = block.lower()
        if "test" in low or "::" in block:
            out.append(("%s block %d" % (rel, i), block))
    return out or [(rel, read(path))]


def verdict(body, today):
    if not OWNER.search(body):
        return "names no owner"
    dates = [d for d in (_date(m) for m in ISO.findall(body)) if d]
    if not dates:
        return "carries no ISO expiry date"
    horizon = today + dt.timedelta(days=WINDOW_DAYS)
    if not any(today <= d <= horizon for d in dates):
        return ("has no expiry inside the next %d days (found %s)"
                % (WINDOW_DAYS, ", ".join(d.isoformat() for d in dates)))
    return ""


def _date(raw):
    try:
        return dt.date.fromisoformat(raw)
    except ValueError:
        return None


def main():
    scratch = scratch_dir()
    today = dt.date.today()

    records = []
    for path in test_files(scratch):
        records.extend(marker_records(path, relative(scratch, path)))
    for path in sorted(scratch.rglob("*")):
        if not path.is_file() or ".git" in path.parts:
            continue
        if "quarantine" in path.name.lower():
            records.extend(file_records(path, relative(scratch, path)))

    if not records:
        emit(CID, PASS,
             "nothing is quarantined in the delivered tree, which the spec "
             "counts as a pass; this criterion only bites once a test is "
             "parked")

    bad = []
    for label, body in records:
        why = verdict(body, today)
        if why:
            bad.append("%s %s" % (label, why))
    if bad:
        emit(CID, FAIL,
             "%d of %d quarantine record(s) are bare: %s"
             % (len(bad), len(records), "; ".join(bad[:4])))
    emit(CID, PASS,
         "all %d quarantine record(s) name an owner and expire inside %d "
         "days: %s" % (len(records), WINDOW_DAYS,
                       ", ".join(label for label, _ in records[:4])))


if __name__ == "__main__":
    main()
