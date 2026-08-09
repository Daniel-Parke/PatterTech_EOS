#!/usr/bin/env python3
"""Criterion 2: the crawler directives parse, and the check discriminates.

Four things settle here: the live file parses under RFC 9309, it is
under 500 KiB, the group that applies to everyone carries no blanket
disallow, and a staging fixture that does carry one exists with a test
that refuses it. The last is the whole point of the criterion: a check
that cannot fail proves nothing, so the negative fixture and the test
naming it are graded rather than assumed.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, all_files, blanket_disallow,  # noqa: E402
                     emit, parse_robots, read, robots_files, scratch_dir)

CID = "c2"

LIMIT = 500 * 1024


def is_test(path):
    rel = path.as_posix().lower()
    return ("test" in rel or "spec" in rel or "check" in rel) and \
        path.suffix.lower() in (".py", ".sh", ".js", ".ts", ".yml", ".yaml",
                                ".mk", ".toml", "")


def main():
    scratch = scratch_dir()
    live, others = robots_files(scratch)
    if live is None:
        emit(CID, FAIL, "no site/robots.txt; the deploy copies site/ as it "
                        "stands, so there are no crawler directives at all")

    size = live.stat().st_size
    if size > LIMIT:
        emit(CID, FAIL, "site/robots.txt is %d bytes, over the 500 KiB a "
                        "crawler is required to read" % size)

    parsed = parse_robots(read(live))
    if parsed["errors"]:
        emit(CID, FAIL, "site/robots.txt does not parse under RFC 9309: %s"
                        % "; ".join(parsed["errors"][:3]))
    if not parsed["groups"]:
        emit(CID, FAIL, "site/robots.txt declares no user-agent group, so it "
                        "states nothing a crawler can follow")
    if blanket_disallow(parsed):
        emit(CID, FAIL, "site/robots.txt still shuts the whole site: the "
                        "group for every crawler carries Disallow: /")

    negatives = []
    for path in others:
        other = parse_robots(read(path))
        if not other["errors"] and blanket_disallow(other):
            negatives.append(path.relative_to(scratch).as_posix())
    if not negatives:
        emit(CID, FAIL,
             "the production profile is clean but no staging fixture carries "
             "Disallow: /, so nothing proves the check can fail. Robots files "
             "found beside the live one: %s"
             % (", ".join(p.relative_to(scratch).as_posix()
                          for p in others) or "none"))

    wired = []
    for path in all_files(scratch):
        if not is_test(path):
            continue
        text = read(path).lower()
        if "robots" not in text:
            continue
        if any(Path(n).name.lower() in text or n.lower() in text
               for n in negatives):
            wired.append(path.relative_to(scratch).as_posix())
    if not wired:
        emit(CID, FAIL,
             "staging fixture %s exists but no test names it, so nothing "
             "asserts the same check refuses it" % negatives[0])

    emit(CID, PASS,
         "site/robots.txt parses, is %d bytes, carries no blanket disallow, "
         "and %s asserts against the negative fixture %s"
         % (size, wired[0], negatives[0]))


if __name__ == "__main__":
    main()
