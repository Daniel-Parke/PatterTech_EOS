---
id: WG-WRIT-004
summary: How is prose checked before it merges, and which signals are allowed to block?
kind: wargame
type: wargame
tags: [ci, content, eos, tooling, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-WRIT-010, DOC-WRIT-009]
applies_when: [writes_user_facing_text]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: decision
evidence_grade: anecdotal
sources: [EV-0435, EV-0436, EV-0437, EV-0438, EV-0446, EV-0335]
review: 2028-09
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-WRIT-004: How is prose checked before it merges?

## Decision question and stakes

Writing quality is mostly not machine-decidable, and a gate that
pretends otherwise gets ignored or gamed. The fork is how much
automation to run over prose and strings, and which of the resulting
signals is allowed to fail a build. Getting this wrong in either
direction is expensive: no check at all lets terminology drift into
every locale, and the wrong check trains a team to route around the
linter.

## Doctrines or coverage gap under pressure

- `DOC-WRIT-010` (default): No readability formula gates a merge, a release or a review.
- `DOC-WRIT-009` (default): Prose in this repository follows the voice law.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **Whether the strings will be translated.** Terminology drift is
  cheap to fix in one language and expensive in five.
- **How many people write.** One writer needs no linter; six do.
- **Whether the team will honour a failing build.** A gate nobody
  respects is worse than no gate, because it teaches the habit of
  overriding.
- **Whether anyone can test copy on real readers.** That is the only
  check that speaks to comprehension at all.

Applicability is `writes_user_facing_text`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. No automation, review only
A human reads the diff. Buys zero false positives and zero tooling.
Costs consistency the moment there are several writers, and it catches
nothing at three in the morning.

### B. Banned-and-preferred term list in CI, blocking
A short list of terms with one approved spelling each, run over
user-facing strings and documentation, failing the build on a banned
term (EV-0335). Buys the one-word-one-meaning property for the
terms that actually matter, at a cost measured in a few dozen lines of
configuration. Costs list maintenance and the occasional false positive
in a quotation. No study was found showing it improves comprehension or
reduces support load, so it is a cheap bet rather than a proven one.

### C. Full controlled language with a maintained termbase
Approved words, restricted grammar, a real linter enforcing both
(EV-0437). Buys machine-checkable correctness for
safety-critical procedures. Costs a termbase owner, a review process
for new vocabulary, and text that reads as deliberately unidiomatic.
Justified where a misread step injures someone, and almost nowhere
else.

### D. Readability score as a gate
A formula score computed per file with a threshold. Named here to be
excluded. Formulas track measured difficulty only patchily and only at
some bands, because they measure surface proxies that sit downstream of
difficulty (EV-0436). The score improves when sentences
are chopped, whether or not anyone understands more. PACK.md B10
forbids this. Reporting the number is a preference; gating on it is
not available.

### E. Comprehension testing with real readers
An A/B of two renderings of one decision, with comprehension questions
as the outcome (EV-0438,
EV-0434). Buys the only evidence that speaks to
understanding rather than to text features. Costs recruitment, time and
a real sample, and it does not fit in a pull request. It gates nothing.
Its job is to turn a claim about clarity into a fact.

## Failure premises

### Premortem for A. No automation, review only

Assume `A. No automation, review only` was selected and the outcome failed. Test this option's stated failure mechanism first: consistency the moment there are several writers, and it catches nothing at three in the morning.

### Premortem for B. Banned-and-preferred term list in CI, blocking

Assume `B. Banned-and-preferred term list in CI, blocking` was selected and the outcome failed. Test this option's stated failure mechanism first: measured in a few dozen lines of configuration. Costs list maintenance and the occasional false positive in a quotation. No study was found showing it improves comprehension or reduces support load, so it is a cheap bet rather than a proven one.

### Premortem for C. Full controlled language with a maintained termbase

Assume `C. Full controlled language with a maintained termbase` was selected and the outcome failed. Test this option's stated failure mechanism first: a termbase owner, a review process for new vocabulary, and text that reads as deliberately unidiomatic. Justified where a misread step injures someone, and almost nowhere else.

### Premortem for D. Readability score as a gate

Assume `D. Readability score as a gate` was selected and the outcome failed. Test this option's stated failure mechanism first: A formula score computed per file with a threshold. Named here to be excluded. Formulas track measured difficulty only patchily and only at some bands, because they measure surface proxies that sit downstream of difficulty (EV-0436). The score improves when sentences are chopped, whether or not anyone understands more. PACK.md B10 forbids this. Reporting the number is a preference; gating on it is not available.

### Premortem for E. Comprehension testing with real readers

Assume `E. Comprehension testing with real readers` was selected and the outcome failed. Test this option's stated failure mechanism first: recruitment, time and a real sample, and it does not fit in a pull request. It gates nothing. Its job is to turn a claim about clarity into a fact.

## Decision rule

Always run B once more than one person writes. Add the pseudo-locale
build as a separate blocking gate wherever a second locale is shipped
or planned, because it catches a different defect class and passing one
says nothing about the other. Reach for C only on procedures where a
misread step causes harm. Never adopt D. Run E before any public claim
that new copy is clearer than the old copy, and not otherwise.

Only one prose linter exists in a repository. A second one disagrees
with the first, and the team learns to ignore both.

## Safe default

B, plus the pseudo-locale gate where it applies, plus human review.
Readability reported if anyone wants it, blocking nothing.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****Whether the strings will be translated.** Terminology drift is cheap to fix in one language and expensive in five.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** B, plus the pseudo-locale gate where it applies, plus human review. Readability reported if anyone wants it, blocking nothing.

**Exit condition:** Stop or roll back the selected branch when consistency the moment there are several writers, and it catches nothing at three in the morning, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **Whether the strings will be translated.** Terminology drift is cheap to fix in one language and expensive in five.

## Counter-evidence and transfer limits

### Counter-evidence to test

Facts that change the engagement answers above can overturn the safe default. Test ****Whether the strings will be translated.** Terminology drift is cheap to fix in one language and expensive in five.** and ****How many people write.** One writer needs no linter; six do.** against the selected option. A contrary result counts only when it uses the same representative constraints and changes the decision rule, rather than merely preferring another style.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
