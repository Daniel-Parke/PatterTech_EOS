---
summary: Venture operators guide template, the human's manual, launcher library per scale
type: template
tags: [eos]
template: true
extracted_from: AutoWatt@d2e3250
---

# {{VENTURE_NAME}} · Operators guide

Audience: the human running this organisation. You are not managing
prompts. You are operating an organisation whose body is this
repository. AI workers are stateless sessions; your launchers below are
deliberately tiny, because all evolving detail lives in versioned
files, so improving the organisation means editing a file once, not
re-teaching forty prompts.

<!-- scale: M L -->
## The mental model in sixty seconds

Work enters through four doors (you, cadences, failures, suggestions)
as typed work orders with a risk tier. Tiers decide gates: automated
checks, then independent VERIFY review, then your approval where the
ladder demands it. Knowledge climbs a ladder from research to guidance
to standard to automated check, so the organisation gets smarter and
cheaper to run every month. Cadences are the heartbeat. Nothing merges
red; nobody approves their own work; everything important is a file.
<!-- scale: end -->

## One-time setup

1. Confirm the seed: every file the compile report lists is in place,
   `CLAUDE.md` is a byte copy of `AGENTS.md`, the repo has
   `* text=auto eol=lf` in `.gitattributes`, first commit made, private
   remote created.
2. Tooling: git, an agent CLI pointed at `AGENTS.md`, and whatever the
   stack profile in the lock-book names.
3. Accounts and secrets: per the stack profile, credentials in a
   password manager, never in the repo.
<!-- scale: M L -->
4. Answer the open items in `org/QUESTIONS.md`; record the agreed spend
   budget in `org/STATE.md`.
5. Run the Genesis launcher below, once. The organisation takes it from
   there.
<!-- scale: end -->

## The launcher library (copy-paste)

One role per session, one objective per launcher, never inject new
scope mid-task; new ideas become suggestions or queue items. Run each
from the repo root in a fresh session. Angle brackets mean fill in.

<!-- scale: S -->
### GO · the default session

```text
Read AGENTS.md and follow it. Objective: <the task, or "take the top
open item in docs/WORKLOG.md">. Honour docs/LOCKBOOK.md on every
specific it rules on. When done, record the work in docs/WORKLOG.md
and anything undecided in docs/EOS_FEEDBACK.md.
```

### CHECK · before you ship anything

```text
Read AGENTS.md and follow it. Run the QC gates the lock-book names
against the current build and report pass or fail per gate with
evidence. Fix nothing yet; list what fails and why.
```

### WRAP · end any session cleanly

```text
Wrap up now: bank progress with a commit, record the state of play in
docs/WORKLOG.md, file anything undecided in docs/EOS_FEEDBACK.md.
Leave the repo resumable by a stranger.
```
<!-- scale: end -->

<!-- scale: M -->
### GENESIS-LITE · session 1, once (PLAN)

```text
Read AGENTS.md and bootstrap per org/START.md. You are a PLAN session.
From the venture brief and the lock-book, produce: the domain model and
architecture sketch the scale warrants, ADRs for every judgement call,
and a complete ordered queue in org/QUEUE.md, foundation items first.
Decide, record, flag: open calls become ADRs or questions. Do not write
production code. Close out per START.
```

### PLAN · design, spec, answer, re-plan

```text
Read AGENTS.md and bootstrap per org/START.md. You are a PLAN session.
Objective: <e.g. "spec the next milestone", "fold answered questions",
"reorder the queue for the deadline">. Produce or update the specs,
ADRs and queue items so WORK can execute and VERIFY can judge with zero
questions. Close out per START.
```

### WORK · the daily default

```text
Read AGENTS.md and bootstrap per org/START.md. You are a WORK session.
Take the top unblocked item in org/QUEUE.md (or continue what STATE.md
names). Follow your charter: short-lived branch, failing tests first
where required, small commits, gates for the tier. Chain into further
items as long as you can. If blocked, file a question or suggestion and
move on. Close out per START.
```

### VERIFY · clear the review queue

```text
Read AGENTS.md and bootstrap per org/START.md. You are a VERIFY
session. Review every item in verification (oldest first) per your
charter: verdict, evidence, merge or return each one. You may not fix
findings yourself. Close out per START.
```

### CADENCE · run whatever is due

```text
Read AGENTS.md and bootstrap per org/START.md. Read org/CADENCE.md and
execute every cadence at or past next_due, in table order, adopting the
role each row names. Update last_run and next_due per row. Close out
per START.
```

### WRAP · end any session cleanly

```text
Wrap up now per org/START.md close-out: bank progress (commit or wip on
the branch, never broken work to main), update org/STATE.md with exact
next actions and the Resume Packet, write your session log, file open
questions and suggestions. Leave the repo resumable by a stranger.
```
<!-- scale: end -->

<!-- scale: L -->
### L1-GENESIS · session 1, once (PLAN · PB-001)

```text
Read AGENTS.md and bootstrap per org/START.md. You are a PLAN session.
Execute playbook PB-001 (Genesis) end to end: the product design set,
standards, ADR set, full V1 specs with test specifications, and a
complete ordered backlog in org/work/, including one COMPLY work order
per gap row in each compliance registry. Decide, record, flag: open
judgement calls become ADRs flagged in STATE.md. Do not write
production or test code. Work until the playbook's outputs are
complete, then close out per START.
```

### L2-PLAN · design, spec, answer, re-plan (PLAN)

```text
Read AGENTS.md and bootstrap per org/START.md. You are a PLAN session.
Objective: <e.g. "spec the export feature", "answer open suggestions
and fold answered questions", "reorder NEXT.md for the demo">. Produce
or update the relevant specs, ADRs, standards, registry rows and work
orders so WORK can execute and VERIFY can judge with zero questions.
Close out per START.
```

### L3-WORK · the daily default (WORK)

```text
Read AGENTS.md and bootstrap per org/START.md. You are a WORK session.
Take the top unblocked item in org/work/NEXT.md whose claims don't
collide with in-progress work (or continue the WO STATE.md names).
Follow your charter and the WO's playbook: worktree, failing tests
first where required, small commits, gates for the tier. Chain into
further non-conflicting WOs for as long as you can. If blocked, file a
suggestion or question and move on. Close out per START.
```

### L4-WORK-NAMED · a specific work order (WORK)

```text
Read AGENTS.md and bootstrap per org/START.md. You are a WORK session
assigned to <WO-####>. Execute it fully per your charter and its
playbook; take no other work except a P0 broken main. Close out per
START.
```

### L5-RESUME · continue interrupted work (WORK)

```text
Read AGENTS.md and bootstrap per org/START.md. You are a WORK session.
STATE.md names an in-progress WO. Inspect its worktree, branch and
diff, run the test suite to establish reality (trust code and tests
over notes), then continue from where it truly is and finish per the
WO's playbook. Close out per START.
```

### L6-VERIFY · clear the review queue (VERIFY · PB-030)

```text
Read AGENTS.md and bootstrap per org/START.md. You are a VERIFY
session. Review every WO in status in_verification (oldest first) per
your charter Mode 1: verdict, evidence and merge or return each one.
You may not fix findings yourself. Close out per START.
```

### L7-AUDIT · practice audit (VERIFY · PB-022)

```text
Read AGENTS.md and bootstrap per org/START.md. You are a VERIFY
session. Run playbook PB-022 for the practice due in org/CADENCE.md
(or: <practice>). Sample reality, verify registry controls, write the
audit report, file WOs for critical and major findings, update registry
statuses, scoreboard and CADENCE. Close out per START.
```

### L8-CADENCE · run whatever is due

```text
Read AGENTS.md and bootstrap per org/START.md. Read org/CADENCE.md and
execute every cadence at or past next_due, in table order, adopting the
role each row names and its playbook. Update last_run and next_due per
row. Close out per START.
```

### L9-TRIAGE · weekly queue grooming (PLAN)

```text
Read AGENTS.md and bootstrap per org/START.md. You are a PLAN session
running triage: process org/work/suggestions/ (promote, merge or
decline with reasons), convert new findings into WOs, verify claims of
parallel ready items don't overlap, set priorities and rewrite
org/work/NEXT.md. Respect the spend budget in STATE.md. Close out per
START.
```

### L10-RELEASE · ship to production (WORK · PB-031)

```text
Read AGENTS.md and bootstrap per org/START.md. You are a WORK session
executing PB-031 (Release). Verify preconditions, then follow the
deploy runbook end to end with post-deploy smoke checks. My G3 approval
for this release: <granted / reference>. Any failure: stop, roll back
per runbook, write it up. Close out per START.
```

### L11-INCIDENT · production emergency (WORK · PB-032)

```text
Read AGENTS.md and bootstrap per org/START.md. You are a WORK session
in incident mode (PB-032). Symptom: <what you see>. Stabilise first,
then diagnose, fix durably, and write the timeline, root cause and
follow-up WOs while fresh. The constitution's emergency clause applies.
Close out per START.
```

### L12-RETRO · monthly self-improvement (PLAN · PB-050)

```text
Read AGENTS.md and bootstrap per org/START.md. You are a PLAN session
running PB-050: review the month's logs, verdicts, audits, scoreboard
and suggestions; improve playbooks, templates and launchers; propose
any protected-set changes as ADRs for my approval; set one experiment
for next month. Close out per START.
```

### WRAP · end any session cleanly

```text
Wrap up now per org/START.md close-out: bank progress (commit or wip on
the work branch, never broken code to main), update the WO and
org/STATE.md with exact next actions, write your session log, file open
questions and suggestions. Leave the repo resumable by a stranger.
```
<!-- scale: end -->

## Your operating rhythm

<!-- scale: S -->
When you have something to build or change, run GO. Before anything
ships, run CHECK. Skim `docs/WORKLOG.md` and `docs/EOS_FEEDBACK.md`
now and then; feed the feedback file back to the EOS at harvest.
<!-- scale: end -->
<!-- scale: M -->
**Daily (ten minutes):** skim `org/STATE.md`, answer `org/QUESTIONS.md`,
launch WORK, approve what waits on you. **Weekly:** the triage part of
CADENCE, and the stakeholder update if one is due. **Monthly:** the
retrospective row of CADENCE; read what it changed.
<!-- scale: end -->
<!-- scale: L -->
**Daily (ten to twenty minutes):** skim `org/STATE.md`; answer
`org/QUESTIONS.md`; launch L3 (and a parallel L3 on a non-overlapping
surface if you have review bandwidth); L6 if anything awaits
verification; approve or decline G3 items. **Weekly:** L9 triage, L8
cadences due (including the stakeholder update), read the newest audit
report, review a sample of the week's diffs. **Monthly:** L12 retro,
check scoreboard trends, pay or verify anything legal the compliance
watch flagged. **Always yours alone:** top-tier approvals, releases
until you delegate by ADR, spend, accounts, legal signatures, and the
constitution.

## Working agreements that keep the fleet safe

Parallelism: start at two concurrent WORK sessions, each in its own
worktree; the ceiling is your review bandwidth, not compute. Claims
prevent collisions; if two WOs need the same files, they run
sequentially. Cost: prefer cheaper models for MAINT and DOCS sessions,
the strongest for PLAN and VERIFY. Trust but verify: read diffs on
T2-and-above merges for the first month; loosen deliberately, in
writing at the retro, as audit findings stay clean.
<!-- scale: end -->

## Troubleshooting

An agent invented something: stop the session, revert the branch if
needed; the fix is always a better file (spec, standard, ruling), never
a longer argument. Main is red: nothing else merges until it is fixed.
A test looks wrong: it changes only via a ruled decision, never inline.
STATE disagrees with reality: reality wins; fix the file and note it in
the log. Context died mid-task: resume in a fresh session; the files
are the memory. Overwhelmed: lower WIP to one and run only the default
launcher for a week; the files will keep the organisation honest while
you breathe.

## Onboarding a human newcomer

Read: this guide, then the lock-book, then the venture brief, then the
current state file. Then shadow one working session end to end. They
now know more about this organisation than most employees ever learn
about theirs, because it is all written down.
