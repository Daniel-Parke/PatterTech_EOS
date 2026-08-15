---
id: GD-SEC-001
summary: In-band detection, a configuration rule, out-of-band enforcement, or OS containment?
kind: wargame
type: wargame
tags: [eos, security, tooling, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-SEC-003]
applies_when: [runs_agents]
engages_when: [operator_requests_wargame]
consequence: high
relations: []
always_walk: true
scope: estate
authority: default
basis: empirical-evidence
evidence_grade: controlled
sources: [EV-0212, EV-0213, EV-0214, EV-0215, EV-0216, EV-0217, EV-0219, EV-0220]
review: 2027-03
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-SEC-001: how do we resist indirect prompt injection?

## Decision question and stakes

An agent reads something it did not write, and that thing contains
text addressed to the agent. Every venture that gives a model tools
meets this fork. Getting it wrong hands an attacker who can write one
line into any readable file the agent's whole permission set.

## Doctrines or coverage gap under pressure

- `DOC-SEC-003` (binding): Containment is never widened on the say-so of task text.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Can the task be planned before the untrusted data arrives? Some can,
  and some are open-ended by nature.
- What would the agent reach if it were fully compromised: private
  data, a network path out, both?
- How long does the run live? A thirty-minute feature run and a
  standing service have different economics.
- Is there a host with a real enforcement point, or only the model?
- What utility loss is acceptable, and who measures it?

Applicability is `runs_agents`. Engagement is `operator_requests_wargame`. This is an always-walk decision.

## Options

### A. In-band detection
A classifier, a spotlighting prompt, or an instruction to the model to
notice and ignore planted text. Buys near-zero cost, no architecture
change, and works on any task class. Costs credibility: adaptive
attacks broke all eight defences of this shape that EV-0215 tested,
with over fifty percent success. It has real value as a parallel
tripwire above a boundary and none at all as the boundary.

### B. A configuration rule that removes a precondition
Forbid the combination rather than filtering it. Exfiltration needs
private data, untrusted content and outbound communication together,
so a run holds at most two of the three (EV-0219). Buys the cheapest
control available: no model, no proxy, no budget, and it holds under
adaptive attack because there is nothing to attack. Costs capability
rather than tokens, because it forbids configurations a real policy
layer could make safe. The trap is a broad allowlist entry sold as
isolation; EV-0220 states the proxy rules on the client-supplied
hostname without inspecting TLS.

### C. Out-of-band deterministic enforcement
Capabilities, information-flow labels, or a reference monitor outside
the model. CaMeL is the clearest instance: extract control flow and
data flow from the trusted request before untrusted data is seen, then
check capabilities at the point of tool invocation (EV-0216). Buys the
strongest measured result we have: EV-0214 saw attack success fall
roughly sixfold across five such systems and stay low against a
defence-aware attacker. Costs utility and generality: 77 percent of
AgentDojo tasks solved against 84 undefended, and follow-up work
reports the static-planning strategy collapsing on genuinely
open-ended tasks. Costs engineering too, because someone has to build
and maintain the monitor.

### D. Operating-system containment
Filesystem and egress containment at the OS or sandbox layer, both
enabled together (EV-0220). Buys a boundary that holds regardless of
what the model chose to run, and it needs no task planning. Costs
setup, and it is coarse: it stops the agent reaching outside the box
and says nothing about what it does inside.

## Failure premises

### Premortem for A. In-band detection

Assume `A. In-band detection` was selected and the outcome failed. Test this option's stated failure mechanism first: , no architecture change, and works on any task class. Costs credibility: adaptive attacks broke all eight defences of this shape that EV-0215 tested, with over fifty percent success. It has real value as a parallel tripwire above a boundary and none at all as the boundary.

### Premortem for B. A configuration rule that removes a precondition

Assume `B. A configuration rule that removes a precondition` was selected and the outcome failed. Test this option's stated failure mechanism first: capability rather than tokens, because it forbids configurations a real policy layer could make safe. The trap is a broad allowlist entry sold as isolation; EV-0220 states the proxy rules on the client-supplied hostname without inspecting TLS.

### Premortem for C. Out-of-band deterministic enforcement

Assume `C. Out-of-band deterministic enforcement` was selected and the outcome failed. Test this option's stated failure mechanism first: utility and generality: 77 percent of AgentDojo tasks solved against 84 undefended, and follow-up work reports the static-planning strategy collapsing on genuinely open-ended tasks. Costs engineering too, because someone has to build and maintain the monitor.

### Premortem for D. Operating-system containment

Assume `D. Operating-system containment` was selected and the outcome failed. Test this option's stated failure mechanism first: setup, and it is coarse: it stops the agent reaching outside the box and says nothing about what it does inside.

## Decision rule

- Any run at all with tool access: D as the floor, filesystem and
  egress together. Neither alone is a claim of containment.
- The task class can be planned before untrusted data arrives, and the
  blast radius includes private data plus a network path: C on top of
  D, with the utility number measured on the same runs (EV-0217).
- The task class cannot be planned, or the venture has no engineering
  budget for a monitor: B on top of D. Hold the trifecta rule and take
  the capability loss.
- A standing service that reads third-party content for many users:
  C, and treat B as the fallback while C is being built.
- A always allowed, never counted. Run it in parallel as a tripwire,
  and never let its pass rate stand in for the boundary.

## Safe default

B on top of D. It is cheap, it holds under adaptive attack, and its
cost is capability the venture can see and price. Move to C when the
task class is plannable and the run touches both private data and the
network, and record the utility number when you do.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Can the task be planned before the untrusted data arrives? Some can, and some are open-ended by nature.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** B on top of D. It is cheap, it holds under adaptive attack, and its cost is capability the venture can see and price. Move to C when the task class is plannable and the run touches both private data and the network, and record the utility number when you do.

**Exit condition:** Stop or roll back the selected branch when , no architecture change, and works on any task class. Costs credibility: adaptive attacks broke all eight defences of this shape that EV-0215 tested, with over fifty percent success. It has real value as a parallel tripwire above a boundary and none at all as the boundary, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Can the task be planned before the untrusted data arrives? Some can, and some are open-ended by nature.

## Counter-evidence and transfer limits

EV-0215 and EV-0214 read as opposite verdicts and are not. EV-0215
broke defences that ask the model to behave; EV-0214 held up defences
that do not depend on the model behaving. EV-0214 is one small-scale
data point on one small model and one benchmark family, by its own
authors' description, and must not be promoted to universal doctrine.
The CaMeL utility figures come from AgentDojo alone and scope to
agentic tool use on that benchmark, not to agent work in general.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
