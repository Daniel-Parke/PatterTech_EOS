---
summary: Field performance as a design constraint, budgets, measurement and the motion safety rules that carry everywhere
kind: fact
scope: estate
sources: [EV-0027, EV-0241]
volatility: slow
review: on-change-of:core-web-vitals-metric-set
type: ux
tags: [perf, motion, web]
---

# Performance and motion

Reference for the performance default in PACK.md and for the motion
safety default. House motion numbers are not here; they belong to the
Wave B preference pack.

## Performance as a design constraint

On a surface with a money number attached, field performance is a
design decision, not a build-time cleanup. The collected case studies
report improvements in loading and interaction metrics alongside
improvements in business metrics (EV-0241). Take the method from that
source and not the numbers:

- The figures are before-and-after correlations chosen by an interested
  party, with no controls or intervals.
- The page has not been revised since 2021 while the metric set has
  changed, so the metric names in it are out of date.
- The source's own note concedes that only an experiment measures
  meaningful impact.

So: set a budget, measure it in the field on real sessions, and settle
any revenue claim by experiment rather than by citing a case study.

## Budget shape

Budgets are written down per surface and gated, not aspired to. The
shape that carries; the numbers are per venture:

- a ceiling per image on the wire, and a total image transfer after a
  full scroll,
- a first-viewport transfer ceiling,
- a cap on font families, subset, with a swap strategy,
- a stated position on third-party scripts, with embeds as facades
  until clicked,
- a rule that client script earns its place, so reveals are CSS and an
  intersection observer rather than a motion library.

Structural choices that keep the budget: prerender what can be
prerendered, pre-generate image variants rather than resizing at
runtime, put intrinsic dimensions on all media so nothing shifts, lazy
load below the fold, pause continuous visuals when hidden and cap the
device pixel ratio.

## Measuring

Measure with a script rather than by feel: drive a headless browser
through a full-page scroll, total the bytes, fail over budget, keep the
script in the repo and the numbers in the gate. Lab numbers are for
regressions; the claim about users is a field claim.

## Motion safety

These carry across every philosophy:

- Reduced-motion preferences are honoured globally, in stylesheets and
  in every script-driven animation. Signature visuals render a static
  frame. Most of this sits at the standard's highest level rather than
  the level usually claimed (EV-0027), so it is a default here and not
  binding.
- No autoplaying media, no parallax on reading surfaces, no
  scroll-jacking.
- Nothing that moves content a person is trying to read or click.
- Reading matter does not animate in. A fade on every paragraph is the
  loudest template tell there is.
- If a reveal hides content before script runs, the hidden state is
  gated behind a scripting query so content is never invisible without
  script.
- One tokenised easing curve per project, so motion reads as one hand.

The v1 doctrine also carries a house table of what may move and for how
long. Those numbers are house taste, and they are the subject of an
unresolved contradiction noted in PACK.md. They arrive with the Wave B
preference pack, not with this one.
