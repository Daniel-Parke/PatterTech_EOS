---
summary: EOS v2 architecture, adaptive agentic development, accepted with eight binding clarifications
type: decision
tags: [eos]
status: accepted
supersedes: ADR-0001
decided_by: Daniel Parke
date: 2026-08-02
---

# ADR-0002: EOS v2, adaptive agentic development

Daniel approved the consolidated v2 plan for implementation on 2026-08-02,
subject to the binding clarifications recorded below. This record is the
authorisation for every protected-set change the build makes. ADR-0001 remains
the founding record of v1; this decision supersedes it as the operative
architecture. Release of v2 is a separate later approval and is not granted
here.

## Context

v1 imported the Venture A machinery unchanged: universal role separation,
session logs and Resume Packets at every close, WIP of one, blanket test-first,
wargame-first for every doctrine change, and a metadata-only checker. Audit of
all twenty v1 sessions measured 20.1 percent of every line written as ceremony,
a 475 to 900 line boot read, and three sessions that were pure paperwork. The
discipline collapsed as soon as work left session ceremony: four of six
post-tag commits are unrecorded, unlogged, one an unwargamed doctrine edit.
The repo passes its own checker while holding at least six false statements
about itself. Knowledge coverage is one deep house web aesthetic and four thin
modules. The full evidence base, friction audit and research ledger live in
the plan of record and are seeded into registry/evidence.json.

## Decision

Adopt EOS v2 as specified in the approved consolidated plan:

1. **Execution modes replace universal role separation.** Express, Standard,
   Exploration, High-assurance and Parallel, chosen per task. Roles become
   situational charters: EXECUTOR, ORACLE, REVIEWER. The one preserved
   separation is oracle authorship: whoever writes a change's gate tests must
   not hold its implementation in context.
2. **Two-layer risk control.** A deterministic semantic router assigns the
   minimum workflow tier (R0 to R3) from declared capabilities and derived
   signals, with machine-readable reasons and an audited, expiring exception
   path. An action-time guard evaluates every consequential tool action with
   four verdicts (allow, require-approval, manual-only, deny), non-waivable
   safety floors, and fail-closed behaviour: without a validated host
   enforcement adapter, every guarded action class is manual-only.
3. **Decision budget replaces "never invent".** Free, durable-record and
   escalation bands. Bounded reversible local decisions are permitted and
   recorded.
4. **Coordinator-assigned concurrency.** Claims are committed to the
   integration branch before worker dispatch; unscheduled concurrent sessions
   are refused; liveness is established from harness state or recorded PID,
   and a timestamp alone never authorises taking a claim. Quarantined
   unscheduled work is never deleted without operator authority.
5. **State as records and derived views.** Per-task JSON records and
   append-only ledgers are canonical; every aggregate view and index is
   derived and regenerated only by the integrator. Universal session logs and
   Resume Packets are retired; git is the log.
6. **Adaptive testing.** Timing by change class; affected tests through a
   queryable test map with confidence fallback; docs carry no behavioural
   tests by default but keep link, snippet, schema and generated-doc checks;
   coverage percentage is never a universal gate. A test-timing ablation sets
   capability-profile defaults from evidence before either test-first or
   end-stage testing is mandated anywhere.
7. **Knowledge as packs.** Twenty substantive packs in two waves under a
   strict definition of done, a domain coverage matrix that makes omissions
   visible, a capability registry for unbuilt domains, progressive disclosure
   on the three-level model, orthogonal metadata axes with per-kind minima,
   and a design pluralism contract. PatterTech house style is a preference
   pack activated only by venture adoption. Hardware stays registry-only this
   build because no venture currently demands it; the reason is recorded in
   the coverage matrix.
8. **Governance.** Graded change path (experimental edit, evidence RFC, ADR);
   precedence that scopes venture rulings locally and protects law and
   standards based rules from vote counts; a smaller protected set;
   promotion requiring argued rulings or a source with basis standard or
   evidence grade controlled.
9. **Tooling.** A tested Python package (python -m tools.eos) with structural,
   semantic, seed and freshness checks, the router, the guard, context packet
   generation, task and claim management, migration and benchmark commands.
   One canonical dependency declaration with hash-locked generated
   requirements.
10. **Benchmark before release.** Frozen kernel comparison (v1 against v2),
    policy ablations, the test-timing ablation, and one frozen acceptance
    drill per built pack, under the release gates of the plan. The sealed
    final suite is encrypted; Daniel retains the private key.
11. **Migration and consolidation.** Deterministic migration path for pinned
    ventures with read-only plans this build; all work on one integration
    branch, feat/eos-v2-agentic-development; main untouched until the release
    approval; no force-push; every v1 commit reachable through the
    archive/v1-final tag.

## Binding clarifications (Daniel, 2026-08-02)

1. This plan does not approve itself. Its proposed decisions became accepted
   through Daniel's explicit approval and are recorded here before any
   protected-set edit.
2. The test-timing ablation uses an independent diagnostic holdout, never the
   sealed suite. The sealed suite serves only the one final frozen-v1 against
   final-v2 evaluation window. Inconclusive timing cells retain the
   conservative existing default.
3. Pack lanes never edit canonical shared registries. Each lane writes
   validated evidence and coverage fragments under its claimed pack path; the
   integrator alone deduplicates and imports them into registry/evidence.json
   and registry/coverage.json, regenerates views and resolves shared source
   ids.
4. Express converts to Standard before circuit-breaker hypothesis logging is
   required, so every hypothesis ledger has a task record and successful
   Express work never creates one.
5. Sealed-suite custody: a separate evaluator-author session creates the
   suite; public-key encryption, or demonstrably isolated ACL storage; no
   implementation or coordinator session receives plaintext or the private
   key; Daniel retains the private key and provides it only to the final
   evaluator after implementation and diagnostic correction are complete.
6. Python support is tested on 3.11 and 3.14, or the support claim is
   narrowed to what was tested. The pip-tools version used to generate
   hash-locked requirements is pinned and documented.
7. Phase-level implementation and research budgets exist separately from the
   65M-token benchmark cap. Crossing a soft phase budget triggers a progress
   and scope review, never silent expansion. The budgets adopted at
   acceptance: P0 3M tokens, P1 2M, P2 6M, P3 5M, P4 12M, P5 3M, P6 12M, P7
   2M orchestration beside the benchmark cap, P8 2M; content volume soft cap
   of roughly 800 lines per pack across its organs; elapsed-time review at
   double the phase estimate.
8. Standard cold-start context is one total budget of 550 lines. The v1
   release item REL is completed only in its push portion by the tag push;
   its remaining bookkeeping lands with the stale-fact fixes. Licensing rules
   are applied per source, never as blanket class rules. Test-generation
   reliability claims are scoped to their exact benchmarks. Quarantined
   unscheduled work is never deleted without operator authority.

## Scheduling hold

The 2026-07-07 hold on WG-DEL-005 is lifted for the EOS v2 build only.
WG-DEL-005 may be argued and authored in Wave A before any dependent delivery
doctrine is written. This does not authorise writes to Venture A.

## Protected set changes authorised

The v2 protected set: GOVERNANCE.md; prompt-injection resistance; secret
protection; production safety; data protection; approval for consequential
external actions; org/decisions/ append-only with one sanctioned amendment,
the superseded_by stamp; the constitution Parts II and III; the role charters;
the policy risk and approvals blocks with POLICY_SPEC. Leaving the protected
set: the module shape invariants, the wargame format, the ID schemes and the
front-matter schema, which now change through the RFC path. Retired v1 rules:
universal separation of duties, universal work orders, WIP limits of one and
two, blanket test-first, universal session logs and Resume Packets, and
wargame-first for every change, each replaced as the plan specifies.

## Approved and reserved actions

Approved with this decision: the P0 branch mechanics (executed 2026-08-02:
feat/estate-manifest tip and tags v1.0.0 and archive/v1-final pushed,
feat/eos-v2-agentic-development created and pushed, containment verified,
feat/estate-manifest deleted locally and remotely); the twenty-pack two-wave
scope; the 65M-token benchmark cap; the sealed evaluation design requiring
Daniel's key participation; the root and estate changes including GUIDE.md
archived, START.md retired, VISION.md merged into README.md, and
estate/repos.yaml converted to repos.json with membership per Daniel's estate
rulings; and the voice law re-scoped to EOS-internal law, venture default and
brand preference.

Reserved for the separate release checkpoint: fast-forwarding main, creating
v2.0.0, pushing the release, amending benchmark thresholds, replacing a failed
sealed suite, and any write to a sibling venture repository.

## Deviation mechanism

org/deviations.md is the append-only implementation-deviation log. A material
departure from the approved plan requires an amendment to this ADR before
proceeding; minor deviations are logged with reasons and surfaced at the
release checkpoint.
