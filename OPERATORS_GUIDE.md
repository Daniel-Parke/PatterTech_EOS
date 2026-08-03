---
summary: Daniel's manual for running the EOS, launchers, approval duties, the guard, cadences and what to do when something looks wrong
type: guide
tags: [eos]
review_by: 2027-03
---

# OPERATORS_GUIDE

How Daniel runs the EOS. Agents read it to know what the human does;
Daniel reads it to know what to launch and when.

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

## The guard, fail-closed, in practice

The action-time guard returns allow, require-approval, manual-only or
deny. Autonomous execution of a guarded class needs a validated host
enforcement adapter. **Without one, every guarded class is
manual-only**: the agent stops and tells you, and you do the action
yourself outside the agent. That is the current state, and it is not
something to work around. Naming a permission system does not satisfy
the requirement, and a seed claiming autonomous guarded actions without
an enforceable adapter fails its check.

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
