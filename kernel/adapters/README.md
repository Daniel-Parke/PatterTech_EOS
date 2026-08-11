---
summary: The shape of a guard adapter mapping file, key by key, and where each rule about it is written
type: kernel
tags: [eos]
---

# Guard adapters

Layer 2 of risk control rules a verdict. An adapter is what makes that
verdict bite on a particular host. `kernel/GUARD_SPEC.md` holds every
rule about adapters: fail closed without one, coverage per class, the
mapping's ruling as a ceiling, and the policy that can withdraw
validation but never grant it. This file holds one thing, the shape of
the mapping file itself.

One adapter ships today, `kernel/adapters/claude-code.json`.

## The mapping file

Named for the host, in this directory, holding:

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
- `validation`: the bypass-suite record. Cases with their results, the
  `covered_classes` and `uncovered_classes` lists, the date, and
  `method` with `host_run`, because a mapping-level run proves the
  mapping and not that the host's hooks fired in a live session.

`tools/eos/guard.py` holds the suite runner and `tests/test_guard.py`
re-runs it against the committed record. A mapping edited without
re-running it fails the tests.
