---
summary: Research synthesis for the data, analytics and experimentation pack, covering quality gates, modelling shape, experiment statistics, event design, storage fit and privacy, with the disagreements left visible
type: example
tags: [eos, testing]
---

# Research notes: data, analytics and experimentation

Cutoff 2026-08-03. New sources are `FRAG-DATA-ANALYTICS-01` to `-17`.
Existing ledger rows reused rather than duplicated: EV-0056 (Great
Expectations), EV-0057 (dbt model contracts), EV-0059 (GrowthBook
experiment decisions), EV-0139 (Confluent schema evolution), EV-0138
(CloudEvents envelope), EV-0041 and EV-0225 (UK data protection),
EV-0240 (dashboards answer one question).

## Pattern one: where the quality rule lives

Three genuinely different philosophies, and they fail differently.

**Contract-first.** The producer declares the interface and the build
refuses to publish anything that breaks it. ODCS puts schema, quality
rules, service level and owner in one document
(`FRAG-DATA-ANALYTICS-01`); dbt contracts freeze the public model's
columns and types while internals refactor freely (EV-0057). Fits when
a table has named consumers outside the team that wrote it. Fails
silently on meaning: the contract checks shape, so a column that
changes from pence to pounds passes every gate.

**Observability-first.** Compute metrics over the data each run and
alert on deviation from the historic series. Deequ does this with
incremental metric computation and anomaly detection over past values
(`FRAG-DATA-ANALYTICS-02`); Great Expectations makes the suite double
as the documentation (EV-0056). Fits when you do not yet know the
invariants, which is most new pipelines. Fails by learning the bug:
constraint suggestion encodes whatever the data currently does,
including the thing you would have called a defect.

**No gate, fast repair.** Land raw, fix in the transformation layer,
detect problems when a human queries. Honest fit: a single-consumer
pipeline where the consumer is the author and the cost of a wrong
number is a wasted afternoon. It stops fitting the moment a number
leaves the room.

The trap common to all three is the unowned gap. A schema contract with
no freshness rule and a freshness monitor with no owner produce the
same outage, which is why ODCS insists both live in one document with a
named team. That structural point is worth more than the format.

## Pattern two: the shape of the model

**Dimensional.** Declare the grain of the fact table first, then
dimensions, then facts; integrate through conformed dimensions; pick a
numbered slowly-changing-dimension policy rather than arguing about
history each time (`FRAG-DATA-ANALYTICS-04`). The grain-first discipline
and the conformed dimension are the durable parts.

**Wide business entities.** dbt's structure guide moves data from
source-conformed to business-conformed through staging, intermediate
and marts, ending in wide rich entities (`FRAG-DATA-ANALYTICS-03`). The
prefix tells you what a model may do, so review is mechanical. Storage
is cheap and columnar, so the old cost argument for narrow facts is
weak.

**Normalised source mirror.** Keep the warehouse close to the source
schema and push logic into the query. Cheapest to build, and it makes
every consumer re-derive the same business logic slightly differently.

The disagreement is real and neither side argues it. Kimball keeps
facts narrow and joins to dimensions; the dbt guide lands on wide
tables and does not mention star schemas at all. What survives both:
declare the grain, name the entity, and never let two models compute
the same business number by different routes.

## Pattern three: how an experiment is allowed to end

**Fixed horizon, locked in advance.** Power the test, set the sample
size, do not look until it lands. Kohavi, Deng and Vermeer show why
this is the default: monitoring a fixed-horizon test continuously can
push the false positive rate far above five per cent, and with roughly
eighty-five to ninety per cent of ideas failing to move the metric, the
prior is already against any given win (`FRAG-DATA-ANALYTICS-09`).

**Always valid, monitor freely.** Johari, Pekelis and Walsh treat
peeking as a property of the stopping rule and fix the statistic
instead of the operator, giving p-values valid at every moment
(`FRAG-DATA-ANALYTICS-08`). spotify/confidence ships group sequential
tests and multiple-comparison correction in an Apache-2.0 library, so
this is not a reason to buy a platform (`FRAG-DATA-ANALYTICS-13`).
GrowthBook's asymmetric gating is the operational form: goal metrics
decide the ship, guardrails only block on significant harm (EV-0059).

**Do not experiment.** Below the traffic where a properly powered test
is reachable, an underpowered A/B test is worse than an argued
decision, because it launders a coin flip as evidence. This is the
common case for a small venture and none of the sources say it plainly.

Two mechanics sit underneath whichever you pick. Sample ratio mismatch
invalidates a result outright and comes with a search order over
assignment, execution, logging, telemetry and interference
(`FRAG-DATA-ANALYTICS-12`). CUPED buys sensitivity with pre-experiment
covariates rather than traffic, around half the variance at Bing, but
only where a stable unit was observed before the test, so it does
nothing for first-session funnels (`FRAG-DATA-ANALYTICS-11`).

## Pattern four: event design

Registry-enforced schemas validate every event at collection and
quarantine failures, with SchemaVer separating breaking from additive
change (`FRAG-DATA-ANALYTICS-14`). Convention-only taxonomy generates
names from object-action pairs and pushes anything varying per
occurrence into properties (`FRAG-DATA-ANALYTICS-15`). The envelope and
compatibility-mode arguments from messaging apply unchanged here
(EV-0138, EV-0139): decide the upgrade order before the first change.
No source compares the two approaches, so the choice rests on whether
you own the collection path.

## Pattern five: where the data sits

The load-bearing contradiction in this pack. The lakehouse paper argues
the two-tier lake-plus-warehouse shape is broken by duplication and
staleness, and that one copy in an open format with a metadata layer
replaces it, with TPC-DS numbers to answer the performance objection
(`FRAG-DATA-ANALYTICS-05`). Tigani reports from BigQuery that most
customers held under a terabyte and around ninety per cent of queries
scanned under 100 MB (`FRAG-DATA-ANALYTICS-07`). Both cannot be the
default. They are not really arguing: one describes an estate that
already has a lake, the other describes everyone else. The decision
rule is the working set, not the storage total. Iceberg is the seam
that keeps the choice reversible, at the cost of catalogue, compaction
and snapshot maintenance that a managed warehouse absorbs for you
(`FRAG-DATA-ANALYTICS-06`).

Note the interested parties on both sides: the lakehouse paper is by
the lakehouse vendor, the small-data post is by a single-node warehouse
vendor. Neither is disqualified, both are discounted.

## Pattern six: privacy in analytics

Collect less is the cheapest control and the sources barely mention it.
Where aggregates must be published, differentially private counts,
sums, means and quantiles are available as Apache-2.0 libraries, and
the load-bearing caveat is that contribution limiting is the caller's
job and getting it wrong voids the guarantee silently
(`FRAG-DATA-ANALYTICS-17`). NIST SP 800-226 frames evaluation as
layered rather than a single epsilon and names the hazards that open
between proof and implementation (`FRAG-DATA-ANALYTICS-16`). UK duties
sit on top: a recorded lawful basis and a named complaints path
(EV-0225), with ceremony proportionate to risk (EV-0041).

## Binding, default, preference

Binding, because the failure is silent and the number leaves the room:
every published table or event has one named owner; sample ratio
mismatch is checked before any experiment result is read; the
randomisation unit, primary metric and stopping rule are written down
before traffic starts; no personal identifier lands in an analytics
table without a recorded lawful basis; a quality gate failure blocks
publication rather than raising a ticket.

Default, overridable with a recorded reason: object-action event names
with variable data in properties; staging, intermediate and marts
layering with grain declared per fact model; fixed-horizon tests unless
a sequential method is chosen deliberately; a single managed warehouse
until the working set argues otherwise; contract on public models only,
no ceremony on private ones.

Preference: the contract file format, the casing convention, the
quality tool, whether marts are wide or star-shaped.

## Open questions and thin evidence

- No source measures the cost of the power penalty for always-valid
  tests at small sample sizes, which is exactly where a venture lives.
- No comparison exists between registry-enforced event schemas and
  convention plus review; both are asserted, neither measured.
- The base rate of eighty-five to ninety per cent failed ideas comes
  from mature products at scale, and may not transfer to a young
  product where the obvious wins remain.
- What a proportionate quality gate looks like for a two-person venture
  is unaddressed by every source here; all of them assume a data team.
- Semantic drift, a column whose meaning changes while its type does
  not, has no gate in any source found. Treat it as unsolved.
