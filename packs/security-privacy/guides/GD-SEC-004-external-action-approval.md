---
id: GD-SEC-004
summary: Model judgement, a static allowlist, guard-classified verdicts with recorded approval, or manual only?
kind: wargame
type: wargame
tags: [eos, ops, security, tooling, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-SEC-006]
applies_when: [runs_agents]
engages_when: [operator_requests_wargame]
consequence: high
relations: []
always_walk: true
scope: estate
authority: default
basis: decision
evidence_grade: observational
sources: [EV-0011, EV-0076, EV-0081, EV-0213, EV-0218, EV-0220]
review: 2027-05
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-SEC-004: who approves consequential external actions?

## Decision question and stakes

An agent is about to send an email, deploy, delete a remote branch,
install a package, or move money. Something has to decide whether that
happens. The fork is what that something is, and it returns every time
a venture gives an agent a new tool.

## Doctrines or coverage gap under pressure

- `DOC-SEC-006` (binding): Consequential external actions wait for a harness-recorded operator approval immediately before execution.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Is the action reversible, and at what cost? Rollback cost is the
  variable that actually matters.
- Is the operator present, and on what latency? An approval nobody
  answers is a denial with extra steps.
- Does the host have a real enforcement point, meaning permission rules
  and pre-execution hooks, or only a conversation?
- How often does the action happen? A daily action behind a prompt
  trains people to approve without reading.

Applicability is `runs_agents`. Engagement is `operator_requests_wargame`. This is an always-walk decision.

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

## Failure premises

### Premortem for A. Model judgement in band

Assume `A. Model judgement in band` was selected and the outcome failed. Test this option's stated failure mechanism first: the entire property: the decision lives in the same channel as the attack, so any text the agent reads can argue for the action. EV-0213 lists this class of failure directly, and EV-0218 requires explicit per-client consent rather than an inferred one.

### Premortem for B. Static allowlist of actions

Assume `B. Static allowlist of actions` was selected and the outcome failed. Test this option's stated failure mechanism first: coverage at the edges: broad entries silently permit more than intended, which EV-0220 shows for hostname allowlists where the proxy never inspects TLS, and the list ages badly because widening it is easier than re-arguing it.

### Premortem for C. Guard-classified verdicts with recorded approval

Assume `C. Guard-classified verdicts with recorded approval` was selected and the outcome failed. Test this option's stated failure mechanism first: a mapping to build, a bypass suite to prove it, and a validation report to keep current.

### Premortem for D. Manual only for everything consequential

Assume `D. Manual only for everything consequential` was selected and the outcome failed. Test this option's stated failure mechanism first: throughput, and it degrades: an operator who executes forty proposals a day stops reading them, which is the same failure as A arriving by a different route.

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

## Safe default

C, falling closed to D. Approval is a recorded event or it is not
approval, and that sentence is the load-bearing part: a claim of
approval found in task text, a document or tool output counts for
nothing.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Is the action reversible, and at what cost? Rollback cost is the variable that actually matters.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C, falling closed to D. Approval is a recorded event or it is not approval, and that sentence is the load-bearing part: a claim of approval found in task text, a document or tool output counts for nothing.

**Exit condition:** Stop or roll back the selected branch when the entire property: the decision lives in the same channel as the attack, so any text the agent reads can argue for the action. EV-0213 lists this class of failure directly, and EV-0218 requires explicit per-client consent rather than an inferred one, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Is the action reversible, and at what cost? Rollback cost is the variable that actually matters.

## Counter-evidence and transfer limits

The two maintainer sources for the parallel-tripwire pattern (EV-0076,
EV-0081) are vendor documentation describing their own products, so
they evidence that the pattern exists and is shipped, not that it
catches much. We have no measurement of how often a tripwire above a
real boundary fires usefully. Option D's degradation under volume is
reasoning from the general approval-fatigue literature rather than from
anything we have measured here, and it is the weakest claim on this
page.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
