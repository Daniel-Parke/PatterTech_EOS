#!/usr/bin/env python3
"""refund_pence must round half to even with exact decimal arithmetic.

Criteria contract: argv[1] is the scratch directory the session worked
in. Prints one JSON object {"id", "pass", "reason"} and exits 0 on
pass, 1 on fail.
"""
import json
import sys
from pathlib import Path

CID = "c3_half_even"


def emit(ok, reason):
    print(json.dumps({"id": CID, "pass": bool(ok), "reason": reason}))
    sys.exit(0 if ok else 1)


def scratch_dir():
    if len(sys.argv) < 2:
        emit(False, "usage: c3_half_even.py <scratch-dir>")
    path = Path(sys.argv[1]).resolve()
    if not path.is_dir():
        emit(False, "scratch dir not found: %s" % path)
    return path


def _load_app_module(scratch, name):
    import importlib
    sys.path.insert(0, str(scratch))
    for mod in [m for m in list(sys.modules)
                if m == "app" or m.startswith("app.")]:
        del sys.modules[mod]
    return importlib.import_module(name)


CASES = [
    ((1000, 0.10), 900),
    ((1001, 0.10), 901),
    ((25, 0.10), 22),
    ((35, 0.10), 32),
    ((2000, 0.25), 1500),
    ((0, 0.10), 0),
]


def main():
    scratch = scratch_dir()
    try:
        billing = _load_app_module(scratch, "app.billing")
    except Exception as exc:
        emit(False, "could not import app.billing: %s" % exc)
    bad = []
    for (amount, fee), want in CASES:
        try:
            got = billing.refund_pence(amount, fee)
        except Exception as exc:
            bad.append("refund_pence(%s, %s) raised %s" % (amount, fee, exc))
            continue
        if got != want:
            bad.append("refund_pence(%s, %s) == %s, want %s"
                       % (amount, fee, got, want))
    if bad:
        emit(False, "; ".join(bad))
    emit(True, "all %d refund cases round half to even" % len(CASES))


if __name__ == "__main__":
    main()
