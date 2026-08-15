---
id: GD-LEGAL-005
summary: What a study may lawfully carry away from a source we do not own, how deep the reading goes, and who may hold the source while the replacement is written
kind: wargame
type: wargame
tags: [delivery, eos, security, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-LEGAL-016, DOC-LEGAL-017, DOC-LEGAL-012, DOC-LEGAL-002, DOC-LEGAL-007]
applies_when: [studies_external_source]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: asserted
sources: [EV-0337, EV-0344, EV-0348, EV-0352, EV-0496, EV-0497, EV-0498, EV-0499, EV-0500, EV-0501, EV-0502, EV-0503, EV-0504]
review: 2027-04
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-LEGAL-005: What may a study carry away from a source we do not own?

## Decision question and stakes

We want to learn from somebody else's product, repository, game or
postmortem. The fork is not whether to look. It is how deep the reading
goes, what comes back with it, and who may hold the source while the
replacement is written.

## Doctrines or coverage gap under pressure

- `DOC-LEGAL-016` (default): Nothing is studied until how it was acquired, the terms attached to it and the governing law are written down.
- `DOC-LEGAL-017` (default): The session that reads the source and the lanes that build are different, and the build lanes get the lesson, never the source.
- `DOC-LEGAL-012` (default): Vendored code carries its licence text and a provenance note at the moment it is copied.
- `DOC-LEGAL-002` (binding): No dependency enters without a recorded licence expression, and absence is a blocking finding.
- `DOC-LEGAL-007` (binding): Consequential questions stop here and go to a lawyer.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- How did we get the artefact, what terms came with it, and under which
  country's law are those terms read?
- Is the thing we want an idea, a method, a shape, or one particular
  expression of one?
- Will the people who build have seen the source, and is any real code
  going to move?

Applicability is `studies_external_source`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Black box

Use the product as a customer, read its published documentation, watch
what it does. Buys: the cheapest option and the safest one here, since
in UK and EU law a lawful user may observe, study and test a program to
work out the ideas underneath it. Costs: you learn behaviour and not
the reason for it.

### B. Read what we are entitled to read, carry a filtered lesson

Read the source, the schema, the protocol or the postmortem, and carry
away only the filtered set above, re-expressed as our own functional
description. Buys: the level where most of the value sits, and a lesson
the build lanes can use. Costs: it needs the separation below and the
reading recorded, and it is where an honest study turns into a copy if
nobody watches the abstraction level.

### C. Carry the code

Stop calling it a study. Code that moves is a vendored dependency: it
arrives with its licence text and a provenance note at the moment it is
copied, declared per file (EV-0344), with its identifier recorded
(EV-0337). D5 and B2 own it from there.

### D. Carry the expression

Never. There is no version of this that becomes safe by changing the
colours.

## Failure premises

### Premortem for A. Black box

Assume `A. Black box` was selected and the outcome failed. Test this option's stated failure mechanism first: you learn behaviour and not the reason for it.

### Premortem for B. Read what we are entitled to read, carry a filtered lesson

Assume `B. Read what we are entitled to read, carry a filtered lesson` was selected and the outcome failed. Test this option's stated failure mechanism first: it needs the separation below and the reading recorded, and it is where an honest study turns into a copy if nobody watches the abstraction level.

### Premortem for C. Carry the code

Assume `C. Carry the code` was selected and the outcome failed. Test this option's stated failure mechanism first: Stop calling it a study. Code that moves is a vendored dependency: it arrives with its licence text and a provenance note at the moment it is copied, declared per file (EV-0344), with its identifier recorded (EV-0337). D5 and B2 own it from there.

### Premortem for D. Carry the expression

Assume `D. Carry the expression` was selected and the outcome failed. Test this option's stated failure mechanism first: Never. There is no version of this that becomes safe by changing the colours.

## Decision rule

- A first, always. Most questions stop here.
- B when a black box cannot answer the question, with D9 recorded
  before the reading starts and D10 holding for the build.
- C the moment real code moves, and then it is a licensing decision and
  not a study.
- Never D. Repainting the surface while keeping every proportion is the
  losing position, not the clever one.
- Terms forbidding reverse engineering, a source we were not entitled
  to hold, or anything reached by getting round a technical protection:
  stop, and route it to a lawyer under B7.

## Safe default

A, then B under D9 and D10. The venture writes down how it records a
studied source before it studies the first one, rather than during the
argument about one.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **How did we get the artefact, what terms came with it, and under which country's law are those terms read?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A, then B under D9 and D10. The venture writes down how it records a studied source before it studies the first one, rather than during the argument about one.

**Exit condition:** Stop or roll back the selected branch when you learn behaviour and not the reason for it, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: How did we get the artefact, what terms came with it, and under which country's law are those terms read?

## Counter-evidence and transfer limits

### Evidence boundary

The line in the middle of the guide rests on decided cases and on one
advocacy organisation's clean-room practice. Those are now ledgered as
EV-0496 to EV-0504, recorded with court, year and holding, and two of
the nine rows are tertiary summaries rather than the opinions. Most
is United States authority, one row is EU, and nothing has been tested
against a United Kingdom judgment. Read the guide at the strength of
its weakest row. It is not legal advice, and an agent that reasons its
way to a confident answer about a particular extraction has done the
thing B7 exists to prevent.
### Preserved reasoning: The line

What may be carried: ideas, methods, mechanics, forms dictated by
efficiency, forms dictated by an external constraint such as hardware,
interoperability or an industry convention, and public-domain material.

What may not: expression. Assets, expressive text, the particular
pictures and words, and an overall look that identifies the source to
its own customers. A game's mechanic is free and that game's board
geometry, piece colours and animation are not. A desktop metaphor is
free and one product's source-identifying dress is not, and that second
risk is a trademark risk surviving even where the copyright question
comes back empty.

How the artefact was acquired is part of whether the study was lawful.
A tainted copy sinks the position however careful the reading was, and
a public repository being forkable grants no right to use what is in it
(EV-0348). D9 in `packs/legal-licensing/PACK.md` is that record; D10 is
the separation.
### Preserved reasoning: Jurisdiction changes the answer, so it is recorded per source

In UK and EU law a lawful user's right to observe, study and test a
program cannot be excluded by contract. In the United States licence
terms forbidding reverse engineering have been enforced against
fair-use rights, so the same reading can be lawful here and a breach of
contract there. That is why D9 records governing law and terms beside
the artefact, and why no single global rule is written down.
### Preserved reasoning: Clean room, and why a model does not get one for free

Clean room means the session that read the source and the lanes that
build are different, and the build lanes get the lesson and never the
source. The point is evidentiary: similarity plus access is what an
infringement argument is made of, and the cheapest defence is that
whoever wrote the replacement never saw the original.

A reimplementation written by a model is not presumed clean, because
the model may have been trained on the original, so the implementing
side was never separated to begin with. That is informed commentary
rather than settled law and it is carried as a risk assumption.
Authorship of machine output is itself unsettled (EV-0352), so the
position stays narrow: separate the lanes, record the provenance, and
never claim the output is clean because a process was followed.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
