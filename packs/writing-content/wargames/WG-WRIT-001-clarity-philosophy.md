---
id: WG-WRIT-001
summary: Which clarity philosophy governs this text, and where the control point sits?
kind: wargame
type: wargame
tags: [a11y, content, eos, voice, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-WRIT-001, DOC-WRIT-002]
applies_when: [writes_user_facing_text]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0433, EV-0434, EV-0435, EV-0437, EV-0438, EV-0439, EV-0440, EV-0441, EV-0442]
review: 2028-09
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-WRIT-001: Which clarity philosophy governs this text?

## Decision question and stakes

Four mature traditions claim to make text clear, and they disagree
about where the control point sits: at the writer, at the word, at the
reader, or in the message data structure. They are not stages of one
method and they cannot all be applied to one piece of text without the
result being incoherent. Pick one per body of text and say which.

## Doctrines or coverage gap under pressure

- `DOC-WRIT-001` (binding): No user-facing sentence is assembled by string concatenation.
- `DOC-WRIT-002` (binding): Plural and gender selection resolves per locale through CLDR categories, never from the English pair.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

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

Applicability is `writes_user_facing_text`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Plain language, control at the writer
Plainness is defined by reader outcome: the intended readers can find,
understand and use the thing (EV-0433). GOV.UK
(EV-0435) and the United States federal guidance
(EV-0434) are the two mature implementations. Buys a
transferable set of moves that work on almost any prose: front-load the
answer, use the reader's own words, write for the lowest literacy in
the audience. Costs a skill that degrades the moment the writer is
rushed or is a subject expert, and nothing in the guidance detects that
degradation. Its own definition makes comprehension the test, and
comprehension is only sometimes gained (EV-0439).

### B. Controlled language, control at the word
Remove the writer's choice. Roughly fifty-three rules and about nine
hundred approved words, each constrained to one meaning and one part of
speech (EV-0437). The claim is that ambiguity is best
attacked at the vocabulary layer, because one word with two meanings
defeats any amount of sentence discipline. Buys machine-checkable
correctness for procedures read under pressure by people whose first
language is not English. Costs a maintained termbase, a linter, and
text that is deliberately not idiomatic. No controlled trial of its
comprehension gains was located.

### C. Content design, control at the reader
The user need comes first and the page exists only to serve it
(EV-0435). In interfaces this becomes microcopy
discipline: placement and timing decided before wording
(EV-0441), and a diagnosis replaced by the shape of the
correct input. Buys the highest-yield rewrites in this pack and forces
the prior question of whether the text should exist. Costs research
time, and it says nothing about how the sentence is assembled.

### D. Message data, control at the structure
The translatable unit is a message with a data model, not a string with
holes in it, and selection on plurality, gender and case happens inside
the message (EV-0442). Buys a translator the freedom to
add a distinction the source language never had, and it is the only one
of the four that fixes a defect the others cannot see. Costs a format
decision, tooling, and a migration from whatever exists. Says nothing
about tone, terminology or whether the sentence is any good.

## Failure premises

### Premortem for A. Plain language, control at the writer

Assume `A. Plain language, control at the writer` was selected and the outcome failed. Test this option's stated failure mechanism first: a skill that degrades the moment the writer is rushed or is a subject expert, and nothing in the guidance detects that degradation. Its own definition makes comprehension the test, and comprehension is only sometimes gained (EV-0439).

### Premortem for B. Controlled language, control at the word

Assume `B. Controlled language, control at the word` was selected and the outcome failed. Test this option's stated failure mechanism first: a maintained termbase, a linter, and text that is deliberately not idiomatic. No controlled trial of its comprehension gains was located.

### Premortem for C. Content design, control at the reader

Assume `C. Content design, control at the reader` was selected and the outcome failed. Test this option's stated failure mechanism first: research time, and it says nothing about how the sentence is assembled.

### Premortem for D. Message data, control at the structure

Assume `D. Message data, control at the structure` was selected and the outcome failed. Test this option's stated failure mechanism first: a format decision, tooling, and a migration from whatever exists. Says nothing about tone, terminology or whether the sentence is any good.

## Decision rule

If a misread step hurts someone or costs money, and the readers are
mostly not first-language English speakers, choose B for the procedural
text and A for everything around it. If the text is a page or a
document a non-specialist reads once to make a decision, choose A. If
the text is interface microcopy, choose C, because placement and timing
dominate wording there. If a second locale exists or is planned, D is
not an alternative to the others: layer it under whichever you picked.

## Safe default

C for interface strings, A for documentation, D layered under both from
the first commit that creates a string file. B only where the harm case
is real, because its ongoing cost is real too.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****What happens if the reader gets it wrong.** Injury, money lost, or a mildly worse afternoon.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C for interface strings, A for documentation, D layered under both from the first commit that creates a string file. B only where the harm case is real, because its ongoing cost is real too.

**Exit condition:** Stop or roll back the selected branch when a skill that degrades the moment the writer is rushed or is a subject expert, and nothing in the guidance detects that degradation. Its own definition makes comprehension the test, and comprehension is only sometimes gained (EV-0439), or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **What happens if the reader gets it wrong.** Injury, money lost, or a mildly worse afternoon.

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test ****What happens if the reader gets it wrong.** Injury, money lost, or a mildly worse afternoon.** and ****How long the reader has.** A document is studied. A button label is glanced at.** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
