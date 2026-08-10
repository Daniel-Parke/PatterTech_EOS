---
summary: The v2 seed compiler's rules, prune, fill, policy fill, distil, report, and the never-list
type: kernel
tags: [eos]
---

# COMPILE

The rules the Session 0 compiler follows at phase D of
inception/INCEPTION.md. The compiler is a slot-filler and a pruner and
never an author. Every output traces to a template plus rulings through
the compile report, and `python -m tools.eos check --seed` is the
mechanical judge of the result.

## Inputs, all of them

The ruled lock-book (scale, stack, packs adopted, add-ons, rulings);
the venture brief content from the interview; the risk-surface map from
phase B; kernel/SCALE_MATRIX.md at the pinned EOS commit; and the
templates and schemas that matrix names, at the same commit.

No other source exists. If a slot has no answer in these inputs, the
compiler stops and asks the operator; it never invents one.

## Prune

For each file the matrix requires at the ruled scale, take its template
and remove every fenced block whose scale list does not include the
ruled scale. A fence opens with a scale marker comment and closes with
the end marker, and wraps whole sentences, bullets or sections. The
fence lines themselves go in the same pass, for the kept blocks as well
as the removed ones. The v2 scales are S and ORG, so a leftover M or L
fence is a template defect: stop and file it in the venture's feedback
file before continuing.

## Fill

Replace every slot marker with content from the inputs, in the voice
the templates already carry. Count the fills per file for the report.
Filling is transcription and condensation of the operator's words and
the rulings, never composition. After filling, the file must contain no
slot syntax anywhere, including inside code spans.

One slot needs its source naming, because it comes from the interview's
risk-surface set rather than its venture set.

- Fill `{{WORKSTREAMS}}` in docs/VENTURE_BRIEF.md from interview
  question 18, the operator's own list of material workstreams, one
  line each, three to eight lines being the usual shape. It is
  transcription like every other fill. If question 18 went unanswered
  the compiler stops and asks, as it does for any empty slot:
  inception/GENESIS.md cuts its research packets and work packages from
  that list, so a brief without it blocks Genesis later rather than
  now.

## Policy fill

The policy file compiles like any other file and is then validated
against kernel/schemas/policy.schema.json, so it gets three extra
rules.

- Fill the path lists from the risk-surface map: reversible, sensitive
  and protected, in the venture's own paths. The factor table, the
  express thresholds, the mode dials, the decision budget and the
  approvals block carry no slots and ship exactly as the template holds
  them. The approvals block is protected content.
- Fill the guard block honestly. Name the adapter and the mapping path.
  Leave validated false until a bypass-suite validation report is
  committed in the venture, which means every guarded class is
  manual-only and the operator acts. A seed claiming autonomous
  guarded actions without a shipped mapping fails at D008.
- Delete the template's `_slots` key once the fills are done. It is a
  note to the compiler and the schema refuses it. The report's ancestry
  row counts the real slots and says so.

## Front-matter rewrite

Compiled files drop template and extracted_from, gain compiled_from
naming the template path, and keep a summary, type and tags that read
true for the venture. The lock-book header carries the machine pins:
eos_root, eos_version, eos_commit, scale, stack, policy_profile,
packs_adopted, addons, compiled and the rulings rows.

## Deferrals

One sanctioned deferral exists. A design-system slot with no truthful
value before a first build fills as `set at first build` plus where it
gets ruled. Deferrals count as fills and are listed beneath the
report's ancestry table, and the first-build lock-in replaces them all
in one sitting.

A deferral without a scheduled lock-in is a broken promise, so the
compile writes the task in the same pass: a row in docs/TASKS.md at S,
or a record under org/tasks/ at ORG, naming the first-build lock-in.
Check D004 enforces it, and the first two v2 seeds failed exactly this
before the rule was written down.

## Genesis forms

Five templates land in a seed as blank forms. The venture fills them
later, in its own repo, during the Genesis phase.

Which scales carry which file is the matrix's call, as for every other
seed file. All five belong at both: none of them costs anything to ship
blank, and a venture rescaling from S to ORG should not discover that it
never had a work package form.

| compiled file | template |
| --- | --- |
| docs/PRODUCT_MAP.md | kernel/templates/PRODUCT_MAP.tpl.md |
| docs/ACCEPTANCE_SPINE.md | kernel/templates/ACCEPTANCE_SPINE.tpl.md |
| docs/genesis/WORK_PACKAGE.md | kernel/templates/WORK_PACKAGE.tpl.md |
| docs/genesis/RESEARCH_PACKET.md | kernel/templates/RESEARCH_PACKET.tpl.md |
| docs/genesis/LENS.md | kernel/templates/LENS.tpl.md |

The map and the spine are one per venture and are filled in place. The
other three are copied per instance, to docs/packages/WP-NN.md,
docs/research/RP-NN.md and docs/lenses/LENS-NNNN.md, by the venture and
never by the compiler.

They compile like any other file, with three things worth saying out
loud.

- Pruning carries the whole scale grading. At S the map loses its
  container view and its hub-file paragraph and takes the lock-book
  variant of its cross-cutting decisions table; the work package loses
  the integrator-reserved hub files and the wide-run justification; the
  research packet loses the conflict pass; the spine loses the mutation
  check and keeps its independence record, which is a floor at both
  scales. The lens contract carries no fences at all, because none of
  its parts gets cheaper at S.
- Filling touches identity only. The map and the spine carry
  `{{VENTURE_NAME}}` and nothing else; the other three carry no slot at
  all. So the ordinary fill leaves nothing behind. A section prompt is
  prose, not a slot, and it stays.
- A blank form is a correct result. It is not a deferral, it carries no
  `set at first build` marker and it needs no queue item, so D004 has
  nothing to say about it. Running Genesis is the operator's launch
  decision; a venture that never runs it carries the blank forms and has
  told no lies.

Each form takes an ancestry row like any other compiled file. A form
shipped blank is not a deviation and does not go in the deviations
table.

## Assemble

Byte-copy the compiled AGENTS.md to CLAUDE.md, last, after every other
edit. Create nothing empty: v2 directories appear with their first
content. Author the trigger add-ons the lock-book names, from the pack
or stack profile the matrix cites, and mark them authored in the
report. That is the one sanctioned authoring, bounded to the add-on
files.

## Distil

For each argued ruling whose guide cites a binding requirement,
condense the venture-facing consequence into the lock-book's contract
sections, where the templates leave room. Distillation quotes or
condenses the cited pack and never adds rules the pack does not hold.
List every distillation in the report with the ruling that pulled it
in. None is a valid answer and the usual one at S.

## Report and gate

Fill docs/COMPILE_REPORT.md from its template: identity, one ancestry
row per compiled file, distillations, deviations. JSON files carry
ancestry rows like any other: the policy and cadence files trace to
their kernel templates with slots filled and no fences, and the claims
file's source is `seeded empty` per its schema. Reseeds of a pre-EOS
repo add two row kinds, normalised for files that gained front-matter
with the content untouched, and preserved for venture content the
compile did not touch.

Then run `python -m tools.eos check --seed <venture path>` from the EOS
repo and paste the summary line with the date. All auto items green
before the human rubric items are judged; the sign-off block closes
Session 0.

## Never

- Never author content outside the recorded add-ons and distillations.
- Never fill a Genesis form's body at compile. Session 0 knows the
  venture, not the product; an invented product map reads as settled,
  and every package cut from it inherits the invention.
- Never renumber, reword or reorder protected template text, which is
  the constitution's Parts II and III, the three role charters and the
  policy's risk and approvals blocks. Pruning their fences is the only
  edit allowed.
- Never leave a fence line, a slot, an unfilled front-matter key or the
  policy template's `_slots` key.
- Never compile from a dirty template tree. The pin is a commit and
  never a branch, because a branch moves and the seed's ancestry stops
  being provable.
- Never fight a seed-check failure forever. The circuit breaker applies:
  once three materially distinct hypotheses about the cause have each
  been tested and falsified and the latest attempt taught nothing new,
  stop, record it in the feedback file and put it to the operator.
