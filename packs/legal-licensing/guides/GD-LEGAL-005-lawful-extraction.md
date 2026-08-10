---
summary: What a study may lawfully carry away from a source we do not own, how deep the reading goes, and who may hold the source while the replacement is written
type: guide
tags: [security, delivery]
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: asserted
sources: [EV-0337, EV-0344, EV-0348, EV-0352, EV-0496, EV-0497, EV-0498, EV-0499, EV-0500, EV-0501, EV-0502, EV-0503, EV-0504]
review: 2027-04
---

# GD-LEGAL-005: What may a study carry away from a source we do not own?

## The question

We want to learn from somebody else's product, repository, game or
postmortem. The fork is not whether to look. It is how deep the reading
goes, what comes back with it, and who may hold the source while the
replacement is written.

## It depends on

- How did we get the artefact, what terms came with it, and under which
  country's law are those terms read?
- Is the thing we want an idea, a method, a shape, or one particular
  expression of one?
- Will the people who build have seen the source, and is any real code
  going to move?

## The line

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

## Default

A, then B under D9 and D10. The venture writes down how it records a
studied source before it studies the first one, rather than during the
argument about one.

## Jurisdiction changes the answer, so it is recorded per source

In UK and EU law a lawful user's right to observe, study and test a
program cannot be excluded by contract. In the United States licence
terms forbidding reverse engineering have been enforced against
fair-use rights, so the same reading can be lawful here and a breach of
contract there. That is why D9 records governing law and terms beside
the artefact, and why no single global rule is written down.

## Clean room, and why a model does not get one for free

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

## Evidence boundary

The line in the middle of the guide rests on decided cases and on one
advocacy organisation's clean-room practice. Those are now ledgered as
EV-0496 to EV-0504, recorded with court, year and holding, and two of
the nine rows are tertiary summaries rather than the opinions. Most
is United States authority, one row is EU, and nothing has been tested
against a United Kingdom judgment. Read the guide at the strength of
its weakest row. It is not legal advice, and an agent that reasons its
way to a confident answer about a particular extraction has done the
thing B7 exists to prevent.

## Worked rulings

- **PatterTech EOS legal-licensing pack (2026-08, argued)**: A then B,
  with the separation in D10 a condition of B rather than advice.
  Argued from the acquisition-taint authority and the clean-room
  practice in the fragment, against the cost of running two sessions
  where one would do.
- **PatterTech EOS itself (2026-08, inherited)**: A then B. It studies
  documents and repositories, carries lessons rather than code, and has
  no exception to claim.
