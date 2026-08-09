import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import {
  createClient, createServer, openStore,
} from "../src/core/index.js";

function client(id, server, at) {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "tern-sync-"));
  let tick = at;
  return createClient(id, openStore(dir), server, { clock: () => (tick += 1) });
}

test("a write is visible locally before anything is flushed", () => {
  const a = client("a", createServer(), 1000);
  a.apply({ class: "notes", id: "note-1", op: "append", text: "milk" });

  const segments = a.state().notes["note-1"].segments;
  assert.equal(segments.length, 1);
  assert.equal(segments[0].text, "milk");
  assert.equal(a.pending().length, 1);
});

test("flushing hands the write to the server and clears the queue",
  async () => {
    const server = createServer();
    const a = client("a", server, 2000);
    a.apply({ class: "bookings", id: "slot-09:00", op: "hold" });

    await a.flush();

    assert.equal(server.state().bookings["slot-09:00"].held_by, "a");
    assert.equal(a.pending().length, 0);
    assert.equal(a.status(), "ok");
  });
