#!/usr/bin/env python3
"""Criterion 11: the synthesis counts something, and says out of what.

`synthesis.json` carries `denominator`, `coding_stance` and a `themes`
array. Every theme carries `count` and `item_ids`, every id is an item
that exists in `triage.json`, `count` equals the number of ids, and the
distinct ids across all themes number at most 40.

The arithmetic clause is the one that bites: a theme claiming eleven
items and listing four is the write-up the fixture's notes describe,
where two weeks counted different things and could not be compared.
Themes may overlap, which is why the ceiling is on distinct ids rather
than on the sum.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, ITEM_COUNT, PASS, emit, find_artefact,  # noqa: E402
                     get, is_empty, load_json, load_triage, normalise_id,
                     rel, scratch_dir, text_of)

CID = "c11"

THEME_KEYS = ("themes", "theme", "topics", "clusters")
IDS_KEYS = ("item_ids", "items", "ids", "item_numbers", "members")


def main():
    scratch = scratch_dir()
    path = find_artefact(scratch, "synthesis.json")
    if path is None:
        emit(CID, FAIL, "no synthesis.json: the week was never written up")
    where = rel(scratch, path)
    doc, err = load_json(path)
    if err:
        emit(CID, FAIL, "%s %s" % (where, err))
    if not isinstance(doc, dict):
        emit(CID, FAIL, "%s is not a JSON object" % where)

    problems = []
    for field in ("denominator", "coding_stance"):
        if is_empty(get(doc, field)):
            problems.append("no %s" % field)
    themes = get(doc, *THEME_KEYS)
    if not isinstance(themes, list):
        problems.append("no themes array")
        emit(CID, FAIL, "%s: %s" % (where, "; ".join(problems)))
    if not themes:
        problems.append("the themes array is empty")
    if problems:
        emit(CID, FAIL, "%s: %s" % (where, "; ".join(problems)))

    by_id, terr = load_triage(scratch)
    if terr:
        emit(CID, FAIL,
             "%s carries %d themes but %s, so no item id can be checked "
             "against the triage" % (where, len(themes), terr))

    distinct = set()
    for i, theme in enumerate(themes):
        label = text_of(get(theme, "name", "theme", "title", "label")) or \
            "theme %d" % (i + 1)
        if not isinstance(theme, dict):
            problems.append("%s is not an object" % label)
            continue
        count = get(theme, "count", "n", "size")
        ids_raw = get(theme, *IDS_KEYS)
        if count is None:
            problems.append("%s has no count" % label)
        if not isinstance(ids_raw, list):
            problems.append("%s has no item_ids array" % label)
            continue
        ids = [normalise_id(v) for v in ids_raw]
        unreadable = [str(v) for v, n in zip(ids_raw, ids) if n is None]
        if unreadable:
            problems.append("%s lists unreadable ids: %s"
                            % (label, ", ".join(unreadable[:4])))
        clean = [n for n in ids if n is not None]
        absent = sorted({n for n in clean if n not in by_id})
        if absent:
            problems.append("%s lists item(s) %s that are not in triage.json"
                            % (label, ", ".join(str(a) for a in absent[:6])))
        if isinstance(count, bool) or not isinstance(count, int):
            try:
                count = int(str(count).strip())
            except (TypeError, ValueError):
                count = None
        if count is not None and count != len(ids_raw):
            problems.append("%s says count %d and lists %d item(s)"
                            % (label, count, len(ids_raw)))
        distinct.update(clean)

    if len(distinct) > ITEM_COUNT:
        problems.append("the themes name %d distinct items, more than the %d "
                        "in the inbox" % (len(distinct), ITEM_COUNT))
    if problems:
        emit(CID, FAIL, "%s: %s" % (where, "; ".join(problems[:6])))

    emit(CID, PASS,
         "%s states a denominator (%s) and a coding stance, and its %d "
         "theme(s) cover %d distinct items, every id in triage.json with "
         "count matching the list"
         % (where, text_of(get(doc, "denominator"))[:20], len(themes),
            len(distinct)))


if __name__ == "__main__":
    main()
