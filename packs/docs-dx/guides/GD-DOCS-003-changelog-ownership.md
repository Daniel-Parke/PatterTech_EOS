---
summary: Who writes the changelog, and whether release notes can be derived from history at all
type: guide
tags: [content, delivery, ci]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0136, EV-0170, EV-0171, EV-0333]
review: on-change-of:keep-a-changelog-beyond-1.1.0
---

# GD-DOCS-003: Who writes the changelog?

## The question

A release goes out. Someone downstream has to decide whether to take
it. The fork is whether that decision is served by an artefact a person
wrote or by one the tooling derived, and the two sources of record
disagree with each other in plain terms.

## It depends on

- Does anyone outside the venture pin a version of this?
- Is there a commit grammar enforced at write time, or is the history
  free-form?
- Who authors most commits, and can they be relied on to describe
  consequence rather than change?
- Is there a machine-readable interface whose compatibility can be
  diffed instead?

## Options

### A. Curated, human-written

One entry per version, newest first, dated, grouped into added,
changed, deprecated, removed, fixed and security, with a running
Unreleased section so cutting a release is a rename rather than an
archaeology exercise, and deprecations announced before removal
(EV-0333). Buys: entries that state a consequence, which is the only
thing that answers "should I upgrade". Costs: discipline on every
change, and it is the first thing dropped under pressure.

### B. Derived from commit history

A grammar constrains commit subjects, and the changelog, the version
bump and the release trigger all fall out of it (EV-0170, EV-0171).
Buys: it cannot be forgotten, and it scales to machine authors who will
not remember a separate file. Costs: it describes changes rather than
consequences, and it inherits whatever noise the grammar failed to
exclude.

### C. Derived draft, curated before release

Tooling produces the entry list from history, and a person edits it
into consequences before the release goes out. Buys: nothing is
missed and the published text is still addressed to a reader. Costs: a
step in the release path that a person has to actually perform.

### D. No prose changelog, machine-readable compatibility diff only

The consumer-facing artefact is a diff of the interface contract,
classified into breaking and non-breaking (EV-0136). Buys: precision,
and it cannot be wrong about the interface. Costs: it says nothing
about behaviour that is not in the schema, and nothing about why.

## Decision rule

- Anything outside the venture pins a version: **C**, and keep the
  Unreleased section running continuously so the derived draft has
  somewhere to land.
- Machine authors write most commits and a grammar is enforced at merge:
  **B** is acceptable as the draft stage of C, never as the published
  artefact.
- No commit grammar and no enforcement: **A**. A derivation from
  free-form history produces noise, which is precisely what the
  specification warns against (EV-0333).
- Internal service, consumers are two other services in the same
  estate: **D**, plus a one-line note for anything not visible in the
  schema.

## Default

C. The reconciliation between the two sources of record is that
constraining the input at write time stops the derivation being noise,
and a person still has to turn a list of changes into a list of
consequences. The Unreleased section is the part that carries most of
the value, because it makes the record a by-product of the change
rather than a task at release time.

## The disagreement, stated plainly

The changelog specification says generating from commit diffs fails,
because a log is full of merges and internal churn no consumer can act
on (EV-0333). The commit grammar exists to make exactly that generation
work (EV-0170). Both are maintained standards, both are widely
followed, and they cannot both be the default. This guide takes the
position that they are describing different artefacts: derived notes
describe changes, curated notes describe consequences, and the second
is what the consumer asked for. Anyone who prefers B as published
output should record that as a lock-book override with the reason,
because it is a defensible position and not the one this pack takes.

## Evidence boundary

EV-0333 is a specification, static since 2019, written for libraries
with external consumers, and it does not address monorepos, per-package
changesets or machine-authored entries. EV-0170 and EV-0171 are
specifications rather than studies. Nothing here measures whether
either form helps a consumer decide anything, and no source in this set
compares them.

## Worked rulings

- **PatterTech EOS docs-dx pack (2026-08, argued)**: C as the default,
  D for internal services with a schema. Argued from EV-0333 read
  against EV-0170, with the disagreement recorded rather than resolved.
- **PatterTech EOS itself (2026-08, inherited)**: A, with a running
  Unreleased section in the root `CHANGELOG.md`, because the repository
  has no enforced commit grammar. Inherited from the release playbook.
