---
id: WG-SUPPORT-004
summary: What do we measure about support, and what may the number be used for?
kind: wargame
type: wargame
tags: [eos, ops, product, testing, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-SUPPORT-003, DOC-SUPPORT-007, DOC-SUPPORT-006]
applies_when: [has_customer_inbound]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0210, EV-0211]
review: 2028-08
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-SUPPORT-004: What do we measure about support, and what may the number be used for?

## Decision question and stakes

Support generates numbers faster than it generates insight. The fork is
not which dashboard: it is what claim each number is allowed to carry.
Three of the four candidates below have a published failure attached,
and the fourth has no evidence at all. Choosing without reading the
failure is how a venture ends up steering on a statistic that describes
nothing.

## Doctrines or coverage gap under pressure

- `DOC-SUPPORT-003` (default): Nothing enters a backlog without a classification, and untriaged is a state rather than an absence.
- `DOC-SUPPORT-007` (default): A loyalty or satisfaction score is a trend about one population, never a cross-firm benchmark.
- `DOC-SUPPORT-006` (default): No target and no published figure is the mean of a duration distribution.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **Who reads it and what they will do on Monday.** A number nobody can
  act on within a week is not a support metric.
- **The shape of the distribution.** Durations are positively skewed,
  which rules out one whole family of summaries (EV-0211).
- **Sample size.** Sixty customers is not an industry panel, and no
  source in this pack says what n makes a score stable.
- **Whether a comparison will be attempted.** Most misuse is
  comparison: against a competitor, an industry figure, or last
  quarter's different population.

Applicability is `has_customer_inbound`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Single-question loyalty score
One likelihood-to-recommend question, scored as promoters minus
detractors. The claimed virtue is that the front line can act on it
without interpretation (EV-0427). Buys a cheap
recurring trend line. Costs credibility if the superiority claim is
repeated: the replication using the same exemplar industries found
explanatory power statistically indistinguishable from a conventional
satisfaction index (EV-0428). Scope note: 21 firms,
more than 15,500 interviews, one national panel, an era predating
subscription software.

### B. Customer effort
How much work the customer had to do. High-effort interactions were
strongly associated with reported disloyalty while exceeding
expectations was not associated with loyalty at all
(EV-0429). Buys a measure that points at something
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
denominator (EV-0431).

### D. Utilisation of the responder
Fraction of available response capacity consumed. Buys the one leading
indicator in this pack with a mechanism behind it: wait time rises as
utilisation over one minus utilisation, so the queue collapses before
any visible capacity problem (EV-0430). Costs an
honest denominator for available hours, which a founder rarely has.
Scope note: single server, first come first served, no priority
classes, nobody giving up.

## Failure premises

### Premortem for A. Single-question loyalty score

Assume `A. Single-question loyalty score` was selected and the outcome failed. Test this option's stated failure mechanism first: credibility if the superiority claim is repeated: the replication using the same exemplar industries found explanatory power statistically indistinguishable from a conventional satisfaction index (EV-0428). Scope note: 21 firms, more than 15,500 interviews, one national panel, an era predating subscription software.

### Premortem for B. Customer effort

Assume `B. Customer effort` was selected and the outcome failed. Test this option's stated failure mechanism first: the same instrument-vendor caveat as A. Scope note: roughly 97,000 customers of contact centres, self-reported loyalty intent rather than observed retention, and headline proportions not independently replicated at the same magnitude.

### Premortem for C. Counts and percentiles over the queue itself

Assume `C. Counts and percentiles over the queue itself` was selected and the outcome failed. Test this option's stated failure mechanism first: interpretation: a count is only a finding once it has a denominator (EV-0431).

### Premortem for D. Utilisation of the responder

Assume `D. Utilisation of the responder` was selected and the outcome failed. Test this option's stated failure mechanism first: an honest denominator for available hours, which a founder rarely has. Scope note: single server, first come first served, no priority classes, nobody giving up.

## Decision rule

Always run C and D. They cost nothing beyond the triage record that
PACK.md B1 asks for, and D is the only number here that warns
before customers do. Add B when there is a self-service layer or more
than one channel, because that is where effort is manufactured. Add A
only if someone will act on the trend, and then report it with its
population, its n and its date range under PACK.md B7.

Never combine: a loyalty score is not comparable across instruments,
across firms, or across two populations that changed between
measurements. No single number captures a system, which the estate
already accepts for developer productivity (EV-0210) and which holds
here for the same reason.

## Safe default

C and D from the first paying customer. Durations at percentiles or as
raw counts only: no key, heading or target names an average or a mean
of a duration, which is PACK.md B5. B5 is a default since the 2026-08
audit, so it is departed from in writing rather than in passing, and
the measurement behind it has not moved (EV-0211). B once a help
centre exists. A is optional and carries its scope statement wherever
it is shown.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Who reads it and what they will do on Monday.** A number nobody can act on within a week is not a support metric.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C and D from the first paying customer. Durations at percentiles or as raw counts only: no key, heading or target names an average or a mean of a duration, which is PACK.md B5. B5 is a default since the 2026-08 audit, so it is departed from in writing rather than in passing, and the measurement behind it has not moved (EV-0211). B once a help centre exists. A is optional and carries its scope statement wherever it is shown.

**Exit condition:** Stop or roll back the selected branch when credibility if the superiority claim is repeated: the replication using the same exemplar industries found explanatory power statistically indistinguishable from a conventional satisfaction index (EV-0428). Scope note: 21 firms, more than 15,500 interviews, one national panel, an era predating subscription software, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Who reads it and what they will do on Monday.** A number nobody can act on within a week is not a support metric.

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test ****Who reads it and what they will do on Monday.** A number nobody can act on within a week is not a support metric.** and ****The shape of the distribution.** Durations are positively skewed, which rules out one whole family of summaries (EV-0211).** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
