---
summary: The seed compiler's rules, prune, fill, distil, report, and the never-list
type: kernel
tags: [eos]
---

# COMPILE

The rules the Session 0 compiler follows at phase D of INCEPTION.md.
The compiler is a slot-filler and pruner, never an author. Every output
traces to a template plus rulings through the compile report, and
`eos_check.py --seed` is the mechanical judge of the result.

## Inputs, all of them

1. The ruled lock-book: scale, stack, add-ons, the rulings rows.
2. The venture brief content from the interview.
3. `kernel/SCALE_MATRIX.md` at the pinned EOS commit.
4. The templates the matrix names, at the same commit.

No other source exists. If a slot has no answer in these inputs, the
compiler stops and asks the operator; it never invents one.

## Prune

For each file the matrix requires at the ruled scale, take its
template and remove every fenced section whose scale list does not
include the ruled scale. A fence opens with `<!-- scale: ... -->` and
closes with the end marker; fences wrap whole sentences, bullets or
sections (kernel/README.md). Remove the fence lines themselves in the
same pass. A fence inside kept content is a template defect: stop and
file it in the venture's feedback file before continuing.

## Fill

Replace every `{{SLOT}}` with content from the inputs, in the voice the
templates already carry. Count the fills per file for the report.
Filling is transcription and condensation of the operator's words and
the rulings, not composition. After filling, the file must contain no
slot syntax anywhere, including inside code spans.

## Front-matter rewrite

Compiled files drop `template: true` and `extracted_from`, gain
`compiled_from: <template path>`, and keep a summary, type and tags
that read true for the venture. The lock-book header carries the
machine pins (eos_root, eos_version, eos_commit, scale, stack, addons,
rulings) per its template.

## Assemble

Byte-copy the compiled AGENTS.md to CLAUDE.md, last. Create the empty
directories the matrix lists for the scale. Author the trigger add-ons
the lock-book names, from the doctrine or pattern the matrix cites,
and mark them `authored` in the report; this is the one sanctioned
authoring, and it is bounded to the add-on files.

## Distil

For each argued ruling whose wargame cites doctrine, condense the
venture-facing consequence into the seed where the templates leave room
(the lock-book's contract sections; standards at Genesis, not at seed).
Distillation quotes or condenses the cited doctrine; it never adds
rules the doctrine does not hold. List every distillation in the
report with the ruling that pulled it in.

## Report and gate

Fill `docs/COMPILE_REPORT.md` from its template: identity, one
ancestry row per compiled file (source, slots filled, fences pruned),
distillations, deviations (none, or stop). Run
`python tools/eos_check.py --seed <venture path>` from the EOS repo and
paste the summary line with the date. All auto items green before the
human rubric items are judged; the sign-off block closes Session 0.

## Never

- Never author content outside the recorded add-ons and distillations.
- Never renumber, reword or reorder protected template text (the
  constitution's Parts II and III, the role charters); pruning their
  fences is the only edit allowed.
- Never leave a fence line, a slot, or an unfilled front-matter key.
- Never compile from a dirty template tree; the pin is a commit, not a
  branch.
- Three strikes applies: the same seed-check failure surviving three
  distinct fix attempts stops Session 0, recorded in the feedback file
  and put to the operator.
