---
summary: How is prose checked before it merges, and which signals are allowed to block?
kind: guide
authority: default
basis: decision
evidence_grade: anecdotal
scope: estate
sources: [FRAG-WRITING-CONTENT-03, FRAG-WRITING-CONTENT-04, FRAG-WRITING-CONTENT-05, FRAG-WRITING-CONTENT-06, FRAG-WRITING-CONTENT-14, FRAG-DOCS-DX-14]
review: 2027-08
type: guide
tags: [content, ci, tooling]
review_by: 2027-08
---

# GD-WRIT-004: How is prose checked before it merges?

## The question

Writing quality is mostly not machine-decidable, and a gate that
pretends otherwise gets ignored or gamed. The fork is how much
automation to run over prose and strings, and which of the resulting
signals is allowed to fail a build. Getting this wrong in either
direction is expensive: no check at all lets terminology drift into
every locale, and the wrong check trains a team to route around the
linter.

## It depends on

- **Whether the strings will be translated.** Terminology drift is
  cheap to fix in one language and expensive in five.
- **How many people write.** One writer needs no linter; six do.
- **Whether the team will honour a failing build.** A gate nobody
  respects is worse than no gate, because it teaches the habit of
  overriding.
- **Whether anyone can test copy on real readers.** That is the only
  check that speaks to comprehension at all.

## Options

### A. No automation, review only
A human reads the diff. Buys zero false positives and zero tooling.
Costs consistency the moment there are several writers, and it catches
nothing at three in the morning.

### B. Banned-and-preferred term list in CI, blocking
A short list of terms with one approved spelling each, run over
user-facing strings and documentation, failing the build on a banned
term (FRAG-DOCS-DX-14). Buys the one-word-one-meaning property for the
terms that actually matter, at a cost measured in a few dozen lines of
configuration. Costs list maintenance and the occasional false positive
in a quotation. No study was found showing it improves comprehension or
reduces support load, so it is a cheap bet rather than a proven one.

### C. Full controlled language with a maintained termbase
Approved words, restricted grammar, a real linter enforcing both
(FRAG-WRITING-CONTENT-05). Buys machine-checkable correctness for
safety-critical procedures. Costs a termbase owner, a review process
for new vocabulary, and text that reads as deliberately unidiomatic.
Justified where a misread step injures someone, and almost nowhere
else.

### D. Readability score as a gate
A formula score computed per file with a threshold. Named here to be
excluded. Formulas track measured difficulty only patchily and only at
some bands, because they measure surface proxies that sit downstream of
difficulty (FRAG-WRITING-CONTENT-04). The score improves when sentences
are chopped, whether or not anyone understands more. PACK.md B10
forbids this. Reporting the number is a preference; gating on it is
not available.

### E. Comprehension testing with real readers
An A/B of two renderings of one decision, with comprehension questions
as the outcome (FRAG-WRITING-CONTENT-06,
FRAG-WRITING-CONTENT-02). Buys the only evidence that speaks to
understanding rather than to text features. Costs recruitment, time and
a real sample, and it does not fit in a pull request. It gates nothing.
Its job is to turn a claim about clarity into a fact.

## Decision rule

Always run B once more than one person writes. Add the pseudo-locale
build as a separate blocking gate wherever a second locale is shipped
or planned, because it catches a different defect class and passing one
says nothing about the other. Reach for C only on procedures where a
misread step causes harm. Never adopt D. Run E before any public claim
that new copy is clearer than the old copy, and not otherwise.

Only one prose linter exists in a repository. A second one disagrees
with the first, and the team learns to ignore both.

## Default

B, plus the pseudo-locale gate where it applies, plus human review.
Readability reported if anyone wants it, blocking nothing.

## Worked rulings

- **This repository (2026-08, inherited)**: check E004 is the house
  linter, failing on em-dashes and warning on exclamation marks and
  cliches. It enforces PACK.md B8 mechanically and nothing else, and it
  is the only prose check here.
- **Worked example (2026-08, argued)**: B over a string file, with the
  injected wrong term failing the step, in
  `packs/writing-content/exemplars/EX-WRIT-001-order-panel-second-locale.md`.
- **Checks (2026-08, inherited)**: what is executable today against
  what needs a person is split in
  `packs/writing-content/CHECKS.md`.
