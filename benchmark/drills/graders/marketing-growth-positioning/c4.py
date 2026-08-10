#!/usr/bin/env python3
"""Criterion 4: every capability claimed is anchored in the repository.

A claim earns its place by naming something a reader can go and look
at: a path that exists in the tree, or a feature name the repository
itself uses. Both sides of that test are read out of the tree, so this
grader holds no private answer key.

Claims are read as items: a bullet with its nested lines, or a table
row. A document whose claims are pure prose has none this grader can
count, and it says that rather than guessing.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, claim_items, emit, feature_names,  # noqa: E402
                     names_a_feature, names_a_path, one_line, repo_paths,
                     scratch_dir, the_doc)

CID = "c4"

MINIMUM = 2


def main():
    scratch = scratch_dir()
    docs = the_doc(CID, scratch)
    features = feature_names(scratch)
    paths = repo_paths(scratch)

    best = None
    for where, text in docs:
        items = claim_items(text)
        if len(items) < MINIMUM:
            best = best or (
                where,
                "only %d claim(s) found. Claims are read as bullets, "
                "numbered items or table rows, so a document that makes "
                "them in flowing prose has none this grader can count. That "
                "is a limit of the grader as much as of the document: read "
                "the document before treating this as a finding"
                % len(items))
            continue
        unanchored = []
        anchored = []
        for item in items:
            path = names_a_path(item, paths)
            if path:
                anchored.append("%s -> %s" % (one_line(item, 45), path))
                continue
            feature = names_a_feature(item, features)
            if feature:
                anchored.append("%s -> %r" % (one_line(item, 45), feature))
                continue
            unanchored.append(item)
        if unanchored:
            best = best or (
                where,
                "%d of %d claims name nothing in the repository. First: %r. "
                "The tree offers %d file paths and %d feature names from the "
                "README, and this claim uses neither"
                % (len(unanchored), len(items), one_line(unanchored[0], 130),
                   len(paths), len(features)))
            continue
        emit(CID, PASS,
             "%s: all %d claims are anchored in the tree, for example %s"
             % (where, len(items), anchored[0]))

    where, why = best
    emit(CID, FAIL, "%s: %s" % (where, why))


if __name__ == "__main__":
    main()
