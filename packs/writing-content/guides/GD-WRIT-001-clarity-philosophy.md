---
summary: Which clarity philosophy governs this text, and where the control point sits?
kind: guide
authority: default
basis: standard
evidence_grade: observational
scope: estate
sources: [FRAG-WRITING-CONTENT-01, FRAG-WRITING-CONTENT-02, FRAG-WRITING-CONTENT-03, FRAG-WRITING-CONTENT-05, FRAG-WRITING-CONTENT-06, FRAG-WRITING-CONTENT-07, FRAG-WRITING-CONTENT-08, FRAG-WRITING-CONTENT-09, FRAG-WRITING-CONTENT-10]
review: 2027-08
type: guide
tags: [voice, content, a11y]
review_by: 2027-08
---

# GD-WRIT-001: Which clarity philosophy governs this text?

## The question

Four mature traditions claim to make text clear, and they disagree
about where the control point sits: at the writer, at the word, at the
reader, or in the message data structure. They are not stages of one
method and they cannot all be applied to one piece of text without the
result being incoherent. Pick one per body of text and say which.

## It depends on

- **What happens if the reader gets it wrong.** Injury, money lost, or
  a mildly worse afternoon.
- **How long the reader has.** A document is studied. A button label is
  glanced at.
- **Whether English is the reader's first language.**
- **How fast the vocabulary moves.** A product that renames a concept
  every quarter cannot maintain an approved-word list.
- **Whether a second locale is coming**, which pulls the control point
  towards the message structure whatever else is true.
- **Whether anyone will ever test the text on a real reader.** Two of
  the four are unfalsifiable without that.

## Options

### A. Plain language, control at the writer
Plainness is defined by reader outcome: the intended readers can find,
understand and use the thing (FRAG-WRITING-CONTENT-01). GOV.UK
(FRAG-WRITING-CONTENT-03) and the United States federal guidance
(FRAG-WRITING-CONTENT-02) are the two mature implementations. Buys a
transferable set of moves that work on almost any prose: front-load the
answer, use the reader's own words, write for the lowest literacy in
the audience. Costs a skill that degrades the moment the writer is
rushed or is a subject expert, and nothing in the guidance detects that
degradation. Its own definition makes comprehension the test, and
comprehension is only sometimes gained (FRAG-WRITING-CONTENT-07).

### B. Controlled language, control at the word
Remove the writer's choice. Roughly fifty-three rules and about nine
hundred approved words, each constrained to one meaning and one part of
speech (FRAG-WRITING-CONTENT-05). The claim is that ambiguity is best
attacked at the vocabulary layer, because one word with two meanings
defeats any amount of sentence discipline. Buys machine-checkable
correctness for procedures read under pressure by people whose first
language is not English. Costs a maintained termbase, a linter, and
text that is deliberately not idiomatic. No controlled trial of its
comprehension gains was located.

### C. Content design, control at the reader
The user need comes first and the page exists only to serve it
(FRAG-WRITING-CONTENT-03). In interfaces this becomes microcopy
discipline: placement and timing decided before wording
(FRAG-WRITING-CONTENT-09), and a diagnosis replaced by the shape of the
correct input. Buys the highest-yield rewrites in this pack and forces
the prior question of whether the text should exist. Costs research
time, and it says nothing about how the sentence is assembled.

### D. Message data, control at the structure
The translatable unit is a message with a data model, not a string with
holes in it, and selection on plurality, gender and case happens inside
the message (FRAG-WRITING-CONTENT-10). Buys a translator the freedom to
add a distinction the source language never had, and it is the only one
of the four that fixes a defect the others cannot see. Costs a format
decision, tooling, and a migration from whatever exists. Says nothing
about tone, terminology or whether the sentence is any good.

## Decision rule

If a misread step hurts someone or costs money, and the readers are
mostly not first-language English speakers, choose B for the procedural
text and A for everything around it. If the text is a page or a
document a non-specialist reads once to make a decision, choose A. If
the text is interface microcopy, choose C, because placement and timing
dominate wording there. If a second locale exists or is planned, D is
not an alternative to the others: layer it under whichever you picked.

## Default

C for interface strings, A for documentation, D layered under both from
the first commit that creates a string file. B only where the harm case
is real, because its ongoing cost is real too.

## Worked rulings

- **writing-content pack (2026-08, argued)**: this pack applies C to
  the error and form requirements, A to the venture documentation
  defaults, and D as B1 and B2, which bind regardless of philosophy.
  B was considered and rejected as a house-wide choice, and survives as
  the option to reach for on a safety-critical procedure.
- **EOS internal prose (2026-08, inherited)**: A, with the house voice
  law of ADR-0002 on top. The readers are agents and one person, and
  the failure mode is drift rather than misunderstanding. See
  `packs/writing-content/guides/GD-WRIT-003-voice-scope.md`.
- **Worked example (2026-08, argued)**: C plus D applied to an order
  panel, in
  `packs/writing-content/exemplars/EX-WRIT-001-order-panel-second-locale.md`.
