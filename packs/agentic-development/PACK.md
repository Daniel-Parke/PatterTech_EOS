---
summary: Which agent topology to run, the invariants that bind every one of them, and how to bound, verify and trace a run
kind: rule
authority: binding
lifecycle: active
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [builds_agent_workflow, orchestrates_multiple_agents, designs_agent_harness, defines_agent_tools]
volatility: fast
review: on-change-of:agent-sdk-major-release
type: guide
tags: [eos, arch, tooling]
review_by: 2027-03
sources: [EV-0001, EV-0021, EV-0046, EV-0050, EV-0051, EV-0052, EV-0076, EV-0078, EV-0079, EV-0080, EV-0082, EV-0083, EV-0085, EV-0086, EV-0087, EV-0088, EV-0089, EV-0106, EV-0107, EV-0108, EV-0109, EV-0110, EV-0111, EV-0112, EV-0113, EV-0114, EV-0115, EV-0117, EV-0118, EV-0119, EV-0120, EV-0121]
---

# Agentic development

This pack covers how to shape agent work: which of ten topologies to
run, how to bound it, how to verify it, and how to feed it context. It
activates when a task designs, changes or reviews an agent workflow, a
harness, a subagent, a tool surface or an orchestration graph. The
governing rule is the simplest topology that satisfies the task, and
anything above a direct single agent must name the pressure that forced
it.

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

## Binding requirements

Seven. Each names the failure it prevents. Violating one is a defect,
not a style disagreement.

**B1. One writer.** Several agents may read shared state. Writes to any
shared artefact are serialised through exactly one owner, or split into
disjoint files each with a single owner. Prevents the conflicting
decisions and silent overwrite failures that dominate multi-agent
traces (EV-0109, EV-0106, EV-0107). This is the constraint that lets
parallel reading and single-writer merging coexist.

**B2. Every loop is bounded.** A loop carries numeric limits on turns,
tokens or wall-clock, at least two of the three, with units, plus a
stated stop condition and what happens when it trips (EV-0051,
EV-0052). Prevents unbounded spend and the stall that looks like
progress.

**B3. Irreversible or externally visible acts pass a human
checkpoint.** The gate sits at the risky act, not at a tidy phase
boundary (EV-0079, EV-0108). Prevents an agent publishing, deploying,
deleting or spending on its own. The checkpoint is a recorded approval
event, never a claim in prose.

**B4. Evaluation is separate from generation, and the evaluator holds
external truth.** Tests, types, schema validators, linters, a fresh
context or a person. Without external truth, self-review degrades the
answer (EV-0111), and an agent asked to grade itself will praise itself
(EV-0089, EV-0115). Prevents verification theatre. Where no external
oracle exists, say so and do not claim an evaluator-optimizer loop.

**B5. Any topology above direct single-agent is recorded.** The record
names the pressure that forced the promotion and the failure mode it
removes (EV-0109). It carries six level-two sections: Topology,
Pressures, Bounds, Resumability, Verification, Approval. Front-matter
carries `summary`, `type` and `tags` including `eos`, it cites at least
four evidence ids of which at least two come from this pack's own set,
and it stays under 120 lines. Prevents topology chosen by fashion, and
prevents a design no reviewer can check. The section-by-section requirements are in
`packs/agentic-development/refs/DECISION_RECORD_SHAPE.md` and a worked
record is
`packs/agentic-development/exemplars/EX-AGENT-001-logging-migration.md`.

**B6. Runs are traceable.** A stable span vocabulary (run, turn, agent,
generation, tool, guardrail, handoff), a workflow name, and a group id
linking related runs, with a switch that keeps spans while excluding
payloads where data policy forbids them (EV-0118, EV-0021). Prevents
failures that cannot be located, which is the whole cost of parallel
work.

**B7. Checkpoint state is a trust boundary.** Never resume from a
checkpoint of unknown provenance, and treat the store as attack surface
(EV-0121). Prevents code execution through a deserialised run state.

## Defaults

Overridable, but the override is recorded with its reason in the
topology decision record.

**D1. Start at direct single-agent with a strong oracle** (EV-0088,
EV-0052). Promote only on a named pressure. Reason: the promotion
always costs tokens, latency or coherence, and often all three.

**D2. Harness richness tracks the model's demonstrated gaps.** Add a
component only by naming the model limitation it compensates for, and
strip components as models improve (EV-0089, EV-0110, EV-0052). Reason:
every component encodes an assumption about what the model cannot do,
and those assumptions expire. This default is the one most likely to
move; the ratio of harness to model can shift without any binding
requirement changing.

**D3. Context arrives just in time, by progressive disclosure.** Load
identifiers and summaries, fetch bodies on demand, rather than
pre-loading everything (EV-0086, EV-0114, EV-0083). Reason: tool and
document surface is a context cost, and one worked vendor example fell
from about 150,000 tokens to about 2,000 on this change alone.

**D4. Tool capability order: explicit tools, then bash, then generated
code, then MCP** (EV-0115). Tools are consolidated around whole
workflows and namespaced, returning meaning rather than identifiers
(EV-0113). Reason: each step down the order costs context and
indirection.

**D5. Continuity across context windows rides on artifacts and git
history, not on compaction alone** (EV-0085, EV-0117). Reason: a
compacted summary loses exactly the detail a resumed run needs.

**D6. Cheap guardrails run beside the work and trip a wire, and
cross-cutting policy sits at the runner rather than inside an agent**
(EV-0076, EV-0120, EV-0119). Reason: a guardrail an agent can configure
away is not a guardrail.

**D7. Memory is a swappable store behind one interface with an explicit
trimming policy** (EV-0117). Reason: recall is not relevance.

**D8. Evaluation suites start at twenty to fifty tasks harvested from
real failures, scored with pass@k and pass^k** (EV-0087). Reason:
agents are non-deterministic, so a single pass proves little.

## Preferences

Taste. Freely overridable, no reason required.

- Event-sourced conversation state over ad-hoc message history
  (EV-0050, EV-0001).
- Functional composition before graph builders, reaching for a graph
  only when the graph earns itself (EV-0078).
- Condensers that always preserve the opening events (EV-0080).
- Mechanical stuck detection with thresholds tuned per model (EV-0082).

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
pack's own set is EV-0109 to EV-0121, imported from this pack's
research fragments; the rest are shared estate rows. Research synthesis
and the disagreements behind this file are in
`packs/agentic-development/research/NOTES.md`.
