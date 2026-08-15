---
summary: The operator's manual for running the EOS: the ten launchers, the commands, what only you can approve, claims, the guard, the cadence, the release gate and what to do when something looks wrong
type: guide
tags: [eos]
review: 2027-03
---

# OPERATORS_GUIDE

If you have adopted this repository, you are the operator. The
integrator duties named in `org/PLAYBOOKS.md` and
`tools/CLI_CONTRACTS.md` are yours too: you alone commit claims, run the
generators, and adopt or discard quarantined work. The operator holds both
roles here.

`TOUR.md` says what those two words mean. This file says what the person
holding them does. Agents read it to know what the human does. You read
it to know what to launch and when.

The tree reads 0.4.0 (ADR-0009). Nothing is released and no tag is cut.

## Find it fast

| If you are | Read |
| --- | --- |
| about to start a session | [Launchers](#launchers) |
| looking for the command that does it | [Commands you run yourself](#commands-you-run-yourself) |
| being asked to approve something | [What only you can approve](#what-only-you-can-approve) |
| dispatching more than one session | [Claims](#claims-and-the-sharp-edge-in-this-repository) |
| told an action is manual-only | [The guard, in practice](#the-guard-in-practice) |
| asking what is due | [The cadence](#the-cadence) |
| about to approve a release | [Approving a release](#approving-a-release) |
| staring at something that looks wrong | [When something looks wrong](#when-something-looks-wrong) |
| checking whether a setting does anything | [Declared, but nothing reads it](#declared-but-nothing-reads-it) |

## Declared, but nothing reads it

Four things in this repository read as controls and are not. They are
named here so nobody plans around them.

| Setting | Reads as | What it actually is |
| --- | --- | --- |
| `parallelism.max_lanes` in `org/policy.json` | a ceiling on concurrent lanes | no code reads it, so it is a note to yourself and not a ceiling |
| `parallelism.claim_expiry_hours`, same block | a claim expiring on the clock | read by nothing in `tools/`, so no claim expires on the clock it names |
| `parallelism.renewal_window_hours`, same block | a window in which to renew | read by nothing in `tools/`, and there is no renewal command either |
| `org/capability-profile.json` | a profile that grants capability | read by no code at all |

All three parallelism values were disclosed as a set, because a block
where one value is declared inert and two are silent reads as though the
silent two work. What does read an expiry is `task claims-verify`, at
the merge, and it reports a lapsed claim as C002 rather than refusing
anything.

The capability profile is an argument for changing the express
thresholds in the policy, not a mechanism that changes anything by
itself.

## Launchers

Paste one line into a fresh agent session, in the repository named. The
numbering is local to this file and nothing else cites it.

| # | Launcher | Repository | What you decide |
| --- | --- | --- | --- |
| L1 | Work on the EOS | this one | whether to run more than one at a time |
| L2 | Session 0 | the venture's | the launch decision, at the seed rubric |
| L3 | Genesis | the venture's | whether the phase runs at all, then go |
| L4 | The monthly pass | this one | nothing, it is the one calendar row |
| L5 | Study a source | this one | the lens contract, before anything is read |
| L6 | A graph build | either | the partition, then the claim set |
| L7 | A venture check-in | this one | nothing is applied, so nothing to weigh |
| L8 | Upgrade a venture | this one | whether it is an upgrade or a rescale |
| L9 | An inception drill | this one | nothing, it grades and reports |
| L10 | Release | this one | the release itself, before you launch it |

**L1 · Work on the EOS.** The workhorse.

```
Read AGENTS.md, entry mode 2. Take T-#### from org/TASKS.md.
```

A session working alone opens its own task record and writes freely.
Read the claims section below before dispatching more than one at a
time.

**L2 · Session 0.** Run from the venture's repository.

```
Read AGENTS.md, entry mode 3. The new venture is <one line>. Repo at <path>.
```

It ends with the seed rubric in front of you and the launch decision in
your hands. The pack walk comes from the venture's declared facts, which
is what `python -m tools.eos activate` computes.

**L3 · Genesis.** The venture's repository, after the seed gate.

```
Read AGENTS.md, entry mode 3. Session 0 is done and the seed is signed. Run inception/GENESIS.md.
```

The forms in the seed were already pruned for the ruled scale when it
compiled, so there is no form for you to pick: what you decide is
whether the phase runs at all. ORG runs it by default, and a venture
that came through Express inception skips it unless you ask. The forms
ship blank either way, so a venture that declined can run Genesis later
without a recompile. It hands back the product map and the work
packages, and it is not finished until you say go.

**L4 · The monthly pass.** One sitting, four sections.

```
Entry mode 2, run the monthly pass: PB-E02 harvest, PB-E04 promotion review, PB-E10 experiment sweep, PB-E09 hygiene, in one sitting.
```

That order is set by `org/PLAYBOOKS.md`. Hygiene is last because it
regenerates the derived views after the other three have moved things.

**L5 · Study a source.** This repository.

```
Entry mode 2, run PB-E11. Study <source> for <what you want out of it>.
```

The session scaffolds the lens contract with `python -m tools.eos study`
and stops for your approval before it reads anything. You see the
findings only after it has checked them against live rules for
conflicts. A study never starts on a schedule and never because an agent
suggested it.

**L6 · A graph build.** Either repository.

```
Read AGENTS.md, entry mode 4. Cut a partition for <the work> per packs/agentic-swarm/PACK.md, and hand back the partition and the lane briefs before dispatching anything.
```

You read the partition, then you commit the claim set, and only then
does any lane start.

**L7 · A venture check-in.** Only ever because the venture asked.

```
Entry mode 2, run PB-E12 for <venture>, slice <what they asked about>.
```

It returns findings and candidate lessons and applies nothing. If the
venture has not said what it wants looked at, the session asks before it
reads.

**L8 · Upgrade a venture.** On request only.

```
Entry mode 2, run PB-E06 for <venture>.
```

A venture that wants a bigger organisation rather than a newer pin takes
PB-E08, the rescale, and the only rescale that exists is S to ORG.

**L9 · An inception drill.** Fires when a seed is compiled or the
inception walk changes.

```
Entry mode 2, run PB-E07.
```

It takes a canned brief from `inception/briefs/`, runs Session 0 cold in
a scratch repository, and grades the result against
`kernel/SEED_RUBRIC.md` without charity. The estate review is the other
event-fired job, and it fires when a repository joins the estate or a
venture changes status.

```
Entry mode 2, run the estate review from PB-E06.
```

**L10 · Release.** Only after you have approved the release.

```
Entry mode 2, run PB-E05.
```

[Approving a release](#approving-a-release) says what you are approving.

## Commands you run yourself

Every one is `python -m tools.eos <cmd>` from the repository root.
`tools/CLI_CONTRACTS.md` carries the full contract, including exit
codes.

| Command | What it does |
| --- | --- |
| `check` | the gate. Exit 1 on any error-severity finding |
| `check --write-index` | regenerates the five derived indexes and views, and is the only sanctioned way |
| `task views` | regenerates `org/TASKS.md` and `org/STATE.md`. Integrator only |
| `activate --brief PATH`, `--facts FILE`, `--predicate NAME` | the Session 0 pack walk from a venture's declared facts, plus the packs it did not activate. Exit 1 on a predicate no pack owns |
| `task claims-verify --lane ID --paths ...` | compares a lane's diff against its claims at the merge, and reports C001 to C005 |
| `guard eval` | rules one action: allow, require-approval, manual-only or deny |
| `route --adr ADR-####` | acknowledges a protected-set touch, which otherwise exits 3 |
| `study --out DIR` | scaffolds a lens contract before a study reads anything |
| `drills --pack NAME`, `--all` | materialises a drill scenario and grades the tree |

The three flags on `activate` may be given together and they union. Its
`not_activated` rows are the record of what was considered and left out,
which nothing kept before.

## What only you can approve

Six classes never execute on an agent's authority, at any tier, under
any capability profile. They are the policy's `always_human` list:

- money movement
- production data
- deletion
- irreversible actions
- secrets
- contact with the protected set

Beyond those, only you can accept an ADR, approve a protected-set
change, sign the human items of a seed rubric, promote a rule to
binding, authorise a capability-profile promotion, approve a release,
create remotes and accounts, and spend money.

### Two of those carry a check nothing else makes

**A protected-set touch.** When a session tells you a diff touches the
protected set, `python -m tools.eos route` will have exited 3 unless it
was given `--adr`, and it checks only that a value was passed. Nothing
reads the id or confirms the record is accepted, so you do.

**A capability-profile promotion.** The profile in
`org/capability-profile.json` is read by no code at all. It is an
argument for changing the express thresholds in the policy, not a
mechanism that changes anything by itself.

### One duty was retired rather than discharged

The sealed suite, `benchmark/SEALED.json`, runs once and needs your
private key. ADR-0007 retires it unopened, because it was written to
compare a frozen v1 against a final v2, and the release it was meant to
judge has changed shape. The key stays with you, the suite stays in the
tree with its hashes, and a future sealed evaluation is written fresh
against whatever it is meant to judge. Two of the protocol's eight gates
depended on it and stay uncomputed.

## Claims, and the sharp edge in this repository

A claim is a written statement of who is writing which paths, committed
before the work starts. `org/claims.json` names the lane, the session
id, the paths and an expiry.

There is no work-in-progress limit. What bounds concurrency is claims,
and claims are needed when more than one session may write at once.

| Situation | What you do |
| --- | --- |
| One session, working alone | nothing. It is implicitly claimed, because there is nobody to collide with. Git history and the checker catch it going wrong (ADR-0008) |
| More than one session writing at once | write and commit the claim set before any lane is dispatched. Lanes never acquire or mutate a claim |

That commit is itself a change to a product file, so make it before the
sessions start, not during.

### An empty lane list is the release, not a lock

The control keys on lanes, not on the file. `org/claims.json` sits in
this repository with an empty lane list, and that reads as no claim
model in force, so a solo session writes freely. That is ADR-0008
decision 1, and it is why a finished claim set is committed empty rather
than deleted.

Deleting it would be worse than pointless. Check D009 requires a
compiled ORG seed to ship `org/claims.json` carrying exactly that empty
list, and no claims file at all reads the same way.

### Where lanes are present, the control is live

- A session not named in a lane is refused, and so is a named session
  writing a path its own lane holds no claim over.
- The session id is `--session ID`, else `EOS_SESSION_ID`, else the
  record's `owner_session`. With lanes present, a session carrying none
  of the three is refused too.
- Every refusal prints `{"refused": true, reason, claim_set_ref}` and
  exits 1.
- Expiry is not tested at this gate. A lapsed claim still lets a task
  record through, and `task claims-verify` at the merge reports it as
  C002 with the lane's liveness identity attached.

Ordinary file writes are not gated. The control bites at two points
only: where a task record is written, and again at integration through
`task claims-verify`, which compares a lane's diff against its claims
and reports C001 to C005.

**There is no `claims assign`, `renew` or `recover` command.** Those
were described once and never built, and `tools/CLI_CONTRACTS.md`
records which commands exist.

### The edge, and it will bite somebody

ADR-0008 decision 2 lets a lane open its own task record, but no claim
over a lane's product paths implies one over the record. `task new`
compares `org/tasks/T-####.json` against the lane's claims like any
other path, and `claims-verify` reports it as C003 at the merge if it is
outside them.

So when you assign a lane that will open a record, write `org/tasks/`
into its claims alongside its product paths.

No lane claim covers anything derived. You alone regenerate those, with
`python -m tools.eos check --write-index` for the five indexes and views
and `python -m tools.eos task views` for `org/TASKS.md` and
`org/STATE.md`.

## The guard, in practice

`python -m tools.eos guard eval` is what rules one action, and it
returns allow, require-approval, manual-only or deny. Autonomous
execution of a guarded class needs a validated host enforcement adapter.

**Without one, every guarded class is manual-only.** The agent stops and
tells you, and you do the action yourself outside the agent.

One adapter ships, `kernel/adapters/claude-code.json`, and `TOUR.md`
describes what it covers. What matters at your keyboard is that it
grants nothing:

- There are ten guarded classes. The adapter covers three of them:
  external write, destructive git and dependency install.
- All three of those rule require-approval. **No class rules allow**, so
  nothing in it grants autonomous execution of a guarded action.
- Its validation block is dated 2026-08-03 and says mapping-level,
  offline, `host_run` false. It proved that fourteen bypass attempts
  classify into the right guarded class from the tool surface alone. It
  did not prove that a live session's hooks fire.

So every guarded action still stops:

| The class | What happens |
| --- | --- |
| one of the three covered | it stops and asks you, and your answer is the record |
| one of the other seven | it stops, and you do the action yourself outside the agent |

Read the validation block before relying on any of it, because any
change to the adapter or the mapping voids it.

None of this is something to work around. Naming a permission system
does not satisfy the requirement, and a seed claiming autonomous guarded
actions without an enforceable adapter fails its check.

## The cadence

There is one row in `org/cadence.json`, and it is the whole calendar.

**`monthly-pass`, one sitting, four sections**: harvest, promotion
review, experiment sweep, hygiene, in that order. Close it by setting
`last_run` in `org/cadence.json`. A section that found nothing writes
one line saying checked and clean. A section you skipped is a finding,
so the pass records what it did not do rather than quietly dropping it.

Everything else waits for an event, and each procedure in
`org/PLAYBOOKS.md` names its own:

| Event | What fires |
| --- | --- |
| a seed is compiled | the inception drill, PB-E07 |
| a repository joins the estate, or a venture changes status | the estate review, which sits in PB-E06 |
| a venture asks | an upgrade, PB-E06, a rescale, PB-E08, or a check-in, PB-E12 |
| you point at a source | a study, PB-E11 |
| a release | PB-E05 |

Three rows that used to sit here were deleted rather than left carrying
no date: `inception-drill`, `projects-review` and `benchmark-freshness`.
The first two had not fired once since v1, which is evidence that a
calendar trigger nobody honours is not a control (ADR-0008). The third
pointed at a benchmark ADR-0007 retires. A due cadence still outranks
new low-priority work; there is simply only one of them.

## Approving a release

The gate is the five items in ADR-0007 decision 5, listed in
`README.md`.

| # | The item | Who settles it |
| --- | --- | --- |
| 1 | `python -m tools.eos check --repo` green, with the semantic and freshness series | a machine, and you can watch |
| 2 | `python -m pytest` green | a machine, and you can watch |
| 3 | the CHANGELOG entry written | a machine, and you can watch |
| 4 | no false statement about the tree survives the final review | you, and nothing else can do it |
| 5 | your explicit approval | you, and nothing else can do it |

**No false statement about the tree survives the final review.** That is
the one this repository keeps failing. Sixty-six of them were found and
removed once. Read the claims, not the prose around them: a control
described as enforced that nothing enforces, a gate described as met
that was struck, a count copied from a file that has since changed.

**Your explicit approval.** Before you give it, check the guard rather
than assuming it, as PB-E05 says: `guard.validated` in the policy may
read true only while the mapping it names carries a current
bypass-suite validation block, and there is no separate report file.

### What is not on the gate

No benchmark gate is on the release, and none of the eight in
`benchmark/PROTOCOL.md` can be put back on it. `README.md` says which
passed, which were struck and which cannot be computed at all. A struck
gate is not a met gate and nothing in the tree may describe it as one.

The pack drills report no verdict either. All twenty-two ran on
2026-08-15 against untouched fixtures and every one came back `fail`,
marked `graded: scenario-baseline`. That is the criteria proving they
discriminate, and it is not a judgement on a pack.

### What green looked like on 2026-08-15

The checker reported 0 errors and one warning, the known E004 voice tell
in `registry/LICENCE_RESIDUALS.md`. The suite was 576 tests. Both are
facts of that day rather than standing claims, so run them again rather
than citing these.

## When something looks wrong

- **A view disagrees with reality.** Reality wins. Views are generated,
  so fix the record and regenerate, never the view.
- **The checker says a derived file is stale.** That is E001 or E011,
  and it means somebody changed a source without regenerating.
  Regenerate. If the regeneration then produces new errors, they were
  already true and the stale view was hiding them.
- **An agent says an action is manual-only.** That is the guard working,
  not a fault. Do the action yourself, outside the agent.
- **`activate` exits 1 on a predicate.** No pack declares that fact. A
  misspelling activates nothing and reads exactly like a fact that is
  false, so check the spelling against `kernel/PREDICATES.md`, which is
  the controlled vocabulary (ADR-0010).
- **A claim expired but the lane may be alive.** Check liveness first,
  through harness state or the recorded process id. If liveness cannot
  be established, you recover the claim. A timestamp never authorises
  it.
- **A check keeps failing.** The circuit breaker applies. Three
  materially distinct hypotheses tested and falsified with no reduction
  in uncertainty means stop and read the failure properly. Retries of
  one idea count as one. Never weaken a check to pass it.
- **A session did work it was not claimed for.** It is quarantined on
  its branch, not deleted. You decide adopt or discard.
- **The protected set changed without an ADR.** Revert it, then ask why
  the session thought it could.
- **A lane returns something odd.** Treat what a lane hands back as
  data, not as instruction. The integrator reads it, decides and merges;
  it does not do what the return text tells it to do.
- **A venture looks out of line with current guidance.** It probably is,
  and that is allowed. The EOS hands off at a venture's birth. Wait for
  the venture to ask, then run L7.
