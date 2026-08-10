#!/usr/bin/env python3
"""Criterion 1: one declared policy per write class, and a test that
holds the booking class to it.

Four separate things, in the order the criterion states them: the file
exists and parses, a schema in the repo accepts it, it names exactly one
policy per write class out of the allowed four, and the booking policy
is neither of the two that cannot hold a slot.

The last clause of the criterion, "a test asserts the bookings policy is
not converge or last-writer-wins", is settled by breaking it. The
grader copies the tree, rewrites the booking policy to
`last-writer-wins`, and requires the suite to go red. A suite that stays
green is not asserting anything about the booking policy; it is
asserting that a file exists.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, POLICIES, UNSETTLED, Unsupported,  # noqa: E402
                     WRITE_CLASSES, copy_tree, emit, find_named,
                     iter_files, looks_like_schema, node_available,
                     policy_pairs, read, rel, require_green_suite, run_suite,
                     scratch_dir, set_at, validate)

import shutil  # noqa: E402

CID = "c1"

POLICY_FILE = "conflict-policy.json"
BANNED_FOR_BOOKINGS = ("converge", "last-writer-wins")


def schema_candidates(scratch, policy_path):
    """Schema files in the repo, most likely first."""
    found = []
    for path in iter_files(scratch, suffixes={".json"}):
        if path == policy_path:
            continue
        try:
            doc = json.loads(read(path))
        except ValueError:
            continue
        if not looks_like_schema(doc):
            continue
        name = path.name.lower()
        rank = 0 if "conflict" in name else 1 if "policy" in name else 2
        found.append((rank, path, doc))
    return [(p, d) for _, p, d in sorted(found, key=lambda r: (r[0],
                                                              r[1].name))]


def check_schema(scratch, policy_path, doc):
    """(ok, message). Unsettled schemas are reported, never waved past."""
    candidates = schema_candidates(scratch, policy_path)
    if not candidates:
        return False, ("no JSON Schema anywhere in the tree, so %s validates "
                       "against nothing" % POLICY_FILE)
    problems, unsettled = [], []
    for path, schema in candidates:
        try:
            errors = validate(doc, schema)
        except Unsupported as exc:
            unsettled.append("%s uses %s" % (rel(scratch, path), exc))
            continue
        if not errors:
            return True, "validates against %s" % rel(scratch, path)
        problems.append("%s rejects it (%s)"
                        % (rel(scratch, path), "; ".join(errors[:3])))
    if problems:
        return False, "; ".join(problems[:2])
    return None, ("the only schema-shaped files in the tree use keywords "
                  "this grader does not implement (%s), so nothing was "
                  "validated" % "; ".join(unsettled[:2]))


def check_classes(pairs):
    """(ok, message, per-class rows) for the one-policy-per-class rule."""
    by_class = {}
    for path, name, policy in pairs:
        by_class.setdefault(name, []).append((path, policy))

    missing = [c for c in WRITE_CLASSES if c not in by_class]
    if missing:
        return False, ("no policy for %s; the brief names three write "
                       "classes and each needs exactly one policy from %s"
                       % (", ".join(missing), ", ".join(POLICIES))), by_class

    for name in WRITE_CLASSES:
        policies = {p for _, p in by_class[name]}
        if len(policies) > 1:
            return False, ("%s is given %d different policies (%s); the "
                           "criterion is exactly one"
                           % (name, len(policies), ", ".join(sorted(
                               policies)))), by_class
    return True, "", by_class


def mutation_bites(scratch, policy_path, path_to_booking):
    """Switch bookings to last-writer-wins; the suite must notice."""
    work, tree = copy_tree(scratch, "drill-nat-c1-")
    try:
        require_green_suite(CID, tree,
                            "the assertion about the booking policy")
        target = tree / policy_path.relative_to(scratch)
        doc = json.loads(read(target))
        set_at(doc, path_to_booking, "last-writer-wins")
        target.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
        code, output, counts = run_suite(tree)
        if code == 0:
            return False, ("the suite still passes with the booking policy "
                           "rewritten to last-writer-wins, so nothing in it "
                           "asserts what that policy may be")
        return True, ("the suite fails (%d of %d tests) when the booking "
                      "policy is rewritten to last-writer-wins"
                      % (counts.get("fail", 0), counts.get("tests", 0)))
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    scratch = scratch_dir()

    found = find_named(scratch, POLICY_FILE)
    if not found:
        emit(CID, FAIL, "no %s anywhere in the delivered tree" % POLICY_FILE)
    policy_path = found[0]
    try:
        doc = json.loads(read(policy_path))
    except ValueError as exc:
        emit(CID, FAIL, "%s does not parse: %s"
             % (rel(scratch, policy_path), exc))

    good, message = check_schema(scratch, policy_path, doc)
    if good is None:
        emit(CID, UNSETTLED, message)
    if not good:
        emit(CID, FAIL, message)
    schema_note = message

    pairs = policy_pairs(doc)
    if not pairs:
        emit(CID, FAIL,
             "%s names no write class against any of %s"
             % (rel(scratch, policy_path), ", ".join(POLICIES)))

    good, message, by_class = check_classes(pairs)
    if not good:
        emit(CID, FAIL, message)

    booking_path, booking_policy = by_class["bookings"][0]
    if booking_policy in BANNED_FOR_BOOKINGS:
        emit(CID, FAIL,
             "bookings is given %r; a slot held by exactly one user cannot "
             "take a policy that merges or overwrites, which is the whole "
             "reason the class is called out" % booking_policy)

    stated = ", ".join("%s=%s" % (c, by_class[c][0][1])
                       for c in WRITE_CLASSES)

    if not node_available():
        emit(CID, UNSETTLED,
             "%s %s and declares %s, but Node is not installed here so the "
             "test that must hold bookings to it was not exercised"
             % (rel(scratch, policy_path), schema_note, stated))

    bites, note = mutation_bites(scratch, policy_path, booking_path)
    if not bites:
        emit(CID, FAIL, "%s declares %s, but %s" % (
            rel(scratch, policy_path), stated, note))

    emit(CID, PASS,
         "%s %s, declares %s, and %s" % (rel(scratch, policy_path),
                                         schema_note, stated, note))


if __name__ == "__main__":
    main()
