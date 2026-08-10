---
summary: Research synthesis for the devops-reliability pack, covering migrations, restore proof, SLO governance, incident practice, FinOps, golden paths, progressive delivery and observability stability.
type: example
tags: [eos]
---

# DevOps and reliability: what the evidence actually supports

Research cutoff 2026-08-03. Fifteen new sources in
`sources.fragment.json`, plus existing ledger records EV-0020 (OpenSLO),
EV-0026 (OpenFeature), EV-0038 (SLSA), EV-0043 (OTel GenAI status),
EV-0057 (dbt contracts), EV-0058 (Backstage templates), EV-0059
(GrowthBook decisions), EV-0071 (OPA) and EV-0096 (SRE Workbook error
budget policy).

## Three materially different philosophies

**1. Reversibility by design.** Every change carries an inverse: down
migrations, undo scripts, blue-green with an instant flip. Fits systems
with rare deploys, hard change windows, or a regulator who wants a
written back-out plan. The trade-off is that the inverse is written but
never run, so it rots. Flyway's own maintainers say the quiet part out
loud (FRAG-11): undo scripts cannot reverse destructive data change and
cannot recover a script that failed on statement seven of ten. Anti-
pattern: a `down()` function that has never been executed against
production-shaped data being treated as a safety net.

**2. Forward-only with compatibility windows.** Never reverse; always
roll forward, and make each deploy safe by keeping the schema compatible
with every application version still running. The mechanism is
expand-migrate-contract (FRAG-10): add the new shape, move the callers
and rows, delete the old shape, three separately deployable steps.
Fits anything deploying more than weekly. Trade-off is dual maintenance
and the named failure mode of skipping contract, leaving permanent
duplication. Anti-pattern: calling yourself forward-only while shipping
expand and contract in the same release, which is just a breaking change
with extra words.

**3. Data-layer isolation.** Treat the migration as a long-running,
pausable operation decoupled from the deploy: gh-ost (FRAG-12) reads the
binary log, can be trialled against a replica, throttled, paused for
real and cut over at a chosen moment. Fits large tables where an
in-place change would lock. Trade-off is real operational complexity for
a specific database topology. Anti-pattern: reaching for it on a table
of ten thousand rows.

Static checks sit under all three. Atlas (FRAG-06) shows the useful
taxonomy: destructive, backwards-incompatible, data-dependent and
non-linear history are four different risks needing four different
verdicts, and only the first two are reliably decidable before running.

## Restore proof, not backup configuration

AWS REL09-BP04 (FRAG-05) is the cleanest statement available and its
value is the anti-pattern list, which reads like a confession: assuming
a backup exists, assuming it is uncorrupted, assuming restore fits the
recovery time objective, restoring without querying the data back out.
The binding practice is a scheduled restore into a fresh location with
per-source validation criteria, elapsed time measured against RTO and
data loss measured against RPO, alerting when either is missed.
Chaos engineering (FRAG-07) supplies the epistemics: state a
steady-state hypothesis before you break anything, or the drill produces
a story rather than evidence. Its prefer-production principle does not
transfer to a small venture with one tenant carrying all the risk; the
defensible reading is a bounded restore drill with a stated hypothesis.

## SLO governance and the metric fights

EV-0020 gives a machine-readable target object and EV-0096 gives the
governance dial: budget remaining means ship with low ceremony, budget
spent means changes halt except P0 and security. EV-0096 is CC BY-NC-ND,
so paraphrase only, never verbatim, and the pack should say so inline.

Two disagreements are load-bearing.

*DORA versus VOID.* DORA (FRAG-03) keeps failed deployment recovery time
as one of five keys and pairs throughput with instability so neither can
be gamed alone. The VOID work (FRAG-15) argues incident duration is
positively skewed and low fidelity, that a mean over it is arithmetic
the data does not support, and that duration showed no correlation with
severity across the corpus. Both can be right: a per-deploy recovery
signal is a delivery-system property, while cross-incident MTTR
aggregates are a claim about resilience the data will not carry. The
pack should record recovery time per event and forbid the fleet-wide
mean as a target.

*DORA versus SPACE.* SPACE (FRAG-14) says no single metric or dimension
captures productivity and asks for at least three dimensions including
perceptual data. A solo or two-person venture cannot run surveys, which
means the honest position is that DORA-style delivery numbers describe
the delivery system and must never be presented as a measure of a
person.

## Platform, flags and observability

Golden paths (EV-0058, FRAG-09) work when the scaffolder stamps out a
compliant skeleton and registers ownership at creation time. The CNCF
maturity model's own caveat is the useful part: the output is the
improvement list, not the level, and voluntary adoption is the quality
signal, because people routing around the path means the path is wrong.
EV-0058 records the counterweight, that golden paths rot without
gardening.

Progressive delivery has two halves. OpenFeature (EV-0026) decouples
deploy from release; Argo Rollouts (FRAG-08) makes promotion a machine
decision against a declared query with a failure limit and an automatic
abort back to the last stable version. Both leave the same hole: flag
lifecycle. Piranha (FRAG-13) closes it by making removal mechanical,
which only works if a flag declares an expiry and terminal value at
creation. EV-0059 supplies the decision discipline for experiment flags.

Observability stability is a per-signal contract (FRAG-02): only stable
signals earn long-term dependencies, deprecated ones keep stable-grade
guarantees until removal, and everything below stable needs pinning plus
schema mapping. EV-0043 shows the bite: GenAI agent conventions were
still Development at v1.42.0.

FinOps (FRAG-01, CC BY 4.0, reusable with attribution) contributes one
precondition worth more than the rest of the framework: allocation.
Until every unit of spend has an owner, optimisation and chargeback are
theatre.

## Binding, default, preference

Binding requirements. Forward-only migration discipline with
expand-migrate-contract for anything backwards-incompatible; destructive
and backwards-incompatible migrations blocked in CI unless explicitly
acknowledged in the change record; a dated restore drill with measured
elapsed time and a validation query, with the drill result recorded, not
just the backup job status; every service carries at least one SLI and
SLO expressed as a machine-readable object; every incident above the
agreed threshold gets an owned postmortem with a deadline, an
evidence-backed timeline and filed follow-ups (FRAG-04, Apache-2.0 so
reusable verbatim, unlike EV-0096); every feature flag declares an owner
and an expiry date at creation; long-term dependencies only on stable
observability signals, anything below stable pinned.

Defaults. Progressive rollout with an automated abort condition for
user-facing changes; error-budget policy in the EV-0096 shape; cost
allocation tags on every deployed resource; golden-path scaffold for new
services.

Preferences. Chaos or failure drills beyond restore; unit-economics
reporting; a platform maturity self-assessment; automated flag removal
tooling.

Two explicit non-requirements, both argued above: no fleet-wide MTTR
target, and no presentation of delivery metrics as individual
productivity.
