#!/usr/bin/env python3
"""Criterion 3: kill the process mid-write, lose nothing, duplicate nothing.

Two claims, and they pull in opposite directions. Keeping a write means
writing it down before the network has it; not duplicating it means the
server has to recognise the same write twice. A queue that satisfies one
and not the other fails here.

The probe acknowledges a write, drops the client and the store objects
without flushing, which is what process death looks like from the
outside, reopens the store from the same directory and asks the revived
client what it still owes the server. Then it delivers that debt twice
and requires the server's state to be the same both times.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, iter_files, read,  # noqa: E402
                     run_probe, scratch_dir)

CID = "c3"

TEST_NAME = re.compile(r"(\.|[-_])test\.(c|m)?js$|(^|[\\/])test[-_.]",
                       re.I)
REPLAY = re.compile(r"idempot|replay|redeliver|restart|crash|process death|"
                    r"kill(ed)? the (app|process)|power", re.I)

PROBE = r"""
  const [openStore, createClient, createServer, canonical] =
    need(["openStore", "createClient", "createServer", "canonical"]);

  const TOKEN = "OUTBOX-SURVIVOR";
  const dir = scratch("crash");
  const server = createServer();
  let tick = 5000;
  const clock = () => (tick += 10);

  // The write is acknowledged the moment apply() returns: by then the
  // person has been told their edit landed.
  const doomed = createClient("device-a", openStore(dir), server, { clock });
  const ack = doomed.apply({ class: "notes", id: "note-1", op: "append",
                             text: TOKEN });
  if (!ack) {
    fail("apply() returned nothing, so there is no acknowledgement to hold " +
         "the client to");
  }

  // Process death. Nothing was flushed and both objects go away.
  const revived = createClient("device-a", openStore(dir), server, { clock });
  const queued = typeof revived.pending === "function" ? revived.pending()
                                                       : null;
  if (!Array.isArray(queued) || queued.length === 0) {
    fail("the acknowledged write did not survive a restart: reopening the " +
         "store from the same directory left the outbox empty, so the write " +
         "was acknowledged to the person and then died with the process");
  }

  const again = JSON.parse(JSON.stringify(queued));
  await revived.flush();

  const once = canonical(server.state());
  const seen = (once.match(new RegExp(TOKEN, "g")) || []).length;
  if (seen !== 1) {
    fail("after the restart flushed, the acknowledged write appears " + seen +
         " time(s) in the server state rather than once");
  }

  await server.receive("device-a", again);
  const twice = canonical(server.state());
  if (twice !== once) {
    const count = (twice.match(new RegExp(TOKEN, "g")) || []).length;
    fail("delivering the same queued write a second time changed the server " +
         "state (the write now appears " + count + " time(s)), so the queue " +
         "is not idempotent under repeated delivery");
  }

  ok("the acknowledged write survived a restart in the outbox, flushed " +
     "once, and redelivering it left the server state unchanged");
"""


def replay_tests(scratch):
    found = []
    for path in iter_files(scratch, suffixes={".js", ".mjs", ".cjs", ".ts",
                                              ".tsx"}):
        name = path.relative_to(scratch).as_posix()
        if not TEST_NAME.search(name):
            continue
        if REPLAY.search(read(path)):
            found.append(name)
    return found


def main():
    scratch = scratch_dir()

    found = replay_tests(scratch)
    if not found:
        emit(CID, FAIL,
             "no test in the tree mentions a restart, a crash, a replay or "
             "idempotence, so nothing in the project itself exercises what "
             "happens to a write when the process dies")

    good, reason, _ = run_probe(CID, scratch, PROBE)
    if good is None or not good:
        emit(CID, FAIL, reason)
    emit(CID, PASS, "%s covers it, and %s" % (found[0], reason))


if __name__ == "__main__":
    main()
