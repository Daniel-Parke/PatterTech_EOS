---
summary: Research synthesis for the docs-dx pack, four documentation philosophies, what is checkable, and what should bind
type: example
tags: [eos, testing]
---

# Docs and DX pack research notes

Cutoff 2026-08-03. Sixteen new sources in `sources.fragment.json`, plus
existing ledger records cited by EV id. The domain question is not "how
do we write good docs". It is: which documentation survives contact
with a codebase that changes faster than anyone reads, and which of it
can be made to fail a build rather than rot quietly.

## Four philosophies, and when each fits

These differ on one axis: where the truth lives. That is what decides
whether documentation can drift at all.

**1. Curate by reader intent (Diataxis).** FRAG-DOCS-DX-01 splits
documentation on two axes, action versus cognition and study versus
work, giving tutorial, how-to, reference, explanation. The load-bearing
claim is not the four boxes. It is that mixing forms inside one page is
the dominant failure, because a reader in work mode cannot use a page
that keeps stopping to teach. Fits: anything read by someone outside
the team, and any page that has grown confusing without anyone being
able to say why. Use it as a diagnostic on an existing page, not as a
folder layout imposed up front. Anti-pattern: four empty directories
created on day one, then a tutorial nobody wrote and a how-to that is
really reference. Evidence is thin, and the framework's own admirers
say so (FRAG-DOCS-DX-02): no study supports the four-way split, it is
one practitioner's model that turned out useful.

**2. Generate it, never write it.** The reference is derived from the
thing itself, so it cannot lie. Already well covered in the ledger:
EV-0023 (OpenAPI as the machine-readable interface contract), EV-0102
(models as code, views regenerated and never hand-edited), EV-0136
(breaking changes detected against the spec), EV-0189 (the schema is
already a property specification, so conformance is testable). New here
is FRAG-DOCS-DX-11, where GitLab makes it a blocking check that a
generated GraphQL reference was regenerated rather than hand-edited.
Fits: API reference, configuration reference, CLI help, schema docs,
anything with a machine-readable source of truth. Anti-pattern:
annotations in code comments treated as generation. Proximity is not
accuracy; a docstring above a function can be wholly wrong about it,
and nothing fails.

**3. Make the example the test.** FRAG-DOCS-DX-09 is the strongest
answer to drift the domain has: every fenced example in a Rust doc
comment is compiled and run, and the design detail that makes it
tolerable is the escape hatches. Hidden setup lines keep the printed
example minimal while it still compiles, and `no_run`, `ignore`,
`should_panic` and `compile_fail` force an unexecutable example to
declare why. The absence of that declaration is itself the check. Fits:
any snippet a reader will copy. Anti-pattern: a README full of shell
blocks nobody has run since the flag was renamed. Limit: a doctest
proves the snippet compiles and does not panic, never that it is the
right snippet to show, and the prose around it stays unverified.

**4. Edit on encounter.** EV-0095: a missing answer is immediately PRed
into the place you looked for it, and substantive decisions live in PRs
and issues so the record writes itself. Fits: internal knowledge with
no external consumer, small teams, high change rate. Anti-pattern: a
documentation backlog. Work that is never scheduled is not a plan.

## What the evidence actually supports

Honest ranking, strongest first.

**Error messages are the most-read documentation you own.**
FRAG-DOCS-DX-06 is a controlled eye-tracking study: developers do read
compiler errors, spend 13 to 25 per cent of task time doing it, find
them about as hard to read as source code, and reading difficulty
significantly predicts time-to-fix. That is a measured effect on the
critical path of every failure. FRAG-DOCS-DX-07 turns it into rules a
repository can apply: one general primary message, the offending span,
detail behind an explicit `--explain` rather than inline, lower case,
no trailing punctuation, identifiers in backticks. The most transferable
idea is that every suggestion carries a declared confidence tier
(machine-applicable, has-placeholders, maybe-incorrect, unspecified),
so a caller can decide whether to auto-apply. That maps straight onto
agent-facing errors, and it pairs with EV-0175: which errors a caller
may react to is an interface decision, so it belongs in the message and
in the declared failure mode, not in a tribal understanding.

**Absence beats style.** FRAG-DOCS-DX-05 surveyed 146 practitioners:
the issues rated both important and frequent are missing installation,
deployment and release instructions (68 per cent), missing user
documentation (65 per cent), missing developer guidelines (60 per
cent). Correctness and completeness dominate prose quality.
FRAG-DOCS-DX-08 agrees from the other side: READMEs cluster on What and
How and systematically omit Why and status, so a reader cannot tell
whether a thing is maintained or what it is for. Both are descriptive,
neither links coverage to an outcome, but they point the same way.

**Documentation quality as a multiplier is plausible and unproven.**
FRAG-DOCS-DX-03 is the headline claim in the field: teams with
above-average documentation get large lifts from adopting other
capabilities, teams below average get small ones. It is cross-sectional
self-report, documentation quality and capability adoption come from
the same respondent, and the page states no causal caveat of its own.
The reported lift percentages are large enough to warrant suspicion of
the modelling. Mature teams plausibly write better docs because they
are mature. Treat the direction as a working hypothesis; do not quote
the numbers.

**Onboarding time is thin.** This was in the brief and the evidence is
not there. FRAG-DOCS-DX-16 does not carry onboarding time as a headline
measure at all, and its most useful contribution is a caution against
its own genre: throughput measures are signal only when counterbalanced,
never made a target, never tied to reward. There is no controlled study
in this set linking documentation to time-to-first-commit. That is an
open question, not a gap to fill with a confident number.

## Disagreements worth recording

**Who curates the changelog.** FRAG-DOCS-DX-12 states flatly that
generating a changelog from commit diffs fails, because the log is full
of merges and internal churn no consumer can act on, and prescribes a
curated human artefact with a six-way vocabulary and a running
Unreleased section. EV-0170 does the opposite: constrain commit
subjects at write time so the changelog, version bump and release
trigger become derivations. This is load-bearing, not cosmetic, and
both cannot be default. The reconciliation is that Conventional Commits
constrains the input so the derivation is not noise, but the residual
disagreement is real: derived changelogs describe changes, curated ones
describe consequences, and only the second is what a consumer needs to
decide whether to upgrade.

**Style enforcement versus coverage.** FRAG-DOCS-DX-13 and
FRAG-DOCS-DX-14 make prose style executable, and GitLab makes it
blocking. FRAG-DOCS-DX-05 says practitioners rank missing content far
above style. A linter that consumes the attention which would have
written the missing runbook is a net loss. Vale catches banned terms
and heading case; it cannot tell you a page is wrong.

**Does architecture still matter when a model is the reader.**
FRAG-DOCS-DX-02 raises it and does not settle it. FRAG-DOCS-DX-15 is
the counterweight: AGENTS.md fixes location and deliberately fixes
nothing else, no schema, no required sections, and that is why vendors
who agree on nothing else adopted it. Predictable placement was the
scarce thing. But adoption counts measure file existence, not accuracy,
and there is no conformance test, so "we have an AGENTS.md" says
nothing. This repository's own CLAUDE.md is byte-identical to
AGENTS.md, which is that bet already taken.

## Binding, default, preference

**Binding.** Internal links and anchors resolve, checked in CI
(FRAG-DOCS-DX-10 gives distinct exit codes so a broken checker is
distinguishable from a broken link; anchors matter most because
internal cross-references break silently on a heading rename). A
deleted or renamed page leaves a redirect or the reference is updated
(FRAG-DOCS-DX-11). Generated reference is verified as regenerated, not
hand-edited (FRAG-DOCS-DX-11, EV-0102). Every executable snippet is
either run in CI or carries an explicit declaration of why it is not
(FRAG-DOCS-DX-09). Every user-visible failure names the condition, the
caller-relevant error identity and what to do (FRAG-DOCS-DX-06,
FRAG-DOCS-DX-07, EV-0175). Every repository has an agent entry file at
the conventional path (FRAG-DOCS-DX-15).

**Default.** Diataxis as a diagnostic applied to any page that has
become confusing, not as an imposed tree (FRAG-DOCS-DX-01). A README
that answers What, Why, How and current status (FRAG-DOCS-DX-08). A
curated changelog with a running Unreleased section, generated only
where the commit grammar is enforced (FRAG-DOCS-DX-12, EV-0170,
EV-0171). Error suggestions carrying a declared confidence tier
(FRAG-DOCS-DX-07). External link checking advisory rather than
blocking, because rate limits buy false failures.

**Preference.** House prose rules beyond the small mechanical subset
(FRAG-DOCS-DX-13). Which static site generator. Whether explanation
lives beside reference or apart. Vale rule severities, and whether a
rule is ever promoted from suggestion to error.

## Open questions

- No controlled evidence here links documentation to onboarding time.
  If the estate wants that measure it has to instrument it locally, and
  the DX caution applies: measure it, never target it.
- Nothing in this set tests whether documentation written for a human
  reader also serves an agent reader, or whether the two want different
  artefacts. Diataxis, README taxonomy and AGENTS.md are three
  different answers and none of them is evidenced.
- Vale exit-code and severity behaviour was not verifiable from the
  repository landing page and must be confirmed against the current
  release before any prose rule is made blocking.
