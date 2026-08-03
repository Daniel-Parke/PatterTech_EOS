---
summary: No declared level, a flat entry bar, a graded catalogue by data sensitivity, or per-practice maturity?
type: guide
tags: [security, testing]
review_by: 2027-06
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
review: 2027-06
sources: [EV-0034, EV-0035, EV-0036, EV-0037, EV-0039, EV-0040]
---

# GD-SEC-003: how much assurance, and graded how?

## The question

A control catalogue with no grading is either ignored or it stops all
work. The fork is how to say how much security this surface needs, in a
way a reviewer can check and a solo operator can actually reach. It
returns whenever a venture adds a surface that holds personal data or
faces a buyer who asks what standard you work to.

## It depends on

- Does the surface hold personal data, money, or credentials for
  someone else's system?
- Is there an external audience for the answer: a buyer, an insurer, a
  regulator? If so, the vocabulary matters as much as the controls.
- How long will the surface live? A grading scheme costs more than it
  returns on a two-week experiment.
- Is one practice the bottleneck, or is the whole surface uniformly
  thin?

## Options

### A. No declared level
Fix what looks wrong when it looks wrong. Buys zero overhead and full
attention on whatever is actually in front of you. Costs any ability to
say what is covered, which fails the moment someone asks, and it hides
uniform thinness because nothing is compared against anything.

### B. A flat entry bar for everything
One level, applied estate-wide. ASVS 5.0 grades its catalogue so the
first tier is roughly a fifth of the whole and is deliberately cheap to
enter (EV-0034, EV-0035). Buys a bar that gets met rather than admired,
and a single sentence that answers the external question. Costs
precision: a payment surface and a marketing page carry the same bar,
so one is over-served and the other under-served.

### C. Graded by data sensitivity
Level 1 as the entry bar, level 2 where personal data or money lives,
the expensive defence-in-depth tier reserved for the top (EV-0035).
Buys proportionality, which is also what the regulator's posture asks
for (EV-0041 sits behind this in the pack body). Costs a tailoring
step: exclusions must be documented per surface or the level becomes
theatre, and someone has to decide which surface is which.

### D. Per-practice maturity
SAMM grades each practice separately, so a venture can be mature in one
area and immature in another with no universal floor (EV-0036). Buys
honesty about where you actually are, and a work list that targets the
weakest practice rather than the whole catalogue. Costs a heavier
assessment, and it can excuse a permanently thin practice by giving it
a number and calling that a position.

## Decision rule

- Any venture surface that will outlive the quarter: C. Level 1
  everywhere, level 2 where the surface holds personal data, money, or
  another party's credentials, with exclusions written down per
  surface.
- No personal data, no money, short-lived: B at level 1, and stop.
- A named practice is the bottleneck and the rest is adequate: D for
  that practice only, as a work list, on top of C. Do not replace C
  with D, because per-practice maturity with no floor lets the weakest
  practice sit still.
- An external audience is asking: C, and say the level out loud with
  its exclusions. A level with undocumented exclusions is worse than no
  level, because it is a claim you cannot support.
- A is only defensible for a spike that will be deleted.

## Default

C. Level 1 as the entry bar, level 2 for anything holding personal
data, exclusions documented. Add D per practice when one practice is
demonstrably the constraint. Whichever is chosen, the level is tested
against, not declared: an untested level is the failure EV-0039 shows
inside a maintained project, whose index still pointed at v4 mappings
long after v5 shipped.

## Worked rulings

- **PatterTech EOS (2026-08, argued)**: C, adopted as the pack default,
  with the graded-tier structure taken from ASVS as the model for how
  our own binding requirements separate from defaults. This repository
  holds no runtime surface, so the level applies to what it seeds, not
  to itself.
- **PatterTech EOS (2026-08, argued)**: D rejected as the primary
  scheme. The argument that decided it: a scheme with no floor cannot
  express a binding requirement, and this pack owns four of them.
- No venture ruling yet.

## Counter-evidence

Levels grade controls, not the reasoning behind them, so a tailored
level can be met by a surface nobody thought about. The NIST AI RMF
functions (EV-0040) organise the same work by activity rather than by
level and would give a different answer for an AI-heavy surface; we
have not argued that fork and it is open. None of the level schemes
here carry outcome evidence that a level-2 surface suffers fewer
incidents than a level-1 one, because nobody has run that study. The
grading is a way of allocating effort, and it should be described that
way rather than as a measured risk reduction.
