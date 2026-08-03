---
summary: Binding devops and reliability practice, migrations, restore proof, SLOs and error budgets, rollout, flags, incidents and cost
type: guide
tags: [ops, data, infra]
kind: rule
authority: binding
lifecycle: active
basis: standard
evidence_grade: observational
scope: estate
applies_when: [deploys_to_environment, stores_persistent_data, runs_schema_migrations]
volatility: slow
review: 2027-05
review_by: 2027-05
sources: [EV-0020, EV-0026, EV-0043, EV-0058, EV-0059, EV-0071, EV-0096, EV-0197, EV-0198, EV-0199, EV-0200, EV-0201, EV-0202, EV-0203, EV-0204, EV-0205, EV-0206, EV-0207, EV-0208, EV-0209, EV-0210, EV-0211]
---

# DevOps and reliability

This pack governs how a venture changes and operates a running system:
schema migrations, restore proof, service level objectives and error
budgets, progressive rollout, feature flags, incident practice and
infrastructure cost. It activates when a task touches migrations,
deployment or infrastructure configuration, when production data is
written or deleted, or when a reliability target or its budget is at
stake. Production safety is protected-set material, so the binding
requirements here are not negotiable inside a task.

## Activation

Load this pack when any of the following is true. Path and keyword
triggers are cheap and noisy; the applicability predicates are what
actually decide, and a task that trips a path trigger but fails every
predicate loads nothing beyond this paragraph.

**Path triggers.** Migration directories (`migrations/`, `db/migrate/`,
Alembic, Flyway or Atlas layouts), CI and pipeline configuration,
infrastructure-as-code, container and orchestration manifests, rollout
and traffic-shaping objects, SLO and alerting definitions, feature flag
configuration, backup and restore scripting, cost and budget
configuration.

**Task types.** Schema change, deploy or release, rollback or recovery,
incident response and postmortem, capacity or cost work, observability
instrumentation, platform or scaffold work.

**Keyword fallback.** migration, rollback, restore, backup, RTO, RPO,
SLO, SLI, error budget, canary, blue-green, feature flag, postmortem,
incident, on-call, deployment, cost ceiling. Keywords are the weakest
signal and never on their own justify the binding requirements below.

**Applicability predicates.**

| Predicate | True when |
| --- | --- |
| `deploys_to_environment` | The venture ships to any environment users or other systems reach. |
| `stores_persistent_data` | Data survives a process restart and matters if lost. |
| `runs_schema_migrations` | A schema is changed by versioned migration files. |
| `has_reliability_target` | A stated SLO or an equivalent promise exists. |
| `spends_on_infrastructure` | A recurring bill is attached to running the thing. |

Requirements 1 to 3 need `runs_schema_migrations` or
`stores_persistent_data`. Requirement 4 needs `has_reliability_target`
or `deploys_to_environment`. Requirement 7 needs
`deploys_to_environment`. Nothing here activates for a library with no
runtime of its own.

**Policy routing.** The predicates above map onto the semantic factors
in `kernel/POLICY_SPEC.md`: `runs_schema_migrations` instantiates the
schema-change factor (floor R2) and, where the diff drops a column or a
table, the destructive-migration factor (floor R3). Restore drills and
production reads instantiate production-data handling. This pack does
not set tiers; the router does. What the pack adds is the evidence a
task at that tier must produce.

**Guard contact.** `kernel/GUARD_SPEC.md` classes deployment,
production-data, deletion and irreversible are all reachable from this
domain. Production data deletion is manual-only and no requirement,
default or preference here can soften that. A contract migration that
drops a column carrying live data is a deletion, not a schema tidy.

## Outcomes and non-goals

**Outcomes.** A change to schema, code or infrastructure can be shipped
without a change window and without a written back-out plan nobody has
run. Data loss has a measured, dated recovery path rather than an
assumed one. Reliability is a number both the operator and the agent can
read. When something breaks, the release rate responds automatically
rather than by argument. Spend has an owner before it has an optimiser.

**Non-goals.** This pack does not choose a hosting platform or a
database (that is architecture and the stack profiles). It does not
define the test suite (delivery-testing owns that) nor the threat model
(security-privacy). It does not measure people: see the two explicit
non-requirements below.

**Two explicit non-requirements**, argued rather than assumed:

- **No fleet-wide mean time to recovery target.** Incident duration is
  positively skewed and low fidelity, and across the VOID corpus
  duration showed no correlation with severity, so a mean over it is
  arithmetic the data will not carry (EV-0211). Record recovery time per
  event; never set the aggregate as a target.
- **No presentation of delivery metrics as individual productivity.**
  DORA describes the delivery system, not a person, and SPACE argues no
  single metric or dimension captures productivity at all (EV-0199,
  EV-0210). A one or two person venture cannot run the perceptual half
  of SPACE, which makes the temptation to use the telemetry half as a
  personal score stronger and worse.

## Binding requirements

Seven. Each names the failure it prevents and cites the evidence that
earns it. Departure needs an accepted ADR, not a task-level judgement.

1. **Backwards-incompatible schema change ships as expand, migrate,
   contract, in separate deploys.** Add the new shape, move every caller
   and row, delete the old shape only once nothing reads it. No deploy
   may break the application version still running beside it (EV-0206,
   EV-0207). *Prevents*: an application rollback that needs a database
   change to go with it, at the exact moment nobody can think straight.

2. **Recovery is forward-only and the change record says so.** No down
   or undo scripts. The maintainer of the most used migration tool says
   plainly that undo cannot reverse destructive data change and cannot
   recover a script that failed on statement seven of ten (EV-0207).
   Corrections are new migrations. *Prevents*: a down function that has
   never executed against production-shaped data being treated as a
   safety net.

3. **CI runs a migration linter that fails the build on destructive and
   backwards-incompatible findings, and the change record names the risk
   class of every migration in the change.** The four classes are
   destructive, backwards-incompatible, data-dependent and non-linear
   history; only the first two are reliably decidable before running, so
   those two fail and the rest warn (EV-0202). *Prevents*: an
   irreversible DDL reaching production because the diff looked small.

4. **Every service carries at least one SLI and SLO as a
   machine-readable object.** OpenSLO gives a vendor-neutral declarative
   shape for SLI, SLO, error budget and alert policy, so the target is
   checkable rather than prose in a wiki (EV-0020). *Prevents*:
   reliability arguments with no shared referent, where whoever speaks
   last wins.

5. **A restore drill runs on cadence and produces a dated evidence
   record with a measured elapsed time, a validation query and a
   result.** Backup job status is not evidence. Define validation
   criteria per data source, restore into a fresh location, measure
   elapsed against RTO and loss against RPO, alert when either is missed
   (EV-0201), and state the steady-state hypothesis before the drill so
   the run can falsify something (EV-0203). *Prevents*: the four named
   assumptions, that a backup exists, that it is uncorrupted, that
   restore fits the RTO, and that a restored snapshot holds the data
   without anybody querying it back out.

6. **Every incident above the agreed threshold gets an owned postmortem
   with a deadline, a timeline reconstructed from evidence, and
   follow-ups filed as tickets.** The incident commander names the
   owner; the owner files the actions and does not then chase them
   (EV-0200, which is Apache-2.0 and so reusable directly). *Prevents*:
   the same outage twice, and a timeline reconstructed from memory that
   flatters everyone in it.

7. **Every feature flag declares an owner and an expiry date at
   creation, and long-term dependencies are taken only on stable
   observability signals.** Flag removal is only mechanisable if a flag
   declares an expiry and terminal value up front (EV-0209); the flag
   API standard itself does not address lifecycle (EV-0026). Signal
   stability is a per-signal contract, and anything below stable is
   pinned and schema-mapped (EV-0198). *Prevents*: permanent dead
   branches nobody owns, and dashboards and alerts silently emptying on
   a minor version bump.

## Defaults

Sensible starting positions. Override any of them with a reason
recorded in the change record or the lock-book; an unrecorded override
is the finding, not the override itself.

- **Progressive rollout with an automated abort condition for
  user-facing change.** Promotion is a machine decision against a
  declared query with a failure limit, and breaching it shifts traffic
  back to the last stable version without a human in the loop (EV-0204).
  *Reason to depart*: no traffic router or metrics backend exists yet,
  in which case say so and use a flag with a manual kill.
- **An error budget policy in the shape the SRE Workbook describes,
  paraphrased.** Budget remaining means ship with low ceremony; budget
  spent means changes halt except P0 and security until back inside the
  SLO (EV-0096). That source is CC BY-NC-ND, so this pack paraphrases it
  and never quotes it. *Reason to depart*: pre-production, or a venture
  where the operator is also the only user.
- **Cost allocation tags on every deployed resource.** Allocation is the
  precondition that makes optimisation and chargeback mean anything;
  without an owner per unit of spend the rest is theatre (EV-0197,
  CC BY 4.0, attribution to the FinOps Foundation). *Reason to depart*:
  a single-resource estate where allocation is trivially the whole bill.
- **A golden-path scaffold for new services, registering ownership at
  creation.** The scaffolder stamps a compliant skeleton and records the
  owner as a side effect of creating the thing (EV-0058). Voluntary
  uptake is the quality signal: people routing around the path means the
  path is wrong (EV-0205). *Reason to depart*: fewer than three services,
  where the scaffold costs more than it saves.
- **Migrations applied before application start, idempotent,
  advisory-locked, failing closed.** A failed migration fails the
  deploy. Nobody edits an applied migration. This carries forward from
  the v1 devops doctrine and is unchanged by the new evidence.
- **Policy checks expressed as code where the inputs are already
  machine-readable.** A decision engine queried with structured input
  beats a prose checklist, but only where structured input exists
  (EV-0071).

## Preferences

Taste. Freely overridable, no reason required, no authority claimed.

- Failure drills beyond restore, once restore itself is boring.
- Unit-economics reporting, cost per active user or per job.
- A periodic platform self-assessment across investment, adoption,
  interfaces, operations and measurement, treating the improvement list
  as the output and the level as noise (EV-0205).
- Automated flag removal that rewrites the syntax tree when a flag
  reaches its terminal state (EV-0209). A scheduled report of flags past
  their expiry gets most of the value in a small codebase.
- Experiment flags governed by asymmetric gating, where goal metrics
  drive the ship decision and guardrails block only on significant harm
  (EV-0059).

## Decision map

The material forks in this domain, each argued in a guide.

| Fork | Guide |
| --- | --- |
| How a backwards-incompatible schema change is made safe | `packs/devops-reliability/guides/GD-DEVOPS-001-schema-change-strategy.md` |
| How a change reaches users once it is deployed | `packs/devops-reliability/guides/GD-DEVOPS-002-release-control.md` |
| What governs the release rate when reliability slips | `packs/devops-reliability/guides/GD-DEVOPS-003-error-budget-dial.md` |
| Which reliability and delivery numbers are kept | `packs/devops-reliability/guides/GD-DEVOPS-004-reliability-measures.md` |
| What proves the backups work | `packs/devops-reliability/guides/WG-OPS-003-restore-proof.md` |

Reference material the body defers to sits in
`packs/devops-reliability/refs/`, and a full worked application is in
`packs/devops-reliability/exemplars/EX-DEVOPS-001-email-to-contacts.md`.
The pack's own evaluation criteria are in
`packs/devops-reliability/CHECKS.md`.

## Failure modes and anti-patterns

- **Forward-only in name.** Shipping expand and contract in one release
  and calling it forward-only. That is a breaking change with extra
  words (EV-0206).
- **The contract phase that never happens.** Expand and migrate land,
  contract is deferred forever, and the schema carries permanent
  duplication. This is the named cost of the pattern, not a surprise.
- **The unexercised inverse.** A down migration, an undo script or a
  documented back-out plan that has never run against production-shaped
  data, trusted because it exists (EV-0207).
- **Backup status as evidence.** A green backup job read as proof of
  recoverability (EV-0201).
- **The drill with no hypothesis.** A restore or failure exercise run
  without stating the expected steady state first, producing a story
  instead of a result (EV-0203).
- **Online schema change as a reflex.** Reaching for binary-log-based
  migration tooling on a table of ten thousand rows, buying real
  operational complexity for nothing (EV-0208).
- **Canary abort mistaken for rollback.** Automatic abort shifts traffic
  back; it does not unwrite the rows the canary already wrote (EV-0204).
  Data written under a canary needs its own compatibility story.
- **Lint configured to warn.** Migration analyzers default to warnings,
  so a project that installs the linter and never sets failures has
  bought a log line (EV-0202).
- **The unowned flag.** A flag with no owner and no expiry, which is a
  permanent untested code path pretending to be a switch (EV-0209).
- **Pre-stable signals load-bearing.** Building alerts on attributes
  below stable status, then blaming the upgrade (EV-0198, EV-0043).
- **Golden path left to rot.** A scaffold that encodes last year's
  practice and is mandated anyway, so people work around it and the
  adoption signal is destroyed (EV-0058, EV-0205).
- **Cost optimisation before allocation.** Cutting a bill nobody owns,
  which moves the number and changes no behaviour (EV-0197).

## Open questions and counter-evidence

Named honestly, because the research found real disagreement and thin
support in places.

- **Recovery time: DORA against VOID.** DORA keeps failed deployment
  recovery time as one of five keys and pairs throughput with
  instability so neither can be gamed alone (EV-0199). The VOID work
  argues incident duration is gray data and that a mean over it is
  unsound (EV-0211). The reconciliation this pack adopts, that a
  per-deploy recovery signal is a property of the delivery system while
  a cross-incident aggregate is a claim about resilience the data will
  not support, is a reading, not a settled result.
- **Delivery metrics against SPACE.** SPACE asks for at least three
  dimensions including perceptual data (EV-0210). A small venture cannot
  supply the perceptual half. The honest position is that we run the
  telemetry half knowing it is incomplete, and refuse the personal
  reading. Nobody has shown this is safe, only that the alternative is
  worse.
- **Flyway is arguing about its own paid feature.** EV-0207 is a vendor
  making a case against a feature it sells at a higher tier, and tools
  that ship down migrations as a first-class primitive disagree with it
  outright. The argument about statement seven of ten stands on its own
  logic, but the source is not disinterested.
- **Chaos engineering has no measurement of benefit.** EV-0203 has been
  unchanged since 2019, carries no licence notice, and its
  prefer-production principle is wrong for a venture where one tenant
  carries all the risk. Only the steady-state hypothesis is taken from
  it here.
- **FinOps and platform maturity are consensus, not evidence.** No
  controlled study links FinOps adoption to lower spend (EV-0197), and
  the CNCF maturity model carries no outcome data (EV-0205). Only
  allocation and the improvement list are treated as load-bearing.
- **Static migration analysis cannot see the data.** Data-dependent
  findings such as a unique constraint that fails only if duplicates
  exist stay probabilistic, and part of the analyzer set sits behind a
  paid tier (EV-0202). The binding requirement is therefore scoped to
  the two decidable classes.
- **Much of what an agentic estate wants to emit is below stable.**
  OpenTelemetry GenAI agent conventions were still in Development at
  v1.42.0 (EV-0043), so requirement 7 will keep biting until they
  stabilise. Pinning and schema mapping is a workaround, not a fix.
- **Argo Rollouts is Kubernetes-shaped.** The declared-query promotion
  pattern is right; the implementation does not transfer as-is to a
  single-instance or serverless deployment (EV-0204), and this pack has
  no equally good citation for those topologies.
- **Postmortems are described, not validated.** EV-0200 is process
  documentation, not evidence that postmortems reduce recurrence, and
  learning-from-incidents research argues action-item counts are a poor
  proxy for learning. The deadline and the evidence-backed timeline are
  kept because they are cheap; the action-item count is not a metric.
