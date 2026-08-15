---
summary: Activation, outcomes and decision map for the agentic-development Doctrine and Wargames
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [builds_agent_workflow, orchestrates_multiple_agents, designs_agent_harness, defines_agent_tools]
activation_paths: [**/agents/**, **/subagents/**, **/.claude/**, **/prompts/**, **/*prompt*.md, **/*agent*.py, **/*agent*.ts, **/mcp*.json, **/tools/**/*tool*.py, **/workflows/**, AGENTS.md, CLAUDE.md]
volatility: fast
review: none
type: guide
tags: [eos, arch, tooling]
sources: [EV-0001, EV-0007, EV-0021, EV-0046, EV-0050, EV-0051, EV-0052, EV-0076, EV-0078, EV-0079, EV-0080, EV-0082, EV-0083, EV-0085, EV-0086, EV-0087, EV-0088, EV-0089, EV-0106, EV-0107, EV-0108, EV-0109, EV-0110, EV-0111, EV-0112, EV-0113, EV-0114, EV-0115, EV-0117, EV-0118, EV-0119, EV-0120, EV-0121, EV-0449]
depends_on: [ai-ml-llm, security-privacy]
---


# Agentic development

This pack covers how to shape agent work: which of ten topologies to
run, and how to bound, verify and feed it. It activates on any task that
designs, changes or reviews an agent workflow, harness, subagent, tool
surface or orchestration graph. The governing rule is the simplest
topology that satisfies the task, and anything above a direct single
agent names the pressure that forced it. How we ourselves build with
agent graphs is `packs/agentic-swarm/`.

## Activation

**Paths.** Changes under an agent or orchestration surface: agent and
subagent definitions, instruction and prompt files, tool or MCP server
definitions, harness runners, workflow and graph definitions, guardrail
and callback registration, checkpoint stores, trace configuration.

**Task types.** Designing an agent workflow. Adding or removing a
subagent. Changing a tool surface. Choosing between one agent and
several. Setting run budgets. Adding a checkpoint or an approval.
Deciding how agent output is verified. Diagnosing an agent that loops,
stalls, duplicates work or contradicts an earlier decision.

**Keywords, fallback only when path and task type are silent.**
orchestrator, subagent, agent team, handoff, fan-out, DAG, workflow
graph, checkpoint, resumable, evaluator, judge, context window,
compaction, condenser, guardrail, tracing, span, token budget.

**Applicability predicates.** `builds_agent_workflow`,
`orchestrates_multiple_agents`, `designs_agent_harness`,
`defines_agent_tools`. Any one activates the pack. A single model call
with no loop, no tools and no shared state does not activate it; that
is ordinary code and belongs to the coding pack.

**Policy routing.** Activation gives advice, never permission. The
topology chosen changes which semantic factors the task declares in
`kernel/POLICY_SPEC.md`, typically irreversible-action, sends-external
and writes-production-data, and the router alone rules the tier. Every
tool action the agent takes is still evaluated by
`kernel/GUARD_SPEC.md`. Nothing in this pack lowers a tier floor or
converts a manual-only class into an autonomous one.

## Outcomes and non-goals

Outcomes. A topology chosen for a named pressure rather than by habit.
Runs that stop at a stated limit instead of drifting. Verification that
holds truth the generator does not. Irreversible acts that wait for a
person. Failures that can be located in a trace rather than guessed at.

Non-goals. This pack does not pick a vendor SDK, does not specify the
prompt wording inside a step, does not cover model selection or
inference cost tuning, and does not restate benchmark league tables.
It also does not govern non-agentic model calls, retrieval quality, or
the security posture of a sandbox, which the security-privacy pack
owns.

**The line with `packs/agentic-swarm/`.** This pack covers agent systems
built into a venture's product. That pack covers how we ourselves build
software, by fanning work out over a dependency graph. Same machinery,
different subject: if the agents ship to a customer, you are here; if
the agents are the ones doing the building, read that pack and follow
its rules there rather than inferring them from these.

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B1"></a>
- `B1` to [DOC-AGENT-001](doctrines/DOC-AGENT-001-one-writer.md) (binding)
<a id="B3"></a>
- `B3` to [DOC-AGENT-002](doctrines/DOC-AGENT-002-irreversible-or-externally-visible-acts-pass-a-human-checkpoint.md) (binding)
<a id="B4"></a>
- `B4` to [DOC-AGENT-003](doctrines/DOC-AGENT-003-evaluation-is-separate-from-generation-and-the-evaluator-holds-e.md) (binding)
<a id="B7"></a>
- `B7` to [DOC-AGENT-004](doctrines/DOC-AGENT-004-checkpoint-state-is-a-trust-boundary.md) (binding)
<a id="B2"></a>
- `B2` to [DOC-AGENT-005](doctrines/DOC-AGENT-005-every-loop-is-bounded.md) (default)
<a id="B5"></a>
- `B5` to [DOC-AGENT-006](doctrines/DOC-AGENT-006-any-topology-above-direct-single-agent-is-recorded.md) (default)
<a id="B6"></a>
- `B6` to [DOC-AGENT-007](doctrines/DOC-AGENT-007-runs-are-traceable.md) (default)
<a id="D1"></a>
- `D1` to [DOC-AGENT-008](doctrines/DOC-AGENT-008-start-at-direct-single-agent-with-a-strong-oracle.md) (default)
<a id="D2"></a>
- `D2` to [DOC-AGENT-009](doctrines/DOC-AGENT-009-harness-richness-tracks-the-models-demonstrated-gaps.md) (default)
<a id="D3"></a>
- `D3` to [DOC-AGENT-010](doctrines/DOC-AGENT-010-context-arrives-just-in-time-by-progressive-disclosure.md) (default)
<a id="D4"></a>
- `D4` to [DOC-AGENT-011](doctrines/DOC-AGENT-011-tool-capability-order-explicit-tools-then-bash-then-generated-co.md) (default)
<a id="D5"></a>
- `D5` to [DOC-AGENT-012](doctrines/DOC-AGENT-012-continuity-across-context-windows-rides-on-artifacts-and-git-his.md) (default)
<a id="D6"></a>
- `D6` to [DOC-AGENT-013](doctrines/DOC-AGENT-013-cheap-guardrails-run-beside-the-work-and-trip-a-wire-and-cross-c.md) (default)
<a id="D7"></a>
- `D7` to [DOC-AGENT-014](doctrines/DOC-AGENT-014-memory-is-a-swappable-store-behind-one-interface-with-an-explici.md) (default)
<a id="D8"></a>
- `D8` to [DOC-AGENT-015](doctrines/DOC-AGENT-015-evaluation-suites-start-at-twenty-to-fifty-tasks-harvested-from.md) (default)
- source `preferences:001` to [DOC-AGENT-016](doctrines/DOC-AGENT-016-event-sourced-conversation-state-over-ad-hoc-message-history-ev.md) (preference)
- source `preferences:002` to [DOC-AGENT-017](doctrines/DOC-AGENT-017-functional-composition-before-graph-builders-reaching-for-a-grap.md) (preference)
- source `preferences:003` to [DOC-AGENT-018](doctrines/DOC-AGENT-018-condensers-that-always-preserve-the-opening-events-ev-0080.md) (preference)
- source `preferences:004` to [DOC-AGENT-019](doctrines/DOC-AGENT-019-mechanical-stuck-detection-with-thresholds-tuned-per-model-ev-00.md) (preference)

## Decision map

| Fork | Guide |
| --- | --- |
| Which of the ten topologies does this work need? | `packs/agentic-development/guides/GD-AGENT-001-topology-selection.md` |
| How does context reach the agent, and what gets dropped? | `packs/agentic-development/guides/GD-AGENT-002-context-engineering.md` |
| Should this be a subagent at all, and of what sort? | `packs/agentic-development/guides/GD-AGENT-003-spawn-a-subagent.md` |
| What holds the truth that checks the work? | `packs/agentic-development/guides/GD-AGENT-004-verification-oracle.md` |

The ten topologies, their pressures and their evidence are carded in
`packs/agentic-development/refs/TOPOLOGY_CARD.md`. Bounding, tracing
and checkpoint mechanics are in
`packs/agentic-development/refs/INVARIANTS_AND_BOUNDS.md`. What a
reviewer or a script can verify about work in this domain is in
`packs/agentic-development/CHECKS.md`.

## Failure modes and anti-patterns

- **Multi-agent by default.** A team spawned where one agent with a
  good oracle would do, paying a large token multiple for coordination
  the task never needed (EV-0112, EV-0106).
- **Fragmented context.** Parallel actors each holding part of the
  truth, producing work that does not compose (EV-0106).
- **Verification theatre.** A model judge with no ground truth, ranked
  as though it were a test (EV-0111, EV-0115).
- **The resume trap.** Code before an interrupt re-executes on resume,
  so a non-idempotent side effect fires twice (EV-0079).
- **Guardrails that fire on false positives.** Stuck detection killing
  an agent that was legitimately polling (EV-0082).
- **Graph ceremony.** Executors, edges and checkpointers around work
  that was a three-step script (EV-0078).
- **Scaffolding rot.** Structure added for a model limitation that no
  longer exists, never removed (EV-0089, EV-0046).
- **Tool sprawl.** One tool per API endpoint, unnamespaced, returning
  identifiers the agent must resolve with more calls (EV-0113).
- **Unbounded delegation.** Subagents spawning subagents with no shared
  budget, duplicating each other's work (EV-0112).

## Open questions and counter-evidence

**Parallelism is genuinely contested.** Anthropic reports a large
uplift from orchestrator-worker on breadth-first research at roughly
fifteen times the tokens, and says plainly it suits neither
shared-context work nor most coding (EV-0112). Cognition argues from
production experience that parallel actors fail through fragmented
context (EV-0106), then softened to writes single-threaded while other
agents contribute intelligence (EV-0107). Both are vendor practice,
neither is a controlled comparison. They reconcile only under B1. We
have no independent study measuring topology against outcome, and this
is the largest gap in the pack.

**Benchmark numbers are narrow and mostly self-reported.** SWE-bench
Verified results (EV-0052, EV-0110) are single-repository Python issue
resolution with a test oracle. They say nothing about work with weak
oracles, shared state or long horizons, and several headline figures
are maintainer-reported rather than independently reproduced. Do not
promote them into doctrine about agents in general.

**MAST is diagnostic, not prescriptive.** It shows multi-agent failures
concentrate in specification gaps, inter-agent misalignment and absent
verification, at good annotator agreement, over 2024 to 2025 framework
and model generations (EV-0109). It does not prove any topology is
better than another, and its absolute rates will have moved.

**Interface effort looks capability-dependent.** Careful agent-computer
interface design moved task success materially in 2024 (EV-0110), and a
hundred-line agent with bash as its only tool later scored far higher
(EV-0052). That is a moving frontier rather than a contradiction, and
it is why D2 is a default rather than a rule.

**Self-correction evidence is off-population.** The controlled result
that models degrade their own answers without external feedback
(EV-0111) studied short-form reasoning on the 2023 to 2024 generation,
not long-horizon coding where compilers and tests supply the signal it
says is missing. B4 survives, because it only requires external truth,
but the size of the effect in coding is unmeasured.

**Where the evidence is thin.** Nothing measured tells us how many
parallel workers is too many, what condensers really cost against
artifact-based continuity, or when an event log pays for itself. Those
are judgement calls today and the guides say so.

## Evidence

Every source is a row in `registry/evidence.json` with version, licence,
access date and review trigger. Cite ids, never re-record sources. The
pack's own set is the fourteen rows imported from its research fragment,
EV-0109 to EV-0121 plus EV-0449; the rest are shared estate rows. The
frozen batch the import was made from stays at
`packs/agentic-development/research/sources.fragment.json`. Research
synthesis and the disagreements behind this file are in
`packs/agentic-development/research/NOTES.md`, and the licence and
quotation sweep, including the rows whose source states no licence, is
at `packs/agentic-development/research/provenance.fragment.json`.
