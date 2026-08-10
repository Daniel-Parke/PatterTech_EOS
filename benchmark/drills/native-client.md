---
summary: Cold-agent acceptance drill for the native-client pack, an offline-capable client with a declared conflict policy and a forward-only release path
type: example
tags: [eos, testing]
---

# Drill: the write that survives the tunnel

Single run, cold agent, no human turns, pack plus this brief only.

## Brief handed to the agent

Build a single-surface task client for one mobile platform of your
choosing, backed by a local store and a stub server. It holds three
write classes: `notes` (concurrent edits expected), `preferences`
(single value per user) and `bookings` (a slot may be held by exactly
one user). Users work offline for arbitrary periods. Record the
architecture choice and the per-class conflict policy in
`CLIENT_DECISIONS.md`, and the release plan in `RELEASE.md`.

## Deterministic acceptance criteria

Pass requires every check. Each is a script exit code.

1. `conflict-policy.json` exists, validates against a schema in the
   repo, and names exactly one policy per write class from the set
   `converge`, `last-writer-wins`, `reserve-then-commit`,
   `reject-offline`. A test asserts the `bookings` policy is not
   `converge` or `last-writer-wins`.
2. A partition test harness runs two clients from a common snapshot,
   applies scripted divergent edits offline, reconnects and asserts the
   documented outcome per class. For `bookings` it asserts exactly one
   holder after convergence and a recorded compensation event for the
   loser. Run twice with swapped reconnection order: byte-identical
   final state both times.
3. Killing the process mid-write and restarting loses no acknowledged
   write and produces no duplicate: a replay test asserts the local
   queue is idempotent under repeated delivery.
4. A stalled server acknowledgement does not deadlock the client: a
   test drives the queue to its documented blocked state and asserts
   the app still reads, still renders, and surfaces a named degraded
   state within a fixed timeout.
5. Automated platform accessibility audit runs in the test suite over
   every screen and fails on any violation. Every item it cannot decide
   appears in `A11Y_MANUAL.md` with a written verdict, and that file's
   count equals the audit's undecided count. A static check asserts no
   unlabelled interactive element and explicit marking of decoration.
6. `RELEASE.md` contains no rollback step. A grep asserts the absence
   of rollback wording, and asserts a named kill-switch flag that a
   test exercises: with the flag off, the new behaviour is unreachable
   and the previous path still passes its tests.
7. Any over-the-air update channel is proved incapable of changing
   native code or permissions: the OTA manifest is diffed against the
   binary manifest and any permission or native-module delta fails.
8. `CLIENT_DECISIONS.md` cites at least three fragment or evidence ids;
   a link check asserts each resolves in the ledger.

## Scoring

All eight pass, or the drill fails. Criterion 2 with swapped order and
criterion 6 discriminate: they fail any agent that reached for a sync
library before choosing a policy, or wrote a runbook assuming it can
take a release back.
