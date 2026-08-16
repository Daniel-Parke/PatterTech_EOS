---
summary: The pack applied end to end to a single-surface task client with three write classes, one of them invariant-bearing
kind: example
scope: estate
type: example
tags: [eos, state, a11y, delivery]
---

# EX-NAT-001: the write that survives the tunnel

A worked example, shaped like the pack's own acceptance drill. One
mobile client, a local store, a stub server, three write classes:
`notes` where concurrent edits are expected, `preferences` with one
value per user, and `bookings` where a slot may be held by exactly one
user. Users work offline for arbitrary periods.

The decisions below were taken in this order, and the order is the
point.

## 1. Activation

`ships_a_binary`, `has_native_ui`, `has_local_write_store`,
`has_invariant_bearing_writes` and `distributes_via_app_store` are all
true. `has_remote_update_channel` is false, because the architecture
chosen at step 2 does not have one. So B1 to B4, B6 and B7 apply, and
B5 does not.

`packs/ui-ux/PACK.md` also loads, for interaction states, tokens and
the philosophy record. Its web requirements do not apply, and this pack
supplies the conformance profile instead.

## 2. Architecture, before any code

WG-NAT-001, ruled B: shared logic with a native user interface. Two
people, six screens, one invariant that must behave identically on both
platforms. Runner-up was A, two native codebases, refused on
release-train cost for a team of two. C was refused because the
accessibility budget would move from the toolkit into our own code for
no product benefit. D was refused because nobody on the team writes
JavaScript.

Recorded in `CLIENT_DECISIONS.md` with three cited evidence ids.

## 3. Write classification, before any sync library

B1. Classified using `packs/native-client/references/WRITE_CLASSES.md`:

| Class | Classification | Policy | Why |
| --- | --- | --- | --- |
| notes | commutative | `converge` | two offline edits in either order give a result both users accept |
| preferences | last-writer-acceptable | `last-writer-wins` | one value per user, losing a concurrent edit is annoying and harmless |
| bookings | invariant-bearing | `reserve-then-commit` | exactly one holder per slot, named out loud |

`conflict-policy.json` holds exactly this, validated against a schema
in the repository. A test asserts the `bookings` policy is neither
`converge` nor `last-writer-wins`, which is B2 made executable.

Only then was the sync approach chosen: WG-NAT-002 option D, read-path
sync with conventional writes, a convergent store for notes only, and a
server-issued reservation for bookings.

## 4. The booking path

B2 in full. Online, the client asks the server to hold the slot and
receives a reservation with an identity and an expiry. Offline, the
client accepts a booking only against an unexpired reservation, and
otherwise degrades to `reject-offline` with a message naming why. On
reconnection the reservation is redeemed. If redemption fails, a named
compensation event fires: the user is told, local state reverts, and
the event is recorded.

The partition test runs two clients from a common snapshot, applies
scripted divergent edits offline, reconnects and asserts the documented
outcome per class. For `bookings` it asserts exactly one holder after
convergence and a recorded compensation event for the loser. It runs
twice with the reconnection order swapped and asserts byte-identical
final state both times, which is what proves the outcome is a property
of the policy rather than of the timing.

## 5. The outbox

B3. Writes are acknowledged in the interface only after the local
commit, so killing the process mid-write loses no acknowledged write. A
client-generated identity on every mutation is deduplicated
server-side, and a replay test drives repeated delivery and asserts one
effect.

The blocked state is named `sync paused`. A test drives the queue into
it with a stalled acknowledgement, then asserts that the app still
reads, still renders, and shows the named state within five seconds.
The flag service is read independently of the sync queue, so the kill
switch still works while the queue is blocked.

## 6. Accessibility

WG-NAT-004, ruled C. Six screens, so six claims, not one.

Semantics declared in code on every screen: content descriptions,
descendant merging on the booking card, explicit heading semantics,
custom actions with human labels, and null descriptions marking
decoration. The platform audit runs in the test suite over every
screen and fails on any violation. A static check asserts no unlabelled
interactive element and that decoration is explicitly marked.

`A11Y_MANUAL.md` carries one written verdict per undecided item, each
naming what was inspected and the conclusion, and its entry count
equals the audit's undecided count. Clause 11 items were checked by
hand: the app is driven end to end with the platform screen reader, and
the system text size and reduce-motion settings are honoured.

Numeric floors came from WCAG 2.2 through the mobile mapping, because
the platform guidance publishes none.

## 7. Release

WG-NAT-003, ruled C. `RELEASE.md` has two sections, one per store,
because the mechanics are not symmetric. Play ships at one per cent
first with the halt trigger written down before the release starts:
crash-free sessions below the previous release's figure by more than
half a point, judged at the two-hour mark. Apple's phased release is
left on and treated as unsteerable.

The reservation path ships behind a flag named
`booking_reservation_v2`. With the flag off, the new behaviour is
unreachable and the previous path still passes its tests. A grep
asserts no rollback wording appears anywhere in `RELEASE.md`, because
no rollback exists.

One rejection cycle is in the calendar. The target SDK bump is on the
roadmap with the published deadline as its date.

## 8. Contract change

B7. The reservation endpoint shipped alongside the old direct-booking
endpoint. The old one is removed only when telemetry shows the last
binary that calls it below the agreed threshold, which is expand,
migrate, contract with the wait measured from live versions rather than
from the release date.

## What this example does not show

No performance comparison between architectures, because none that we
could retrieve is serious. No claim that this policy set is right for
another product: the classification is the transferable part, and the
policies fall out of it.
