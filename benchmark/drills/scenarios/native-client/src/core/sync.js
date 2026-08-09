// The client. A write goes into the local state and into the outbox,
// and the outbox goes to the server the next time we flush.

import { createOutbox } from "./outbox.js";
import { clone } from "./state.js";

// Every write goes through here, on the client and on the server, so
// the two cannot drift.
//
// Today it just applies whatever it is handed, in the order it is
// handed it. Nobody has decided what any of the three classes should do
// when two devices have both written, so the answer is "whichever one
// the server saw last".
export function applyOp(state, op) {
  const next = clone(state);
  if (op.class === "notes") {
    const note = next.notes[op.id] || { segments: [] };
    note.segments = note.segments.concat([
      { text: op.text, by: op.client, at: op.at },
    ]);
    next.notes[op.id] = note;
    return next;
  }
  if (op.class === "preferences") {
    next.preferences[op.id] = { value: op.value, by: op.client, at: op.at };
    return next;
  }
  if (op.class === "bookings") {
    next.bookings[op.id] = { held_by: op.client, at: op.at };
    return next;
  }
  throw new Error("unknown write class: " + op.class);
}

export function createClient(id, store, server, options = {}) {
  const outbox = createOutbox();
  const clock = options.clock || (() => Date.now());
  let seq = 0;
  let status = "ok";

  return {
    id,

    // What the screens read.
    state() {
      return store.read();
    },

    // What the status bar reads.
    status() {
      return status;
    },

    // Accept a write. Returning is the acknowledgement: by the time this
    // comes back the person has been told their edit landed.
    apply(op) {
      seq += 1;
      const stamped = Object.assign({}, op, {
        client: id,
        seq,
        opId: id + ":" + seq,
        at: clock(),
      });
      store.write(applyOp(store.read(), stamped));
      outbox.push(stamped);
      return stamped;
    },

    pending() {
      return outbox.pending();
    },

    // Push everything we have and take the server's state back.
    async flush() {
      const ops = outbox.pending();
      if (ops.length === 0) {
        return { state: store.read() };
      }
      status = "syncing";
      const reply = await server.receive(id, ops);
      outbox.clear();
      store.write(reply.state);
      status = "ok";
      return reply;
    },
  };
}
