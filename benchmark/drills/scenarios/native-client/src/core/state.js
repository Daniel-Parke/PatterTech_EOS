// The state shape, and the one way we turn it into text.

export const WRITE_CLASSES = ["notes", "preferences", "bookings"];

export function emptyState() {
  return { notes: {}, preferences: {}, bookings: {}, events: [] };
}

export function clone(value) {
  return JSON.parse(JSON.stringify(value));
}

function sorted(value) {
  if (Array.isArray(value)) {
    return value.map(sorted);
  }
  if (value && typeof value === "object") {
    const out = {};
    for (const key of Object.keys(value).sort()) {
      out[key] = sorted(value[key]);
    }
    return out;
  }
  return value;
}

// Stable text for a state. Two states that mean the same thing produce
// the same string, so comparing runs is a string comparison. Object key
// order is normalised; array order is not, because array order is
// meaning here and hiding it would hide a bug.
export function canonical(state) {
  return JSON.stringify(sorted(state));
}
