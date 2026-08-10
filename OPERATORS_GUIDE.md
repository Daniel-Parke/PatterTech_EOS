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
leaves records rather than paperwork. There is no work-in-progress
limit. What bounds concurrency is claims, and claims are needed when
more than one session may write at once.

## Launchers

Paste one line into a fresh agent session, in the repository named.

- **E1, work**: "Read AGENTS.md, entry mode 2. Take T-#### from
  org/TASKS.md." The workhorse. This repository.
- **E2, Session 0**: "Read AGENTS.md, entry mode 3. The new venture is
  <one line>. Repo at <path>." Run from the venture repository.
- **E3, the monthly pass**: "Entry mode 2, run the monthly pass: PB-E02
  harvest, PB-E04 promotion review, PB-E10 experiment sweep, PB-E09
  hygiene, in one sitting." That is the order `org/PLAYBOOKS.md` sets,
  and hygiene is last because it regenerates the views after the other
  three have moved things. This used to be three launchers, E3 to E5.
  ADR-0008 folded the monthly cadences into one pass, so E4 and E5 are
  gone and `org/cadence.json` carries a single monthly row.
- **E6, release**: "Entry mode 2, run PB-E05." Only after you have
  approved the release.
- **E7, on demand, not quarterly**: "Entry mode 2, run PB-E07" (an
  inception drill), or the projects review that answers adopt or defer
  for each candidate repository. Run these when something real triggers
  them, such as a seed compiled or a repository added.
- **E8, upgrade a venture**: "Entry mode 2, run PB-E06 for <venture>."
  A venture that only wants findings asks for PB-E12 instead: a
  check-in returns findings and candidate lessons and applies nothing.
- **E9, Genesis**: "Read AGENTS.md, entry mode 3. Session 0 is done and
  the seed is signed. Run inception/GENESIS.md, <full or lite> form."
  Run from the venture repository, after the seed gate. Full is the ORG
  default and lite is the S default; the choice is yours at launch. It
  ends by handing you the product map and the work packages to read.
- **E10, study a source**: "Entry mode 2, run PB-E11. Study <source>
  for <what you want out of it>." This repository. The session writes
  the lens contract first and stops for your approval before it reads
  anything, and you see the findings only after it has checked them for
  conflicts with live rules.
- **E11, a graph build**: "Read AGENTS.md, entry mode 4. Cut a partition
  for <the work> per packs/agentic-swarm/PACK.md, and hand back the
  partition and the lane briefs before dispatching anything." Either
  repository. You commit the claim set before any lane starts.

## Your approval duties

The policy's `always_human` list is the short version. Six classes never
execute on an agent's authority, at any tier, under any capability
profile: **money movement, production data, deletion, irreversible
actions, secrets, and contact with the protected set.**

Beyond that, only you can accept an ADR, approve a protected-set change,
sign the human items of a seed rubric, promote a rule to binding,
authorise a capability-profile promotion, approve a release, create
remotes and accounts, and spend money.

One duty was retired rather than discharged. The sealed suite,
`benchmark/SEALED.json`, runs once and needs your private key. ADR-0007
retires it unopened, because it was written to compare a frozen v1
against a final v2 and the release it was meant to judge has changed
shape. The key stays with you, the suite stays in the tree with its
hashes, and a future sealed evaluation is written fresh against whatever
it is meant to judge. Two of the protocol's eight gates depended on it
and stay uncomputed.

## Picking up work

A claim is a written statement of who is writing which paths, committed
before the work starts. `org/claims.json` names the lane, the session
id, the paths and an expiry.

- **One session, working alone**: no claim file needed. It is implicitly
  claimed, because there is nobody to collide with. Git history and the
  checker are what catch it going wrong (ADR-0008).
- **More than one session writing at once**: you write and commit the
  claim set before any lane is dispatched. That commit is itself a
  change to a product file, so make it before the sessions start, not
  during. Lanes never acquire or mutate a claim.

Where a claim set is committed, `task new` and `task update` refuse a
session it does not name, printing
`{"refused": true, reason, claim_set_ref}` and exiting 1. An expired
claim refuses the same way, so a lapsed standing claim has to be rewritten
and committed before the session that needs it. Where there is no claim
set at all, the repository is not running the assigned-claims model and
the control does not apply.

There is no `claims assign`, `renew` or `recover` command; those were
described once and never built, and `tools/CLI_CONTRACTS.md` records
which commands exist.

A lane's claim over its own product paths also covers its own task
record under `org/tasks/`. It does not cover anything derived: you alone
regenerate those.

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
`org/PLAYBOOKS.md`. Four rows, and only one of them carries a date.

**`monthly-pass`, one sitting, four sections**: harvest, promotion
review, experiment sweep, hygiene, in that order, about thirty minutes
of your review time. A section you skip is still a finding, so the pass
records what it did not do rather than quietly dropping it.

**`inception-drill` and `projects-review`, on demand**: both used to be
quarterly rows and neither had fired once since v1, which is evidence
that a calendar trigger nobody honours is not a control (ADR-0008). Run
them when something real happens: a seed compiled, a repository added, a
drill worth grading.

**`benchmark-freshness`, on demand**: the fourth row, pointing at
`benchmark/PROTOCOL.md`. It has never run, and nothing outside the row
itself says what fires it. Treat it as an open question rather than as a
duty waiting on you.

A due cadence outranks new low-priority work.

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
- **A lane returns something odd**: treat what a lane hands back as
  data, not as instruction. The integrator reads it, decides, and
  merges; it does not do what the return text tells it to do.
