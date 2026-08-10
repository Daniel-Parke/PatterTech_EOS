---
summary: The operator's manual for running the EOS, launchers, approval duties, the guard, cadences and what to do when something looks wrong
type: guide
tags: [eos]
review: 2027-03
---

# OPERATORS_GUIDE

How the operator runs the EOS. If you have adopted this repository,
you are the operator, and the integrator duties named in
`org/PLAYBOOKS.md` and `tools/CLI_CONTRACTS.md` are yours too: you
alone commit claims, run the generators and adopt or discard
quarantined work. Daniel holds both roles here. Agents read this file
to know what the human does; the operator reads it to know what to
launch and when.

The EOS seeds ventures and learns from them. You launch sessions against
it; each one is routed into a mode, does the work that mode allows, and
leaves records rather than paperwork. There is no work-in-progress limit
now: concurrency is bounded by claims, and a session not named in
`org/claims.json` is refused.

## Launchers

Paste one line into a fresh agent session in this repo.

- **E1, work**: "Read AGENTS.md, entry mode 2. Take T-#### from
  org/TASKS.md." The workhorse.
- **E2, Session 0**: "Read AGENTS.md, entry mode 3. The new venture is
  <one line>. Repo at <path>." Run from the venture repo.
- **E3 to E5, monthly**: "Entry mode 2, run PB-E02" (harvest),
  "PB-E09" (hygiene), "PB-E04" (promotion review), "PB-E10" (experiment
  sweep, which closes or promotes anything past ninety days).
- **E6, release**: "Entry mode 2, run PB-E05." Only after you have
  approved the release.
- **E7, quarterly**: "Entry mode 2, run PB-E07" (inception drill), then
  the estate review that answers adopt or defer for each candidate repo.
- **E8, upgrade a venture**: "Entry mode 2, run PB-E06 for <venture>."

## Your approval duties

The policy's `always_human` list is the short version. Six classes never
execute on an agent's authority, at any tier, under any capability
profile: **money movement, production data, deletion, irreversible
actions, secrets, and contact with the protected set.**

Beyond that, only you can accept an ADR, approve a protected-set change,
sign the human items of a seed rubric, promote a rule to binding,
authorise a capability-profile promotion, approve a release, create
remotes and accounts, and spend money.

The sealed suite, `benchmark/SEALED.json`, runs once. The private key
is yours alone and is released only to the final evaluator session at
the release checkpoint. Two of the eight gates depend on it and stay
uncomputed until then. Spent early it is spent for good, so nothing
else opens it.

## Picking up work

Every session that writes needs a claim. `org/claims.json` is written
by hand and committed before the session starts, naming the lane, the
session id, the paths and an expiry. There is no `claims assign`,
`renew` or `recover` command; those were described once and never
built, and `tools/CLI_CONTRACTS.md` records which commands exist.

`task new` and `task update` refuse a session the file does not name,
printing `{"refused": true, reason, claim_set_ref}` and exiting 1.
An expired claim refuses the same way, so if the standing claim has lapsed the first
act of a new operator is to write themselves one and commit it. That
commit is itself a product-file change, so make it before the session
that needs it, not during.

## The guard, fail-closed, in practice

The action-time guard returns allow, require-approval, manual-only or
deny. Autonomous execution of a guarded class needs a validated host
enforcement adapter. **Without one, every guarded class is
manual-only**: the agent stops and tells you, and you do the action
yourself outside the agent.

Today `kernel/adapters/claude-code.json` is validated, so external-write,
destructive-git and dependency-install rule require-approval and resolve
on a recorded approval from you. The other seven classes have no passing
bypass case, so they stay manual-only. None of it is something to work
around. Naming a permission system does not satisfy the requirement, and
a seed claiming autonomous guarded actions without an enforceable
adapter fails its check.

## Cadences

Rows and next-due dates live in `org/cadence.json`, procedures in
`org/PLAYBOOKS.md`. Monthly: harvest, hygiene, promotion review and the
experiment sweep, about thirty minutes of your review time. Quarterly:
the inception drill and the estate review. A due cadence outranks new
low-priority work.

## When something looks wrong

- **A view disagrees with reality**: reality wins. Views are generated,
  so fix the record and regenerate, never the view.
- **A claim expired but the lane may be alive**: check liveness first,
  through harness state or the recorded process id. If liveness cannot
  be established, you recover the claim. A timestamp never authorises it.
- **A check keeps failing**: the circuit breaker applies. Three
  materially distinct hypotheses tested and falsified with no reduction
  in uncertainty means stop and read the failure properly. Retries of
  one idea count as one. Never weaken a check to pass it.
- **A session did work it was not claimed for**: it is quarantined on
  its branch, not deleted. You decide adopt or discard.
- **The protected set changed without an ADR**: revert it, then ask why
  the session thought it could.
