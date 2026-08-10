#!/usr/bin/env python3
"""Check the sending domain before a bulk send.

Not written. See lifecycle/README.md for the command this is meant to
be, and lifecycle/dns/production.json for the shape of a zone file.
"""

import sys


def main(argv):
    if len(argv) != 3 or argv[1] != "--zone":
        print("usage: preflight.py --zone <path>", file=sys.stderr)
        return 64
    print("preflight is not implemented", file=sys.stderr)
    return 70


if __name__ == "__main__":
    sys.exit(main(sys.argv))
