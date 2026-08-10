#!/usr/bin/env python3
"""notecat, a very small notes bundler.

Reads every Markdown file in a source directory and writes one combined
file into an output directory. No dependencies, no configuration file.
"""

import os
import sys

USAGE = "usage: cli.py [--source DIR] [--out-dir DIR] [--title TEXT]"

DEFAULTS = {"source": "notes", "out_dir": "build", "title": "Notes"}


def take(rest, flag):
    if not rest:
        print("error")
        sys.exit(1)
    return rest.pop(0)


def parse_args(argv):
    opts = dict(DEFAULTS)
    rest = list(argv)
    while rest:
        arg = rest.pop(0)
        if arg in ("-h", "--help"):
            print(USAGE)
            sys.exit(0)
        elif arg == "--source":
            opts["source"] = take(rest, arg)
        elif arg == "--out-dir":
            opts["out_dir"] = take(rest, arg)
        elif arg == "--title":
            opts["title"] = take(rest, arg)
        else:
            print("error")
            sys.exit(1)
    return opts


def collect(source):
    if not os.path.isdir(source):
        print("error")
        sys.exit(1)
    names = sorted(n for n in os.listdir(source) if n.endswith(".md"))
    return [os.path.join(source, n) for n in names]


def bundle(paths, title):
    parts = ["# %s" % title, ""]
    for path in paths:
        with open(path, encoding="utf-8") as handle:
            parts.append(handle.read().rstrip("\n"))
        parts.append("")
    return "\n".join(parts) + "\n"


def main(argv):
    opts = parse_args(argv)
    paths = collect(opts["source"])
    os.makedirs(opts["out_dir"], exist_ok=True)
    out = os.path.join(opts["out_dir"], "notes.md")
    with open(out, "w", encoding="utf-8") as handle:
        handle.write(bundle(paths, opts["title"]))
    print("wrote %s (%d notes)" % (out, len(paths)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
