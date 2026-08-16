---
summary: Observability signal stability tiers and the allocation precondition that makes cost work mean anything
type: implementation
tags: [ops, infra, money]
kind: recipe
scope: estate
review: 2027-12
sources: [EV-0043, EV-0058, EV-0071, EV-0197, EV-0198, EV-0205]
---

# Signal stability, platform paths and cost allocation

Level-3 reference for binding requirement 7 and for the golden-path and
cost allocation defaults in `packs/devops-reliability/PACK.md`.

## Stability is a per-signal contract

Signals move through development, stable, deprecated and removed, and
only stable signals carry a promise that existing calls keep working
across minor versions. Deprecated components keep stable-grade
guarantees until they are removed, which makes deprecated safer than
anything below stable (EV-0198).

The operating rule:

| Signal status | What you may do |
| --- | --- |
| stable | Take a long-term dependency: alerts, SLIs, retention schemas |
| deprecated | Keep the existing dependency, plan the move, do not add new ones |
| development or experimental | Emit if useful, pin the version, map the schema, never alert on it |

The bite is real: GenAI agent conventions were still in Development at
v1.42.0 and moved to a dedicated repository without a 1.0, so attribute
names can still change without a major version bump (EV-0043). An
agentic estate therefore has a large emission surface it is not allowed
to build alerts on. Pinning and schema mapping is a workaround and
should be recorded as one, with a date to look again.

## Golden paths

A scaffolder that stamps out a compliant skeleton and registers
ownership at creation time is how practice gets encoded without anyone
reading a document (EV-0058). Two caveats that matter more than the
mechanism:

- Golden paths rot without continual gardening. A scaffold encoding last
  year's practice is worse than none, because it is trusted (EV-0058).
- Voluntary adoption is the quality signal. People routing around the
  path means the path is wrong, so mandating the path destroys the only
  honest measurement you had (EV-0205).

The maturity model behind that second point assesses investment,
adoption, interfaces, operations and measurement across four levels, and
says plainly that the output that matters is the improvement list, not
the level. It is a consensus whitepaper with no outcome data, and for a
venture with no internal customers only the interfaces and measurement
aspects carry over.

## Cost allocation

The precondition worth more than the rest of the framework: until every
unit of spend has an owning thing, optimisation and chargeback are
theatre (EV-0197, CC BY 4.0, attribution to the FinOps Foundation).
Allocation comes first, then anomaly detection, then unit economics. The
maturity ladder is not load-bearing at venture scale.

In practice that means every deployed resource carries tags for the
venture, the environment and the component, applied by the
infrastructure code rather than by hand, so an untagged resource is a
build failure and not a monthly tidy-up. The test is simple: can the
bill be split with no remainder? A remainder line called "other" is an
unallocated estate wearing a label.

No controlled study links adoption of this framework to lower spend, so
nothing here binds. What binds elsewhere in the estate is the cost
ceiling itself, which is a v1 devops doctrine position and is unchanged.

## Policy as code

Where the inputs are already machine-readable, a decision engine queried
with structured input beats a prose checklist, because the policy is
then versioned, tested and changed in one place (EV-0071).
Where the inputs are prose, policy as code buys nothing and costs a
learning curve. Check which case you are in before reaching for it.
