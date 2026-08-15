---
summary: The operator's manual for running the EOS, launchers, approval duties, claims, the guard, the monthly pass, the release gate and what to do when something looks wrong
type: guide
tags: [eos]
review: 2027-03
---

# OPERATORS_GUIDE

How the operator runs the EOS. If you have adopted this repository, you
are the operator, and the integrator duties named in `org/PLAYBOOKS.md`
and `tools/CLI_CONTRACTS.md` are yours too: you alone commit claims, run
the generators and adopt or discard quarantined work. Daniel holds both
roles here. `TOUR.md` says what those two words mean; this file says
what the person holding them does.

Agents read this to know what the human does. You read it to know what
to launch and when. There is no work-in-progress limit. What bounds
concurrency is claims, and claims are needed when more than one session
may write at once. `org/policy.json` declares `parallelism.max_lanes`,
but no code reads it, so it is a note to yourself and not a ceiling.

The other two values in that block are the same. `claim_expiry_hours`
and `renewal_window_hours` are read by nothing in `tools/`, so a claim
does not expire on the clock they name. What does read an expiry is
`task claims-verify`, at the merge, and it reports a lapsed claim as
C002 rather than refusing anything. All three were disclosed as a set
because a block where one value is declared inert and two are silent
reads as though the silent two work.

## Launchers

Paste one line into a fresh agent session, in the repository named. The
numbering is local to this file and nothing else cites it.

- **L1, work on the EOS.** "Read AGENTS.md, entry mode 2. Take T-####
  from org/TASKS.md." The workhorse. This repository. A session working
  alone opens its own task record and writes freely. Read the claims
  section below before dispatching more than one at a time.
- **L2, Session 0.** "Read AGENTS.md, entry mode 3. The new venture is
  <one line>. Repo at <path>." Run from the venture's repository. It
  ends with the seed rubric in front of you and the launch decision in
  your hands.
- **L3, Genesis.** "Read AGENTS.md, entry mode 3. Session 0 is done and
  the seed is signed. Run inception/GENESIS.md." The venture's
  repository, after the seed gate. The forms in the seed were already
  pruned for the ruled scale when it compiled, so there is no form for
  you to pick: what you decide is whether the phase runs at all. ORG
  runs it by default; a venture that came through Express inception
  skips it unless you ask. Either way the forms ship blank, so a venture
  that declined can run Genesis later without a recompile. It ends by
  handing you the product map and the work packages, and it is not
  finished until you say go.
- **L4, the monthly pass.** "Entry mode 2, run the monthly pass: PB-E02
  harvest, PB-E04 promotion review, PB-E10 experiment sweep, PB-E09
  hygiene, in one sitting." That order is set by `org/PLAYBOOKS.md`, and
  hygiene is last because it regenerates the derived views after the
  other three have moved things.
- **L5, study a source.** "Entry mode 2, run PB-E11. Study <source> for
  <what you want out of it>." This repository. The session scaffolds the
  lens contract with `python -m tools.eos study` and stops for your
  approval before it reads anything. You see the findings only after it
  has checked them against live rules for conflicts. A study never
  starts on a schedule and never because an agent suggested it.
- **L6, a graph build.** "Read AGENTS.md, entry mode 4. Cut a partition
  for <the work> per packs/agentic-swarm/PACK.md, and hand back the
  partition and the lane briefs before dispatching anything." Either
  repository. You read the partition, then you commit the claim set, and
  only then does any lane start.
- **L7, a venture check-in.** "Entry mode 2, run PB-E12 for <venture>,
  slice <what they asked about>." Only ever because the venture asked.
  It returns findings and candidate lessons and applies nothing. If the
  venture has not said what it wants looked at, the session asks before
  it reads.
- **L8, upgrade a venture.** "Entry mode 2, run PB-E06 for <venture>."
  On request only. A venture that wants a bigger organisation rather
  than a newer pin takes PB-E08, the rescale, and the only rescale that
  exists is S to ORG.
- **L9, an inception drill.** "Entry mode 2, run PB-E07." Fires when a
  seed is compiled or the inception walk changes. It takes a canned
  brief from `inception/briefs/`, runs Session 0 cold in a scratch
  repository, and grades the result against `kernel/SEED_RUBRIC.md`
  without charity. The estate review is the other event-fired job:
  "Entry mode 2, run the estate review from PB-E06", when a repository
  joins the estate or a venture changes status.
- **L10, release.** "Entry mode 2, run PB-E05." Only after you have
  approved the release. The section below says what you are approving.

## Your approval duties

The policy's `always_human` list is the short version. Six classes never
execute on an agent's authority, at any tier, under any capability
profile: **money movement, production data, deletion, irreversible
actions, secrets, and contact with the protected set.**

Beyond that, only you can accept an ADR, approve a protected-set change,
sign the human items of a seed rubric, promote a rule to binding,
authorise a capability-profile promotion, approve a release, create
remotes and accounts, and spend money.

Two of those carry a check nothing else makes. When a session tells you
a diff touches the protected set, `python -m tools.eos route` will have
exited 3 unless it was given `--adr`, and it checks only that a value
was passed. Nothing reads the id or confirms the record is accepted, so
you do. And the capability profile in `org/capability-profile.json` is
read by no code at all. It is an argument for changing the express
thresholds in the policy, not a mechanism that changes anything by
itself.

One duty was retired rather than discharged. The sealed suite,
`benchmark/SEALED.json`, runs once and needs your private key. ADR-0007
retires it unopened, because it was written to compare a frozen v1
against a final v2 and the release it was meant to judge has changed
shape. The key stays with you, the suite stays in the tree with its
hashes, and a future sealed evaluation is written fresh against whatever
it is meant to judge. Two of the protocol's eight gates depended on it
and stay uncomputed.

## Claims, and the sharp edge in this repository

A claim is a written statement of who is writing which paths, committed
before the work starts. `org/claims.json` names the lane, the session
id, the paths and an expiry.

- **One session, working alone**: no claim needed. It is implicitly
  claimed, because there is nobody to collide with. Git history and the
  checker are what catch it going wrong (ADR-0008).
- **More than one session writing at once**: you write and commit the
  claim set before any lane is dispatched. That commit is itself a
  change to a product file, so make it before the sessions start, not
  during. Lanes never acquire or mutate a claim.

The control keys on lanes, not on the file. `org/claims.json` sits in
this repository with an empty lane list, and an empty list is the
release rather than a lock: it reads as no claim model in force, so a
solo session writes freely. That is ADR-0008 decision 1, and it is why a
finished claim set is committed empty rather than deleted. Deleting it
would be worse than pointless, because check D009 requires a compiled
ORG seed to ship `org/claims.json` carrying exactly that empty list. No
claims file at all reads the same way.

Where lanes are present the control is live. A session not named in one
is refused, and so is a named session writing a path its own lane holds
no claim over. The session id is `--session ID`, else `EOS_SESSION_ID`,
else the record's `owner_session`, and with lanes present a session
carrying none of the three is refused too. Every refusal prints
`{"refused": true, reason, claim_set_ref}` and exits 1. Expiry is not
tested at this gate: a lapsed claim still lets a task record through,
and it is `task claims-verify` at the merge that reports it as C002,
with the lane's liveness identity attached.

Ordinary file writes are not gated. The control bites at two points
only: where a task record is written, and again at integration through
`task claims-verify`, which compares a lane's diff against its claims
and reports C001 to C005.

There is no `claims assign`, `renew` or `recover` command. Those were
described once and never built, and `tools/CLI_CONTRACTS.md` records
which commands exist.

Here is the edge, and it will bite somebody. ADR-0008 decision 2 lets a
lane open its own task record, but no claim over a lane's product paths
implies one over the record: `task new` compares
`org/tasks/T-####.json` against the lane's claims like any other path,
and `claims-verify` reports it as C003 at the merge if it is outside
them. So when you assign a lane that will open a record, write
`org/tasks/` into its claims alongside its product paths.

No lane claim covers anything derived: you alone regenerate those, with
`python -m tools.eos check --write-index` for the five indexes and views
and `python -m tools.eos task views` for `org/TASKS.md` and
`org/STATE.md`.

## The guard, fail-closed, in practice

The action-time guard returns allow, require-approval, manual-only or
deny, and `python -m tools.eos guard eval` is what rules one action.
Autonomous execution of a guarded class needs a validated host
enforcement adapter. **Without one, every guarded class is manual-only**:
the agent stops and tells you, and you do the action yourself outside
the agent.

One adapter ships, `kernel/adapters/claude-code.json`. `TOUR.md`
describes what it covers. What matters at your keyboard is that it
grants nothing. Its validation block is dated 2026-08-03 and says
mapping-level, offline, `host_run` false, which proved that fourteen
bypass attempts classify into the right guarded class from the tool
surface alone and did not prove that a live session's hooks fire. So
every guarded action still stops. The three covered classes stop and ask
you, and your answer is the record. The other seven stop and you do the
action yourself, outside the agent. Read the validation block before
relying on any of it, because any change to the adapter or the mapping
voids it.

None of this is something to work around. Naming a permission system
does not satisfy the requirement, and a seed claiming autonomous guarded
actions without an enforceable adapter fails its check.

## The cadence

There is one row in `org/cadence.json`, and it is the whole calendar.

**`monthly-pass`, one sitting, four sections**: harvest, promotion
review, experiment sweep, hygiene, in that order. Close it by
setting `last_run` in
`org/cadence.json`. A section that found nothing writes one line saying
checked and clean. A section you skipped is a finding, so the pass
records what it did not do rather than quietly dropping it.

Everything else waits for an event, and each procedure in
`org/PLAYBOOKS.md` names its own: a seed compiled fires the inception
drill, a repository joining the estate fires the estate review, a
venture asking fires an upgrade, a rescale or a check-in, you pointing
at a source fires a study, and a release fires PB-E05.

Three rows that used to sit here were deleted rather than left carrying
no date: `inception-drill`, `projects-review` and `benchmark-freshness`.
The first two had not fired once since v1, which is evidence that a
calendar trigger nobody honours is not a control (ADR-0008). The third
pointed at a benchmark ADR-0007 retires. A due cadence still outranks
new low-priority work; there is simply only one of them.

## Approving a release

The gate is the five items in ADR-0007 decision 5, listed in
`README.md`. Three of them a machine settles and you can watch: the
checker green with the semantic and freshness series, the test suite
green, the CHANGELOG entry written. The other two are yours and nothing
else can do them.

**No false statement about the tree survives the final review.** That is
the one this repository keeps failing. Sixty-six of them were found and
removed once. Read the claims, not the prose around them: a control
described as enforced that nothing enforces, a gate described as met
that was struck, a count copied from a file that has since changed.

**Your explicit approval.** Before you give it, check the guard rather
than assuming it, as PB-E05 says: `guard.validated` in the policy may
read true only while the mapping it names carries a current
bypass-suite validation block, and there is no separate report file.

No benchmark gate is on the release, and none of the eight in
`benchmark/PROTOCOL.md` can be put back on it. `README.md` says which
passed, which were struck and which cannot be computed at all. A struck
gate is not a met gate and nothing in the tree may describe it as one.

## When something looks wrong

- **A view disagrees with reality**: reality wins. Views are generated,
  so fix the record and regenerate, never the view.
- **The checker says a derived file is stale**: that is E001 or E011 and
  it means somebody changed a source without regenerating. Regenerate.
  If the regeneration then produces new errors, they were already true
  and the stale view was hiding them.
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
- **A venture looks out of line with current guidance**: it probably is,
  and that is allowed. The EOS hands off at a venture's birth. Wait for
  the venture to ask, then run L7.
