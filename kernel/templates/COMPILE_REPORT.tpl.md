---
summary: Compile report template, the seed's ancestry proof and the rubric sign-off record
type: template
tags: [eos]
template: true
---

# Compile report · {{VENTURE_NAME}}

Proof that this seed was compiled, not authored. Written by the
Session 0 compiler; validated by `eos_check.py --seed`; signed by the
operator against the human rubric items. A seed file that cannot be
traced to a row below is a compile failure.

## Seed identity

- venture: {{VENTURE_NAME}}
- scale: {{SCALE}} · add-ons: {{ADDONS}}
- eos_version: {{EOS_VERSION}} · eos_commit: {{EOS_COMMIT}}
- compiled: {{COMPILED_DATE}} · compiler session: {{SESSION_ID}}

## Ancestry

One row per compiled file. Source is the kernel template path, `byte
copy of AGENTS.md` for CLAUDE.md, or `authored` for trigger add-ons
written at Session 0 from doctrine (name the doctrine).

| file | source | slots filled | fences pruned |
| --- | --- | --- | --- |
| AGENTS.md | kernel/templates/AGENTS.tpl.md | {{N}} | {{N}} |

## Distillations

Standards or notes distilled into the seed from the doctrine the
rulings cite, each with the ruling that pulled it in. None is a valid
answer at S.

## Deviations from the matrix

None expected. Anything here blocks the gate until ruled.

## Check results

Paste the `eos_check.py --seed` summary line and date. All auto items
green before the human items are judged.

## Sign-off (human rubric items)

- [ ] H1 cold-start test · - [ ] H2 brief reads true · - [ ] H3
  rulings honest · - [ ] H4 voice holds · - [ ] H5 operator can run it
- Signed: {{OPERATOR}} · date: {{SIGNOFF_DATE}}
