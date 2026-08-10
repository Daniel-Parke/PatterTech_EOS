---
summary: Where does this rule live, in code, in a table, in a machine or in an engine?
kind: guide
authority: default
basis: standard
evidence_grade: observational
scope: estate
sources: [EV-0071, EV-0274, EV-0277, EV-0278, EV-0279, EV-0280]
review: on-change-of:DMN-1.7-formal
type: guide
tags: [arch, product, tooling]
---

# GD-BLM-002: Where does this rule live?

## The question

A rule can sit in a conditional, in a table, in a state machine or in
an engine. The fork is not about elegance, it is about who changes the
rule, how often, and whether anyone can still predict the outcome by
reading it.

## It depends on

- **Whose clock the rule runs on.** Rules that move weekly while the
  code ships quarterly are the case for externalising.
- **Who edits it.** The claim that business people will maintain the
  rules themselves is named as the thing that usually fails (EV-0274),
  so plan for a developer editing a readable artefact.
- **How many conditions combine.** Three inputs with three values each
  is twenty-seven cases, which is past comfortable reading in
  conditionals and comfortable in a table.
- **Whether a transition can be illegal.** A lifecycle with forbidden
  transitions is a different problem from a decision.
- **Whether rules can trigger each other.** Chaining is the property
  that makes rule sets unpredictable, and it is separable from the
  table form (EV-0278).

## Options

### A. Conditionals in code
The rule is an `if`, next to the thing it governs, versioned with the
code. Buys one artefact, one deployment, one place to look, and a
debugger. Costs readability once the combinations grow, and costs a
release cycle for every rule change.

### B. A decision table, hand-rolled or standardised
Inputs, outputs and rows in a closed form. The standard version adds a
requirements graph, a defined expression language and declared overlap
handling, which makes completeness and ambiguity machine-checkable in a
way a chain of conditionals is not (EV-0277). Buys review by
inspection: a missing combination is visible. Costs an evaluator, and
the standardised form costs a second runtime (EV-0278).

### C. An explicit state machine
The lifecycle is declared as states and transitions, and the machine
refuses anything not declared. Hierarchy and parallel regions stop the
state explosion that makes flat machines unusable on real lifecycles
(EV-0280, EV-0279). Buys illegal transitions refused rather than
noticed, and a definition that is directly inspectable. Costs a
declaration to keep in step with the code that acts on transitions.

### D. A production rule engine with chaining
Rules whose actions satisfy other rules' conditions, matched by the
engine. Buys expressive power for genuinely large rule sets. Costs
predictability: nobody predicts the outcome from reading any single
rule, and a set large enough to need a clever matching algorithm for
speed is already too large to reason about (EV-0274). Also costs a
runtime, an authoring story and a deployment story.

## Decision rule

Stay at A while the rules ship with the code and the combinations fit
on a page. Move to B when either the clock or the combination count
breaks, and prefer a small purpose-built evaluator inside one narrow
context over a general engine (EV-0274); a policy engine such as
EV-0071 is the same trade in a different domain. Use C wherever a thing
has a status and at least one transition must never happen, which is
orthogonal to A and B: the machine governs the transition, the table or
the conditional governs the decision. Choose D only when a named person
will author rules in the engine's own language and the rule set is
large enough that the matching algorithm earns its keep. In this estate
that has not happened yet.

## Default

A, with C wherever a lifecycle has forbidden transitions, and B when
the clock or the combination count breaks. Never D without a recorded
argument. Whatever is chosen, an illegal transition raises rather than
silently doing nothing, because a silent no-op leaves the caller
believing the change happened.

## Worked rulings

- **Booking hold expiry (estate, argued)**: four statuses, five legal
  transitions, a hand-written transition table under A plus C. No
  library. The transition table is data, the guard is a constructor,
  and the illegal pair raises.
- **Subscription price bands (2026-08, argued)**: five bands changing
  on a commercial clock, moved to B as a flat table with declared
  overlap handling, evaluated in-process. No engine, no second runtime.
  See
  `packs/business-logic-modelling/exemplars/EX-BLM-001-subscription-renewal.md`.

## Counter-evidence

The critique of engines is from 2009 and predates a standardised
non-chaining decision-table form with defined evaluation semantics
(EV-0274 against EV-0277). It lands hardest on chaining and least on
flat tables, which is why this guide separates B from D rather than
treating externalised rules as one choice. The statecharts paper behind
C was read at abstract level only, so no detailed semantic claim rests
on it (EV-0280), and the maintained implementation offers popularity
rather than evidence of defect reduction (EV-0279).
