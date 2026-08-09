// Writes waiting to reach the server.
//
// In memory for now. It was fine on the demo laptop.

export function createOutbox() {
  const queue = [];
  return {
    push(op) {
      queue.push(op);
    },
    pending() {
      return queue.slice();
    },
    clear() {
      queue.length = 0;
    },
  };
}
