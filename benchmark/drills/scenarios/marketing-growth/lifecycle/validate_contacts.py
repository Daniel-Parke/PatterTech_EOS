#!/usr/bin/env python3
"""Check a contact file before it is mailed.

Not written. See lifecycle/README.md for the command this is meant to
be.
"""

import sys


def main(argv):
    if len(argv) != 2:
        print("usage: validate_contacts.py <path>", file=sys.stderr)
        return 64
    print("validate_contacts is not implemented", file=sys.stderr)
    return 70


if __name__ == "__main__":
    sys.exit(main(sys.argv))
