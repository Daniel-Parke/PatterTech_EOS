---
summary: Four false statements in protected files, the corrections applied to them, and why they needed a record first
type: decision
tags: [eos]
status: accepted
decided_by: Daniel Parke
date: 2026-08-10
---

# ADR-0005: four corrections in the protected set

**Where this stands.** Accepted, and all four corrections are in the
tree. Everything below was written while the record was still a
proposal, and it says so in the present tense; `org/decisions/` is
append-only, so it is left exactly as written rather than tidied. The
Decision section at the foot is the ruling. Only the summary line in
the front matter was corrected, because it feeds `INDEX.md` and a
reader scanning that index would otherwise read these four corrections
as still pending.

Proposed on 2026-08-10 by the post-merge documentation pass. Not
accepted. `GOVERNANCE.md` requires an accepted ADR and Daniel before
anything in the protected set changes, so these four are written down
rather than fixed. Every other finding from the same pass was corrected
in place, because nothing else it found was protected.

ADR-0002, ADR-0003 and ADR-0004 stand. This changes no rule. It
corrects four descriptions of rules that the repository does not
enforce, in files a reader is entitled to trust most.

## Context

A seven-group review swept the prose documentation against the code and
the tree. It found seventy statements that were false about the current
state. Sixty-six sit in files that can be edited and were. Four sit in
the protected set:

- `kernel/POLICY_SPEC.md`, protected as "the policy risk and approvals
  blocks, with `kernel/POLICY_SPEC.md`".
- `kernel/templates/org/CONSTITUTION.tpl.md` Part II, protected as "the
  constitution Parts II and III in the kernel templates".
- `kernel/templates/org/roles/REVIEWER.tpl.md`, protected as one of
  "the three role charters, EXECUTOR, ORACLE and REVIEWER".

Two of the four ship into every venture. The constitution and the role
charters compile into every ORG seed, so a venture is handed the
unimplemented rule as law.

## The four

**1. `kernel/POLICY_SPEC.md`: "An expired standing exception is a
checker finding."** No check reads an expiry date, on an ADR or
anywhere else. ADR-0004 named this exact sentence as an example of the
repository describing more control than it implements, and then built
two controls that were not this one. Proposed replacement:

> An expired standing exception is caught by the monthly governance
> review, which samples recorded exceptions. No check reads expiry
> dates.

**2. `kernel/POLICY_SPEC.md`: "a sandboxed spike on `spike/T-####` that
the checker refuses to merge".** Nothing reads a branch name for this.
`grep -rni spike tools/ tests/ .github/` returns nothing at all, and
the CI workflow runs only `check` and pytest. The rule is real
doctrine, carried by the exploration playbook rather than by a check.
Proposed replacement:

> a sandboxed spike on `spike/T-####` that never merges, held by the
> exploration playbook rather than by a check

**3. `kernel/templates/org/CONSTITUTION.tpl.md` Part II, clause 7:
"spikes live on spike branches the checker refuses to merge".** The
same claim, in the worst place, because Part II is constitutional law
in every compiled ORG seed. Proposed replacement:

> spikes live on spike branches that never merge

**4. `kernel/templates/org/roles/REVIEWER.tpl.md`: a one-off tier
exception "lands in the append-only exception ledger".** ADR-0004
withdrew `org/exceptions.jsonl`. `kernel/POLICY_SPEC.md` already
records the replacement, that an exception lives on the task record it
applies to. This charter still hands every venture the withdrawn
mechanism. Proposed replacement:

> it is recorded on the task record it applies to, beside the ruling it
> lowers, with evidence, authoriser and date

## The same claim, in the files that were not protected

The spike claim sat in six places. The four editable ones were
corrected in this pass: `TOUR.md`, `org/PLAYBOOKS.md`,
`packs/coding/PACK.md` and `kernel/templates/org/TEMPLATES.tpl.md`.
Two remain, both above. Until this ADR is accepted the repository says
two different things about the same rule, which is worse than either
version alone, and that is the argument for taking it.

## Decision

Accepted by Daniel on 2026-08-10, at the start of the v2.1 build. The
four replacements above are applied and nothing else. No rule changes,
no threshold moves, and no behaviour is added: each edit makes a
description match what the code already does.

One further instance of the same defect was found while applying this
and is corrected under ADR-0006, because it sits in a protected file
this record did not name: `packs/security-privacy/PACK.md` B3 and its
choices list still pointed at the withdrawn exception ledger.

If declined, the alternative is to build the two controls the text
claims, a check that reads expiry dates and a merge gate that refuses
a spike branch. That is real work and it was considered and rejected
once already, in ADR-0004, on the grounds that a control worth
describing is worth building and a control not worth building is not
worth describing.
