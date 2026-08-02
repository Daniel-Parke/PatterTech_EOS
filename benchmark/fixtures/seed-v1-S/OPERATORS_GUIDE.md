---
summary: Herbfield Lane operators guide, the sole trader's manual and S-scale launcher library
type: template
tags: [eos]
compiled_from: kernel/templates/OPERATORS_GUIDE.tpl.md
---

# Herbfield Lane · Operators guide

Audience: the human running this organisation. You are not managing
prompts. You are operating an organisation whose body is this
repository. AI workers are stateless sessions; your launchers below are
deliberately tiny, because all evolving detail lives in versioned
files, so improving the organisation means editing a file once, not
re-teaching forty prompts.

## One-time setup

1. Confirm the seed: every file the compile report lists is in place,
   `CLAUDE.md` is a byte copy of `AGENTS.md`, the repo has
   `* text=auto eol=lf` in `.gitattributes`, first commit made, private
   remote created.
2. Tooling: git, an agent CLI pointed at `AGENTS.md`, and whatever the
   stack profile in the lock-book names.
3. Accounts and secrets: per the stack profile, credentials in a
   password manager, never in the repo.

## The launcher library (copy-paste)

One role per session, one objective per launcher, never inject new
scope mid-task; new ideas become suggestions or queue items. Run each
from the repo root in a fresh session. Angle brackets mean fill in.

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

## Your operating rhythm

When you have something to build or change, run GO. Before anything
ships, run CHECK. Skim `docs/WORKLOG.md` and `docs/EOS_FEEDBACK.md`
now and then; feed the feedback file back to the EOS at harvest.

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
