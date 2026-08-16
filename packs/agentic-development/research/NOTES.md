---
summary: Research synthesis for the agentic development and orchestration pack, topologies, context, tools, checkpoints, guardrails
type: example
tags: [eos]
---

# Agentic development: what the field actually disagrees about

Research cutoff 2026-08-03. Thirteen new sources in
`sources.fragment.json`, plus existing ledger records EV-0001, EV-0045 to
EV-0053, EV-0076 to EV-0089 and EV-0106 to EV-0108. Refresh triggers are
event-driven, not calendar: a major version of any of the six SDKs, a
new Anthropic harness or context publication, a Cognition-style public
reversal, or a controlled study that measures topology against outcome.

## Three materially different philosophies

**One thread, rich runtime services.** OpenHands puts the loop on an
event-sourced conversation and hangs condenser, security analyser, stuck
detector and confirmation policy off it as services (EV-0050, EV-0080 to
EV-0082); the MLSys paper reports the move cut system-attributable
failures at negligible overhead (EV-0001). Cognition argues the same
from the other end: fragmented context and conflicting decisions are the
failure, so keep one coherent thread (EV-0106), softened later to writes
single-threaded while other agents contribute intelligence (EV-0107).
Fits long-lived work on shared state where failure localisation matters
more than wall-clock.

**Minimal loop, strong model, hard budget.** mini-swe-agent is roughly a
hundred lines with bash as the only tool and a linear history, and
maintainer-reported results above 74% on SWE-bench Verified (EV-0052);
SWE-agent governs everything through one YAML and bounds runs by budget
rather than phase (EV-0051). Anthropic's C compiler run is the extreme
case: a minimal loop, sixteen parallel agents, no orchestrator, held up
only because the oracle was near-perfect (EV-0053). The harness posts
give the rule that generalises this pole: every component encodes an
assumption about what the model cannot do, so strip scaffolding as
models improve (EV-0089).

**Explicit graph with durable state.** LangGraph, Microsoft Agent
Framework and ADK all say the same thing in different syntax: reserve
determinism for order, retries and termination, let the model own the
inside of each step (EV-0077), and pay for graph machinery only when the
work is long-running, durable and human-gated (EV-0048, EV-0078). MAF
makes the barrier explicit, checkpointing executor state, pending
messages, pending requests and shared state at each superstep, with save
and restore hooks the participant must implement
(FRAG-AGENTIC-DEVELOPMENT-13).

Anti-patterns each pole produces. Rich runtime: services that fire on
false positives, such as stuck detection killing an agent that was
legitimately polling (EV-0082). Minimal loop: no failure localisation
when the oracle is weak, and regressions accumulate (EV-0053). Explicit
graph: ceremony for work that never needed a graph, plus the resume
trap, where pre-interrupt code re-executes so side effects must be
idempotent (EV-0048, EV-0079).

## Topology map, with what supports each

| Topology | Supported by | Choose when |
| --- | --- | --- |
| Direct single-agent | EV-0052, EV-0088, EV-0089 | Task fits one context, oracle exists, reversible |
| Sequential pipeline | EV-0077, EV-0078, FRAG-08 (chaining) | Stages have a stable order and typed handover |
| Bounded loop | EV-0051, EV-0052 | Free agency is fine but the resource envelope is not |
| Router | EV-0045 handoffs, EV-0077, FRAG-08 | Routing itself is the decision and the specialist owns what follows |
| DAG | EV-0048, EV-0078 | Real dependencies plus a need to inspect and edit state |
| Fan-out / fan-in | EV-0084, FRAG-08 (parallel gather) | Subtasks are separable and read-mostly |
| Orchestrator-worker | FRAG-04, EV-0108 | Breadth-first search where token cost buys coverage |
| Evaluator-optimizer | EV-0089, FRAG-03, FRAG-07 | An external oracle the generator does not hold |
| Event-driven resumable | EV-0001, EV-0048, FRAG-13 | Runs outlive a process, or must pause for hours |
| Human checkpoint | EV-0079, EV-0081, EV-0108 | Irreversible or costly actions, gate at the risk not the phase |

Selection order. Take the simplest topology that satisfies the task, and
promote only on a named pressure: decomposability and low shared-state
coupling permit fan-out; poor oracle quality demands an evaluator that
holds external truth; irreversibility demands a human checkpoint; latency
budgets buy fan-out at a token multiple; context pressure buys
delegation with condensed returns (EV-0086, EV-0084); failure
localisation demands the event log (EV-0001).

## Counter-evidence and live disagreements

**Parallelism.** Anthropic reports 90.2% uplift from orchestrator-worker
on research at roughly fifteen times the tokens, and says plainly that
it suits neither shared-context work nor most coding (FRAG-04).
Cognition says parallel actors fail through fragmented context
(EV-0106). Both are vendor practice. They reconcile only under the rule
many agents may read, one agent writes (EV-0107), which is the strongest
load-bearing constraint in this domain.

**Self-review.** Huang et al. show intrinsic self-correction degrades
answers without external feedback (FRAG-03); Anthropic separates
evaluation from generation because agents praise their own work
(EV-0089) and ranks defined rules and visual feedback above a model
judge (FRAG-07). MAST attributes a whole failure category to absent
verification (FRAG-01). Together: an evaluator without ground truth is
theatre.

**Scaffolding.** EV-0085 prescribes initialiser plus repeated coding
agent with progress artifacts; its March 2026 successor reports parts of
that scaffolding became unnecessary as models improved (EV-0089), and
ADK 2.0 now calls its own template workflow agents the rigid option
(EV-0046). Anything the pack fixes in place will rot.

**Interface effort.** SWE-agent's ACI paper shows interface design moved
task success materially in 2024 (FRAG-02); mini-swe-agent shows a single
bash tool beating it later (EV-0052). Read as capability-dependent, not
contradictory.

## Binding, default, preference

Binding requirements, because a violation is a defect:

- Single-writer rule. Parallel agents may read; writes to shared state
  are serialised through one owner or disjoint file ownership
  (EV-0107, EV-0108).
- Every topology above direct single-agent must name the pressure that
  forced it and the MAST-style failure it removes (FRAG-01).
- Any loop is bounded: turns, tokens, wall-clock, or all three
  (EV-0051), with a documented stop condition.
- Irreversible or externally visible actions pass a human checkpoint,
  placed at the risk rather than at a phase boundary (EV-0079, EV-0081).
- Evaluation is separate from generation and the evaluator holds
  external truth, tests, types, linters or a fresh context
  (FRAG-03, EV-0089).
- Runs are traceable: a stable span vocabulary, a workflow name and a
  group id linking related runs, with a switch to exclude payloads
  (FRAG-10, EV-0021, EV-0043).
- Checkpoint state is a trust boundary; never resume from a checkpoint
  of unknown provenance (FRAG-13).

Defaults, overridable with a recorded reason:

- Start at direct single-agent with a strong oracle (EV-0088, EV-0052).
- Context by just-in-time retrieval and progressive disclosure, not
  pre-loading (EV-0086, EV-0083, FRAG-06).
- Tool capability order: explicit tools, bash, generated code, MCP
  (FRAG-07); tools consolidated around workflows and namespaced
  (FRAG-05).
- Continuity across context windows carried by artifacts on disk plus
  git history, not by compaction alone (EV-0085).
- Cheap guardrails run in parallel with the work and trip a wire
  (EV-0076); cross-cutting policy sits at the runner, not the agent
  (FRAG-12).
- Memory is a swappable store behind one interface with an explicit
  trimming policy (FRAG-09).
- Evals start at twenty to fifty tasks harvested from real failures,
  with pass@k and pass^k for non-determinism (EV-0087).

Preferences, taste rather than law: event-sourced conversation over
ad-hoc history; functional composition before graph builders
(EV-0078); condensers that always preserve the opening events
(EV-0080); mechanical stuck detection with thresholds tuned per model
(EV-0082).

## Gathered, and what it settles

Eight sources were read for this pack and no binding requirement rests
on any of them. That is recorded here rather than left as a silent gap:
a record nothing cites is weight, and the choice is to cite it or prune
it. These are cited, because each one settles a question the pack
answers and would otherwise answer from taste.

**Progressive disclosure is a contract, not a habit.** The Agent Skills
specification sets a three-level loading contract, metadata at startup,
body on activation, resources on demand, with hard size limits
(EV-0014), and the reference skill collection packages capability as
self-contained directories costing about a hundred tokens until
something needs them (EV-0054). Both are what the pack's own activation
model claims to be, from outside this estate. They are why the model is
stated as a contract with limits rather than as advice about restraint.

**The harness boundary is becoming a protocol.** The Agent Client
Protocol is a versioned JSON-RPC surface in the LSP style, adopted by
JetBrains, Google and more than twenty-five agents (EV-0042), and a
platform layer is forming above it to govern asynchronous fleets of
heterogeneous agents (EV-0072). Neither binds anything: the estate runs
one harness and a protocol for swapping harnesses buys it nothing
today. They are recorded because the Wargame's topology forks assume the
boundary stays local, and that assumption now has a date on it.

**Durability belongs to the boundary.** Superstep checkpoints with a
request-response pattern make human-in-the-loop resumable without the
worker knowing it was ever suspended (EV-0047), and a mature harness
ships as a control plane over interchangeable agents and backends with
work triggered by events and schedules (EV-0049). Both are exemplars of
a mechanism this estate does not have and the pattern it would adopt if
it did.

**Instrument the work, not the model.** Standard span types with shared
gen_ai attributes and token-usage metrics make agent throughput and
quality measurable without inventing a schema per harness (EV-0013).
The pack prefers rather than binds this, because the estate's own
benchmark measures from transcripts and does not yet emit spans.

**Harness-sensitive benchmarking now exists.** Eighty-nine
human-verified terminal tasks in isolated containers, under a harness
built to make the harness itself a variable (EV-0073). Recorded as the
standard this estate's own benchmark falls short of: ours ran a variant
that never reached the tree, which is exactly the class of defect a
harness-aware design is built to expose.

## Where durability lives, unresolved

Two maintainers put the mechanism in different places and the pack
takes neither as doctrine. LangGraph makes durability a property of the
checkpointer: snapshots are thread-scoped, addressed by a thread_id,
and the default in-memory savers lose every one when the process
restarts, so a graph is durable only if it was deployed against a
persistent backend (EV-0449). Microsoft's framework
puts it at the boundary instead, where superstep checkpoints and a
request-response pattern let a paused run resume without the worker
knowing it was ever suspended (EV-0047).

The disagreement is worth carrying because it decides what a venture
has to operate. The first needs a database the graph owns; the second
needs a boundary that can hold a request open. Neither source measures
the other, and the LangGraph documentation says nothing about the
determinism requirements on node code, which is the constraint that
decides whether a resumed run is sound at all.

## What the pack must not do

Do not copy any vendor's agent taxonomy wholesale. Do not restate
maintainer-reported benchmark figures as doctrine; EV-0052, EV-0080 and
FRAG-04 are all self-reported. Do not encode a mechanism that needs
infrastructure this estate lacks, checkpointers, thread stores and
Cosmos containers are mechanisms, the pattern is what transfers
(EV-0079). Do not add scaffolding without naming the model limitation it
compensates for (EV-0089).
