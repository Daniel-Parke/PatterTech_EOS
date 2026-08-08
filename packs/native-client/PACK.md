---
summary: Software that ships as a binary, four client architectures, the offline write question, forward-only release and the non-web accessibility profile
kind: rule
authority: binding
lifecycle: active
basis: standard
evidence_grade: observational
scope: estate
applies_when: [ships_a_binary, has_native_ui, has_local_write_store, distributes_via_app_store]
volatility: fast
review: on-change-of:EN-301-549-v4-publication
sources: [EV-0026, EV-0027, EV-0104, EV-0171, EV-0204, EV-0206, EV-0230, EV-0235, EV-0236]
type: playbook
tags: [eos, a11y, delivery, ops, state]
---

# native-client

This pack covers software that ships as a binary to a device: iOS and
Android apps, and desktop clients. It activates when work touches
client platform code, an offline store, a sync path or a store release.
It owns three hard-to-reverse choices: client architecture, what
happens to a write made with no network, and how a fix reaches a user.
It also owns the non-web accessibility profile that the ui-ux pack
defers to.

The through-line for everything below: on the web you own the ship
path, on a client you rent it.

## Activation

**Paths.** ios, android, app, mobile, client, desktop, shared and core
directories holding platform code; Swift, Kotlin, Dart, Objective-C and
platform-bridge sources; manifest, plist and entitlement files; Gradle,
Xcode and CocoaPods projects; fastlane, store metadata and release
lanes; local database schemas and sync configuration.

**Task types.** Choosing or changing a client architecture; adding a
local store or an offline write path; changing a sync protocol;
preparing a store submission; writing a release runbook; adding a
remote update channel; accessibility work on a non-web surface; raising
a target SDK level.

**Keywords, fallback only.** Mobile, app, iOS, Android, offline, sync,
CRDT, conflict, App Store, Play, TestFlight, staged rollout, phased
release, over-the-air, kill switch, VoiceOver, TalkBack.

**Applicability predicates**, which are the real gate.

| Predicate | True when |
| --- | --- |
| ships_a_binary | the product is installed on a device rather than fetched fresh each visit |
| has_native_ui | the surface ships as an iOS, Android or desktop app |
| has_local_write_store | the client can accept a write while the device is offline |
| has_invariant_bearing_writes | some write class carries a uniqueness, balance, permission or booking invariant |
| distributes_via_app_store | the ship path goes through Apple or Google review |
| has_remote_update_channel | anything changes client behaviour without a store round trip |

**The seam with ui-ux.** `packs/ui-ux/PACK.md` binds accessibility on
`has_web_ui`, then says a surface with no web UI activates its platform
profile instead. This pack is that profile. ui-ux keeps what an
interface must achieve for the person using it, the philosophy, tokens,
interaction states, and the numeric floors, which come from WCAG 2.2
(EV-0027) because the platform guidance publishes none
(EV-0387). This pack owns the conformance model: unit of
conformance, reviewable artefact, audit route, and the obligations WCAG
never states (EV-0370, EV-0371). Both packs load on a
native surface, and neither lowers a `kernel/POLICY_SPEC.md` or
`kernel/GUARD_SPEC.md` floor.

## Outcomes and non-goals

**Outcomes.** A write made in a tunnel has a documented fate before any
sync library is chosen. A bad build has a lever that is not another
submission. The app can be operated with the platform's assistive
technology, and the claim is backed by an artefact a reviewer can read.
The release calendar survives contact with review. A binary shipped two
years ago still talks to today's server.

**Non-goals.** No framework, language, CRDT or sync vendor is picked
here. Service boundaries and datastore choice sit in the architecture
pack, API versioning in api-integration, how a surface looks in ui-ux.
Games, embedded firmware and console distribution are out of scope:
the research covered none of them.

## Binding requirements

Each names its predicate, its evidence and the failure it prevents.
Where basis says decision, it binds because the estate ruled it, not
because evidence compels it. `EV-` ids resolve in
`registry/evidence.json`; `FRAG-NATIVE-` ids resolve for now in
`packs/native-client/research/sources.fragment.json`, pending the
ledger import recorded at the end of this file. Several sources are
readable and not reusable, so no source prose is copied here.

**B1. A conflict policy per write class, named before a sync library is
chosen.** `has_local_write_store`. Every class is classified as
commutative, last-writer-acceptable or invariant-bearing, and each gets
exactly one policy from `converge`, `last-writer-wins`,
`reserve-then-commit` or `reject-offline`, recorded in a decisions file
citing at least three evidence ids. Prevents the library choosing the
policy by default: convergence proofs say replicas agree and no update
is lost, and say nothing about whether the agreed value satisfies an
invariant (EV-0379), while the shipped server-authoritative
product states outright that there is no single correct choice for
handling a write failure (EV-0383). Basis: decision. See
`packs/native-client/guides/GD-NAT-002-offline-write-model.md`.

**B2. No offline acceptance of an invariant-bearing write without a
reservation or compensation path.** `has_invariant_bearing_writes` and
`has_local_write_store`. Either the client holds a server-issued
reservation before accepting the write, or the write is rejected
offline, or a named compensation event fires for the loser on
reconnection. Prevents two users holding one slot after a merge the
algorithm correctly calls converged (EV-0379). Basis: decision.

**B3. The outbox is durable, ordered and idempotent, and its blocked
state is named.** `has_local_write_store`. A write acknowledged to the
user survives process death, replays without duplicating, and the
blocked state is surfaced within a stated timeout while reads keep
working. Prevents the two failures of a FIFO upload queue: the write
lost to a crash between acknowledgement and flush, and head-of-line
blocking, where one unacknowledged mutation stalls the whole client and
nothing on screen says so (EV-0383). Basis: decision.

**B4. Release is forward-only.** `distributes_via_app_store`. Every
shipping binary carries a remote kill switch for the behaviour it
introduces, and no runbook step says roll back. Apple ramps automatic
updates on a fixed schedule with no developer dial and no rollback
(EV-0374); Play gives the dial and a halt, but halting only
stops further delivery and the documented remedy for a bad build is to
ship another one (EV-0375). Flags are the rollback on a client
(EV-0026). Prevents an incident plan whose first step is impossible.
Basis: standard. See `packs/native-client/guides/GD-NAT-003-release-path.md`.

**B5. A remote update channel changes presentation and content, never
capability.** `has_remote_update_channel`. Copy, styling, assets and
layout may ship out of band. Native code, native dependencies,
permissions, SDK levels and anything a reasonable person would call a
new feature may not. Prevents rejection or removal: the technical
boundary sits at native code (EV-0377) and the review rule sits
tighter still, at introducing or changing features (EV-0372).
Basis: standard, taking the narrower of two documented lines.

**B6. Non-web accessibility conformance is stated per screen, declared
in code, and gated by an automated audit with a written verdict on
every undecided item.** `has_native_ui`. The unit of conformance is a
screen, not a page (EV-0370), and the reviewable artefact is the
semantics declaration, not a screenshot (EV-0387). The audit
runs inside the platform test runner over every screen and fails the
build on any violation (EV-0388); the verdict file's entry count
equals the audit's undecided count. Where EN 301 549 applies, the
target is clause 11 plus its WCAG mapping (EV-0371, EV-0027),
which adds assistive-technology interoperability and user preference
support. Prevents web conformance language being waved at an app, and a
green audit being read as proof, which the web census warns against
directly (EV-0235). Basis: standard. See
`packs/native-client/guides/GD-NAT-004-a11y-profile.md`.

**B7. Client and server contracts change by expand, migrate,
contract.** `ships_a_binary`. The new shape ships alongside the old,
waits out the installed base, then the old is removed (EV-0206).
Prevents a server release breaking a binary its user cannot update
today and may never update. Version numbers mean nothing until that
surface is declared precisely (EV-0171). Basis: decision.

## Defaults

Followed unless the task records a reason to depart.

**D1. Shared logic with a native user interface.** Sharing domain logic
and sharing pixels are two decisions; the first is graded Stable per
target while the interface layer carries its own grade
(EV-0386). Reason: it removes business-rule divergence without
forfeiting platform behaviour.

**D2. Online-first with a read cache, until an offline write is a named
requirement.** Reason: no local writes means no conflicts and no policy
to maintain, and a serious sync project narrowed itself to the read
path and left writes to the application (EV-0382).

**D3. A one per cent first slice on Play with the halt trigger written
down before the release starts, and phased release left on for Apple.**
Reason: Play's only real containment lever is how small the first slice
is (EV-0375) and Apple's ramp is fixed, unsteerable and
bypassable by anyone updating manually (EV-0374), so the trigger
comes from your own telemetry on both.

**D4. Budget one rejection cycle into every release calendar.** Roughly
one submission in four was rejected in the 2025 reporting year, the
largest bucket by a wide margin being Performance (EV-0373).
That is a vendor census of its own decisions and sizes a calendar risk
only; the scope note sits in
`packs/native-client/refs/RELEASE_MECHANICS.md`.

**D5. The annual target SDK bump is fixed roadmap work.** From 31
August 2026 Play requires API 36 for new submissions and API 35 for an
existing app to stay visible to new users on current devices
(EV-0376). Reason: an unmaintained client goes quietly
invisible.

**D6. Plan against a low automated accessibility catch rate and put the
weight on the manual verdict list.** No coverage figure is published
for the native audits (EV-0388) and the web figure is contested
between roughly 57 per cent and roughly a third (EV-0236, EV-0104).

**D7. Storage and compaction are budgeted on day one wherever a
convergent store is used.** Text-suitable CRDTs only grow and the
answer is conditional tombstone collection (EV-0381). Reason:
compaction found at month six is a migration, not a tuning pass.

**D8. Start from the platform's own control with its own behaviour**,
and apply house style inside it (EV-0230). Reason: accessibility
services, system gestures and preference settings arrive with the
control and have to be rebuilt if you decline it.

## Preferences

Taste. Depart freely, no reason needed. Framework family inside a
chosen architecture; language for a shared core; the specific CRDT or
sync vendor once B1 has fixed the policy; document store or relational
store; release cadence beyond the store's constraints; whether a
companion watch or TV surface exists at all, noting only that those
targets carry lower stability grades (EV-0386).

## Decision map

| Fork | What it decides | Guide |
| --- | --- | --- |
| Which client architecture | Team shape, platform feel, accessibility cost, migration surface | `packs/native-client/guides/GD-NAT-001-client-architecture.md` |
| What happens to a write made offline | Conflict policy, storage growth, blocking behaviour | `packs/native-client/guides/GD-NAT-002-offline-write-model.md` |
| How a fix reaches a user | Containment lever, calendar risk, OTA envelope | `packs/native-client/guides/GD-NAT-003-release-path.md` |
| How much non-web accessibility assurance | What a passing build may claim, and against which instrument | `packs/native-client/guides/GD-NAT-004-a11y-profile.md` |

Detail sits in `packs/native-client/refs/`, a worked example in
`packs/native-client/exemplars/EX-NAT-001-offline-booking-client.md`,
and evaluation criteria in `packs/native-client/CHECKS.md`.

## Failure modes and anti-patterns

- **Choosing the sync library first.** The policy is then whatever the
  library does, found in production on the one write class that could
  not take it (EV-0379, EV-0383).
- **Reading "conflict-free" as "correct".** Convergence is a claim
  about replicas agreeing, not about the agreed value being wanted
  (EV-0379).
- **The rollback step in the runbook**, and its cousin, one runbook
  assuming both stores behave alike. Neither can take a version back
  and the two ramps are mirror images (EV-0374, EV-0375).
- **Treating Apple's phased release as a control plane.** Fixed
  percentages, no steering, no metric halt, manual updaters walking
  past it. Not progressive delivery in EV-0204's sense.
- **Shipping a feature over the air because it technically works.**
  The technical boundary and the review boundary are in different
  places (EV-0377, EV-0372). Its sibling is the wrapped
  website, rejected outright under rule 4.2: a web shell has to earn
  its binary.
- **A screenshot offered as the accessibility artefact**, or an empty
  verdict file beside a green audit. The semantics tree is what a
  screen reader reads (EV-0387), and no coverage figure exists
  for these audits at all (EV-0388).
- **The silently blocked client.** A stuck mutation stalls sync, the
  screen shows stale data with no message, and support hears "it is
  slow" for a week (EV-0383).
- **The client that stopped shipping**, which decays on a fixed annual
  clock (EV-0376).

## Open questions and counter-evidence

- **No serious comparison of client architectures exists.** Nothing
  retrievable on performance, energy or defect rate at this cutoff, so
  framework performance claims are unevidenced and GD-NAT-001 decides
  on team shape, platform feel and the documented properties.
- **Apple's rules 2.5.2 and 4.7 are in visible tension.** One forbids
  downloaded code that introduces or changes features, the other
  permits classes of non-embedded software under conditions
  (EV-0372). B5 takes the narrower reading; the wider one would
  be an argued departure.
- **The accessibility instruments disagree.** EN 301 549 v3.2.1 is in
  force, references an older WCAG level than the mobile mapping
  targets, and a v4 revision was in approval and unpublished at cutoff
  (EV-0371), so an app on WCAG 2.2 is ahead of the binding
  standard. The mapping is a Group Draft Note, informative,
  replaceable, Level A and AA only, closed functionality acknowledged
  as a gap (EV-0370): it translates and does not oblige.
- **The two conflict philosophies contradict each other by design.**
  Convergent replication has no head-of-line blocking and accepts a
  value nobody chose. Server-authoritative sync removes local conflicts
  and stalls globally on one bad mutation. Both ship, both are right
  about the other's weakness, and neither answers B1.
- **The local-first argument is advocacy**, seven ideals from a 2019
  position paper by CRDT authors evaluating CRDTs, no measurement, no
  user study (EV-0378). Library benchmarks are no better: the
  two main projects benchmark against each other and each claim is the
  vendor's own (EV-0380, EV-0381).
- **Two Apple primary sources resisted plain fetch** (EV-0230 and
  EV-0388), rest partly on secondary write-ups, and want
  re-verifying before anything is quoted.
- **The evidence import is incomplete.** The nineteen `FRAG-NATIVE-`
  rows are frozen in this pack's research directory and are not yet in
  `registry/evidence.json` with final `EV-` ids. The citations are
  stable text and the ids will change on import. Until then no
  `FRAG-NATIVE-` id resolves in the ledger, and CHECKS row C4 fails for
  those ids by design.
- **Refresh triggers.** Publication of EN 301 549 v4; a change to
  either store's staged release mechanics; the next annual Play target
  API deadline; a published coverage figure for a native audit; any
  retrievable independent comparison of architectures.
