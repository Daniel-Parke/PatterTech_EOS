---
summary: Activation, outcomes and decision map for the agentic-swarm Doctrine and Wargames
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [fans_work_across_lanes, cuts_a_build_partition, integrates_parallel_lanes, writes_a_lane_packet]
activation_paths: [org/claims.json, org/GRAPH_BUILD.md, **/PARTITION.md, **/partition*.json, **/lanes/**, **/packets/**, **/worktrees/**, .claude/workflows/**, **/*swarm*.md, kernel/templates/org/GRAPH_BUILD.tpl.md]
volatility: fast
review: none
type: guide
tags: [eos, arch, delivery, tooling]
sources: [EV-0010, EV-0053, EV-0107, EV-0108, EV-0109, EV-0111, EV-0112, EV-0244, EV-0450, EV-0451, EV-0452, EV-0453, EV-0454, EV-0455, EV-0456, EV-0457, EV-0458, EV-0459, EV-0460, EV-0461, EV-0463, EV-0464, EV-0466, EV-0467, EV-0468, EV-0469, EV-0470, EV-0472, EV-0475, EV-0476, EV-0477, EV-0478, EV-0480, EV-0481, EV-0482, EV-0483, EV-0484, EV-0485, EV-0486, EV-0487, EV-0488, EV-0489, EV-0491, EV-0493, EV-0494, EV-0495]
depends_on: [agentic-development, delivery-testing]
---


# Agentic swarm and graph engineering

This pack covers how we build software with agent graphs: cutting the
partition, writing the lane packet, bounding the run, verifying a lane
and merging it. It activates when work is fanned out across more than
one writing session. The governing rule is that you fan out over a
measured dependency graph, with one integrator and an external verifier
that predates the lanes. Anything else is either a single agent or an
expensive mistake.

## Activation

**Paths.** The claim file, a partition artefact, lane briefs and
packets, worktree layout, orchestration scripts, and the graph-build
method a venture seed compiles from
`kernel/templates/org/GRAPH_BUILD.tpl.md`.

**Task types.** Deciding whether to fan out at all. Cutting a partition
from a product map. Writing or reviewing a lane packet. Sizing lanes.
Choosing between a script and model-driven delegation. Setting the run
budget. Merging lanes. Reviewing what a lane produced. Diagnosing a run
that cost more than it returned.

**Keywords, fallback only when path and task type are silent.**
swarm, fan-out, lane, partition, integrator, worktree, work packet,
merge order, merge queue, claim file, orchestrator script, run budget.

**Applicability predicates.** `fans_work_across_lanes`,
`cuts_a_build_partition`, `integrates_parallel_lanes`,
`writes_a_lane_packet`. Any one activates the pack. One session doing
one job does not activate it, however many subagents it reads with;
this pack starts where a second writer starts.

**Boundary with agentic-development.** That pack owns agent systems
built into venture products. This pack owns how we ourselves build.
Where the neighbour states a rule, this one cites it and adds only what
a graph needs on top: one writer per artefact is theirs, which
artefacts may never be delegated is ours; believing a checkpoint's
contents is theirs, the store as an execution surface is ours. Read
`packs/agentic-development/PACK.md` first when the question is what
shape the agent system should be.

**Policy routing.** Activation gives advice, never permission. Fanning
out changes which semantic factors a task declares under
`kernel/POLICY_SPEC.md`, and every tool action is still ruled by
`kernel/GUARD_SPEC.md`. Nothing here lowers a tier floor or turns a
manual-only action class into an autonomous one.

## Outcomes and non-goals

Outcomes. A partition that survives contact with the merge gate. Lanes
that fail loudly instead of guessing. A run that stops at a number
rather than at an invoice. Work checked by something the lane did not
write. An integrator that can say which lane produced a line, and what
passed it.

Non-goals. This pack does not pick a harness, does not prescribe prompt
wording inside a lane, does not set test timing (see
`packs/delivery-testing/PACK.md`), and does not govern the security
posture of a lane's sandbox, which `packs/security-privacy/PACK.md`
owns. It carries no vendor version number, model name or price: those
live in a venture's profile, because the harness we use moved its
delegation-depth default three times in about two months (EV-0463).

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B1"></a>
- `B1` to [DOC-SWARM-001](doctrines/DOC-SWARM-001-the-partition-is-written-before-any-lane-starts-and-it-is-cut-on.md) (binding)
<a id="B2"></a>
- `B2` to [DOC-SWARM-002](doctrines/DOC-SWARM-002-the-packet-is-closed-and-literal.md) (binding)
<a id="B3"></a>
- `B3` to [DOC-SWARM-003](doctrines/DOC-SWARM-003-returns-are-schema-constrained-and-carry-a-receipt.md) (binding)
<a id="B4"></a>
- `B4` to [DOC-SWARM-004](doctrines/DOC-SWARM-004-node-output-is-untrusted-data-at-the-integrator.md) (binding)
<a id="B5"></a>
- `B5` to [DOC-SWARM-005](doctrines/DOC-SWARM-005-constraints-are-pinned-and-never-compactable.md) (binding)
<a id="B6"></a>
- `B6` to [DOC-SWARM-006](doctrines/DOC-SWARM-006-every-run-declares-a-global-budget-and-every-node-a-cap-both-enf.md) (binding)
<a id="B7"></a>
- `B7` to [DOC-SWARM-007](doctrines/DOC-SWARM-007-the-artefact-that-decides-a-lanes-success-is-authored-outside-th.md) (binding)
<a id="B8"></a>
- `B8` to [DOC-SWARM-008](doctrines/DOC-SWARM-008-agreement-between-lanes-is-not-evidence-of-correctness.md) (binding)
<a id="B9"></a>
- `B9` to [DOC-SWARM-009](doctrines/DOC-SWARM-009-one-lane-one-worktree-one-branch-one-owned-file-set-and-the-inte.md) (binding)
<a id="B10"></a>
- `B10` to [DOC-SWARM-010](doctrines/DOC-SWARM-010-every-dependency-any-lane-introduces-is-resolved-against-the-rea.md) (binding)
<a id="D1"></a>
- `D1` to [DOC-SWARM-011](doctrines/DOC-SWARM-011-three-to-five-lanes.md) (default)
<a id="D2"></a>
- `D2` to [DOC-SWARM-012](doctrines/DOC-SWARM-012-do-not-swarm-work-a-single-agent-already-does-well.md) (default)
<a id="D3"></a>
- `D3` to [DOC-SWARM-013](doctrines/DOC-SWARM-013-if-the-graph-will-not-cut-do-not-swarm.md) (default)
<a id="D4"></a>
- `D4` to [DOC-SWARM-014](doctrines/DOC-SWARM-014-partition-the-failure-surface-not-only-the-code.md) (default)
<a id="D5"></a>
- `D5` to [DOC-SWARM-015](doctrines/DOC-SWARM-015-claims-are-committed-files-not-messages.md) (default)
<a id="D6"></a>
- `D6` to [DOC-SWARM-016](doctrines/DOC-SWARM-016-serialise-worktree-creation-then-run-the-lanes-in-parallel.md) (default)
<a id="D7"></a>
- `D7` to [DOC-SWARM-017](doctrines/DOC-SWARM-017-cap-diff-width-per-package-and-land-in-dependency-order.md) (default)
<a id="D8"></a>
- `D8` to [DOC-SWARM-018](doctrines/DOC-SWARM-018-one-strong-clean-context-reviewer-per-concern-and-reviewers-repo.md) (default)
<a id="D9"></a>
- `D9` to [DOC-SWARM-019](doctrines/DOC-SWARM-019-machine-detectable-defect-classes-go-to-scanners-not-to-reviewer.md) (default)
<a id="D10"></a>
- `D10` to [DOC-SWARM-020](doctrines/DOC-SWARM-020-route-by-role.md) (default)
<a id="D11"></a>
- `D11` to [DOC-SWARM-021](doctrines/DOC-SWARM-021-irreversible-external-effects-are-staged-and-executed-once-by-th.md) (default)
<a id="D12"></a>
- `D12` to [DOC-SWARM-022](doctrines/DOC-SWARM-022-pilot-one-slice-then-journal-the-whole-run.md) (default)
<a id="D13"></a>
- `D13` to [DOC-SWARM-023](doctrines/DOC-SWARM-023-continuity-is-by-artefact-not-by-summary.md) (default)
<a id="D14"></a>
- `D14` to [DOC-SWARM-024](doctrines/DOC-SWARM-024-run-a-single-agent-control-on-a-sample-and-instrument-the-landin.md) (default)
- source `preferences:001` to [DOC-SWARM-025](doctrines/DOC-SWARM-025-if-a-step-can-be-code-make-it-code.md) (preference)
- source `preferences:002` to [DOC-SWARM-026](doctrines/DOC-SWARM-026-spend-the-budget-on-the-specification-before-spending-it-on-revi.md) (preference)
- source `preferences:003` to [DOC-SWARM-027](doctrines/DOC-SWARM-027-prefer-breadth-of-independent-attempts-to-rounds-of-cross-talk.md) (preference)
- source `preferences:004` to [DOC-SWARM-028](doctrines/DOC-SWARM-028-one-worked-example-of-a-correct-return-beats-five-rules-about-ed.md) (preference)
- source `preferences:005` to [DOC-SWARM-029](doctrines/DOC-SWARM-029-name-nodes-by-their-artefact-so-a-trace-reads-as-a-work-breakdow.md) (preference)

## Decision map

| Fork | Guide |
| --- | --- |
| Should this be a swarm at all, or one agent? | `packs/agentic-swarm/guides/GD-SWARM-001-swarm-or-single-agent.md` |
| Where do the cuts go? | `packs/agentic-swarm/guides/GD-SWARM-002-cut-the-partition.md` |
| Who holds the plan, a script or a model? | `packs/agentic-swarm/guides/GD-SWARM-003-who-holds-the-plan.md` |
| What decides that a lane's work is good? | `packs/agentic-swarm/guides/GD-SWARM-004-verifying-a-lane.md` |

Packet and return mechanics are in
`packs/agentic-swarm/refs/PACKET_AND_RETURN.md`, merge gate and review
topology in `packs/agentic-swarm/refs/MERGE_AND_REVIEW.md`, the full
risk table in `packs/agentic-swarm/refs/RISK_REGISTER.md`, a worked
partition and its one recorded departure from B7 in
`packs/agentic-swarm/exemplars/EX-SWARM-001-eos-v2-1-partition.md`, and
what a reviewer or script can verify in `packs/agentic-swarm/CHECKS.md`.

## The risk that governs the rest

Read the register named above before cutting a partition for the first
time. One risk governs all fifteen of its rows: every rule in this pack
compensates for something a model cannot do today, and those
assumptions expire. So every rule names its failure precisely, and a
rule whose failure can no longer be reproduced goes. The clearest
public instance is a practitioner who argued against multi-agent
systems in 2025 and published three working patterns ten months later
(EV-0107).

## Failure modes and anti-patterns

- **Fan-out by file count.** One file per lane is not a partition, and
  it cost 44 to 60 per cent more than sequential for one to three
  points (EV-0450).
- **The hub file everyone touches.** A registry or schema left in the
  shared write set, which is the highest-probability conflict class.
- **The open packet.** A brief that describes the target instead of
  naming it, and assumes the lane inherits the orchestrator's
  conversation (EV-0108).
- **The silent kill.** A rate-limited lane returning nothing, read as
  "nothing to fix", entering the integrator as a fact.
- **The panel.** Five judges bought for the price of five and worth
  about two (EV-0486).
- **Explain-and-fix review.** A reviewer told to produce a fix,
  inventing requirements to justify one (EV-0484).
- **Merge order by finish time**, with hidden relations deciding the
  rest (EV-0455).

## Counter-evidence and open questions

This pack argues for a method its owner already believes in, which is
exactly the condition under which a pack lies. So the case against is
carried here in the body, at length, and not in a footnote.

**Most multi-agent systems lose to one good agent.** On a normalised
substrate holding benchmark loading, tool access and accounting
constant across ten benchmarks, a single-agent baseline scored 74.12
per cent at 27,435 average tokens. The best of six multi-agent systems
reached 75.56 per cent, inside the uncertainty band, at 24 per cent more
tokens. The other five scored 62.83 to 71.56 per cent, one of them at
286 per cent more tokens (EV-0451). Five of six were
below baseline while costing more. That is the single strongest result
in this corpus and it points away from swarms.

**Under equal thinking budgets, single agents match or win.** Holding
reasoning tokens constant rather than architecture, single agents
consistently matched or beat multi-agent systems on multi-hop
reasoning across three model families (EV-0453). The
stated exception is the whole of our case: fan-out pays when one
context would degrade. That is a much narrower claim than "parallelism
is fast", and it is the only one we make.

**Naive parallelism costs more and buys almost nothing.** File-per-agent
fan-out ran at 1.44 to 1.60 times sequential cost for 0.9 and 3.2 points
of pass rate. An unstructured agent team was genuinely cheaper and
faster than sequential and scored below it on both benchmarks
(EV-0450). Cheap is not the same as efficient.

**The baseline paradox.** Where a single agent already succeeds above
roughly 45 per cent, adding agents predicts a loss, at beta -0.408,
p<0.001 (EV-0452). The better single agents get, the
smaller the space where this pack applies.

**Coordination cost is superlinear.** Turn count fits T =
2.72(n+0.5)^1.724 at R-squared 0.974, and under a fixed budget
per-agent reasoning becomes prohibitively thin beyond three or four
agents (EV-0452).

**Nobody has measured the thing we are actually doing.** No public
benchmark measures a ten to fifty node dependency-graph build with a
single integrator. The architecture rests on one partitioning study,
one vendor case study and product documentation. Our own runs will be
the best evidence we have, which is the argument for D12 and for
stating n and spread on any claim that one configuration beats another:
single-run pass@1 varies by 2.2 to 6.0 percentage points at fixed
configuration (EV-0493).

**We cannot claim swarms are faster end to end.** Every measured
pipeline says the same thing: generation got faster and landing did
not. Agent changes land within thirty days at 32.7 per cent against
84.5 per cent, waiting roughly five times longer for pickup
(EV-0457), and one randomised trial measured developers
19 per cent slower while they believed they were 20 per cent faster
(EV-0010). Swarm speed is demonstrated at the lane and unproven at the
pipeline. Until a venture measures agent-done-to-merged on its own
work, that is the honest position and this pack holds it.

**Where the pro-swarm evidence is thin.** The partitioning result is 28
tasks on Python repositories with no ablation over its own thresholds
(EV-0450). The sixteen-lane success is one uncontrolled case in the most
oracle-rich domain in software, and its own author lists frequent
regressions near the end (EV-0053). The vendor whose research system
reports a large uplift says in the same post that the pattern is a poor
fit for most coding tasks (EV-0112). The optimistic scaling law that
finds emergence at sixteen agents was measured on short-horizon
generation with no merge gate (EV-0495).

**Where our own rules are thinly evidenced, named.** B5 rests on one
unreplicated single-author study, kept binding because the design is
clean and the failure it prevents is a lane breaking a governance rule.
D1's three-to-five figure is a converging heuristic from three
directions, not a measured optimum: no published study varies lane
count on real repositories and measures pass-at-merge, and the conflict
rates behind it are per-pair, textual only, and an explicitly
conservative lower bound (EV-0454). The merge-debt
metrics in D14 are one practitioner's unvalidated definitions
(EV-0494), so they are instrumentation to test.

**A finding that cuts against our worry.** One merge-queue dataset of
153,000 merges found AI-assisted changes broke trunk less often than
unassisted ones, 1.9 against 4.4 per cent, holding within the same
repositories despite being larger (EV-0456). It contradicts the
review-burden telemetry that reports bugs per change up 54 per cent
(EV-0458). Both cannot be straightforwardly true of the same population
and neither source establishes the reconciliation. We record the
disagreement rather than pick the convenient side.

**What no evidence supports either way.** No measured catch rate exists
for clean-context reviewer agents on realistic multi-file changes, and
that hole sits directly under D8. No study measures defect escape for a
full swarm-plus-integrator pipeline against a controlled baseline. No
published defence against social engineering of review agents has been
tested, so B4 is inference from the attack surface
(EV-0489). Degradation results widely quoted as
lane-count evidence measure sequential iteration and say nothing about
parallel lanes (EV-0459).

**Read this before quoting the pack at someone.** The evidence does not
say fan-out is right. It says fan-out over a real dependency graph,
with hub artefacts held back, one integrator and independent contexts
per lane, is the narrow shape that survives measurement. Independent
contexts are the defence this pack relies on against one lane's errors
poisoning another's reasoning, and neither row behind that reliance
measures contamination between agents (EV-0244, EV-0470). Generic
multi-agent, meaning more agents on a fixed topology with no verifier,
loses to one good agent and loses expensively.

## Evidence

Every source is a row in `registry/evidence.json` with version,
licence, access date and review trigger. Cite ids, never re-record
sources. Five rows this pack cites were merged into older ledger rows by
URL at import and kept the older summary; the release tidy enriched all
five, so each row now carries what this pack cites it for. The synthesis
behind this file, those five rows, and the questions the research could
not close are in `packs/agentic-swarm/research/NOTES.md`. The licence
and quotation sweep is at
`packs/agentic-swarm/research/provenance.fragment.json`, and it is
blunt about the position: of the sixty-two ids cited across this pack,
ten carry licence evidence and fifty-two are assertions read back off
the ledger.
