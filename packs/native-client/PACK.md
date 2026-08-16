---
summary: Activation, outcomes and decision map for the native-client Doctrine and Wargames
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [ships_a_binary, has_native_ui, has_local_write_store, distributes_via_app_store]
activation_paths: [**/ios/**, **/android/**, **/*.swift, **/*.kt, **/*.xcodeproj/**, **/AndroidManifest.xml, **/electron/**, **/*.plist]
volatility: fast
review: none
sources: [EV-0026, EV-0027, EV-0104, EV-0171, EV-0204, EV-0206, EV-0230, EV-0235, EV-0236, EV-0370, EV-0371, EV-0372, EV-0373, EV-0374, EV-0375, EV-0376, EV-0377, EV-0378, EV-0379, EV-0380, EV-0381, EV-0382, EV-0383, EV-0386, EV-0387, EV-0388]
type: pack
tags: [eos, a11y, delivery, ops, state]
display_name: Native Clients
category: engineering
id_namespace: NAT
depends_on: [ui-ux, architecture]
---


# Native Clients

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

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B1"></a>
- `B1` to [DOC-NAT-001](doctrines/DOC-NAT-001-a-conflict-policy-per-write-class-named-before-a-sync.md) (default)
<a id="B2"></a>
- `B2` to [DOC-NAT-002](doctrines/DOC-NAT-002-no-offline-acceptance-of-an-invariant-bearing-write-without.md) (default)
<a id="B3"></a>
- `B3` to [DOC-NAT-003](doctrines/DOC-NAT-003-the-outbox-is-durable-ordered-and-idempotent-and-its-blocked.md) (default)
<a id="B4"></a>
- `B4` to [DOC-NAT-004](doctrines/DOC-NAT-004-release-is-forward-only.md) (binding)
<a id="B5"></a>
- `B5` to [DOC-NAT-005](doctrines/DOC-NAT-005-a-remote-update-channel-changes-presentation-and-content.md) (binding)
<a id="B6"></a>
- `B6` to [DOC-NAT-006](doctrines/DOC-NAT-006-non-web-accessibility-conformance-is-stated-per-screen.md) (binding)
<a id="B7"></a>
- `B7` to [DOC-NAT-007](doctrines/DOC-NAT-007-client-and-server-contracts-change-by-expand-migrate.md) (default)
<a id="D1"></a>
- `D1` to [DOC-NAT-008](doctrines/DOC-NAT-008-shared-logic-with-a-native-user-interface.md) (default)
<a id="D2"></a>
- `D2` to [DOC-NAT-009](doctrines/DOC-NAT-009-online-first-with-a-read-cache-until-an-offline-write-is-a.md) (default)
<a id="D3"></a>
- `D3` to [DOC-NAT-010](doctrines/DOC-NAT-010-a-one-per-cent-first-slice-on-play-with-the-halt-trigger.md) (default)
<a id="D4"></a>
- `D4` to [DOC-NAT-011](doctrines/DOC-NAT-011-budget-one-rejection-cycle-into-every-release-calendar.md) (default)
<a id="D5"></a>
- `D5` to [DOC-NAT-012](doctrines/DOC-NAT-012-the-annual-target-sdk-bump-is-fixed-roadmap-work.md) (default)
<a id="D6"></a>
- `D6` to [DOC-NAT-013](doctrines/DOC-NAT-013-plan-against-a-low-automated-accessibility-catch-rate-and.md) (default)
<a id="D7"></a>
- `D7` to [DOC-NAT-014](doctrines/DOC-NAT-014-storage-and-compaction-are-budgeted-on-day-one-wherever-a.md) (default)
<a id="D8"></a>
- `D8` to [DOC-NAT-015](doctrines/DOC-NAT-015-start-from-the-platforms-own-control-with-its-own-behaviour.md) (default)
- source `preferences:001` to [DOC-NAT-016](doctrines/DOC-NAT-016-framework-family-within-the-selected-client-architecture-is.md) (preference), [DOC-NAT-017](doctrines/DOC-NAT-017-language-for-a-shared-client-core-is-a-venture-preference.md) (preference), [DOC-NAT-018](doctrines/DOC-NAT-018-the-crdt-or-synchronisation-vendor-is-a-preference-after-the.md) (preference), [DOC-NAT-019](doctrines/DOC-NAT-019-document-versus-relational-local-storage-is-a-venture.md) (preference), [DOC-NAT-020](doctrines/DOC-NAT-020-release-cadence-beyond-store-constraints-is-a-venture.md) (preference), [DOC-NAT-021](doctrines/DOC-NAT-021-whether-to-ship-a-companion-watch-or-television-surface-is-a.md) (preference)

## Decision map

| Fork | What it decides | Wargame |
| --- | --- | --- |
| Which client architecture | Team shape, platform feel, accessibility cost, migration surface | `packs/native-client/wargames/WG-NAT-001-client-architecture.md` |
| What happens to a write made offline | Conflict policy, storage growth, blocking behaviour | `packs/native-client/wargames/WG-NAT-002-offline-write-model.md` |
| How a fix reaches a user | Containment lever, calendar risk, OTA envelope | `packs/native-client/wargames/WG-NAT-003-release-path.md` |
| How much non-web accessibility assurance | What a passing build may claim, and against which instrument | `packs/native-client/wargames/WG-NAT-004-a11y-profile.md` |

Detail sits in `packs/native-client/references/`: the write classes, the
store release mechanics, and the non-web accessibility profile. A
worked example is in
`packs/native-client/examples/EX-NAT-001-offline-booking-client.md`,
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
  framework performance claims are unevidenced and WG-NAT-001 decides
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
- **The evidence import is done.** The nineteen fragment rows are in
  `registry/evidence.json` as EV-0370 to EV-0388, and every citation in
  this pack uses the ledger id. The fragment file stays in the research
  directory as the frozen batch the import was made from, and the
  synthesis behind the pack is in
  `packs/native-client/research/NOTES.md`.
- **Refresh triggers.** Publication of EN 301 549 v4; a change to
  either store's staged release mechanics; the next annual Play target
  API deadline; a published coverage figure for a native audit; any
  retrievable independent comparison of architectures.
