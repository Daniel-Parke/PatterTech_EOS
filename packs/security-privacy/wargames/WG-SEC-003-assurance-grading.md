---
id: WG-SEC-003
summary: No declared level, a flat entry bar, a graded catalogue by data sensitivity, or per-practice maturity?
kind: wargame
type: wargame
tags: [eos, security, testing, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-SEC-011]
applies_when: [runs_agents]
engages_when: [operator_requests_wargame]
consequence: high
relations: []
always_walk: true
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0034, EV-0035, EV-0036, EV-0037, EV-0039, EV-0040]
review: 2027-06
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-SEC-003: how much assurance, and graded how?

## Decision question and stakes

A control catalogue with no grading is either ignored or it stops all
work. The fork is how to say how much security this surface needs, in a
way a reviewer can check and a solo operator can actually reach. It
returns whenever a venture adds a surface that holds personal data or
faces a buyer who asks what standard you work to.

## Doctrines or coverage gap under pressure

- `DOC-SEC-011` (default): ASVS level 1 as the entry bar, level 2 for anything holding personal data, exclusions documented.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Does the surface hold personal data, money, or credentials for
  someone else's system?
- Is there an external audience for the answer: a buyer, an insurer, a
  regulator? If so, the vocabulary matters as much as the controls.
- How long will the surface live? A grading scheme costs more than it
  returns on a two-week experiment.
- Is one practice the bottleneck, or is the whole surface uniformly
  thin?

Applicability is `runs_agents`. Engagement is `operator_requests_wargame`. This is an always-walk decision.

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

## Failure premises

### Premortem for A. No declared level

Assume `A. No declared level` was selected and the outcome failed. Test this option's stated failure mechanism first: any ability to say what is covered, which fails the moment someone asks, and it hides uniform thinness because nothing is compared against anything.

### Premortem for B. A flat entry bar for everything

Assume `B. A flat entry bar for everything` was selected and the outcome failed. Test this option's stated failure mechanism first: precision: a payment surface and a marketing page carry the same bar, so one is over-served and the other under-served.

### Premortem for C. Graded by data sensitivity

Assume `C. Graded by data sensitivity` was selected and the outcome failed. Test this option's stated failure mechanism first: a tailoring step: exclusions must be documented per surface or the level becomes theatre, and someone has to decide which surface is which.

### Premortem for D. Per-practice maturity

Assume `D. Per-practice maturity` was selected and the outcome failed. Test this option's stated failure mechanism first: a heavier assessment, and it can excuse a permanently thin practice by giving it a number and calling that a position.

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

## Safe default

C. Level 1 as the entry bar, level 2 for anything holding personal
data, exclusions documented. Add D per practice when one practice is
demonstrably the constraint. Whichever is chosen, the level is tested
against, not declared: an untested level is the failure EV-0039 shows
inside a maintained project, whose index still pointed at v4 mappings
long after v5 shipped.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Does the surface hold personal data, money, or credentials for someone else's system?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C. Level 1 as the entry bar, level 2 for anything holding personal data, exclusions documented. Add D per practice when one practice is demonstrably the constraint. Whichever is chosen, the level is tested against, not declared: an untested level is the failure EV-0039 shows inside a maintained project, whose index still pointed at v4 mappings long after v5 shipped.

**Exit condition:** Stop or roll back the selected branch when any ability to say what is covered, which fails the moment someone asks, and it hides uniform thinness because nothing is compared against anything, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Does the surface hold personal data, money, or credentials for someone else's system?

## Counter-evidence and transfer limits

Levels grade controls, not the reasoning behind them, so a tailored
level can be met by a surface nobody thought about. The NIST AI RMF
functions (EV-0040) organise the same work by activity rather than by
level and would give a different answer for an AI-heavy surface; we
have not argued that fork and it is open. None of the level schemes
here carry outcome evidence that a level-2 surface suffers fewer
incidents than a level-1 one, because nobody has run that study. The
grading is a way of allocating effort, and it should be described that
way rather than as a measured risk reduction.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
