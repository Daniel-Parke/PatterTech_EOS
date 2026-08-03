---
summary: What do we measure about support, and what may the number be used for?
kind: guide
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
sources: [EV-0210, EV-0211]
review: 2028-08
type: guide
tags: [ops, product, testing]
review_by: 2028-08
---

# GD-SUPPORT-004: What do we measure about support, and what may the number be used for?

## The question

Support generates numbers faster than it generates insight. The fork is
not which dashboard: it is what claim each number is allowed to carry.
Three of the four candidates below have a published failure attached,
and the fourth has no evidence at all. Choosing without reading the
failure is how a venture ends up steering on a statistic that describes
nothing.

## It depends on

- **Who reads it and what they will do on Monday.** A number nobody can
  act on within a week is not a support metric.
- **The shape of the distribution.** Durations are positively skewed,
  which rules out one whole family of summaries (EV-0211).
- **Sample size.** Sixty customers is not an industry panel, and no
  source in this pack says what n makes a score stable.
- **Whether a comparison will be attempted.** Most misuse is
  comparison: against a competitor, an industry figure, or last
  quarter's different population.

## Options

### A. Single-question loyalty score
One likelihood-to-recommend question, scored as promoters minus
detractors. The claimed virtue is that the front line can act on it
without interpretation (FRAG-SUPPORT-OPERATIONS-07). Buys a cheap
recurring trend line. Costs credibility if the superiority claim is
repeated: the replication using the same exemplar industries found
explanatory power statistically indistinguishable from a conventional
satisfaction index (FRAG-SUPPORT-OPERATIONS-08). Scope note: 21 firms,
more than 15,500 interviews, one national panel, an era predating
subscription software.

### B. Customer effort
How much work the customer had to do. High-effort interactions were
strongly associated with reported disloyalty while exceeding
expectations was not associated with loyalty at all
(FRAG-SUPPORT-OPERATIONS-09). Buys a measure that points at something
fixable, usually a channel switch. Costs the same instrument-vendor
caveat as A. Scope note: roughly 97,000 customers of contact centres,
self-reported loyalty intent rather than observed retention, and
headline proportions not independently replicated at the same
magnitude.

### C. Counts and percentiles over the queue itself
Volume by kind, count untriaged, count reopened, count of duplicate
reports per cause, and durations reported at stated percentiles.
Buys numbers the venture owns end to end, with no instrument and no
panel. Costs interpretation: a count is only a finding once it has a
denominator (FRAG-SUPPORT-OPERATIONS-11).

### D. Utilisation of the responder
Fraction of available response capacity consumed. Buys the one leading
indicator in this pack with a mechanism behind it: wait time rises as
utilisation over one minus utilisation, so the queue collapses before
any visible capacity problem (FRAG-SUPPORT-OPERATIONS-10). Costs an
honest denominator for available hours, which a founder rarely has.
Scope note: single server, first come first served, no priority
classes, nobody giving up.

## Decision rule

Always run C and D. They cost nothing beyond the triage record that
PACK.md B1 already requires, and D is the only number here that warns
before customers do. Add B when there is a self-service layer or more
than one channel, because that is where effort is manufactured. Add A
only if someone will act on the trend, and then report it with its
population, its n and its date range under PACK.md B7.

Never combine: a loyalty score is not comparable across instruments,
across firms, or across two populations that changed between
measurements. No single number captures a system, which the estate
already accepts for developer productivity (EV-0210) and which holds
here for the same reason.

## Default

C and D from the first paying customer. Durations at percentiles or as
raw counts only: no key, heading or target names an average or a mean
of a duration, which is PACK.md B5 and is a hard stop rather than a
style note (EV-0211). B once a help centre exists. A is optional and
carries its scope statement wherever it is shown.

## Worked rulings

- **support-operations exemplar (2026-08, argued)**: the week's report
  carried counts by kind, a duplicate count against the one incident,
  a queue-untriaged count of zero, and the outage duration as a single
  raw figure with no target attached. No average appeared anywhere, and
  no loyalty score was collected at 60 customers because nobody had
  named a decision it would change. See
  `packs/support-operations/exemplars/EX-SUPPORT-001-one-inbox-week.md`.
- **Deflection was left unmeasured on purpose (2026-08, argued)**: no
  primary source was found supporting a customer benefit from
  self-service deflection, so the venture measured resolution and
  onward contacts instead, under PACK.md D10, and recorded that the
  deflection rate itself was deliberately not collected.
