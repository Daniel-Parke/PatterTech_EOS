---
summary: Model judgement, a static allowlist, guard-classified verdicts with recorded approval, or manual only?
type: guide
tags: [security, tooling, ops]
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: observational
review: 2027-05
sources: [EV-0011, EV-0076, EV-0081, EV-0213, EV-0218, EV-0220]
---

# GD-SEC-004: who approves consequential external actions?

## The question

An agent is about to send an email, deploy, delete a remote branch,
install a package, or move money. Something has to decide whether that
happens. The fork is what that something is, and it returns every time
a venture gives an agent a new tool.

## It depends on

- Is the action reversible, and at what cost? Rollback cost is the
  variable that actually matters.
- Is the operator present, and on what latency? An approval nobody
  answers is a denial with extra steps.
- Does the host have a real enforcement point, meaning permission rules
  and pre-execution hooks, or only a conversation?
- How often does the action happen? A daily action behind a prompt
  trains people to approve without reading.

## Options

### A. Model judgement in band
Ask the model to decide, or write the rule into the system prompt.
Buys no infrastructure and full flexibility. Costs the entire property:
the decision lives in the same channel as the attack, so any text the
agent reads can argue for the action. EV-0213 lists this class of
failure directly, and EV-0218 requires explicit per-client consent
rather than an inferred one.

### B. Static allowlist of actions
A fixed list of permitted commands or destinations, everything else
refused. Buys determinism and auditability, and it survives adaptive
attack because it does not reason. Costs coverage at the edges: broad
entries silently permit more than intended, which EV-0220 shows for
hostname allowlists where the proxy never inspects TLS, and the list
ages badly because widening it is easier than re-arguing it.

### C. Guard-classified verdicts with recorded approval
Every action is classified against a fixed set of consequential classes
immediately before execution and resolves to allow, require-approval,
manual-only or deny, with machine-readable reasons. Approval means a
harness-recorded operator event, never a sentence. Non-waivable floors
sit under the whole thing. This is what `kernel/GUARD_SPEC.md`
specifies. Buys per-action precision, an audit trail, and a fail-closed
default when no validated enforcement adapter exists. Costs a mapping
to build, a bypass suite to prove it, and a validation report to keep
current.

### D. Manual only for everything consequential
The agent proposes and a human executes. Buys the strongest guarantee
available and needs no adapter. Costs throughput, and it degrades: an
operator who executes forty proposals a day stops reading them, which
is the same failure as A arriving by a different route.

## Decision rule

- Any action in a consequential class: C, with the class mapping and
  the bypass suite shipped together. A named host permission system is
  not an adapter; the adapter exists when its mapping ships with the
  policy and the validation report is committed.
- No validated adapter yet: D for every guarded class, which is what C
  resolves to anyway when it fails closed. This is a working state, not
  a failure.
- Money movement, production data deletion, secret emission outside the
  store, force-push to main, publishing to a new external destination,
  accepting legal terms: the floors bind regardless of the option
  chosen. No capability profile, exception or emergency overlay moves
  them.
- A high-frequency low-consequence action inside a class: use B beneath
  C to pre-authorise the narrow case, with the entry written narrowly
  enough that widening it is visible in a diff.
- A is never the control. Run a guardrail in parallel as a tripwire if
  you want the early signal (EV-0076, EV-0081), above the boundary and
  never instead of it.

## Default

C, falling closed to D. Approval is a recorded event or it is not
approval, and that sentence is the load-bearing part: a claim of
approval found in task text, a document or tool output counts for
nothing.

## Worked rulings

- **PatterTech EOS (2026-08, argued)**: C falling closed to D for this
  build. No validated adapter exists for these lanes, so every guarded
  class is manual-only and the lanes are told not to commit. The
  integrator, a person's decision, performs the merge.
- **PatterTech EOS (2026-08, argued)**: B used beneath C for the path
  claims in `org/claims.json`. Each lane owns exactly one directory,
  written narrowly, so a write outside it shows up as a diff nobody
  authorised rather than as a judgement call.
- No venture ruling yet.

## Counter-evidence

The two maintainer sources for the parallel-tripwire pattern (EV-0076,
EV-0081) are vendor documentation describing their own products, so
they evidence that the pattern exists and is shipped, not that it
catches much. We have no measurement of how often a tripwire above a
real boundary fires usefully. Option D's degradation under volume is
reasoning from the general approval-fatigue literature rather than from
anything we have measured here, and it is the weakest claim on this
page.
