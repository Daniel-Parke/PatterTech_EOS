---
summary: The nine metadata axes, per-kind required minima, derived defaults and compatibility rules
type: kernel
tags: [eos]
---

# METADATA_SPEC

Knowledge metadata is nine axes. Eight are orthogonal classifications;
the ninth, `conflicts_with`, is a link to what the artefact
contradicts. Required metadata varies by kind; everything else derives,
so a simple recipe never carries hand-written provenance scaffolding.
The checker enforces the enums and the review axis. The minima, the
derivation and the compatibility rules are law here and mostly
unchecked, and Enforcement at the foot says which is which.

ADR-0008 counts eight axes where this file counts nine. It was written
before ADR-0006 added `conflicts_with`, so the two records count the
same set at two moments rather than disagreeing.

## The nine axes

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
- **conflicts_with**: what this artefact contradicts, written as
  references a reader can follow: a pack requirement id, a guide id, a
  lesson id, a policy pointer. Optional everywhere, and absent claims
  nothing. Naming a conflict obliges settling it, with one of
  `stricter-applies`, `scoped-differently`, `superseded` or
  `operator-ruling`; an operator ruling also records what was ruled,
  because a row that says the operator decided without saying what cannot be
  reviewed and cannot be argued with later. The row shape for lessons
  is fixed by `kernel/schemas/lesson.schema.json`. What is checked and
  what is not is under Enforcement.

## Required minima by kind

ADR-0008 decision 7 set the shape. Required everywhere: `summary`,
`type` and `tags`, which E002 asks of every markdown file in the tree.
Required where they change what an agent does: `authority`,
`applies_when`, `sources` and `review`. The rest of the axes are
optional and derive.

`kind` is not a minimum in that sense. It is the discriminator that
picks the row below, and it is what switches the axis checks on. A file
carrying no `kind` carries no knowledge metadata, and E002 plus the
shape of whatever `review` it does carry is all that governs it.

| Kind | Required, beyond summary, type and tags |
| --- | --- |
| record | nothing further |
| exemplar | nothing further |
| recipe | sources |
| fact | sources, review |
| stack-profile | sources, review |
| guide | authority, sources, review |
| rule | authority, applies_when, sources, review |

Why the four sit where they do. `authority` is on the two kinds that
tell an agent what to do, because a guide or a rule whose strength has
to be guessed is worse than one that says nothing. `applies_when` is on
rules alone: a rule with no activation condition fires everywhere,
which is how a house preference ends up governing a venture that never
adopted it. `sources` is on everything claiming something outside
itself, which is everything bar a record of what happened and a worked
example of our own. `review` is on the kinds whose ground truth moves
underneath them.

Guides additionally mark rulings inline: venture, date, and whether the
ruling was argued or inherited, using canonical venture names.

Do not read that table as enforcement. It is law here and mostly
unchecked; Enforcement at the foot says which columns a check reads and
which are a reader's job.

`status` is a file-type requirement rather than one of the nine axes,
which is why it is absent above. Dropping it from a wargame or a
decision on the strength of this table fails E002.

## Derived defaults

Where a field is not required for a kind it derives, and a hand-written
copy of the derived value is scaffolding:

| Kind | Derived when absent |
| --- | --- |
| any | scope estate, lifecycle active, volatility slow |
| record | authority none, evidence_grade not-applicable, review none |
| exemplar | authority none, evidence_grade not-applicable |
| recipe | authority advisory |
| fact, stack-profile | authority default |
| guide, rule | basis decision, evidence_grade asserted |

Three of these want a second look. Defaulting `scope` to estate reads a
file as broader than it may be, so anything narrower says so and keeps
saying so: `eos-internal` and `brand:<name>` are always written down.
Defaulting `volatility` to slow claims the ground truth sits still, so
a fact or a profile over something that moves says otherwise, and its
review date is the control either way. Defaulting `basis` to decision
and `evidence_grade` to asserted is deliberately the weakest pair on
offer: it cannot carry `authority: binding` under the compatibility
rules below, so binding has to be stated and argued rather than
inherited from a silence.

An absent `review` is not the same as `review: none`. The first says
nothing and no check minds; the second is a claim that the file never
needs looking at again, and F001 allows it only on records and archived
items.

Defaults are exactly that: a file may state a field explicitly to
depart from the default, and then owns keeping it true.

## Axis compatibility rules

The eight classification axes are orthogonal, and not every
combination of them is legal:

- `authority: binding` requires `basis` in law, standard or
  empirical-evidence, and the rule must prevent a concrete failure that
  is serious or hard to reverse. That is ADR-0008's test, and it is now
  this spec's test too: `basis: decision` on its own no longer earns
  binding. The failure it prevents is a house preference written as
  law. A reader cannot argue with one, cannot check it, and ends up
  ignoring the binding list wholesale, which costs the rules that were
  earned. Everything that fails the test is a `default`: do it unless
  you record why not. Asserted-only material can never bind. Binding
  also requires named sources and `applies_when` predicates; a binding
  rule with no activation condition is a defect, and the authority
  audit under ADR-0008 decision 8 is what catches it, not the checker.
- The safety floors are the exception, and they are exempt by where
  they sit rather than by what their `basis` field says.
  `packs/security-privacy` B1 to B6 and the production-safety rules in
  `packs/devops-reliability` stay binding whatever basis they carry,
  because they are protected-set floors: prompt-injection resistance,
  secret protection, production safety and data protection are the
  things the protected set exists to hold, and a floor that can be
  demoted by an audit is not a floor. Nothing outside those two places
  claims the exemption.
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

A recipe carries two axes, beside the summary, type and tags E002 asks
of every markdown file:

```yaml
---
summary: Add an incremental mutation run to a JS package
kind: recipe
sources: [EV-0019]
---
```

Scope estate, authority advisory, lifecycle active and volatility slow
all derive, so a recipe leaves them out. No check catches a
hand-written copy yet.

A binding rule states a good deal more, because binding is the most
expensive claim the system makes:

```yaml
---
summary: Applicable web interfaces meet WCAG 2.2 AA
kind: rule
authority: binding
basis: standard
evidence_grade: observational
applies_when: [has_web_ui]
review: on-change-of:WCAG-2.2
sources: [EV-0027]
---
```

Four of those are the rule minimum: `authority`, `applies_when`,
`sources` and `review`. `basis` and `evidence_grade` are what the
compatibility rules charge for the word binding, since the defaults
they would otherwise take cannot carry it. Lifecycle, scope and
volatility derive and stay out.

Writing evidence_grade not-applicable there breaks the rule above:
that grade is legal only where basis is decision or kind is record. No
check catches the pair yet, so it is a reader's job.

## Enforcement

E002 is the only check that reads required keys, and it reads the
file's `type` rather than its `kind`: `summary`, `type` and `tags` on
every markdown file, `status` on types wargame, decision, stack and
registry, `review` on types wargame, stack, registry and guide. Either
spelling satisfies that last one, `review` or v1's `review_by`.

So the `review` column of the minima table binds only where the file's
type is one of those four, and the two axes part company often:
`packs/coding/refs/ORACLES.md` is a fact typed foundation, and a
`PACK.md` is a rule typed either playbook or guide, so some pack bodies
are asked for a review date and some are not. Nothing anywhere reads
`sources`, `authority` or `applies_when`.

S001 checks the axis enums, and only on files that declare a `kind`.
S002 checks supersession bidirectionality. F001 checks that a stated
`review` is a YYYY-MM month, an on-change-of trigger or `none`, and
that `none` appears only on records and archived items.

`conflicts_with` is read in one place. S018 reads it on the rows of
`registry/lessons.json` and fails a row that names a conflict with no
resolution, a resolution outside the four values, or an operator ruling
with nothing recorded. Nothing reads a file-level `conflicts_with`: a
rule or guide that records one is recording it for the next reader, and
for a check that does not exist yet. Say it anyway. The alternative is
that the contradiction is found by whoever next reads two rules that
disagree, which is late and is somebody else's afternoon.

The binding test is in the same position: no check reads a rule's
`basis` and demotes it, so that work is done by the ADR-0008 authority
audit and by whoever writes the rule. A hand-written derived default
costs nothing today. Restating a field at its derived value is still a
defect, because manually authored metadata is ceremony and ceremony
carries a budget; departing from a default is not a defect, because
that is the file saying something.

The front-matter parser is hardened: unterminated blocks, bad key
charsets and malformed lists are findings, never silent skips.
