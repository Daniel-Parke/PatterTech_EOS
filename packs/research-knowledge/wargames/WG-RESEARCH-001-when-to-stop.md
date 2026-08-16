---
id: WG-RESEARCH-001
summary: One authoritative source, a fixed budget, agreement from independent routes, or an exhaustive sweep?
kind: wargame
type: wargame
tags: [content, data, eos, product, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-RESEARCH-010, DOC-RESEARCH-015]
applies_when: [researches_before_building]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0532, EV-0533, EV-0534, EV-0535, EV-0537, EV-0545, EV-0097]
review: 2029-04
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-RESEARCH-001: how much evidence is enough, and how do we know to stop?

## Decision question and stakes

Somebody has to decide when the reading stops and the building starts.
Stop too early and the venture builds on a fact it half knows. Stop too
late and the research budget eats the build budget, which is the same
failure with better manners. Every venture that has to establish an
outside fact before committing meets this fork, and it meets it on every
question, not once.

The honest published answer is that there is no threshold. The nearest
thing to a standard for this decision answers it by naming the cost of
each limit on the search rather than by naming a number of sources
(EV-0535). So the fork is not how many, it is which stopping rule,
chosen before the search begins so that stopping is a decision rather
than fatigue.

## Doctrines or coverage gap under pressure

- `DOC-RESEARCH-010` (default): Record every limit put on the search, with what it might have cost.
- `DOC-RESEARCH-015` (default): Timebox the search half of a research task and record the box.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Is there a primary source that settles the question by construction?
  A specification, a licence file, an API response and a release note
  usually do. A performance figure never does.
- Is the claim definitional or empirical? A definitional claim is
  settled by reading; an empirical one has a distribution behind it and
  a body of evidence with a direction of bias.
- How reversible is the decision the research feeds? A dependency choice
  is cheap to undo in week one and expensive in year two.
- What would change the answer? If nothing would, the search is theatre.

Applicability is `researches_before_building`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. The primary source, and stop
Read the specification, the source, the licence or the maintainer's own
statement, record it, stop. Buys the shortest path to the most reliable
thing available, and for a software venture it is often the most
reliable thing available, because the specification is primary and the
secondary reading is where the error enters (EV-0545). Costs everything
the source does not say: what it does in practice, what it costs, what
its maintainer has since decided. A specification cannot tell you it is
not implemented.

### B. A fixed budget, then take what you have
Timebox the search, spend the box, write down what was found and what
the box excluded. Buys predictability, and it is the only option that
bounds the research cost of a question nobody can answer. Costs recall
in an unknown direction, because a box that ends mid-search ends
wherever the search happened to be. The exclusions go on the record, so
the next reader can at least see the shape of what was skipped.

### C. Agreement from independent routes
Reach the question by two or more routes that do not read each other,
and stop when they agree and nothing new changes the answer. Buys the
only cheap defence against the commonest failure in a small knowledge
base, one source cited five times through five people who all read it.
Costs the work of establishing independence: tracing one chain back to
its primary is often the most expensive half-hour in the search. Costs
nothing against a fact everyone is wrong about together.

### D. The exhaustive sweep against a stated frame
Define the population of sources, search it systematically, record
inclusions and exclusions, and disclose the whole thing (EV-0532). Buys
a result somebody else can audit and repeat, and it is the only option
that makes non-reporting bias visible, which matters because the
direction of that bias is known and it favours the positive result
(EV-0537). Costs a great deal, and its own authors are explicit that a
complete disclosure checklist says the work is inspectable and says
nothing about whether it reached the right answer.

## Failure premises

### Premortem for A. The primary source, and stop

Assume `A. The primary source, and stop` was selected and the outcome failed. Test this option's stated failure mechanism first: everything the source does not say: what it does in practice, what it costs, what its maintainer has since decided. A specification cannot tell you it is not implemented.

### Premortem for B. A fixed budget, then take what you have

Assume `B. A fixed budget, then take what you have` was selected and the outcome failed. Test this option's stated failure mechanism first: of a question nobody can answer. Costs recall in an unknown direction, because a box that ends mid-search ends wherever the search happened to be. The exclusions go on the record, so the next reader can at least see the shape of what was skipped.

### Premortem for C. Agreement from independent routes

Assume `C. Agreement from independent routes` was selected and the outcome failed. Test this option's stated failure mechanism first: the work of establishing independence: tracing one chain back to its primary is often the most expensive half-hour in the search. Costs nothing against a fact everyone is wrong about together.

### Premortem for D. The exhaustive sweep against a stated frame

Assume `D. The exhaustive sweep against a stated frame` was selected and the outcome failed. Test this option's stated failure mechanism first: a great deal, and its own authors are explicit that a complete disclosure checklist says the work is inspectable and says nothing about whether it reached the right answer.

## Decision rule

- A definitional question with a primary source: A. Read the
  specification, record it, move.
- Anything empirical, or any claim about behaviour, cost or reliability:
  C as the floor. One source is one source however good it looks.
- The decision is cheap to reverse, or the venture is still deciding
  whether the question matters: B, with the box recorded and the
  exclusions named.
- The decision is expensive to reverse and the venture will be asked to
  defend it, to a customer, a regulator or a buyer: D on the narrow
  question only, never on the whole domain.
- Any of the four: write the stop condition down before searching, and
  record whether it was met. A stop condition written afterwards is a
  description of when somebody got tired.

## Safe default

C on top of B. Timebox the search, and inside the box require two
independent routes to the answer before the claim is written. It is
cheap, it catches the failure a small knowledge base actually has, and
its cost is visible in the record rather than hidden in a judgement.
Move to D when the decision is expensive to reverse, and narrow the
question until D is affordable rather than widening the budget until D
fits.

Whichever is chosen, the finding becomes a decision record sized to the
decision (EV-0097). Research that never becomes a decision gets
researched again by the next person.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Is there a primary source that settles the question by construction? A specification, a licence file, an API response and a release note usually do. A performance figure never does.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C on top of B. Timebox the search, and inside the box require two independent routes to the answer before the claim is written. It is cheap, it catches the failure a small knowledge base actually has, and its cost is visible in the record rather than hidden in a judgement. Move to D when the decision is expensive to reverse, and narrow the question until D is affordable rather than widening the budget until D fits. Whichever is chosen, the finding becomes a decision record sized to the decision (EV-0097). Research that never becomes a decision gets researched again by the next person.

**Exit condition:** Stop or roll back the selected branch when everything the source does not say: what it does in practice, what it costs, what its maintainer has since decided. A specification cannot tell you it is not implemented, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Is there a primary source that settles the question by construction? A specification, a licence file, an API response and a release note usually do. A performance figure never does.

## Counter-evidence and transfer limits

The published guidance this rests on refuses to give a threshold and
gives costs instead, which means every decision rule above is this
estate's construction rather than a finding. The Oxford levels record
that hierarchies of evidence have been used inflexibly and criticised
for decades, and that no ranking scheme works unless judgement is
applied to its output (EV-0534); a stopping rule applied without
judgement is that same failure in a different coat.

The best empirical answer to this fork lives in the rapid-review
literature, which measures what abbreviating a full search actually
costs. It is not in this pack: the publisher returned 403 on the day of
the sweep, so no record exists and nothing here rests on one. That is
the hole, and it is where the next person should look.

One source cuts against C directly. The handbook that expects two
readers on inclusion says two people running the search in parallel is
not desirable (EV-0535). Independence is worth paying for on judgement
and is waste on retrieval, so C means two routes to the answer, not two
people doing one search.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
