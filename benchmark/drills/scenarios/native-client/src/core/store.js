// The local store: one JSON file in the app's data directory.

import fs from "node:fs";
import path from "node:path";

import { clone, emptyState } from "./state.js";

export function openStore(dir) {
  fs.mkdirSync(dir, { recursive: true });
  const file = path.join(dir, "state.json");

  let state = emptyState();
  if (fs.existsSync(file)) {
    try {
      state = JSON.parse(fs.readFileSync(file, "utf8"));
    } catch {
      // A half-written file is treated as no file. Rare, and the server
      // is the backstop.
      state = emptyState();
    }
  }

  return {
    dir,
    read() {
      return clone(state);
    },
    write(next) {
      state = clone(next);
      fs.writeFileSync(file, JSON.stringify(state), "utf8");
    },
  };
}
