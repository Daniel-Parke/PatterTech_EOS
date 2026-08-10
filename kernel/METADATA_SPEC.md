---
summary: The eight metadata axes, per-kind required minima, derived defaults and compatibility rules
type: kernel
tags: [eos]
---

# METADATA_SPEC

Knowledge metadata is eight orthogonal axes. Required metadata varies
by kind; everything else derives. The checker enforces enums, axis
compatibility and derivation, so a simple recipe never carries
hand-written provenance scaffolding.

## The eight axes

- **kind**: `rule | guide | recipe | exemplar | stack-profile | fact |
  record`. What the artefact is.
- **authority**: `binding | default | advisory | preference | none`.
  How strongly it binds. Binding must be earned, see compatibility
  below.
- **lifecycle**: `draft | experimental | active | contested |
  superseded | archived`. Where it is in its life. Experimental items
  carry an expiry of at most ninety days and a hypothesis in the body.
- **basis**: `decision | law | standard | empirical-evidence |
  local-observation`. Why it exists.
- **evidence_grade**: `controlled | observational | anecdotal |
  asserted | not-applicable`. How good the support is.
- **scope**: `estate | venture | eos-internal | brand:<name>`, plus
  explicit `applies_when:` predicates stating when it activates (for
  example `applies_when: [has_web_ui]`).
- **volatility**: `stable | slow | fast | event-driven`. How often the
  ground truth moves.
- **review**: a `YYYY-MM` date, `on-change-of:<source>`, or `none`.
  `none` is legal only for records and archived items. A rule based on
  law or standard must carry a versioned source plus either an
  on-change-of trigger or a scheduled date.

## Required minima by kind

Only these fields are hand-written. The rest derive.

| Kind | Required fields |
| --- | --- |
| record | summary, kind, scope |
| exemplar | summary, kind, scope |
| recipe | summary, kind, scope, sources |
| fact | summary, kind, scope, sources, volatility, review |
| stack-profile | summary, kind, scope, sources, volatility, review |
| guide | summary, kind, scope, authority, basis, evidence_grade, sources, review |
| rule | all eight axes, sources, applies_when |

Guides additionally mark rulings inline: venture, date, and whether the
ruling was argued or inherited, using canonical venture names.

## Derived defaults

Where a field is not required for a kind, the checker derives it and
flags a hand-written copy as scaffolding:

| Kind | Derived defaults |
| --- | --- |
| record | authority none, lifecycle active, evidence_grade not-applicable, review none |
| exemplar | authority none, lifecycle active, evidence_grade not-applicable, review a date |
| recipe | authority advisory, volatility slow |
| fact, stack-profile | authority default unless stated |
| guide | volatility slow unless stated |

Defaults are exactly that: a file may state a field explicitly to
depart from the default, and then owns keeping it true.

## Axis compatibility rules

The axes are orthogonal, and not every combination is legal:

- `authority: binding` requires `basis` in decision, law, standard or
  empirical-evidence. Asserted-only material can never bind. Binding
  also requires named sources and `applies_when` predicates; a binding
  rule with no activation condition is a finding.
- `basis: law` or `basis: standard` requires a versioned source and a
  review trigger (on-change-of or a date). Such rules are immune to
  vote counts; they change only via an ADR citing the changed
  source.
- `basis: empirical-evidence` requires `evidence_grade` controlled or
  observational, and the sources must be evidence-ledger rows.
- `evidence_grade: not-applicable` is legal only where basis is
  decision, or kind is record.
- `lifecycle: superseded` requires a `superseded_by` reference, and
  supersession is bidirectional: the successor names what it replaces.
- `lifecycle: contested` marks an estate default challenged by a newer
  argued venture ruling with overlapping applicability; the marker
  carries a one-line generalisability note.
- `scope: brand:<name>` caps authority at preference. House style
  activates by venture adoption, never by default.

## Worked examples

A recipe carries these four axes, beside the summary, type and tags
E002 asks of every markdown file:

```yaml
---
summary: Add an incremental mutation run to a JS package
kind: recipe
scope: estate
sources: [EV-0019]
---
```

Authority advisory and volatility slow derive, so a recipe leaves them
out. No check catches a hand-written copy yet.

A binding rule carries the full set, because binding is the most
expensive claim the system makes:

```yaml
---
summary: Applicable web interfaces meet WCAG 2.2 AA
kind: rule
authority: binding
lifecycle: active
basis: standard
evidence_grade: observational
scope: estate
applies_when: [has_web_ui]
volatility: slow
review: on-change-of:WCAG-2.2
sources: [EV-0027]
---
```

Writing evidence_grade not-applicable there breaks the rule above:
that grade is legal only where basis is decision or kind is record. No
check catches the pair yet, so it is a reader's job.

## Enforcement

The checker enforces the enums (S001), supersession bidirectionality
(S002) and the review axis, including that review: none is legal only
for records and archived items (F001). The per-kind minima, the
derivation rule and the rest of the compatibility table are law here
and not yet checked, so a hand-written derived default costs nothing
today. Metadata beyond the minima on a kind that derives it is still a
defect, because manually authored metadata is ceremony and ceremony
carries a budget. The front-matter
parser is hardened: unterminated blocks, bad key charsets and
malformed lists are findings, never silent skips.
