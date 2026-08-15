---
summary: One authoritative source, a fixed budget, agreement from independent routes, or an exhaustive sweep?
type: guide
tags: [data, content, product]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
review: 2029-04
sources: [EV-0532, EV-0533, EV-0534, EV-0535, EV-0537, EV-0545, EV-0097]
---

# GD-RESEARCH-001: how much evidence is enough, and how do we know to stop?

## The question

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

## It depends on

- Is there a primary source that settles the question by construction?
  A specification, a licence file, an API response and a release note
  usually do. A performance figure never does.
- Is the claim definitional or empirical? A definitional claim is
  settled by reading; an empirical one has a distribution behind it and
  a body of evidence with a direction of bias.
- How reversible is the decision the research feeds? A dependency choice
  is cheap to undo in week one and expensive in year two.
- What would change the answer? If nothing would, the search is theatre.

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

## Default

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

## Worked rulings

- **PatterTech EOS (2026-08, argued)**: C on top of B for this pack's
  own source sweep. Seventeen sources fetched inside one research pass,
  with the primary and its counter-source read for each contested claim.
  D was rejected as unaffordable for a domain this wide, and the
  narrowing that made C honest was to argue four forks rather than to
  survey the field.
- **PatterTech EOS (2026-08, argued)**: A for every question about what
  a standard says, on the grounds that the standard is primary and the
  commentary is not. The two places this pack cites a figure rather than
  a rule, link rot rates and the reboxetine case, are both taken from
  the primary and both carry their own stated limits.
- No venture ruling yet. The first venture to argue this fork afresh
  becomes promotion evidence under `GOVERNANCE.md`.

## Counter-evidence

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
