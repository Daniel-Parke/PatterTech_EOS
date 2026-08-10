#!/usr/bin/env python3
"""Criterion 5: the exception callers really get, spelled the same in three places.

The criterion asks for string equality across `parser.py`, the test from
criterion 3 and `README.md`, and it asks it of one particular thing: the
exception type callers may catch. So the name is not guessed from the
source, it is taken from the call. This grader feeds `parse_records` a
malformed numeric row, catches what comes out, and takes the type and
its ancestors as the only names that are allowed to satisfy the
criterion. Any of them is fair, because a caller can catch a base class,
but a name that never reaches a caller is not.

That is the repair. The earlier version collected every name `parser.py`
raised anywhere and accepted whichever one happened to appear in a test
and the README. A tree that declared `RecordError`, documented it,
tested it on a short line and went on dropping malformed numeric rows
was told it had passed, and the three files agreeing with each other
about a name no malformed row ever produces is exactly the failure the
criterion is written against.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (BAD_ROWS, FAIL, PASS, emit, malformed_probe,  # noqa: E402
                     parser_files, raised_names, read, read_malformed, rel,
                     scratch_dir, test_files)

CID = "c5"


def mentions(text, name):
    return re.search(r"\b%s\b" % re.escape(name), text) is not None


def find_readme(scratch):
    for path in scratch.glob("*.md"):
        if path.name.lower() == "readme.md":
            return path
    for path in scratch.rglob("README.md"):
        if ".git" not in path.parts:
            return path
    return None


def caller_names(scratch):
    """What a caller of parse_records can actually catch. Never a guess."""
    result = malformed_probe(scratch)
    if not result.get("ok"):
        emit(CID, FAIL,
             "the grader could not call parse_records in the delivered tree "
             "(%s), so what callers may catch could not be read"
             % result.get("error", "no reason given"))
    raised, dropped, unclear = read_malformed(result)
    if not raised:
        if dropped:
            emit(CID, FAIL,
                 "the row %r is still dropped silently, so no exception "
                 "reaches a caller and there is no type for the module, the "
                 "test and the README to agree on"
                 % BAD_ROWS[dropped[0]])
        emit(CID, FAIL,
             "a malformed numeric row raises nothing, so there is no "
             "exception type callers may catch, whatever the three files "
             "say")
    return raised_names(result), raised


def main():
    scratch = scratch_dir()
    files = parser_files(scratch)
    if not files:
        emit(CID, FAIL, "no parser.py in the delivered tree")

    names, raised = caller_names(scratch)
    thrown = names[0] if names else "?"
    parser_text = "\n".join(read(path) for path in files)

    readme = find_readme(scratch)
    if readme is None:
        emit(CID, FAIL, "no README.md in the delivered tree")
    readme_text = read(readme)

    tests = [(rel(scratch, p), read(p)) for p in test_files(scratch)]
    raising = [(name, text) for name, text in tests
               if "raises" in text or "assertRaises" in text]
    if not raising:
        emit(CID, FAIL,
             "no test asserts a raise, so the criterion's third place to "
             "check does not exist")

    misses = []
    for name in names:
        in_parser = mentions(parser_text, name)
        in_test = [n for n, text in raising if mentions(text, name)]
        in_readme = mentions(readme_text, name)
        if in_parser and in_test and in_readme:
            emit(CID, PASS,
                 "a malformed numeric row raises %s, and %r appears in "
                 "parser.py, in %s and in %s, spelled the same in all three"
                 % (thrown, name, in_test[0], rel(scratch, readme)))
        where = []
        if not in_parser:
            where.append("parser.py")
        if not in_test:
            where.append("no raising test")
        if not in_readme:
            where.append(rel(scratch, readme))
        misses.append("%s: missing from %s" % (name, " and ".join(where)))

    emit(CID, FAIL,
         "%s is what a caller gets for %s, but neither it nor any base it "
         "carries is spelled the same in parser.py, a raising test and the "
         "README (%s)"
         % (thrown, BAD_ROWS[raised[0]], "; ".join(misses[:4])))


if __name__ == "__main__":
    main()
