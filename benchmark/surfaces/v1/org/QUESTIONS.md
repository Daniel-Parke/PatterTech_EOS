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
split.

## Open

- Q-001 (ops): the agreed monthly spend budget for hosting; context:
  the one-time setup list in `OPERATORS_GUIDE.md`; owner: the
  operator.

## Folded

- (none)
