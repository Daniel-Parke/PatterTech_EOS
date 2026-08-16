---
summary: Activation, outcomes and decision map for the architecture Doctrine and Wargames
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [has_server_code, has_multiple_modules, has_database, has_cross_language_contract, has_vendor_holding_identity_or_money]
activation_paths: [**/.importlinter, **/.dependency-cruiser*, **/adr/**, **/decisions/**, **/migrations/**, **/*arc42*, **/*c4*, **/services/**, **/modules/**]
volatility: slow
review: none
sources: [EV-0010, EV-0023, EV-0024, EV-0025, EV-0057, EV-0097, EV-0098, EV-0099, EV-0100, EV-0101, EV-0102, EV-0146, EV-0147, EV-0148, EV-0149, EV-0150, EV-0151, EV-0152, EV-0153, EV-0154, EV-0155, EV-0156, EV-0157, EV-0158, EV-0159, EV-0160, EV-0161, EV-0162, EV-0163]
type: pack
tags: [arch, data, infra, tooling, ci]
display_name: Software Architecture
category: engineering
id_namespace: ARCH
depends_on: [business-logic-modelling]
---


# Software Architecture

This pack covers structure inside a venture's own code: where module
boundaries live and how they are enforced, which decisions get written
down, what proves a build, where data rests, and how deep a vendor is
allowed to reach. It activates on server-side code with more than one
module, on any database, on a contract that crosses a language boundary,
and on any vendor holding identity or money. Interface design, test
strategy and hosting live in other packs.

## Activation

Triggers, in the order the router should read them.

**Paths.** Import or dependency contract files (`.importlinter`,
`.dependency-cruiser.json`, an ArchUnit test source), migration
directories, `docs/decisions/`, any C4 or arc42 artefact, any directory
named for a module or service, webhook handlers, and files declaring a
public API schema.

**Task types.** Adding or moving a module, declaring or changing a
boundary, choosing a datastore, splitting or merging a deployable,
adding a background job substrate, integrating a vendor, recording a
decision that closes a door, proving a restructure changed nothing.

**Keywords, fallback only.** boundary, layering, module, monolith,
microservice, ADR, decision record, C4, arc42, coupling, adapter, port,
outbox, topology, schema drift, webhook signature.

**Applicability predicates.** The pack claims exactly these:

| Predicate | True when |
| --- | --- |
| `has_server_code` | the venture runs code it deploys, not only static output |
| `has_multiple_modules` | two or more units of code with distinct owners or lifecycles |
| `has_database` | any persistent store the venture writes |
| `has_cross_language_contract` | a request or response shape crosses a language boundary |
| `has_vendor_holding_identity_or_money` | a third party holds identity, payment or contractual data |

None true means the pack does not load. `has_server_code` alone loads
the decision-record and reproducible-build requirements and nothing
else.

**Routing.** Activation is not authorisation. Architecture work usually
touches CI configuration, schema and public contract surfaces, so
`kernel/POLICY_SPEC.md` will floor most of it at R2, and vendor and
webhook work meets the guarded classes in `kernel/GUARD_SPEC.md`.
Declare the facts honestly and let the router rule.

## Outcomes and non-goals

Outcomes this pack is trying to buy:

- A boundary an agent cannot cross without a red build.
- A decision an agent arriving cold in six months can reconstruct,
  including the options that lost.
- A change that can be proved harmless rather than asserted harmless.
- An exit from every vendor holding something that matters.
- The option to split later, kept cheap by keeping the module graph
  honest now.

Non-goals. This pack does not choose your framework, size your
infrastructure, rule on test strategy or deployment platform, or design
your domain model for you. It does not claim a shape is right; it claims
a declared shape must be enforced and a closed door must be recorded.

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B1"></a>
- `B1` to [DOC-ARCH-001](doctrines/DOC-ARCH-001-a-declared-boundary-is-machine-checked-in-ci-from-the-first.md) (binding)
<a id="B4"></a>
- `B4` to [DOC-ARCH-002](doctrines/DOC-ARCH-002-generated-contract-artefacts-are-produced-deterministically.md) (binding), [DOC-ARCH-003](doctrines/DOC-ARCH-003-a-typed-client-verifies-that-a-response-succeeded-before.md) (binding)
<a id="B5"></a>
- `B5` to [DOC-API-002](../api-integration/doctrines/DOC-API-002-webhook-receivers-authenticate-the-exact-raw-request-before.md) (binding)
<a id="D1"></a>
- `D1` to [DOC-ARCH-004](doctrines/DOC-ARCH-004-one-deployable-one-database-modules-enforced-in-the-build.md) (default)
<a id="D2"></a>
- `D2` to [DOC-ARCH-005](doctrines/DOC-ARCH-005-split-only-on-a-measured-signal-never-on-a-label.md) (default)
<a id="D3"></a>
- `D3` to [DOC-ARCH-006](doctrines/DOC-ARCH-006-boundary-tool-matched-to-the-stack.md) (default)
<a id="D4"></a>
- `D4` to [DOC-ARCH-007](doctrines/DOC-ARCH-007-c4-container-and-component-views-authored-in-structurizr.md) (default)
<a id="D5"></a>
- `D5` to [DOC-ARCH-008](doctrines/DOC-ARCH-008-derived-values-are-computed-not-stored.md) (default)
<a id="D6"></a>
- `D6` to [DOC-ARCH-009](doctrines/DOC-ARCH-009-background-jobs-run-on-a-durable-database-claim-queue.md) (default)
<a id="D7"></a>
- `D7` to [DOC-ARCH-010](doctrines/DOC-ARCH-010-identity-money-and-handover-bound-vendors-sit-behind-an.md) (default)
<a id="D8"></a>
- `D8` to [DOC-ARCH-011](doctrines/DOC-ARCH-011-one-database-until-a-second-real-owner-or-a-volume.md) (default)
<a id="D9"></a>
- `D9` to [DOC-ARCH-012](doctrines/DOC-ARCH-012-every-persisted-table-names-its-consumer-and-its-retention.md) (default)
<a id="D10"></a>
- `D10` to [DOC-ARCH-013](doctrines/DOC-ARCH-013-proof-of-harmless-change-is-a-byte-stable-output-canary.md) (default)
<a id="D11"></a>
- `D11` to [DOC-ARCH-014](doctrines/DOC-ARCH-014-a-decision-that-closes-a-door-is-recorded-as-a-madr-record.md) (default)
<a id="D12"></a>
- `D12` to [DOC-ARCH-015](doctrines/DOC-ARCH-015-builds-are-reproducible-from-pinned-inputs-and-verified-by.md) (default)
- source `preferences:001` to [DOC-ARCH-016](doctrines/DOC-ARCH-016-run-a-bounded-context-canvas-and-a-context-mapping-pass.md) (preference)
- source `preferences:002` to [DOC-ARCH-017](doctrines/DOC-ARCH-017-create-a-port-only-where-a-second-driver-or-a-second-device.md) (preference)
- source `preferences:003` to [DOC-ARCH-018](doctrines/DOC-ARCH-018-name-the-specific-event-pattern-in-use-rather-than-saying.md) (preference)
- source `preferences:004` to [DOC-ARCH-019](doctrines/DOC-ARCH-019-raw-sql-behind-a-repository-layer-over-an-orm-when-the-data.md) (preference)
- source `preferences:005` to [DOC-ARCH-020](doctrines/DOC-ARCH-020-defer-domain-grouping-and-per-domain-gateways-until-service.md) (preference)

### Later evidence-led admissions

These records were admitted after the frozen source migration.
Their own metadata is canonical; this map does not restate it.

- [WG-ARCH-009](wargames/WG-ARCH-009-messaging-and-flow.md) (Wargame)
- [WG-ARCH-010](wargames/WG-ARCH-010-storage-engine-selection.md) (Wargame)
- [WG-ARCH-011](wargames/WG-ARCH-011-locality-and-consistency.md) (Wargame)
- [WG-ARCH-012](wargames/WG-ARCH-012-capability-ownership.md) (Wargame)

## Decision map

| Fork | Question | Argued at | Default |
| --- | --- | --- | --- |
| Deployment shape | One deployable, several, or contract-shaped seams inside one? | `packs/architecture/wargames/WG-ARCH-013-deployment-shape.md` | One deployable, modules enforced |
| Boundary enforcement | Convention, machine contract, or the tree itself? | `packs/architecture/wargames/WG-ARCH-001-boundary-enforcement.md` | Machine contract, rising to tree |
| Vendor depth | SDK throughout, owned adapter, or raw protocol? | `packs/architecture/wargames/WG-ARCH-007-vendor-seams.md` | Owned adapter, raw protocol at webhooks |
| Data topology | One database, one per service, or records plus readings? | `packs/architecture/wargames/WG-ARCH-008-database-topology.md` | One, until a second real owner |
| Derived state | Computed, cached, or snapshotted? | `packs/architecture/wargames/WG-ARCH-003-derived-state.md` | Computed |
| Job substrate | In-process, database queue, or broker? | `packs/architecture/wargames/WG-ARCH-004-job-execution.md` | Database claim queue |
| Contract seam | Hand-maintained, generated and gated, or one language? | `packs/architecture/wargames/WG-ARCH-005-contract-seam.md` | Generated, committed, gated |
| Change proof | Green suite, pinned behaviour, or byte-stable output? | `packs/architecture/wargames/WG-ARCH-006-change-proof.md` | Output canary where deterministic |
| ORM or SQL | ORM, raw SQL behind repositories, or a builder? | `packs/architecture/wargames/WG-ARCH-002-orm-or-raw-sql.md` | Raw SQL behind repositories |

Every fork in this map is argued inside the pack. The five that used to
delegate into the archived v1 module (derived state, job substrate,
contract seam, change proof, ORM or SQL) were re-graded against the 2026
evidence sweep and written as Wargames here, so a reader following this
table no longer lands on a file stamped `status: archived`. Their v1
originals are at `archive/v1-final:doctrine/architecture/wargames/` for
provenance, and are not guidance.

## What changed from v1

The v1 module stated seven binding rules. Re-graded rule by rule against
the evidence now in the ledger, and re-graded again by the ADR-0008
authority audit:

| v1 rule | Grade now | Why |
| --- | --- | --- |
| 1. Boundaries are records | binding, as B1 | Three maintained tools plus a peer-reviewed mechanism source |
| 2. Door-closing decisions are ADRs | default, as D11 | Estate decision; format evidence only, and its own source disclaims outcome evidence |
| 3. Nothing generative in a build | split, both defaults | Reproducibility is D12; the output canary is D10 |
| 4. Generated artefacts drift-gated | binding, as B4 | Four maintained specification sources, and the failure is a silent wrong success |
| 5. One writer per fact | default, as D5 | Local observation only, no external evidence |
| 6. Vendors are guests | split | Raw-byte webhook verification binds as B5; adapter depth is D7 |
| 7. Data topology is ruled | default, as D8 and D9 | Case reports at hyperscale, none at venture scale |

One of seven survives intact as binding, two survive in narrowed binding
form, and four are defaults. That is the honest reading of the evidence,
not a softening of the discipline: a default still has to be argued away
in writing, and the two that moved in the audit moved because the pack
could not name a serious or irreversible failure behind them, not
because anyone stopped wanting them done.

## Failure modes and anti-patterns

- **The documented boundary.** A layering described in prose with no
  failing check. The rule does not exist. This is the drill's first
  named failure condition.
- **The contract nobody runs.** A committed contract file that no CI
  workflow or pre-commit hook invokes.
- **The single-option decision record.** A template filled in after the
  fact with one option. It teaches the shape and hides the argument.
- **The networked monolith.** Services that look independent and must be
  released together (EV-0160).
- **The premature split.** Separate deployables before the boundary has
  proved stable under change (EV-0153).
- **The adapter per dependency.** Ports where no second device is
  plausible (EV-0150).
- **The parsed webhook.** Framework middleware reading the body before
  the signature is checked (EV-0161).
- **The typed client that ignores failure.** A generated client that
  never checks the response succeeded.
- **The tolerated violation.** Isolation scores that count crossings
  instead of blocking them. That is a migration tactic for legacy mass
  (EV-0159), not a greenfield rule.
- **The unowned table.** A persisted table with no named consumer and no
  retention plan.

## Open questions and counter-evidence

Named honestly, because the research found real disagreement.

**Splitting: helps, hurts, or irrelevant?** Fowler (EV-0153) says
monolith first and says so tentatively, on stated anecdote. Service
Weaver (EV-0152) reports up to 15x latency and 9x cost improvement from
co-locating the same modules, but it is a workshop position paper using
the authors' own prototype and Go example workloads, with no independent
replication. DORA (EV-0151) refuses the framing outright. The pack takes
DORA's resolvable form and measures signals rather than counting
processes. It could be wrong.

**Is a shared database an anti-pattern?** EV-0162 names it one and then
offers private tables with distinct credentials in one database as a
legitimate isolation level. The disagreement is vocabulary: uncontrolled
access is the defect, physical colocation is not.

**Static or runtime boundary checks?** Every static tool in the ledger
states the same blind spot: reflection, dependency injection, service
locators and string-keyed dynamic loading (EV-0146, EV-0147, EV-0148).
Shopify's answer was call graphs from CI runs (EV-0159), and that tool
is not public. The honest position is that static checking is the cheap
default and dynamic wiring is the known gap. B1 binds the cheap default;
it does not claim completeness.

**How much architecture description?** ISO 42010 (EV-0158) gives the
rigorous vocabulary and was read only as a public abstract, since the
standard is paywalled. arc42 (EV-0149) gives twelve sections and its own
authors ship a lighter canvas, which is evidence that section-complete
templates invite box-filling. C4 (EV-0101) is a single-author practice
framework with no controlled comprehension study. There is no strong
evidence for any particular volume of description.

**Population warning, carried across the whole pack.** Almost none of
this evidence observed a one-person, agent-assisted venture. DORA
surveys team and enterprise organisations. The mirroring study observes
firms and open source communities. Shopify and Uber are hyperscale case
reports with no counterfactual. Service Weaver is a prototype benchmark.
Read every rule here as a rule for machine-enforced boundaries in a
small codebase, not as inherited enterprise practice. EV-0010 is the
standing reminder that intuitions about agent-era productivity have
already been measured wrong once, with the sign inverted.

**Thin spots we are not pretending about.** D9 rests on local
observation across three ventures. D11 rests on an estate decision, not
on measured benefit, which is why the authority audit moved it out of
the binding set. No source in the ledger measures whether
machine-checked boundaries improve outcomes in a codebase this small; B1
stands on the mechanism in EV-0154 and on three ventures' experience of
what happens without it, and it is the binding rule in this pack most
likely to move next.

## Where the rest lives

- Wargames: `packs/architecture/wargames/`
- Reference material: what each boundary tool cannot see,
  `packs/architecture/references/boundary-tooling.md`; how much description a
  system earns and in what form,
  `packs/architecture/references/architecture-description.md`
- Worked example: a boundary declared, enforced and then crossed,
  `packs/architecture/examples/EX-ARCH-001-billing-catalogue-boundary.md`
- Evaluation criteria: `packs/architecture/CHECKS.md`
- Evidence pointer: `packs/architecture/references/evidence-map.md`, which
  maps every claim above to its ledger row, its population limit and its
  licence constraint. The eighteen rows from this pack's own sweep were
  imported into `registry/evidence.json` as EV-0146 to EV-0163; the rest
  are estate rows this pack borrows. The frozen batch they came from
  stays at `packs/architecture/research/sources.fragment.json`, the
  synthesis behind this file is
  `packs/architecture/research/NOTES.md`, and the licence and quotation
  sweep is at `packs/architecture/research/provenance.fragment.json`.
