---
summary: FieldKit compile report, the seed's ancestry proof and sign-off record
type: template
tags: [eos]
compiled_from: kernel/templates/COMPILE_REPORT.tpl.md
---

# Compile report · FieldKit

Proof that this seed was compiled, not authored. Written by the
Session 0 compiler; validated by `eos_check.py --seed`; signed by the
operator against the human rubric items. A seed file that cannot be
traced to a row below is a compile failure.

## Seed identity

- venture: FieldKit
- scale: ORG · add-ons: none
- eos_version: 2.0.0-dev · eos_commit: 2c7468d
- compiled: 2026-08-03 · compiler session: EOS v2 build, lane P3

## Ancestry

One row per compiled file. Source is the kernel template path, `byte
copy of AGENTS.md` for CLAUDE.md, or `authored` for trigger add-ons
written at Session 0 from doctrine (name the doctrine). JSON seed
files carry ancestry rows like any other: the policy and cadence
files trace to their kernel templates with slots filled and no
fences, and the claims file's source is `seeded empty` per its
schema. Reseeds add two row kinds: `normalised` (pre-EOS venture
files that gained front-matter only, content untouched) and
`preserved` (venture content the compile did not touch).

| file | source | slots filled | fences pruned |
| --- | --- | --- | --- |
| AGENTS.md | kernel/templates/AGENTS.tpl.md | 2 | 2 |
| CLAUDE.md | byte copy of AGENTS.md | 0 | 0 |
| OPERATORS_GUIDE.md | kernel/templates/OPERATORS_GUIDE.tpl.md | 1 | 5 |
| docs/VENTURE_BRIEF.md | kernel/templates/VENTURE_BRIEF.tpl.md | 14 | 0 |
| docs/LOCKBOOK.md | kernel/templates/LOCKBOOK.tpl.md | 29 | 0 |
| docs/EOS_FEEDBACK.md | kernel/templates/EOS_FEEDBACK.tpl.md | 0 | 0 |
| docs/COMPILE_REPORT.md | kernel/templates/COMPILE_REPORT.tpl.md | 12 | 0 |
| org/CONSTITUTION.md | kernel/templates/org/CONSTITUTION.tpl.md | 4 | 0 |
| org/START.md | kernel/templates/org/START.tpl.md | 0 | 0 |
| org/TESTING.md | kernel/templates/org/TESTING.tpl.md | 0 | 0 |
| org/TEMPLATES.md | kernel/templates/org/TEMPLATES.tpl.md | 0 | 0 |
| org/QUESTIONS.md | kernel/templates/org/QUESTIONS.tpl.md | 0 | 0 |
| org/PLAYBOOKS.md | kernel/templates/org/PLAYBOOKS.tpl.md | 0 | 0 |
| org/policy.json | kernel/templates/org/policy.tpl.json | 6 | 0 |
| org/claims.json | seeded empty per kernel/schemas/claims.schema.json | 0 | 0 |
| org/cadence.json | kernel/templates/org/cadence.tpl.json | 5 | 0 |
| org/roles/EXECUTOR.md | kernel/templates/org/roles/EXECUTOR.tpl.md | 0 | 0 |
| org/roles/ORACLE.md | kernel/templates/org/roles/ORACLE.tpl.md | 0 | 0 |
| org/roles/REVIEWER.md | kernel/templates/org/roles/REVIEWER.tpl.md | 0 | 0 |
| org/tasks/T-0001.json | authored per the task-record shape in org/TEMPLATES.md and kernel/schemas/task-record.schema.json | 0 | 0 |

Fence counts are fenced blocks resolved: blocks kept for the ruled
scale have their fence lines removed, blocks for other scales are
removed whole. Only AGENTS.tpl.md and OPERATORS_GUIDE.tpl.md carry
scale fences; every other v2 template is scale-neutral. The policy
row counts the six real slots (`VENTURE_NAME`,
`CAPABILITY_PROFILE_REF`, the three path lists and
`GUARD_MAPPING_REF`); the seventh slot marker sits inside the
template's own `_slots` note, which was deleted after filling per
that note. The risk factor table, the express thresholds, the mode
dials, the decision budget and the approvals list carry no slots, so
they ship exactly as the template holds them; the approvals block is
protected content and instantiates Article 8 of the constitution
unchanged. The four org/QUESTIONS.md rows transcribe questions the
Session 0 interview left open; transcription, not authoring.

Deferral fills (`set at first build`, COMPILE.md) count as fills and
are listed here by slot, with where each gets ruled. All seventeen are
in docs/LOCKBOOK.md and all get ruled at the first-build lock-in under
org/tasks/T-0001.json: signature motif, signature animated pieces,
token home, code mirror, styleguide route, surface ladder, accents,
text tiers, reading measure, wide measure, full measure, block gap,
and the five QC gates (build, overflow at 375, page weight,
screenshots, regression smokes).

## Distillations

Standards or notes distilled into the seed from the doctrine the
rulings cite, each with the ruling that pulled it in. None is a valid
answer at S.

None. Part I of the constitution condenses the operator's own words
from the interview, and the structural contracts in the lock-book do
the same; neither pulls a rule the doctrine does not already hold.

## Deviations from the matrix

None expected. Anything here blocks the gate until ruled.

One, and it is deliberate. The v2 matrix says directories appear with
their first content and never at compile, so org/tasks/ would arrive
with the venture's first real task. This seed ships
org/tasks/T-0001.json at compile instead: the venture's first build
step as a routed work order, declared facts, ruled tier and reasons
list, valid against kernel/schemas/task-record.schema.json. It closes
the v1 hole where the seeded first item was a queue row nobody had
routed, which a session taking it could not honour under Part II
Article 3. Ruled by the Session 0 compile instruction; recorded here
because the matrix sentence still reads the other way.

Two compile-time notes that are not deviations but must be read
before the gate:

- `guard.mapping_ref` names `org/guard-mapping.json`, which does not
  exist yet. That is the fail-closed state the guard spec intends:
  `guard.validated` is false, so every guarded class is manual-only
  and the operator acts. Q-004 in org/QUESTIONS.md carries it.
- The lock-book ships `addons: []` and `packs_adopted: []` because
  nothing is deployed and no pack has been argued in. The ops-runbook
  add-on attaches at the first deploy and the restore-test add-on at
  the first production data.

## Check results

Paste the `eos_check.py --seed` summary line and date. All auto items
green before the human items are judged.

- 2026-08-03 · `python -m tools.eos check --seed benchmark/fixtures/seed-v2-ORG`
  · `1 errors, 0 warnings`, and the one error is the pin, not the
  seed: the check resolves the governing matrix at the pinned
  `eos_commit`, and at 2c7468d `kernel/SCALE_MATRIX.md` still holds
  the v1 S/M/L matrix while the v2 matrix waits at
  `kernel/SCALE_MATRIX_v2.staging.md`. Under a matrix with no ORG
  column the ruled scale cannot resolve.
- 2026-08-03 · the same seed against the staged v2 matrix ·
  `0 errors, 0 warnings`. Recorded for the integrator who swaps the
  matrix in; not fixable from inside a seed.

## Sign-off (human rubric items)

- [ ] H1 cold-start test · - [ ] H2 brief reads true · - [ ] H3
  rulings honest · - [ ] H4 voice holds · - [ ] H5 operator can run it
- Signed: (awaiting operator) · date: (awaiting sign-off)
