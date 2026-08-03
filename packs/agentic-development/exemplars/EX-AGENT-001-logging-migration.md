---
summary: Worked topology decision record for a coupled logging migration across one service, and why fan-out was refused
kind: exemplar
scope: estate
type: example
tags: [eos, arch, tooling]
---

# EX-AGENT-001: coupled logging migration

A real-shaped worked example. The file below is both the example and
the artefact binding requirement B5 asks for, so the six sections are
the record itself rather than a description of one.

**The situation.** One service repository. About thirty modules call an
ad-hoc logging helper. The job is to move every call site to a
structured logger, introduce one shared configuration module, delete
the helper, and ship it. The test suite is good and runs in four
minutes. Deployment is externally visible. Two of the modules are hot
paths where a wrong log level floods a paid log sink.

## Topology

Two stages.

Stage one, the code change: **direct single-agent** inside a **bounded
loop**, with an **evaluator-optimizer** wrapper on each batch where the
test suite is the evaluator. The agent changes a batch of call sites,
runs the suite, and iterates until it passes.

Stage two, shipping: **sequential pipeline** ending in a **human
checkpoint**. Review, then approval, then deploy.

## Pressures

**Shared-state coupling** is the deciding pressure. Every call site
depends on one new configuration module whose interface is still
settling, so parallel workers would each write a different version of
the same assumption. That refuses fan-out/fan-in.

**Oracle quality** is high: the test suite plus the type checker catch
almost every mistake this change can make, which licenses the
evaluator-optimizer wrapper and removes any argument for a model judge.

**Reversibility** is low at the deploy step and at the hot-path log
levels, which forces the human checkpoint.

**Context pressure** is moderate. Thirty modules do not fit one window
comfortably, which is handled by batching and on-disk progress rather
than by spawning workers, because the cheaper answer to context
pressure is retrieval, not headcount.

**Cost** vetoes nothing here; the run is small either way.

## Bounds

- Turns: 120 agent turns for the whole run, counted across batches.
- Wall-clock: 90 minutes.
- Tokens: 1.5 million for the run.

On trip: stop, commit what passes, write the remaining call sites to a
progress file, and report the partial state. Do not deploy a partial
migration.

## Resumability

State survives a restart through git history plus a progress file
listing call sites done and remaining. That is event-log resumption in
the cheap form: the commits are the log.

Resumed side effects are idempotent because every batch is a commit
with a natural key, the module path, and the agent checks the progress
file before touching a module. Re-running a completed batch is a no-op.

## Verification

The test suite and the type checker hold external truth for the code
change, and they run on every batch. The deletion of the old helper is
verified mechanically by a grep for its import returning nothing.

There is no external oracle for whether the new log messages are
usefully worded, so no evaluator-optimizer loop is claimed for message
wording. It goes to the human at the checkpoint instead.

The **single-writer** rule holds trivially: one agent writes the
repository for the whole run. The configuration module has one writer
by construction.

## Approval

Two irreversible or externally visible acts, both gated by recorded
human approval at the act.

- Deleting the old helper, because downstream repositories may import
  it. Approval sits at the deletion, not at the end of the stage.
- Deploying. Approval sits before the deploy command, and the hot-path
  log levels are named in the approval request.

## Evidence

EV-0088 and EV-0052 for starting at a single agent, EV-0109 for
justifying the topology against a named failure mode, EV-0111 and
EV-0053 for putting iteration behind a real oracle, EV-0051 for
bounding by budget, EV-0079 for the idempotency requirement on resume,
and EV-0108 for gating the irreversible acts.

## What this example is for

It shows the more common answer. Most work does not need a graph, a
team or an orchestrator, and the discipline the pack asks for is
naming the pressure that would justify one and then noticing that it is
absent. Here decomposability looked high and shared-state coupling
killed it.
