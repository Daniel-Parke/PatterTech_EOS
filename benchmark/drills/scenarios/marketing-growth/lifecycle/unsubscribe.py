#!/usr/bin/env python3
"""Handle a one-click unsubscribe.

Not written. See lifecycle/README.md for the command this is meant to
be.
"""

import sys


def main(argv):
    if len(argv) != 3 or argv[1] != "post":
        print("usage: unsubscribe.py post <uri>", file=sys.stderr)
        return 64
    print("unsubscribe is not implemented", file=sys.stderr)
    return 70


if __name__ == "__main__":
    sys.exit(main(sys.argv))
