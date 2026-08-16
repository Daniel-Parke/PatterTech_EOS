---
summary: The metadata axes, canonical knowledge shapes, compatibility rules and current enforcement
type: kernel
tags: [eos]
---

# METADATA_SPEC

Front-matter answers two different questions. `type` tells the repository how
to classify and check a file. `kind` declares the semantic artefact where the
file carries knowledge metadata. They are deliberately separate, but the core
knowledge classes use the same value for both.

Every Markdown file with front-matter carries `summary`, `type` and `tags`.
Specialised schemas may require more. `kernel/NAMING_SPEC.md` owns terminology,
identifiers and file naming.

## The nine knowledge axes

- **kind**: `doctrine | wargame | recipe | example | stack-profile | fact |
  record`, plus `rule` and `guide` for genuine non-Wargame instructional
  material retained by the current schema.
- **authority**: `binding | default | advisory | preference | none`.
- **lifecycle**: `draft | experimental | active | contested | superseded |
  archived`.
- **basis**: `decision | law | standard | empirical-evidence |
  local-observation`.
- **evidence_grade**: `controlled | observational | anecdotal | asserted |
  not-applicable`.
- **scope**: `estate | venture | eos-internal | brand:<name>`, accompanied by
  `applies_when` where applicability changes what an agent should do.
- **volatility**: `stable | slow | fast | event-driven`.
- **review**: `YYYY-MM`, `on-change-of:<source>` or `none`. `none` is valid
  only for records and archived items.
- **conflicts_with**: resolvable references to the knowledge this artefact
  contradicts. Absence claims nothing.

ADR-0008 described eight axes before `conflicts_with` was added. The two counts
refer to different versions of the same contract.

## Canonical record shapes

| Artefact | Required identity shape |
| --- | --- |
| Pack entry | `kind: record`, `type: pack`, `display_name`, `category`, `id_namespace` |
| Pack checks | `kind: record`, `type: checks` |
| Worked example | `kind: example`, `type: example` |
| Doctrine | `kind: doctrine`, `type: doctrine`, `DOC-*` identity |
| Wargame | `kind: wargame`, `type: wargame`, `WG-*` identity |

Each `PACK.md` also declares activation and applicability as required by
`packs/PACK_CONTRACT.md`. A worked example may state `scope`; its authority is
none and its evidence grade is not applicable unless the file explicitly
claims something more.

Atomic Doctrine requires:

- `id`, `statement`, `summary`, `kind`, `type`;
- `authority`, `basis`, `evidence_grade`, `scope` and `lifecycle`;
- non-empty `applies_when`, `challenge_triggers`, `sources` and
  `verification_refs`;
- `review`.

A Wargame requires:

- `id`, `summary`, `kind`, `type` and at least one `scenario_modes` value;
- `applicable_doctrines` or `gap_domain`;
- `applies_when`, `engages_when`, `consequence` and `relations`;
- non-empty `sources`, plus `review` and `lifecycle`.

The Wargame body carries the decision question and stakes, the Doctrine or gap
under pressure, engagement conditions, materially different options and their
premortems, the decision rule, safe default or reason none is safe, cheapest
discriminating test, fallback, exit and revisit conditions, counter-evidence
and transfer limits. A venture outcome belongs in a separate `RUL-*` record.

## Minima for other knowledge kinds

These are the current minima beyond the universal `summary`, `type` and
`tags`. A specialised schema may require more.

| Kind | Required fields |
| --- | --- |
| `record` | none |
| `example` | none |
| `recipe` | `sources` |
| `fact` | `sources`, `review` |
| `stack-profile` | `sources`, `review` |
| `guide` | `authority`, `sources`, `review` |
| `rule` | `authority`, `applies_when`, `sources`, `review` |

Here `guide` means a genuine instructional document, not a decision procedure.
Every decision procedure is a Wargame and follows the Wargame schema.
A mutation-testing recipe, for example, cites the source that supports it such
as EV-0019 without acquiring Doctrine authority.

## Derived defaults

Where a field is not required and is absent, it derives as follows:

| Kind | Derived value |
| --- | --- |
| any | `scope: estate`, `lifecycle: active`, `volatility: slow` |
| `record` | `authority: none`, `evidence_grade: not-applicable`, `review: none` |
| `example` | `authority: none`, `evidence_grade: not-applicable` |
| `recipe` | `authority: advisory` |
| `fact`, `stack-profile` | `authority: default` |
| `guide`, `rule` | `basis: decision`, `evidence_grade: asserted` |

An explicit value may depart from a default and then owns keeping that claim
true. Restating a derived value without adding meaning is metadata ceremony.
An absent `review` says nothing; `review: none` asserts that no review is due.

`review_cohort` names a joint scheduled review for files admitted from one
evidence packet. It is valid only with the same `YYYY-MM` review date on at
least two files. It does not replace source-specific freshness in the evidence
ledger.

## Compatibility rules

- Binding Doctrine prevents a serious or hard-to-reverse failure and rests on
  law, a standard, empirical evidence or a protected-set floor. Decision-only
  or asserted-only material cannot bind without an accepted ADR explicitly
  carrying the exception.
- Binding also requires named sources and applicability predicates. A Wargame
  or ordinary Ruling cannot waive it; contrary evidence opens Doctrine review
  or an ADR.
- The binding safety floors in Security, Privacy and Safety and in Reliability
  Engineering and Operations retain their protected-set status.
- `basis: law` or `basis: standard` requires a versioned source and a dated or
  on-change review trigger. A WCAG-based proposition cites the applicable
  versioned standard record, such as EV-0027. Vote counts do not amend it.
- `basis: empirical-evidence` requires controlled or observational evidence
  and evidence-ledger sources.
- `evidence_grade: not-applicable` is valid only with `basis: decision` or
  `kind: record`.
- `lifecycle: superseded` requires `superseded_by`, and the successor names
  what it supersedes.
- `lifecycle: contested` names an overlapping argued Ruling and includes a
  short reason the challenge might generalise.
- `scope: brand:<name>` caps authority at preference. A house style activates
  only when the venture adopts it.
- A declared conflict records one of `stricter-applies`,
  `scoped-differently`, `superseded` or `operator-ruling`. An operator
  resolution also records what was ruled.

## Enforcement

The checker deliberately has layers:

- E002 checks universal front-matter and the type-driven `status` and `review`
  requirements.
- S001 checks declared axis enums; S002 checks bidirectional supersession.
- S006 checks the canonical pack, checks and example shapes, the pack naming
  fields and collection layout.
- S022 validates Doctrine, Wargame, Relation and Ruling records against their
  schemas, resolves their references and checks decision-only binding.
- F001 checks review syntax and expiry; F003 validates review cohorts.

Not every compatibility rule is mechanically proved. Where no check exists,
the author and reviewer still own the rule. Front-matter parse failures are
findings rather than silent skips.
