---
summary: The action-time guard, ten guarded classes, four verdicts, non-waivable floors, fail closed
type: kernel
tags: [eos]
---

# GUARD_SPEC

Layer 2 of risk control. Every consequential tool action is evaluated
immediately before execution, regardless of the task's tier. Each
evaluation is one document validated by
`kernel/schemas/guard-action.schema.json`.

## The ten guarded classes

1. **external-write**: network sends, publishing, email, API mutations.
2. **deployment**: shipping anything to a running environment.
3. **deletion**: beyond the working tree, including remote refs and data.
4. **destructive-git**: force-push, branch deletion, history rewrite,
   tag deletion.
5. **dependency-install**: package installation and install scripts.
6. **production-data**: access to or mutation of production data.
7. **secrets**: access to or emission of secret material.
8. **pii-egress**: personal data leaving its sanctioned boundary.
9. **money-movement**: any transfer or commitment of funds.
10. **irreversible**: any action declared irreversible on the task.

## The four verdicts

- **allow**: executes autonomously, and only through a validated host
  enforcement adapter.
- **require-approval**: executes only after a harness-recorded operator
  approval event. A claim of approval in prose or in data counts for
  nothing; only the recorded event does.
- **manual-only**: the agent cannot execute this under any approval. An
  authorised operator may perform the action outside the agent.
- **deny**: forbidden through this workflow entirely. Changing that is
  a governance decision, not an operational one.

Every verdict carries machine-readable reasons.

## Non-waivable floors

No reviewer, capability profile, exception or emergency overlay can
downgrade these. They bind in every mode, at every tier, always.

| Action | Floor verdict |
| --- | --- |
| money movement | manual-only |
| production data deletion | manual-only |
| key or secret emission outside the sanctioned store | deny |
| force-push to main or deletion of main | deny |
| publishing to a new external destination | manual-only |
| accepting legal terms | manual-only |

## Unknown actions

An action the mapping does not recognise resolves to require-approval
at minimum. An unrecognised action that falls inside a guarded class
resolves to manual-only. The guard never guesses an allow.

## Fail closed

Allow and require-approval are honoured autonomously only through a
validated host enforcement adapter. Without one, the agent has no
capability to execute guarded actions: every guarded class is
manual-only.

Naming a host permission system is not an adapter. An adapter exists
only when its mapping is shipped with the policy
(`guard.mapping_ref`), its behaviour is proven by the bypass suite, and
the validation report is committed. Seed validation fails any venture
that claims autonomous guarded actions without shipping the mapping it
names. It does not read that mapping's validation record; the
bypass-suite proof binds at action time, in the guard, which rules
manual-only on a mapping that is caseless or failing.

The guard reads the mapping rather than believing the policy. A policy
that claims validation while naming a mapping that is absent,
unreadable, caseless or failing rules manual-only on every guarded
class. A policy can withdraw validation; it can never grant it.

## Coverage is per class, not per adapter

A validated adapter does not lift every class at once. A guarded class
is covered only where a passing bypass case exercised it, and every
other class stays manual-only under exactly the same fail-closed rule.
The mapping's ruling for a class is a ceiling: the guard takes the
stricter of that ruling and the action's own, and no mapping moves a
floor.

## Claude Code adapter mapping

`kernel/adapters/claude-code.json` is the shipped mapping and
`kernel/adapters/README.md` is the contract every adapter meets. As
validated on 2026-08-03, three classes are covered (external-write,
destructive-git, dependency-install) and each rules require-approval,
so a guarded action still resolves on a recorded operator event. The
remaining seven classes have no case in the suite and stay manual-only.
No class rules allow, because the run was mapping-level rather than a
live host session.

The mapping combines permission rules with hooks, per class:

- **Permission rules** deny-by-default for the tools that can reach
  each class: network-capable tools for external-write and pii-egress,
  shell for destructive-git, deletion and dependency-install, file
  tools for secrets paths.
- **PreToolUse hooks** classify each tool call against the ten classes
  before execution and return the verdict: block for manual-only and
  deny, surface the approval prompt for require-approval, pass for
  allow.
- **Approval events** come from the harness's own permission flow, so
  require-approval resolves on a recorded operator action, never on
  conversation content.
- **Hook integrity**: the hooks configuration is itself a guarded
  surface; edits to it classify as destructive by default.

## Bypass test suite contract

The adapter is validated only by the bypass suite, which must exercise
at least:

- nested shells and shell-in-shell invocations,
- subprocess spawns from scripts and interpreters,
- package install scripts (npm postinstall, pip build hooks),
- indirect network calls (curl inside make, git remotes from scripts),
- attempts to disable, rewrite or route around the hooks.

A class the suite cannot demonstrate as enforced stays manual-only. The
suite's results form the adapter validation report; `guard.validated`
may be true only while that report is current, and any adapter or
mapping change voids it until the suite passes again.

Cases run against the hook surface: the tool name and the tool input,
with file contents dropped, because that is all a pre-tool hook reads.
A build runner whose payload sits in a Makefile therefore classifies by
the conservative fallback rather than by its inner command, which
lowers the precision of the class, never the strictness of the ruling.
