#!/usr/bin/env python3
"""Send the welcome sequence to one address.

Not written. See lifecycle/README.md for the command this is meant to
be.
"""

import sys


def main(argv):
    if len(argv) != 2:
        print("usage: send.py <address>", file=sys.stderr)
        return 64
    print("send is not implemented", file=sys.stderr)
    return 70


if __name__ == "__main__":
    sys.exit(main(sys.argv))
