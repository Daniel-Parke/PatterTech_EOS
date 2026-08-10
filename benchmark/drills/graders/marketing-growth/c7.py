#!/usr/bin/env python3
"""Criterion 7: the preflight fails closed, and each gate names itself.

Six negative fixtures, six distinct non-zero exits, and the healthy zone
still exits 0. The last is what stops a script that refuses everything
from passing: absent evidence must be a failure, but so must a preflight
that cannot tell a good zone from a bad one.

Fixtures are matched by filename. A zone missing SPF has to say so in
its name, which is how a human reading a CI log finds it too.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, all_files, emit, find_script,  # noqa: E402
                     run, scratch_dir, work_copy)

CID = "c7"

GATES = (
    ("SPF", ("spf",)),
    ("DKIM", ("dkim",)),
    ("DMARC", ("dmarc",)),
    ("forward DNS", ("forward", "fdns", "a-record", "a_record")),
    ("reverse DNS", ("reverse", "rdns", "ptr")),
    ("TLS", ("tls",)),
)

ZONE_SUFFIXES = (".json", ".zone", ".txt", ".yaml", ".yml", ".toml")


def zone_files(scratch):
    out = []
    for path in all_files(scratch):
        if path.suffix.lower() not in ZONE_SUFFIXES:
            continue
        rel = path.relative_to(scratch).as_posix().lower()
        if "dns" in rel or "zone" in rel or "preflight" in rel:
            out.append(path)
    return out


def main():
    scratch = scratch_dir()
    script = find_script(scratch, "preflight")
    if script is None:
        emit(CID, FAIL, "no preflight script in the tree")
    rel_script = script.relative_to(scratch).as_posix()

    zones = zone_files(scratch)
    if not zones:
        emit(CID, FAIL, "no zone files found, so the preflight has nothing "
                        "to check against")

    healthy = [z for z in zones
               if "production" in z.name.lower() or "live" in z.name.lower()]
    if not healthy:
        healthy = [z for z in zones
                   if not any(k in z.name.lower()
                              for _, keys in GATES for k in keys)]
    if not healthy:
        emit(CID, FAIL, "no healthy zone among %d zone file(s), so nothing "
                        "shows the preflight can pass" % len(zones))

    negatives = {}
    for name, keys in GATES:
        for zone in zones:
            rel = zone.relative_to(scratch).as_posix().lower()
            if zone in healthy:
                continue
            if any(key in rel for key in keys):
                negatives.setdefault(name, zone)
                break

    missing = [name for name, _ in GATES if name not in negatives]
    if missing:
        emit(CID, FAIL,
             "no negative fixture for %s. Zone files seen: %s"
             % (", ".join(missing),
                ", ".join(z.relative_to(scratch).as_posix()
                          for z in zones)[:200]))

    with work_copy(scratch) as tree:
        rel_good = healthy[0].relative_to(scratch).as_posix()
        code, out = run(tree / rel_script, ["--zone", rel_good], tree)
        if code is None:
            emit(CID, FAIL, "%s would not run: %s"
                            % (rel_script, out[:200]))
        if code != 0:
            emit(CID, FAIL,
                 "%s exits %d on the healthy zone %s, so it refuses "
                 "everything rather than gating anything (%s)"
                 % (rel_script, code, rel_good,
                    out.strip()[-160:] or "no output"))

        codes, passed = {}, []
        for name, _ in GATES:
            rel_zone = negatives[name].relative_to(scratch).as_posix()
            code, out = run(tree / rel_script, ["--zone", rel_zone], tree)
            if code == 0:
                passed.append("%s (%s)" % (name, rel_zone))
            codes[name] = code
        if passed:
            emit(CID, FAIL, "the preflight does not fail closed: it exits 0 "
                            "with %s absent" % ", ".join(passed))

    seen = list(codes.values())
    if len(set(seen)) != len(GATES):
        emit(CID, FAIL,
             "six gates but %d distinct exit code(s): %s. A failure that "
             "does not name itself reports a generic red"
             % (len(set(seen)),
                ", ".join("%s=%s" % (n, c) for n, c in codes.items())))

    emit(CID, PASS,
         "%s exits 0 on %s and gives six distinct non-zero exits: %s"
         % (rel_script, rel_good,
            ", ".join("%s=%s" % (n, c) for n, c in codes.items())))


if __name__ == "__main__":
    main()
