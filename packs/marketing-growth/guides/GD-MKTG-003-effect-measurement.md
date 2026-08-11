---
summary: How is a channel's effect measured, and what may be claimed from it?
kind: guide
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
sources: [EV-0059, EV-0362, EV-0363, EV-0364, EV-0367]
review: on-change-of:GA4-attribution-model-set
type: guide
tags: [content, testing, tooling]
---

# GD-MKTG-003: How is a channel's effect measured?

## The question

Someone will ask what the campaign did. The answer can be a measured
causal effect, a bookkeeping convention, or a guess wearing a
percentage sign. PACK.md D3 requires a holdout or a label; this guide
decides which measurement route a given claim can afford, and what each
route entitles you to say.

## It depends on

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

## Decision rule

If the claim will drive spend and the volume supports it, run A. If an
experiment programme already exists and per-touchpoint reporting is
needed, run B on top of it. If neither, run C and label every number, or
run D and make no causal claim at all. Never present C or D output as an
effect. Guardrail metrics block only on significant harm (EV-0059);
they are not the effect measurement.

## Default

D for diagnostics, A for anything that changes a budget. A venture with
no holdout runs D and labels its C output UNVERIFIED, which is a
work-around and is recorded as one.

## Worked rulings

- **marketing-growth pack exemplar (2026-08, argued)**: D as the
  measurement plan, with the three funnel parameters stored as
  configuration and every stated rate carrying the UNVERIFIED token,
  because a launch has no volume for a holdout. See
  `packs/marketing-growth/exemplars/EX-MKTG-001-launch-and-first-sequence.md`.
- **Estate default (2026-08, argued)**: the field is a spectrum rather
  than a prohibition. Later work in the same journal as EV-0362
  treats non-experimental approaches more sympathetically, which is why
  D3 in PACK.md is a default and not a binding rule. If an affordable
  design for a low-volume venture is published, this guide is the first
  thing to re-argue.
