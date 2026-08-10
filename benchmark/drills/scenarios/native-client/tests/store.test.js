import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { canonical, openStore } from "../src/core/index.js";

function scratch() {
  return fs.mkdtempSync(path.join(os.tmpdir(), "tern-store-"));
}

test("the store survives a reopen", () => {
  const dir = scratch();
  const store = openStore(dir);
  const state = store.read();
  state.preferences.theme = { value: "dark", by: "a", at: 1 };
  store.write(state);

  const reopened = openStore(dir);
  assert.equal(reopened.read().preferences.theme.value, "dark");
});

test("canonical does not care what order the keys went in", () => {
  const one = { notes: {}, preferences: { a: 1, b: 2 }, bookings: {},
                events: [] };
  const two = { events: [], bookings: {}, preferences: { b: 2, a: 1 },
                notes: {} };
  assert.equal(canonical(one), canonical(two));
});
