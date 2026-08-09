#!/usr/bin/env python3
"""Criterion 4: a server that never answers must not take the app with it.

The probe stalls the stub server, pushes a write, and then waits. Three
things have to be true inside the window: the client stops waiting and
says so, the name it says is one the decisions file already uses, and
reads keep working the whole time.

The naming half matters as much as the behaviour. A client that flips an
internal boolean nobody has written down has not surfaced a degraded
state; it has one. So the status the probe observes is looked up in
`CLIENT_DECISIONS.md`, and a state the document never mentions fails.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (DECISIONS, FAIL, PASS, emit, find_named,  # noqa: E402
                     read, rel, run_probe, scratch_dir)

CID = "c4"

WINDOW_MS = 12000

PROBE = r"""
  const [openStore, createClient, createServer] =
    need(["openStore", "createClient", "createServer"]);

  const TOKEN = "STALLED-WRITE";
  const HEALTHY = new Set(["ok", "idle", "ready", "online", "synced",
                           "syncing", "sync", "up-to-date", "uptodate",
                           "connected", "clean", "pending", "true", "false"]);

  function statusName(value) {
    if (typeof value === "string") return value;
    if (value && typeof value === "object") {
      for (const key of ["state", "status", "name", "kind", "label"]) {
        if (typeof value[key] === "string") return value[key];
      }
    }
    return null;
  }

  const server = createServer();
  if (typeof server.stall !== "function") {
    fail("the stub server no longer offers stall(), so an acknowledgement " +
         "that never arrives cannot be reproduced against this tree");
  }

  const dir = scratch("stall");
  let tick = 7000;
  const client = createClient("device-a", openStore(dir), server,
                              { clock: () => (tick += 10) });
  client.apply({ class: "notes", id: "note-1", op: "append", text: TOKEN });

  server.stall();
  // Deliberately not awaited. The whole question is what the app does
  // while this never comes back.
  Promise.resolve().then(() => client.flush()).catch(() => {});

  const started = Date.now();
  let degraded = null;
  let last = null;
  while (Date.now() - started < %(window)d) {
    const name = statusName(
      typeof client.status === "function" ? client.status() : undefined);
    last = name;
    if (name && !HEALTHY.has(String(name).toLowerCase())) {
      degraded = name;
      break;
    }
    await sleep(25);
  }
  const waited = Date.now() - started;

  if (!degraded) {
    fail("with the server never acknowledging, the client's status stayed " +
         "at " + JSON.stringify(last) + " for " + waited + "ms and no named " +
         "degraded state was surfaced");
  }

  const state = client.state();
  if (!JSON.stringify(state === undefined ? null : state).includes(TOKEN)) {
    fail("the client reports " + JSON.stringify(degraded) + " but can no " +
         "longer read back its own write, so the stall took the read path " +
         "with it");
  }

  ok("the client surfaced " + JSON.stringify(degraded) + " after " + waited +
     "ms with the server silent, and still reads its own state",
     { status: String(degraded), waited_ms: waited });
"""


def tokens(name):
    return [t for t in re.split(r"[^A-Za-z0-9]+", str(name).lower()) if t]


def documented(text, name):
    body = text.lower()
    if str(name).lower() in body:
        return True
    words = [t for t in tokens(name) if len(t) >= 4]
    return bool(words) and all(w in body for w in words)


def main():
    scratch = scratch_dir()

    good, reason, extra = run_probe(CID, scratch, PROBE % {"window":
                                                           WINDOW_MS},
                                    timeout=180)
    if good is None or not good:
        emit(CID, FAIL, reason)

    found = find_named(scratch, DECISIONS)
    if not found:
        emit(CID, FAIL,
             "%s and there is no %s, so the state it surfaces is not a "
             "documented one" % (reason, DECISIONS))

    status = extra.get("status", "")
    if not documented(read(found[0]), status):
        emit(CID, FAIL,
             "%s, but %s never mentions %r, so the blocked state the client "
             "shows is not the one the project wrote down"
             % (reason, rel(scratch, found[0]), status))

    emit(CID, PASS,
         "%s, and %s names that state" % (reason, rel(scratch, found[0])))


if __name__ == "__main__":
    main()
