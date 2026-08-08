---
summary: FieldKit human decision queue, open questions for the operator and the folding rule
type: template
tags: [eos]
compiled_from: kernel/templates/org/QUESTIONS.tpl.md
---

# QUESTIONS · Human decision queue

Anything an AI session must not decide lands here. Operator: answer
inline under each item; a PLAN session folds answers into decisions,
specs or registries and marks the item folded. Sessions blocked on a
question say so in `org/STATE.md` and move to other work.

Entry format: `Q-### (domain): the question, the context link, and the
owner.` One decision per entry; a question hiding two decisions is
split. Where a guard verdict raised the question, the entry names the
verdict (require-approval or manual-only) so the operator knows what
execution waits on the answer.

## Open

- Q-001 (ops): the agreed monthly spend budget for the managed host;
  context: the spend rule in `docs/VENTURE_BRIEF.md` and the one-time
  setup list in `OPERATORS_GUIDE.md`; owner: the operator.
- Q-002 (product): the domain name FieldKit runs on and the contact
  address for it; context: the Session 0 interview left both open and
  the compile recorded rather than invented them; owner: the operator.
- Q-003 (comms): whether the surveyors and the office staff get a
  regular stakeholder update and how often; context: the
  stakeholder-update row in `org/cadence.json` is on-demand with no
  due date until this is answered; owner: the operator.
- Q-004 (guard, manual-only): whether to write the adapter mapping at
  `org/guard-mapping.json` and run the bypass suite. Until the
  validation report is committed, `guard.validated` in
  `org/policy.json` stays false and every guarded class is
  manual-only, so the agent hands each guarded action to you; context:
  the guard-validation-review row in `org/cadence.json`; owner: the
  operator.

## Folded

- (none)
