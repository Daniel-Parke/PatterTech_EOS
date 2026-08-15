---
id: GD-DOCS-001
summary: Where a document's truth lives, and therefore whether it can drift at all
kind: wargame
type: wargame
tags: [content, delivery, eos, tooling, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-DOCS-004]
applies_when: [publishes_docs]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: observational
sources: [EV-0023, EV-0095, EV-0102, EV-0136, EV-0189, EV-0322, EV-0323, EV-0330, EV-0332, EV-0333]
review: 2028-04
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-DOCS-001: Where does this document's truth live?

## Decision question and stakes

Something needs writing down. The fork is not how to write it well. It
is where the authoritative version of the fact sits, because that
decides whether the document can go stale without anyone noticing.
Every other documentation question is downstream of this one.

## Doctrines or coverage gap under pressure

- `DOC-DOCS-004` (binding): Generated reference is verified as regenerated, not hand-edited.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Is there a machine-readable artefact that already states the fact?
- Will a reader copy this and run it?
- Is there a consumer outside the team who decides something based on
  it?
- How often does the underlying thing change?
- Who notices first when it is wrong, the author or the reader?

Applicability is `publishes_docs`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Derived from the artefact

The document is generated from a schema, model, interface document or
help text, and regenerating it is the only way to change it (EV-0023,
EV-0102). Buys: it cannot lie about what it describes, and a difference
between the artefact and the document is a build failure rather than a
discovery. Costs: a generator, a pinned version, and a regeneration
check in CI. Also a ceiling, because generated reference explains what
a field is and never why you would use it.

### B. The example is the test

The document contains the example, and the example is executed by the
test run (EV-0330). Buys: the strongest available answer to drift, and
it covers the exact thing readers copy. Costs: a harness, and
escape-hatch markers for the examples that genuinely cannot run.
Ceiling: it proves the snippet runs, never that it is the right snippet
to show, and the prose around it stays unverified.

### C. Curated by a person on a cadence

A human writes it and owns keeping it true, with a review trigger
(EV-0333). Buys: the only form that can state a consequence, a
rationale or a caveat, which is what a consumer deciding whether to
upgrade actually needs. Costs: it drifts by default, and the cost is
paid by the reader rather than the author.

### D. Edited on encounter

Nobody owns it. Whoever went looking and did not find the answer writes
it into the place they looked, in the same change, and substantive
decisions are left in the pull request and issue trail rather than
being copied out (EV-0095). Buys: no documentation backlog, and the
record writes itself. Costs: uneven coverage, and it fails completely
where the reader has no write access.

## Failure premises

### Premortem for A. Derived from the artefact

Assume `A. Derived from the artefact` was selected and the outcome failed. Test this option's stated failure mechanism first: a generator, a pinned version, and a regeneration check in CI. Also a ceiling, because generated reference explains what a field is and never why you would use it.

### Premortem for B. The example is the test

Assume `B. The example is the test` was selected and the outcome failed. Test this option's stated failure mechanism first: a harness, and escape-hatch markers for the examples that genuinely cannot run. Ceiling: it proves the snippet runs, never that it is the right snippet to show, and the prose around it stays unverified.

### Premortem for C. Curated by a person on a cadence

Assume `C. Curated by a person on a cadence` was selected and the outcome failed. Test this option's stated failure mechanism first: it drifts by default, and the cost is paid by the reader rather than the author.

### Premortem for D. Edited on encounter

Assume `D. Edited on encounter` was selected and the outcome failed. Test this option's stated failure mechanism first: uneven coverage, and it fails completely where the reader has no write access.

## Decision rule

- A machine-readable source of truth exists: **A**. Do not hand-write
  what a generator can derive, and do not accept a code comment as a
  substitute for derivation.
- A reader will copy it and run it: **B**, on top of A or C. This is
  additive, not an alternative.
- An outside consumer decides something from it, such as whether to
  upgrade: **C**, and only C. Generation cannot state a consequence.
- Internal knowledge, no outside consumer, high change rate: **D**.
- Nothing fits and it still needs writing: **C** with an explicit
  review trigger, and accept that it will drift.

## Safe default

A where a machine-readable source exists, B for anything copyable, D
for internal knowledge, C reserved for what a consumer needs in order
to decide. Most repositories need three of the four at once, applied
per document rather than per repository.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Is there a machine-readable artefact that already states the fact?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A where a machine-readable source exists, B for anything copyable, D for internal knowledge, C reserved for what a consumer needs in order to decide. Most repositories need three of the four at once, applied per document rather than per repository.

**Exit condition:** Stop or roll back the selected branch when a generator, a pinned version, and a regeneration check in CI. Also a ceiling, because generated reference explains what a field is and never why you would use it, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Is there a machine-readable artefact that already states the fact?

## Counter-evidence and transfer limits

### Evidence boundary

Options A and B are supported by working toolchains and one large
worked deployment (EV-0330, EV-0332, EV-0102, EV-0136, EV-0189), which
is existence proof rather than comparative evidence. Nothing in this
set compares the four approaches against each other on any outcome.
Option D rests on a single company handbook (EV-0095). Anyone claiming
a measured winner here is asserting.
### Preserved reasoning: Where the four forms fit

The tutorial, how-to, reference and explanation split (EV-0322) is a
diagnostic that runs after this fork, not before it. Its useful claim
is that mixing forms inside one page is what makes a page unusable. It
is one practitioner's model with no research base (EV-0323), so use it
to work out why a page is confusing and do not create empty folders in
its shape. Reference is usually option A or B. Explanation is always C.
Tutorials are C with B underneath them, because a tutorial that does
not run is worse than no tutorial.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
