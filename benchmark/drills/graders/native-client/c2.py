#!/usr/bin/env python3
"""Criterion 2: two clients, a partition, and the same answer either way.

The criterion has three parts and this grader takes all three.

- A partition harness exists in the tree and the suite it belongs to
  passes. Nothing here reads the harness to see what it asserts; that
  is what the probe below is for.
- The grader then runs its own partition, twice, with the reconnection
  order swapped, driving the delivered core through the surface the
  fixture's own tests use. The two converged states are compared as
  text. Byte-identical is the criterion's word and it is taken
  literally.
- After convergence exactly one device holds the contested slot, and
  the state records something about the other one. A merge that quietly
  drops the loser converges and is still wrong.

What this grader does not settle: "the documented outcome per class".
Reading a decisions file and deciding whether the converged notes match
what it promised is not a thing a script can do honestly, so the notes
and preferences classes are only held to order-independence here.
"""

import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, copy_tree, emit, iter_files,  # noqa: E402
                     require_green_suite, run_probe, scratch_dir)

CID = "c2"

PROBE = r"""
  const [openStore, createClient, createServer, canonical] =
    need(["openStore", "createClient", "createServer", "canonical"]);

  const HOLDER_KEYS = ["held_by", "heldBy", "holder", "owner", "winner",
                       "held", "by", "client"];
  const COMPENSATION =
    /compensat|releas|refund|reject|supersed|surrender|declin|conflict|lost|freed|notif|bump|evict/i;

  function holderOf(entry) {
    if (typeof entry === "string") return entry;
    if (entry && typeof entry === "object" && !Array.isArray(entry)) {
      for (const key of HOLDER_KEYS) {
        if (typeof entry[key] === "string") return entry[key];
      }
    }
    const text = JSON.stringify(entry === undefined ? null : entry);
    const named = ["device-a", "device-b"].filter((id) => text.includes(id));
    return named.length === 1 ? named[0] : null;
  }

  // One snapshot, two devices, the same scripted divergence every time.
  // Only the order in which they reconnect changes.
  async function converge(order) {
    const server = createServer();
    const made = {};
    for (const id of ["device-a", "device-b"]) {
      let tick = id === "device-a" ? 1000 : 1005;
      made[id] = createClient(id, openStore(scratch(id)), server,
                              { clock: () => (tick += 10) });
    }
    const a = made["device-a"];
    const b = made["device-b"];

    a.apply({ class: "notes", id: "note-1", op: "append", text: "buy milk" });
    b.apply({ class: "notes", id: "note-1", op: "append", text: "and bread" });
    a.apply({ class: "preferences", id: "theme", op: "set", value: "dark" });
    b.apply({ class: "preferences", id: "theme", op: "set", value: "light" });
    a.apply({ class: "bookings", id: "slot-09:00", op: "hold" });
    b.apply({ class: "bookings", id: "slot-09:00", op: "hold" });

    for (const id of order) {
      await made[id].flush();
    }
    return server.state();
  }

  const first = await converge(["device-a", "device-b"]);
  const second = await converge(["device-b", "device-a"]);

  const one = canonical(first);
  const two = canonical(second);
  if (one !== two) {
    let at = 0;
    while (at < one.length && at < two.length && one[at] === two[at]) at += 1;
    fail("the converged state depends on which device reconnected first: " +
         "the two runs differ from character " + at + " (" +
         JSON.stringify(one.slice(at, at + 90)) + " against " +
         JSON.stringify(two.slice(at, at + 90)) + ")");
  }

  const slot = first.bookings && first.bookings["slot-09:00"];
  if (slot === undefined) {
    fail("nothing holds slot-09:00 after convergence, though both devices " +
         "held it offline");
  }
  const holder = holderOf(slot);
  if (holder !== "device-a" && holder !== "device-b") {
    fail("after convergence slot-09:00 does not name exactly one holder: " +
         JSON.stringify(slot));
  }
  const loser = holder === "device-a" ? "device-b" : "device-a";

  const events = first.events;
  if (events === undefined || events === null) {
    fail("the converged state records no events at all, so nothing says " +
         "what happened to " + loser + ", which also held slot-09:00 " +
         "offline");
  }
  const record = JSON.stringify(events);
  if (!record.includes(loser)) {
    fail(holder + " holds slot-09:00 and nothing recorded against " + loser +
         ", whose offline hold was dropped in silence");
  }
  if (!COMPENSATION.test(record)) {
    fail("the events mention " + loser + " but name no compensation: " +
         record.slice(0, 200));
  }

  ok("byte-identical convergence in both reconnection orders (" +
     one.length + " characters), " + holder + " alone holds slot-09:00, " +
     "and the events carry a compensation for " + loser);
"""


def harnesses(scratch):
    return [p.relative_to(scratch).as_posix() for p in iter_files(scratch)
            if "partition" in p.relative_to(scratch).as_posix().lower()]


def main():
    scratch = scratch_dir()

    found = harnesses(scratch)
    if not found:
        emit(CID, FAIL,
             "no partition harness in the tree: nothing under any path "
             "naming a partition, so the two-client scenario is never run "
             "by the project itself")

    work, tree = copy_tree(scratch, "drill-nat-c2-")
    try:
        counts = require_green_suite(CID, tree, "the partition harness")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    good, reason, _ = run_probe(CID, scratch, PROBE)
    if good is None:
        emit(CID, FAIL, reason)
    if not good:
        emit(CID, FAIL, reason)
    emit(CID, PASS,
         "%s, the suite passes (%d tests), and %s"
         % (", ".join(found[:3]), counts.get("tests", 0), reason))


if __name__ == "__main__":
    main()
