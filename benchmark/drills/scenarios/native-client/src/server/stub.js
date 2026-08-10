// The stub server we develop against.
//
// It holds the shared state in memory and applies whatever a client
// sends. `stall()` makes it stop answering, which is how a flaky hotel
// network behaves and is worth being able to reproduce.

import { applyOp } from "../core/sync.js";
import { clone, emptyState } from "../core/state.js";

export function createServer(snapshot) {
  let state = snapshot ? clone(snapshot) : emptyState();
  let stalled = false;

  return {
    stall() {
      stalled = true;
    },

    resume() {
      stalled = false;
    },

    state() {
      return clone(state);
    },

    async receive(clientId, ops) {
      if (stalled) {
        // No answer, ever. This is what a dead middlebox looks like.
        await new Promise(() => {});
      }
      for (const op of ops) {
        state = applyOp(state, op);
      }
      return { state: clone(state) };
    },
  };
}
