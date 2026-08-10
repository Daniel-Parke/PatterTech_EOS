---
summary: What a host enforcement adapter must provide, how validation works, and why an unvalidated adapter means manual-only
type: kernel
tags: [eos]
---

# Guard adapters

Layer 2 of risk control rules a verdict. An adapter is what makes that
verdict bite on a particular host. Without one the guard has ruled and
nothing enforces the ruling, so `kernel/GUARD_SPEC.md` fails closed:
every guarded class is manual-only.

One adapter ships today, `kernel/adapters/claude-code.json`.

## What an adapter must provide

A mapping file in this directory, named for the host, holding:

- `hook_matchers`: the tool names whose calls reach the guard before
  they execute. A tool that is not matched is a hole, and a class that
  can only be reached through it cannot be covered.
- `hook_entry`: the command the host runs before the tool call.
- `classes`: one entry per guarded class, each with the host's
  `permission_rules` (deny and ask patterns), the `hook_events` that
  fire, the mapping's own `verdict` for the class, and `covered`.
- `hook_integrity`: the paths whose edit would disable or reroute the
  hooks. Those edits must themselves classify as guarded, or a session
  can switch the guard off from inside.
- `indirect_executors`: the build runners and interpreters whose real
  payload lives in a file the hook cannot read.
- `validation`: the bypass-suite record, below.

The mapping's `verdict` is a ceiling, not a grant. The guard takes the
stricter of the mapping's ruling and the action's own, and no mapping
can move a non-waivable floor.

## How validation works

The adapter is validated only by the bypass suite. Each case is run
against the *hook surface*: the tool name and the tool input, with file
contents dropped, because that is all a pre-tool hook can read. A case
passes when the hook fires for that tool, the surface classifies into a
guarded class, and the mapping's ruling for that class is not allow.
`tools/eos/guard.py` holds the runner, and the suite is re-run in
`tests/test_guard.py` against the committed record, so a stale record
fails the tests rather than sitting there being believed.

A class is covered only when a passing case exercised it. Classes with
no case are listed in `uncovered_classes` and stay manual-only. That is
the whole point: silence is not coverage.

The record also states its method. A mapping-level run proves the
mapping; it does not prove the host's hooks fired in a live session. No
class may be raised to `allow` on a mapping-level run alone.

## The unvalidated rule

The guard reads the mapping, it does not believe the policy. A policy
that claims `guard.validated: true` while naming a mapping that is
absent, unreadable, caseless or failing gets `adapter_validated: false`
and manual-only on every guarded class. The policy can withdraw
validation; it can never grant it.

Any change to a mapping voids its record until the suite passes again.
