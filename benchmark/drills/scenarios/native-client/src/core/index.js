// The core's surface. The screens and the tests import from here and
// nothing else, so the inside can be rearranged without a sweep through
// the app.

export { WRITE_CLASSES, canonical, clone, emptyState } from "./state.js";
export { openStore } from "./store.js";
export { createOutbox } from "./outbox.js";
export { applyOp, createClient } from "./sync.js";
export { flag, flags } from "./flags.js";
export { createServer } from "../server/stub.js";
