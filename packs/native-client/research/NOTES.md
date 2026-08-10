---
summary: Research synthesis for the native-client pack, four client architectures, three sync philosophies, store release mechanics and the non-web accessibility profile
type: example
tags: [eos, testing]
---

# native-client research synthesis (cutoff 2026-08-03)

Purpose: give the pack an honest basis for three decisions that are
hard to reverse once a product ships. Which client architecture. What
happens to a write made with no network. How a fix reaches a user.

The through-line: on the web you own the ship path, on a client you
rent it. Every recommendation below falls out of that.

## The spine that does not vary

1. **The store owns the rollback, and there is no rollback.** Apple
   ramps automatic updates on a fixed 1, 2, 5, 10, 20, 50, 100 per cent
   schedule over seven days with no developer dial, and anyone can pull
   the new build manually at any moment (FRAG-NATIVE-05). Play gives
   the dial and a halt, but halting only stops further delivery and the
   documented remedy for a bad build is to ship another one
   (FRAG-NATIVE-06). Neither store can take a version back. So every
   release is forward-only, and the only real containment lever is a
   remote kill switch inside the binary. Flags (EV-0026) are not a
   nicety on a client, they are the rollback.
2. **Rejection is the normal case.** Apple rejected 2,093,244 of
   9,100,620 submissions in 2025, roughly one in four, with Performance
   the largest bucket at 1,354,418 (FRAG-NATIVE-04). Plan a release
   calendar with a rejection cycle in it, not as an exception path.
   Note the bucket is coarse and self-categorised, so it cannot be
   decomposed into engineering actions.
3. **Non-web accessibility is its own conformance profile.** This is
   the profile the ui-ux pack defers to. The unit of conformance is a
   screen, not a page (FRAG-NATIVE-01), and the instrument that binds
   in the EU is EN 301 549 clause 11 (FRAG-NATIVE-02), which adds
   assistive-technology interoperability and user-preference support on
   top of the WCAG criteria in EV-0027. The reviewable artefact is the
   semantics declaration in code (FRAG-NATIVE-18), not a screenshot.
4. **Distribution decays without a release train.** From 31 August 2026
   Play requires API 36 for new submissions and API 35 for an existing
   app to stay visible to new users on current devices
   (FRAG-NATIVE-07). An unmaintained client does not stagnate, it goes
   quietly invisible.

## Four client architectures

**A. Two native codebases** (SwiftUI plus Compose). Platform
conventions, accessibility services and system controls arrive for
free, which is what Apple's HIG assumes (EV-0230) and where the
platform semantics APIs are richest (FRAG-NATIVE-18). Cost is two of
everything, including two accessibility passes and two release trains.

*Fits when*: the surface is small and deep, the product competes on
platform feel, or one platform carries the revenue.

**B. Shared logic, native user interface** (Kotlin Multiplatform, or a
Rust core with native shells). JetBrains grades this honestly: core KMP
is Stable on Android, iOS, JVM and JS while Compose Multiplatform is a
separate and independent grade (FRAG-NATIVE-17). Sharing domain logic
and sharing pixels are two decisions, and B takes only the first.

*Fits when*: the risk is business-rule divergence between platforms
rather than user-interface cost. This is the default we would argue for
most products with real domain logic.

**C. Own the renderer** (Flutter). One behaviour everywhere because the
framework draws everything itself (FRAG-NATIVE-16). The same property
means platform conventions and accessibility behaviour arrive only as
far as the framework reimplemented them, and the repository does not
grade its targets.

*Fits when*: brand-uniform interface across platforms is the goal, the
design language is deliberately non-native, or a small team must ship
one surface to many places.

**D. Platform widgets driven by shared code** (React Native). The
project rewrote its own interop layer, default from 0.76 after opt-in
from 0.68, and still ships an opt-out without declaring the old path
dead (FRAG-NATIVE-15). Read that as the honest cost model: the seam
between shared and platform code is a permanent migration surface. On
a zero-major version scheme, SemVer expectations (EV-0171) do not
apply.

*Fits when*: web and client teams are the same people, or an existing
JavaScript product needs a client quickly and the OTA path in
FRAG-NATIVE-08 is worth real money.

**Not a fourth option: the wrapped website.** Apple rule 4.2 rejects a
repackaged site outright (FRAG-NATIVE-03). A web shell has to earn its
binary.

**Where the evidence is thin.** We could not obtain a retrievable,
methodologically serious comparison of these architectures on
performance, energy or defect rate. The trade press comparisons found
at this cutoff are unsourced or vendor-adjacent, and the one academic
study surfaced benchmarks a tic-tac-toe app behind a paywall. Treat all
framework performance claims as unevidenced, and choose on team shape,
platform-feel requirements and the accessibility and release properties
above, which are documented.

## Three sync philosophies

**1. Online-required with a read cache.** No local writes. Conflicts
cannot occur. Cheapest correct answer and the right default until an
offline write is a named requirement.

**2. Server-authoritative sync** (PowerSync FRAG-NATIVE-14, and
Electric's read-path engine FRAG-NATIVE-13). Local reads are fast, a
blocking FIFO upload queue holds the client at its last confirmed
checkpoint until the backend acknowledges, so the client never resolves
a conflict locally. The vendor states plainly that there is no single
correct choice for handling a write failure: the conflict policy is
application code you write and test. Failure mode is head-of-line
blocking, one stuck mutation stalls the whole client.

**3. Convergent replication** (Automerge FRAG-NATIVE-11, Yjs
FRAG-NATIVE-12, semantics in FRAG-NATIVE-10). Merges without a round
trip, no blocking, and the documents grow: Yjs says outright that
text-suitable CRDTs only grow and answers with conditional tombstone
collection. Storage and compaction are first-class, not tuning.

**The load-bearing contradiction.** "Conflict-free" is a claim about
convergence, not about correctness. FRAG-NATIVE-10 proves replicas
agree and no update is lost; it says nothing about whether the agreed
value satisfies a uniqueness constraint, a balance, an approval state
or a user's intent. Meanwhile the shipped server-authoritative products
say there is no single correct write-failure policy. Both are right,
and together they mean the choice of library never answers the question
that matters. The pack should force the question first: classify writes
into commutative (notes, sets, counters), last-writer-acceptable
(preferences, drafts) and invariant-bearing (money, bookings,
permissions), and forbid offline acceptance of the third class without
a named reservation or compensation mechanism.

Note also that a serious project narrowed itself to reads only
(FRAG-NATIVE-13). That is evidence the write path is the expensive
half, and that syncing reads while keeping writes conventional captures
much of the benefit for a fraction of the risk. The local-first ideals
(FRAG-NATIVE-09) are a menu of seven, not a package, and the essay is
advocacy by the CRDT authors themselves.

## Release and update mechanics

Over-the-air updating draws a hard line at the native boundary:
JavaScript, styling, assets and copy can ship without review, native
code, native dependencies, permissions and SDK upgrades cannot
(FRAG-NATIVE-08). Apple rule 2.5.2 narrows it further, forbidding
downloaded code that introduces or changes features, while rule 4.7
permits whole classes of non-embedded software under conditions
(FRAG-NATIVE-03). Those two rules are in visible tension. The safe
reading, and what the pack should bind: OTA changes presentation and
content, never capability, and the same expand-migrate-contract
discipline used for schemas (EV-0206) applies to client and server
contracts because old binaries live for years.

## Binding, default, preference

**Binding.** A named conflict policy per write class before any sync
library is chosen. No offline acceptance of invariant-bearing writes
without a reservation or compensation path. A remote kill switch in
every shipping binary. A screen-level accessibility conformance target
stated against EN 301 549 clause 11 plus the WCAG mapping, with an
automated audit in the test suite and a written verdict on everything
the audit cannot decide. Forward-only release assumption: no runbook
step may say roll back.

**Default.** Shared logic with native user interface (B). Online-first
with a read cache until an offline write is a named requirement. Fixed
percentage first slice on Play, phased release on by default on Apple,
with the halt trigger defined in advance against a metric.

**Preference.** Framework family within an architecture, renderer
choice, the specific CRDT or sync vendor, and design language beyond
platform conformance.

## Open questions

- No retrievable serious comparison of client architectures on
  performance, energy or defect rate. State framework choice as a team
  and product judgement, not a measured one.
- No published coverage figure for native automated accessibility
  audits (FRAG-NATIVE-19). On the web the figure is contested at 57 per
  cent against roughly a third (EV-0236, EV-0104). We have nothing
  equivalent, so the manual verdict list carries more weight here.
- The primary Apple sources for both HIG (EV-0230) and the XCTest audit
  API (FRAG-NATIVE-19) resisted plain fetch. Re-verify before quoting.
- EN 301 549 v4 was in approval at cutoff. The version in force still
  references an older WCAG level than WCAG2Mobile maps to, so an app
  targeting WCAG 2.2 is ahead of the binding standard rather than
  behind it. Recheck on publication.
- Whether Apple's phased release cohort can be steered or halted on a
  metric is not documented; assume not.
