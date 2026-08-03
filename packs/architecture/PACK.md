---
summary: Architecture pack for boundaries declared and machine-checked, decisions recorded as ADRs, and one deployable with one database until measured evidence says otherwise
kind: rule
authority: binding
lifecycle: active
basis: decision
evidence_grade: observational
scope: estate
applies_when: [has_server_code, has_multiple_modules, has_database, has_cross_language_contract, has_vendor_holding_identity_or_money]
volatility: slow
review: 2027-02
sources: [EV-0010, EV-0023, EV-0024, EV-0025, EV-0057, EV-0097, EV-0098, EV-0099, EV-0100, EV-0101, EV-0102, EV-0146, EV-0147, EV-0148, EV-0149, EV-0150, EV-0151, EV-0152, EV-0153, EV-0154, EV-0155, EV-0156, EV-0157, EV-0158, EV-0159, EV-0160, EV-0161, EV-0162, EV-0163]
type: guide
tags: [arch, data, infra, tooling, ci]
review_by: 2027-02
---

# Architecture

This pack covers structure inside a venture's own code: where module
boundaries live and how they are enforced, which decisions get written
down, what proves a build, where data rests, and how deep a vendor is
allowed to reach. It activates on server-side code with more than one
module, on any database, on a contract that crosses a language
boundary, and on any vendor holding identity or money. Interface
design, test strategy and hosting live in other packs.

## Activation

Triggers, in the order the router should read them.

**Paths.** Import or dependency contract files (`.importlinter`,
`.dependency-cruiser.json`, an ArchUnit test source), migration
directories, `docs/decisions/`, any C4 or arc42 artefact, any
directory named for a module or service, webhook handlers, and files
declaring a public API schema.

**Task types.** Adding or moving a module, declaring or changing a
boundary, choosing a datastore, splitting or merging a deployable,
adding a background job substrate, integrating a vendor, recording a
decision that closes a door, proving a restructure changed nothing.

**Keywords, fallback only.** boundary, layering, module, monolith,
microservice, ADR, decision record, C4, arc42, coupling, adapter,
port, outbox, topology, schema drift, webhook signature.

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

**Routing.** Activation is not authorisation. Architecture work
usually touches CI configuration, schema and public contract surfaces,
so `kernel/POLICY_SPEC.md` will floor most of it at R2, and vendor and
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
infrastructure, rule on test strategy or deployment platform, or
design your domain model for you. It does not claim a shape is right;
it claims a declared shape must be enforced and a closed door must be
recorded.

## Binding requirements

Five. Each names the failure it prevents and the evidence it stands
on. Everything else in this pack is a default or a preference and can
be argued with in a paragraph.

**B1. A declared boundary is machine-checked in CI from the first
week.** The contract lives in a committed file and a crossing fails
the build. Evidence: import-linter (EV-0147), dependency-cruiser
(EV-0148) and ArchUnit (EV-0146) all show the same thing, that the
contract file makes the intended architecture reviewable rather than
folklore. Prevents: quiet, one-way boundary erosion. MacCormack et al.
(EV-0154) is the mechanism, since structure mirrors the communication
structure that built it, and for a one-person or agent-run codebase
the untreated prediction is a single tightly coupled artefact.

**B2. A decision that closes a door is recorded as a MADR record with
two or more considered options.** Options, why each lost, consequences
accepted. Immutable once accepted; reversal is a superseding record.
Evidence: MADR (EV-0097) for the format, which scales from three lines
to three pages so ceremony stays opt-in. Prevents: silent reversal and
re-litigation. Basis is an estate decision, not measured benefit, and
MADR itself notes there is no measured evidence that decision records
improve outcomes.

**B3. Builds are reproducible from pinned inputs, and verified by
rebuilding.** Tools are versioned dependencies rather than host
installations, inputs are identified by content, and where a timestamp
is embedded the SOURCE_DATE_EPOCH rules apply exactly as written.
Evidence: SOURCE_DATE_EPOCH (EV-0155), Bazel hermeticity (EV-0156).
Prevents: a change that cannot be proved harmless because the output
was never stable to begin with. Note the limit both sources state:
clamping timestamps does not buy reproducibility on its own.

**B4. Generated contract artefacts are committed with a drift gate.**
Schemas, types and clients are generated offline and deterministically,
committed, and a CI check fails when the committed copy lags its
source. A typed client checks the response succeeded or it is not a
client. Evidence: OpenAPI (EV-0023), AsyncAPI (EV-0024), JSON Schema
(EV-0025), dbt model contracts (EV-0057). Prevents: the silent
failure, where a renamed field makes a mutation fail and the caller
reports success.

**B5. A vendor webhook is verified over the raw request bytes, with a
bounded recency window, before anything parses it.** No framework body
parsing ahead of verification, non-zero replay tolerance, idempotency
keys on the handler, and the payload version pinned. Evidence: Stripe
webhook documentation (EV-0161), paraphrased. Prevents: a forged or
replayed event accepted as truth, and the specific defect where
middleware re-serialises the body and destroys the signature. What
transfers is the rule, never the constants; each vendor's tolerance
and header format differ.

## Defaults

Chosen unless a recorded decision argues otherwise. Departing is
normal; departing without writing down why is the finding.

**D1. One deployable, one database, modules enforced in the build.**
Reason: the module decomposition and the process decomposition are
separate decisions, and forcing them to be one buys the wrong boundary
at the highest price (EV-0152, EV-0153). Shopify (EV-0159) is the
existence proof that a very large codebase can hold boundaries inside
one process.

**D2. Split only on a measured signal, never on a label.** The signals
are DORA's: changes needing approval outside the owner, inability to
test in isolation, and unplanned work caused by upstream change
(EV-0151). DORA is explicit that the label does not determine the
outcome.

**D3. Boundary tool matched to the stack.** import-linter for Python,
dependency-cruiser for TypeScript, ArchUnit for the JVM. Reason: each
runs in the build the venture already has. See
`packs/architecture/refs/boundary-tooling.md` for what each one cannot
see.

**D4. C4 container and component views authored in Structurizr DSL.**
Reason: one text model generates many views that cannot drift from
each other (EV-0101, EV-0102). Borrow arc42 headings (EV-0149) only
for the non-diagram content actually needed, and reach for ISO 42010
vocabulary (EV-0158) only when a stakeholder demands that rigour.

**D5. Derived values are computed, not stored.** The two sanctioned
exceptions are a cache with a named invalidation owner and an
immutable snapshot carrying its input digest. Reason: a stored
derivation drifts from its source silently, and a cache without an
owner is a slow bug. Argued at
`archive/v1/doctrine/architecture/wargames/WG-ARCH-003-derived-state.md`.

**D6. Background jobs run on a durable database claim queue.** Reason:
one store, exactly the database's guarantees, and jobs survive a
deploy. Argued at
`archive/v1/doctrine/architecture/wargames/WG-ARCH-004-job-execution.md`. Where a
state change must also produce a message, use an outbox in the same
transaction and make every consumer idempotent (EV-0157).

**D7. Identity, money and handover-bound vendors sit behind an adapter
the venture owns, with a written exit route.** The venture's own
database stays the authorisation truth. Reason: the exit cost grows
with every import site.

**D8. One database until a second real owner or a volume-asymmetric
feed appears, and records never mingle with readings.** Reason:
ownership and physical separation are different decisions, and private
tables with distinct credentials enforce ownership without paying for
sagas and cross-database joins (EV-0162).

**D9. Every persisted table names its consumer and its retention plan
before it lands.** Reason: local observation across three ventures
that unowned tables become unbounded ones. Grade: anecdotal, and it is
a default for exactly that reason.

**D10. Proof of harmless change is a byte-stable output canary where
output is deterministic.** Otherwise pin behaviour with
characterisation tests over the touched surface before changing it.
Argued at
`archive/v1/doctrine/architecture/wargames/WG-ARCH-006-change-proof.md`.

## Preferences

Taste. Argue freely, no record needed.

- Run a Bounded Context Canvas and a Context Mapping pass before
  declaring a boundary (EV-0098, EV-0099, EV-0100).
- Create a port only where a second driver or a second device is
  genuinely plausible. Cockburn's 2005 statement (EV-0150) never
  bounded this, and an adapter per dependency is ceremony.
- Name the specific event pattern in use rather than saying
  event-driven. The four have different costs (EV-0163).
- Raw SQL behind a repository layer, over an ORM, when the data is
  hot. Argued at
  `archive/v1/doctrine/architecture/wargames/WG-ARCH-002-orm-or-raw-sql.md`.
- Defer domain grouping and per-domain gateways until service count
  makes them a real problem. Uber reached for them at roughly 2,200
  services (EV-0160).

## Decision map

| Fork | Question | Argued at | Default |
| --- | --- | --- | --- |
| Deployment shape | One deployable, several, or contract-shaped seams inside one? | `packs/architecture/guides/GD-ARCH-001-deployment-shape.md` | One deployable, modules enforced |
| Boundary enforcement | Convention, machine contract, or the tree itself? | `packs/architecture/guides/WG-ARCH-001-boundary-enforcement.md` | Machine contract, rising to tree |
| Vendor depth | SDK throughout, owned adapter, or raw protocol? | `packs/architecture/guides/WG-ARCH-007-vendor-seams.md` | Owned adapter, raw protocol at webhooks |
| Data topology | One database, one per service, or records plus readings? | `packs/architecture/guides/WG-ARCH-008-database-topology.md` | One, until a second real owner |
| Derived state | Computed, cached, or snapshotted? | `archive/v1/doctrine/architecture/wargames/WG-ARCH-003-derived-state.md` | Computed |
| Job substrate | In-process, database queue, or broker? | `archive/v1/doctrine/architecture/wargames/WG-ARCH-004-job-execution.md` | Database claim queue |
| Contract seam | Hand-maintained, generated and gated, or one language? | `archive/v1/doctrine/architecture/wargames/WG-ARCH-005-contract-seam.md` | Generated, committed, gated |
| Change proof | Green suite, pinned behaviour, or byte-stable output? | `archive/v1/doctrine/architecture/wargames/WG-ARCH-006-change-proof.md` | Output canary where deterministic |
| ORM or SQL | ORM, raw SQL behind repositories, or a builder? | `archive/v1/doctrine/architecture/wargames/WG-ARCH-002-orm-or-raw-sql.md` | Raw SQL behind repositories |

The four forks still pointing at `archive/v1/doctrine/architecture/wargames/`
carry their v1 argument unchanged and have not been re-graded against
the 2026 evidence sweep. Treat their defaults as current and their
grading as pending.

## What changed from v1

The v1 module stated seven binding rules. Re-graded rule by rule
against the evidence now in the ledger:

| v1 rule | v2 grade | Why |
| --- | --- | --- |
| 1. Boundaries are records | binding, as B1 | Three maintained tools plus a mechanism source |
| 2. Door-closing decisions are ADRs | binding, as B2 | Estate decision; format evidence only, no outcome evidence |
| 3. Nothing generative in a build | split | Reproducibility binds as B3 on standards; the output canary is D10 |
| 4. Generated artefacts drift-gated | binding, as B4 | Four maintained specification sources |
| 5. One writer per fact | default, as D5 | Local observation only, no external evidence |
| 6. Vendors are guests | split | Raw-byte webhook verification binds as B5; adapter depth is D7 |
| 7. Data topology is ruled | default, as D8 and D9 | Case reports at hyperscale, none at venture scale |

Two of seven survive intact as binding, two survive in narrowed form,
and three become defaults. That is the honest reading of the evidence,
not a softening of the discipline: a default still has to be argued
away in writing.

## Failure modes and anti-patterns

- **The documented boundary.** A layering described in prose with no
  failing check. The rule does not exist. This is the drill's first
  named failure condition.
- **The contract nobody runs.** A committed contract file that no CI
  workflow or pre-commit hook invokes.
- **The single-option decision record.** A template filled in after
  the fact with one option. It teaches the shape and hides the
  argument.
- **The networked monolith.** Services that look independent and must
  be released together (EV-0160).
- **The premature split.** Separate deployables before the boundary
  has proved stable under change (EV-0153).
- **The adapter per dependency.** Ports where no second device is
  plausible (EV-0150).
- **The parsed webhook.** Framework middleware reading the body before
  the signature is checked (EV-0161).
- **The typed client that ignores failure.** A generated client that
  never checks the response succeeded.
- **The tolerated violation.** Isolation scores that count crossings
  instead of blocking them. That is a migration tactic for legacy mass
  (EV-0159), not a greenfield rule.
- **The unowned table.** A persisted table with no named consumer and
  no retention plan.

## Open questions and counter-evidence

Named honestly, because the research found real disagreement.

**Splitting: helps, hurts, or irrelevant?** Fowler (EV-0153) says
monolith first and says so tentatively, on stated anecdote. Service
Weaver (EV-0152) reports up to 15x latency and 9x cost improvement
from co-locating the same modules, but it is a workshop position paper
using the authors' own prototype and Go example workloads, with no
independent replication. DORA (EV-0151) refuses the framing outright.
The pack takes DORA's resolvable form and measures signals rather than
counting processes. It could be wrong.

**Is a shared database an anti-pattern?** EV-0162 names it one and
then offers private tables with distinct credentials in one database
as a legitimate isolation level. The disagreement is vocabulary:
uncontrolled access is the defect, physical colocation is not.

**Static or runtime boundary checks?** Every static tool in the ledger
states the same blind spot: reflection, dependency injection,
service locators and string-keyed dynamic loading (EV-0146, EV-0147,
EV-0148). Shopify's answer was call graphs from CI runs (EV-0159), and
that tool is not public. The honest position is that static checking
is the cheap default and dynamic wiring is the known gap. B1 binds the
cheap default; it does not claim completeness.

**How much architecture description?** ISO 42010 (EV-0158) gives the
rigorous vocabulary and was read only as a public abstract, since the
standard is paywalled. arc42 (EV-0149) gives twelve sections and its
own authors ship a lighter canvas, which is evidence that
section-complete templates invite box-filling. C4 (EV-0101) is a
single-author practice framework with no controlled comprehension
study. There is no strong evidence for any particular volume of
description.

**Population warning, carried across the whole pack.** Almost none of
this evidence observed a one-person, agent-assisted venture. DORA
surveys team and enterprise organisations. The mirroring study
observes firms and open source communities. Shopify and Uber are
hyperscale case reports with no counterfactual. Service Weaver is a
prototype benchmark. Read every rule here as a rule for
machine-enforced boundaries in a small codebase, not as inherited
enterprise practice. EV-0010 is the standing reminder that intuitions
about agent-era productivity have already been measured wrong once,
with the sign inverted.

**Thin spots we are not pretending about.** D9 rests on local
observation across three ventures. B2 binds on an estate decision, not
on measured benefit. No source in the ledger measures whether
machine-checked boundaries improve outcomes in a codebase this small;
B1 stands on the mechanism and on three ventures' experience of what
happens without it.

## Where the rest lives

- Decision guides: `packs/architecture/guides/`
- Reference material: `packs/architecture/refs/`
- Worked example: `packs/architecture/exemplars/`
- Evaluation criteria: `packs/architecture/CHECKS.md`
