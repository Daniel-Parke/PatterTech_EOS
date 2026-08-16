---
summary: The seed compiler's rules, prune, fill and the slot table, policy fill, distil, report, and the never-list
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

The ruled lock-book (scale, stack, packs adopted and add-ons), the
structured Wargame selection log and Rulings in `docs/RULINGS.json`;
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
as the removed ones. The scales are S and ORG, so a fence naming M or L
is a template older than the pin: stop and file it in the venture's
feedback file before continuing.

## Fill

Replace every slot marker with content from the inputs, in the voice
the templates already carry. Count the fills per file for the report.
Filling is transcription and condensation of the operator's words and
the rulings, never composition. After filling, the file must contain no
slot syntax anywhere, including inside code spans.

Every slot the templates hold is in the table below, with what fills
it. A slot marker that is not in the table means a template moved
without this file moving with it: stop and file it in the venture's
feedback file, because a slot nobody has a source for is the slot that
ships unfilled and fails E008. The question numbers below are
inception/INTERVIEW.md's.

| slot | filled from |
| --- | --- |
| VENTURE_NAME | the venture name as it appears in public, taken at the interview's close |
| SCALE, STACK_PROFILE, POLICY_PROFILE, ADDONS | the phase B rulings, as the lock-book header records them |
| EOS_ROOT, EOS_VERSION, EOS_COMMIT | the pinned EOS checkout: its repository name, version and commit |
| COMPILED_DATE, SESSION_ID | the compile itself: today's date, and the compiling session's id |
| N, in the ancestry table | the compiler's own counts, one pair per compiled file |
| OPERATOR, SIGNOFF_DATE | nobody, at compile. The operator fills both when they sign at phase E |
| ONE_PARAGRAPH, ONE_LINE, AUDIENCE | questions 1 and 2 |
| WHY_NOW, AGREEMENTS | question 3 |
| TIME_CONSTRAINTS | questions 3 and 4: the deadline behind it, and how long it should live |
| TRIGGERS | questions 4 to 11, read back as the yes-or-no facts WG-EOS-001 ruled on |
| VENTURE_FACTS | the same interview answers as TRIGGERS and the rest, written as the predicate names kernel/PREDICATES.md gives them, one per line. Only rows that file settles with a question number: a `task` row is about a piece of work and is not knowable at Session 0. Transcription, not inference: a fact goes in because an answer put it there |
| SPEND_RULE | question 8 |
| PEOPLE | questions 8 and 11: who else holds a decision, who approves spend |
| SUCCESS_90 | question 12 |
| OUT_OF_SCOPE | question 13 |
| WORKSTREAMS | question 18, the operator's own list, one line each |
| RESTATEMENT_NOTE, THREE_DEATHS, SMALLER_VERSION_VERDICT | the three challenge steps, in the operator's words |
| REVERSIBLE_PATHS, SENSITIVE_PATHS, PROTECTED_PATHS | the risk-surface map from questions 14 to 16 |
| CAPABILITY_PROFILE_REF | the capability-profile record this policy binds to, seeded at level conservative because a new venture has earned nothing |
| GUARD_MAPPING_REF | the adapter mapping path, from question 17 |
| FEEL, NARRATIVE | condensed from the corrected restatement and question 13, in the operator's register |
| STRUCTURAL_CONTRACTS | what the interview said must not break: question 15, the smaller-version verdict, and the shape the operator insisted on |
| MOTIF, SIGNATURE_PIECES, TOKEN_HOME, TOKEN_MIRROR, STYLEGUIDE_ROUTE, SURFACE_LADDER, ACCENTS, TEXT_TIERS, MEASURE_READING, MEASURE_WIDE, MEASURE_FULL, BLOCK_GAP | nothing yet. Every one takes the deferral below |
| GATE_BUILD, GATE_OVERFLOW, GATE_WEIGHT, GATE_SCREENSHOTS, GATE_SMOKES | the stack profile where it names the exact command, the deferral below where it does not |
| PRODUCT_DOCTRINE (ORG) | the product doctrine the interview and the rulings fix, or `none` |
| ADOPTED_DATE, AMENDMENT_HISTORY (ORG) | the compile date, and `none` until the first amendment |
| UPDATE_FREQUENCY (ORG) | the stakeholder-update rhythm taken at the interview's close |
| FIRST_UPKEEP_DUE, FIRST_RETRO_DUE, FIRST_UPDATE_DUE, FIRST_GUARD_REVIEW_DUE (ORG) | the compile date plus that cadence row's own frequency |

One marker is never filled: the `{{SLOT}}` inside the policy template's
`_slots` note. It sits in a note written to the compiler, and the note
is deleted rather than filled.

`{{WORKSTREAMS}}` is the fill that blocks a later phase rather than
this one. If question 18 went unanswered the compiler stops and asks,
as it does for any empty slot, because a brief with no workstream list
blocks Genesis when it comes rather than now.

A slot the operator cannot answer is a template defect rather than a
harder question. Session 0 knows the venture and not the
product, so a slot wanting a fact from a later phase, or a number
belonging to a run nobody has designed yet, has no truthful fill at
compile. Stop and file it in the venture's feedback file as for a
fence older than the pin. The repair is to the EOS template, because a
compiled file may carry no slot at all and check E008 fails the seed on
every one that survives. Inventing a value is the worst of the three
outcomes: a made-up figure reads as ruled, and nothing in the seed says
that nobody ruled it.

## Policy fill

The policy file compiles like any other file and is then validated
against kernel/schemas/policy.schema.json, so it gets three extra
rules.

- Fill the path lists in the venture's own paths. The factor table, the
  express thresholds, the mode dials, the decision budget and the
  approvals block carry no slots and ship exactly as the template holds
  them. The approvals block is protected content.
- Fill the guard block honestly. Name the adapter and the mapping path.
  Leave validated false until a bypass-suite validation report is
  committed in the venture, which means every guarded class is
  manual-only and the operator acts. A seed claiming autonomous
  guarded actions without a shipped mapping fails at D008.
- Delete the template's `_slots` key once the fills are done. It is a
  note to the compiler and the schema refuses it, so a policy still
  carrying it fails at D007. The report's ancestry row counts the real
  slots and says so.

## Front-matter rewrite

Compiled files drop template and extracted_from, gain compiled_from
naming the template path, and keep a summary, type and tags that read
true for the venture. The lock-book header carries the machine pins:
eos_root, eos_version, eos_commit, scale, stack, policy_profile,
packs_adopted, addons, compiled and `rulings_record`. Wargame selections
and outcomes live in `docs/RULINGS.json`, never as delimiter rows in the
header.

## Deferrals

One sanctioned deferral exists, and its test is whether a truthful
value can exist yet. A slot that only a first build settles, which is
every design-system slot and every QC gate command the stack profile
does not already name, fills as `set at first build` plus where it gets
ruled. Deferrals count as fills and are listed beneath the report's
ancestry table, and the first-build lock-in replaces them all in one
sitting.

A deferral without a scheduled lock-in is a broken promise, so the
compile writes the task in the same pass: a row in docs/TASKS.md at S,
or a record under org/tasks/ at ORG, naming the first-build lock-in.
Check D004 enforces it, and the first two v2 seeds failed exactly this
before the rule was written down.

## Genesis forms

Five templates land in a seed as blank forms, at both scales, per the
ruling kernel/SCALE_MATRIX.md carries. The venture fills them later, in
its own repo, during the Genesis phase; inception/GENESIS.md says which
form becomes what, and where each instance lands.

| compiled file | template |
| --- | --- |
| docs/PRODUCT_MAP.md | kernel/templates/PRODUCT_MAP.tpl.md |
| docs/ACCEPTANCE_SPINE.md | kernel/templates/ACCEPTANCE_SPINE.tpl.md |
| docs/genesis/WORK_PACKAGE.md | kernel/templates/WORK_PACKAGE.tpl.md |
| docs/genesis/RESEARCH_PACKET.md | kernel/templates/RESEARCH_PACKET.tpl.md |
| docs/genesis/LENS.md | kernel/templates/LENS.tpl.md |

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
edit. Create nothing empty: directories appear with their first
content. Author the trigger add-ons the lock-book names, from the pack
or stack profile the matrix cites, and mark them authored in the
report. That is the one sanctioned authoring, bounded to the add-on
files.

## Distil

For each argued Ruling whose Wargame cites a binding Doctrine, condense
the venture-facing consequence into the lock-book's contract sections,
where the templates leave room. Distillation quotes or condenses the
Doctrine atom and never adds a rule it does not hold. List every
distillation in the report with the `RUL-*` identity that pulled it in.
None is a valid answer and the usual one at S.

## Report

Fill docs/COMPILE_REPORT.md from its template. The report records, in
its own order: the seed identity; one ancestry row per compiled file,
the JSON files included, in the row kinds the template itself defines;
the deferral fills with where each gets ruled; the distillations; the
deviations from the matrix; the check results; and the Wargame selection
totals from inception/WALK_ORDER.md, split into required,
candidate-included, candidate-omitted and uncovered pressure. It then
carries the sign-off block.

The sign-off block is the operator's rather than the compiler's.
Besides the five human rubric items it carries two lines the compiler
leaves blank and the operator writes: which path the seed took and
which of the items were signed, and whether Genesis was launched or
declined and why. Declined with a reason is a complete answer. Blank is
not, because blank cannot tell declined from forgotten.

Then phase E of inception/INCEPTION.md gates the result.

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
