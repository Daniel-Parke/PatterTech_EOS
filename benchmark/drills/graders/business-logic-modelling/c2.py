#!/usr/bin/env python3
"""Criterion 2: no float in `booking/`, and the money amount is an int.

Two halves, and both must hold.

The source half reads `booking/**/*.py` with `tokenize`, so the word
inside a docstring or a comment is not a finding and only real code
counts. A `float(` call fails outright. The name `float` anywhere else
fails as well, with one exemption: inside an `isinstance` or
`issubclass` call, because a model that refuses a float at the door is
doing the opposite of the thing this criterion is about.

The behaviour half asks the delivered type. An amount held as a
`Decimal` or a `float` fails here even though the source may be clean.
"""

import io
import sys
import token as toklib
import tokenize
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (BOOKING_SETUP, FAIL, PASS, booking_modules,  # noqa: E402
                     emit, read, require_implementation, run_probe,
                     scratch_dir)

CID = "c2"

EXEMPT_CALLERS = ("isinstance", "issubclass")

PROBE = BOOKING_SETUP + '''
price = Money(1099, "GBP")
amount = getattr(price, "amount", None)
if amount is None:
    fail("Money(1099, 'GBP') has no `amount`, so there is no internal "
         "amount to check")
if isinstance(amount, bool):
    fail("Money(1099, 'GBP').amount is a bool, not an int")
if not isinstance(amount, int):
    fail("Money(1099, 'GBP').amount is a %s holding %r, not an int"
         % (type(amount).__name__, amount))
if amount != 1099:
    fail("Money(1099, 'GBP').amount is %r; the constructor is not taking "
         "minor units" % (amount,))
ok("Money(1099, 'GBP').amount is the int 1099")
'''


def float_uses(path, text):
    """Every real use of the name `float` in one file, with its line."""
    hits = []
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
    except (tokenize.TokenError, IndentationError, SyntaxError) as exc:
        return [("the file does not tokenise (%s), so it was read as text "
                 "and the word float appears in it" % exc.__class__.__name__,
                 0)] if "float" in text else []

    meaningful = [t for t in tokens
                  if t.type not in (toklib.COMMENT, toklib.NL, toklib.NEWLINE,
                                    toklib.INDENT, toklib.DEDENT)]
    callers = []
    for i, tok in enumerate(meaningful):
        if tok.type == toklib.OP and tok.string in "([{":
            previous = meaningful[i - 1] if i else None
            callers.append(previous.string
                           if previous and previous.type == toklib.NAME
                           and tok.string == "(" else None)
        elif tok.type == toklib.OP and tok.string in ")]}":
            if callers:
                callers.pop()
        elif tok.type == toklib.NAME and tok.string == "float":
            following = meaningful[i + 1] if i + 1 < len(meaningful) else None
            called = (following is not None and following.type == toklib.OP
                      and following.string == "(")
            enclosing = callers[-1] if callers else None
            if called:
                hits.append(("a float() call", tok.start[0]))
            elif enclosing in EXEMPT_CALLERS:
                continue
            else:
                hits.append(("the name float", tok.start[0]))
    return hits


def main():
    scratch = scratch_dir()
    require_implementation(CID, scratch)

    found = []
    for path in booking_modules(scratch):
        rel = path.relative_to(scratch).as_posix()
        for what, line in float_uses(path, read(path)):
            found.append("%s:%d %s" % (rel, line, what))
    if found:
        emit(CID, FAIL,
             "%d use(s) of float in booking/: %s"
             % (len(found), "; ".join(found[:5])))

    good, reason = run_probe(scratch, PROBE)
    if good is None:
        emit(CID, FAIL, reason)
    if not good:
        emit(CID, FAIL, "no float appears in booking/, but %s" % reason)
    emit(CID, PASS, "no float appears in booking/, and %s" % reason)


if __name__ == "__main__":
    main()
