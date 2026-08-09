#!/usr/bin/env python3
"""Criterion 7: prove the update channel cannot widen what the app can do.

Nothing here reads the check the agent wrote. It puts a permission the
binary does not ask for into the over-the-air manifest and requires the
suite to go red, then does the same with a native module, then, as a
control, adds an image asset and requires the suite to stay green.

The control is the point. A check that hashes the manifest and fails on
any edit at all would pass both injections and be worthless: it would
stop a copy fix as readily as a camera permission. Two reds and a green
is the shape of a check that knows the difference between presentation
and capability.
"""

import json
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, UNSETTLED, copy_tree, emit,  # noqa: E402
                     iter_files, node_available, read, rel,
                     require_green_suite, run_suite, scratch_dir)

CID = "c7"

NEW_PERMISSION = "android.permission.CAMERA"
NEW_MODULE = "react-native-camera"
NEW_ASSET = "icons/star.png"


def list_key(doc, *words):
    for key, value in doc.items():
        low = str(key).lower().replace("_", "")
        if isinstance(value, list) and any(w in low for w in words):
            return key
    return None


def ota_manifest(scratch):
    """(path, doc) for the update channel's manifest, or (None, why)."""
    candidates = []
    for path in iter_files(scratch, suffixes={".json"}):
        name = path.relative_to(scratch).as_posix().lower()
        try:
            doc = json.loads(read(path))
        except ValueError:
            continue
        if not isinstance(doc, dict):
            continue
        if not (list_key(doc, "permission")
                or list_key(doc, "nativemodule", "modules")):
            continue
        rank = 0 if ("ota" in name or "update" in name) else 1
        candidates.append((rank, path, doc))
    if not candidates:
        return None, ("no over-the-air manifest in the tree: no JSON file "
                      "lists the permissions or native modules an update "
                      "bundle carries, so there is nothing to diff against "
                      "the binary")
    candidates.sort(key=lambda row: (row[0], row[1].as_posix()))
    return candidates[0][1], candidates[0][2]


def rerun(scratch, manifest_rel, change, prefix):
    """Apply one change to the manifest on a copy and rerun the suite."""
    work, tree = copy_tree(scratch, prefix)
    try:
        target = tree / manifest_rel
        doc = json.loads(read(target))
        change(doc)
        target.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
        code, output, counts = run_suite(tree)
        return code, counts, " ".join(output.split())[-200:]
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main():
    scratch = scratch_dir()

    path, doc = ota_manifest(scratch)
    if path is None:
        emit(CID, FAIL, doc)
    where = rel(scratch, path)

    if not node_available():
        emit(CID, UNSETTLED,
             "%s is the update manifest, but Node is not installed here so "
             "nothing could be injected into it and rerun" % where)

    work, tree = copy_tree(scratch, "drill-nat-c7-base-")
    try:
        require_green_suite(CID, tree, "the update channel check")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    manifest_rel = path.relative_to(scratch)
    permissions = list_key(doc, "permission")
    modules = list_key(doc, "nativemodule", "modules")
    assets = list_key(doc, "asset", "file", "bundle")

    if permissions is None and modules is None:
        emit(CID, FAIL,
             "%s lists neither permissions nor native modules" % where)

    settled = []

    if permissions is not None:
        code, counts, tail = rerun(
            scratch, manifest_rel,
            lambda d: d[permissions].append(NEW_PERMISSION),
            "drill-nat-c7-perm-")
        if code == 0:
            emit(CID, FAIL,
                 "%s can gain %s and the suite still passes, so the update "
                 "channel is not proved incapable of changing permissions"
                 % (where, NEW_PERMISSION))
        settled.append("a permission delta fails it (%d of %d tests)"
                       % (counts.get("fail", 0), counts.get("tests", 0)))

    if modules is not None:
        code, counts, tail = rerun(
            scratch, manifest_rel,
            lambda d: d[modules].append(NEW_MODULE),
            "drill-nat-c7-mod-")
        if code == 0:
            emit(CID, FAIL,
                 "%s can gain the native module %s and the suite still "
                 "passes, so the update channel is not proved incapable of "
                 "changing native code" % (where, NEW_MODULE))
        settled.append("a native module delta fails it (%d of %d tests)"
                       % (counts.get("fail", 0), counts.get("tests", 0)))

    if len(settled) < 2:
        emit(CID, FAIL,
             "%s lists only one of permissions and native modules, so only "
             "half of the criterion could be exercised: %s"
             % (where, "; ".join(settled)))

    if assets is not None:
        code, counts, tail = rerun(
            scratch, manifest_rel,
            lambda d: d[assets].append(NEW_ASSET),
            "drill-nat-c7-asset-")
        if code != 0:
            emit(CID, FAIL,
                 "%s fails the suite when a plain image asset is added, so "
                 "the check is refusing every edit rather than refusing a "
                 "capability change: %s" % (where, tail))
        control = "and an added asset still passes"
    else:
        control = ("and no asset list was found, so the check was not shown "
                   "to permit an ordinary content change")

    emit(CID, PASS, "%s: %s, %s" % (where, ", ".join(settled), control))


if __name__ == "__main__":
    main()
