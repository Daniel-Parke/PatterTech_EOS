#!/usr/bin/env python3
"""Criterion 10: every flag the change adds has an owner and a date.

"Added" is measured against the flag file the fixture shipped, so the
two flags that were already there are nobody's problem here. A tree
that adds no flag at all does not pass by default: the rollout this
drill asks for is gated on something, and an ungated switch is the
failure this criterion is about, not an exemption from it.
"""

import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, find_one, load_structured,  # noqa: E402
                     require_baseline, scratch_dir)

CID = "c10"

FLAG_TOKENS = {"flags", "flag", "featureflags", "toggles", "toggle"}


def entries(doc):
    """The flag entries in a flag document, however it is nested."""
    if not isinstance(doc, dict):
        return {}
    for key in ("flags", "featureFlags", "feature_flags", "toggles"):
        inner = doc.get(key)
        if isinstance(inner, dict):
            return inner
        if isinstance(inner, list):
            out = {}
            for item in inner:
                if isinstance(item, dict):
                    name = item.get("name") or item.get("key") or item.get(
                        "flag")
                    if name:
                        out[str(name)] = item
            return out
    if all(isinstance(v, dict) for v in doc.values()) and doc:
        return doc
    return {}


def as_date(value):
    text = str(value).strip()
    if not text:
        return None
    text = text.replace("Z", "").split("T")[0].split(" ")[0]
    for fmt in ("%Y-%m-%d", "%d/%m/%Y", "%Y/%m/%d", "%d-%m-%Y"):
        try:
            return dt.datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def flag_files(root):
    found = find_one(root, FLAG_TOKENS)
    preferred = root / "config" / "flags.json"
    if preferred.is_file():
        found = [preferred] + [p for p in found if p != preferred]
    return found


def collect(root):
    out, errors = {}, []
    for path in flag_files(root):
        doc, error = load_structured(path)
        if error:
            errors.append(error)
            continue
        found = entries(doc)
        for name, entry in found.items():
            out.setdefault(name, (path, entry))
    return out, errors


def main():
    scratch = scratch_dir()
    baseline = require_baseline(CID)

    shipped, _ = collect(baseline)
    delivered, errors = collect(scratch)
    if not delivered and errors:
        emit(CID, FAIL, "the flag configuration does not parse: %s"
                        % "; ".join(errors[:2]))

    added = sorted(name for name in delivered if name not in shipped)
    if not added:
        emit(CID, FAIL,
             "no flag was added to the flag configuration, so the change "
             "ships behind no switch; the %d flag(s) present are the ones "
             "the repository already had" % len(shipped))

    today = dt.date.today()
    problems = []
    for name in added:
        path, entry = delivered[name]
        where = path.relative_to(scratch).as_posix()
        if not isinstance(entry, dict):
            problems.append("%s in %s is not an object" % (name, where))
            continue
        owner = str(entry.get("owner") or "").strip()
        expires = entry.get("expires", entry.get("expiry",
                                                 entry.get("expires_at")))
        if not owner:
            problems.append("%s has no owner" % name)
        if not str(expires or "").strip():
            problems.append("%s has no expires" % name)
            continue
        when = as_date(expires)
        if when is None:
            problems.append("%s expires is %r, which is not a date"
                            % (name, expires))
        elif when <= today:
            problems.append("%s expires %s, which is not after today (%s)"
                            % (name, when.isoformat(), today.isoformat()))

    if problems:
        emit(CID, FAIL, "; ".join(problems[:4]))

    emit(CID, PASS,
         "%d added flag(s) (%s), each with an owner and an expiry after %s"
         % (len(added), ", ".join(added), today.isoformat()))


if __name__ == "__main__":
    main()
