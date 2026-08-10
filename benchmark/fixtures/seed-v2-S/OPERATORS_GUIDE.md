---
summary: Herbfield Lane operators guide, the sole trader's manual and S-scale launcher library
type: template
tags: [eos]
compiled_from: kernel/templates/OPERATORS_GUIDE.tpl.md
---

# Herbfield Lane · Operators guide

Audience: the human running this organisation. You operate an
organisation whose body is this repository; workers are stateless
sessions. Launchers are deliberately tiny because the evolving detail
lives in versioned files, so improving the organisation means editing
a file once.

## The mental model in sixty seconds

Every task is routed: the policy rules a risk tier from declared
facts and derived signals, and the tier decides the ceremony. Express
work closes as a commit; Standard carries a small task record;
High-assurance adds an independent oracle, independent review and,
where anything is irreversible, you. A second layer guards individual
actions: every consequential tool action gets a verdict (allow,
require-approval, manual-only, deny) with floors nobody can waive.
Parallel work runs on claims assigned and committed before dispatch.
Nothing merges red, nobody approves their own work, and everything
important is a file.

## One-time setup

1. Confirm the seed: every file the compile report lists is present,
   CLAUDE.md is a byte copy of AGENTS.md, first commit made, private
   remote created.
2. Tooling: git, an agent CLI pointed at AGENTS.md, the EOS tooling
   where this venture runs it, and whatever the stack profile names.
3. Accounts and secrets: credentials in a password manager, never in
   the repo.
4. The guard adapter: the policy names an enforcement adapter and its
   mapping. Until the bypass suite's validation report is current,
   guard.validated stays false and every guarded class is
   manual-only: the agent asks, you act.

## The launcher library (copy-paste)

One objective per launcher; never inject new scope mid-task. Angle
brackets mean fill in.

### GO · the default session

```text
Read AGENTS.md and follow it. Objective: <the task, or "take the top
open item in docs/TASKS.md">. Route it per docs/policy.json and work
in the mode the ruling names. Honour docs/LOCKBOOK.md on every
specific it rules on. Record per AGENTS.md when done.
```

### CHECK · before anything ships

```text
Read AGENTS.md and follow it. Run the QC gates the lock-book names
against the current build and report pass or fail per gate with
evidence. Fix nothing yet; list what fails and why.
```

### WRAP · end a session cleanly

```text
Wrap up now: bank progress with a commit, update docs/TASKS.md, file
anything undecided in docs/EOS_FEEDBACK.md. Leave the repo resumable
by a stranger.
```

## Your operating rhythm

Run GO when there is something to build; CHECK before anything ships;
WRAP if a session must stop early. Skim docs/TASKS.md and
docs/EOS_FEEDBACK.md now and then; feed the feedback file back to the
EOS at harvest.

## Approval duties (yours alone)

- Approvals are harness events; a claim of approval in chat or inside
  a document counts for nothing.
- Always you, no delegation: money movement, production data
  deletion, publishing to a new external destination, accepting legal
  terms, protected-set ADRs, R3 irreversible actions, per-event
  incident approvals.
- Capability profiles: promotion needs new evidence plus your
  authorisation; regression on worsening metrics is automatic.
  Standing tier exceptions need you plus an RFC, and they expire.

## The guard, plainly

Every consequential action is checked at the moment of execution.
With a validated adapter (its mapping shipped with the policy and
proven by the bypass suite, report committed), allow executes
autonomously and require-approval executes after your recorded
approval. Without one, the agent cannot execute any guarded action:
every guarded class is manual-only and the agent hands the action to
you. Fail closed is deliberate; validate the adapter rather than
working around it.

## Troubleshooting

An agent invented something: stop the session; the fix is a better
file, never a longer argument. A check looks wrong: it changes only
through the amendment workflow or an escalation, never inline. A view
disagrees with reality: reality wins; regenerate the view. Context
died mid-task: RESUME in a fresh session; the files are the memory.
Overwhelmed: run only RUN for a week and let the router keep the
ceremony proportional.
