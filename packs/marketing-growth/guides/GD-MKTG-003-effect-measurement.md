---
id: GD-MKTG-003
summary: How is a channel's effect measured, and what may be claimed from it?
kind: wargame
type: wargame
tags: [content, eos, testing, tooling, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-MKTG-006]
applies_when: [publishes_public_content]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0059, EV-0362, EV-0363, EV-0364, EV-0367]
review: on-change-of:GA4-attribution-model-set
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-MKTG-003: How is a channel's effect measured?

## Decision question and stakes

Someone will ask what the campaign did. The answer can be a measured
causal effect, a bookkeeping convention, or a guess wearing a
percentage sign. PACK.md D3 requires a holdout or a label; this guide
decides which measurement route a given claim can afford, and what each
route entitles you to say.

## Doctrines or coverage gap under pressure

- `DOC-MKTG-006` (default): Effect comes from a randomised holdout, or the number is labelled.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **Volume.** A holdout needs enough events for the difference to clear
  the noise, and small ventures usually do not have them.
- **Whether withholding is possible.** Some channels cannot be turned
  off for a random half of an audience.
- **How large the expected effect is.** Small percentage effects need
  large samples, which is why the platform studies are the size they
  are.
- **Who reads the number**, and whether they will treat a labelled
  estimate as a measurement anyway.
- **Consent coverage**, because identity-based methods degrade silently
  where tracking is refused and no vendor documents the gap
  (EV-0364).

Applicability is `publishes_public_content`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Randomised holdout
Withhold the activity from a randomly assigned group and compare. Buys
the only unbiased estimate available, and the only kind of number this
pack lets you call an effect. Costs volume, patience and deliberately
forgone reach. This is the ground truth the whole comparison rests on:
across fifteen randomised experiments at platform scale, observational
estimators on the same far richer data could not reproduce it
(EV-0362).

### B. Calibrated attribution
Run an attribution model, but anchor its total to an experimental
estimate and let the model only distribute credit within that anchor
(EV-0363). Buys per-touchpoint reporting that does not invent its
own total. Costs a continuous experiment programme underneath it, which
is the part small ventures skip. The source is a platform preprint about
its own product, so take the architecture of the argument and not the
numbers.

### C. Platform attribution as declared bookkeeping
Use the vendor's model, and label every output a reporting convention.
Buys cheap directional reporting and step-level diagnostics. Costs any
right to call the result an effect. The vendor deleted four of its own
heuristic models in November 2023 (EV-0364), which is a concession
that the credit-splitting rules were arbitrary.

### D. Funnel diagnostics with the definition attached
Do not estimate effect at all. Report step-level drop-off with the
ordering mode, exclusion steps and denominator stored as configuration
beside the number (EV-0367). Buys the cheapest useful diagnostic
there is. Costs nothing except the discipline of not reading drop-off as
cause, which is the mistake most funnel reporting actually makes.

## Failure premises

### Premortem for A. Randomised holdout

Assume `A. Randomised holdout` was selected and the outcome failed. Test this option's stated failure mechanism first: volume, patience and deliberately forgone reach. This is the ground truth the whole comparison rests on: across fifteen randomised experiments at platform scale, observational estimators on the same far richer data could not reproduce it (EV-0362).

### Premortem for B. Calibrated attribution

Assume `B. Calibrated attribution` was selected and the outcome failed. Test this option's stated failure mechanism first: a continuous experiment programme underneath it, which is the part small ventures skip. The source is a platform preprint about its own product, so take the architecture of the argument and not the numbers.

### Premortem for C. Platform attribution as declared bookkeeping

Assume `C. Platform attribution as declared bookkeeping` was selected and the outcome failed. Test this option's stated failure mechanism first: any right to call the result an effect. The vendor deleted four of its own heuristic models in November 2023 (EV-0364), which is a concession that the credit-splitting rules were arbitrary.

### Premortem for D. Funnel diagnostics with the definition attached

Assume `D. Funnel diagnostics with the definition attached` was selected and the outcome failed. Test this option's stated failure mechanism first: nothing except the discipline of not reading drop-off as cause, which is the mistake most funnel reporting actually makes.

## Decision rule

If the claim will drive spend and the volume supports it, run A. If an
experiment programme already exists and per-touchpoint reporting is
needed, run B on top of it. If neither, run C and label every number, or
run D and make no causal claim at all. Never present C or D output as an
effect. Guardrail metrics block only on significant harm (EV-0059);
they are not the effect measurement.

## Safe default

D for diagnostics, A for anything that changes a budget. A venture with
no holdout runs D and labels its C output UNVERIFIED, which is a
work-around and is recorded as one.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Volume.** A holdout needs enough events for the difference to clear the noise, and small ventures usually do not have them.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** D for diagnostics, A for anything that changes a budget. A venture with no holdout runs D and labels its C output UNVERIFIED, which is a work-around and is recorded as one.

**Exit condition:** Stop or roll back the selected branch when volume, patience and deliberately forgone reach. This is the ground truth the whole comparison rests on: across fifteen randomised experiments at platform scale, observational estimators on the same far richer data could not reproduce it (EV-0362), or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Volume.** A holdout needs enough events for the difference to clear the noise, and small ventures usually do not have them.

## Counter-evidence and transfer limits

### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
