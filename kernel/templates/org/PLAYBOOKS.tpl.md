---
summary: Venture playbook template, per-mode procedures plus wide build, hardening, incident, upkeep and retro
type: template
tags: [eos]
template: true
---

# Playbooks

One versioned procedure per kind of session. Launchers stay tiny and
stable; the evolving detail lives here, so improving a procedure
means editing one file. Every procedure starts from the router's
ruling and ends with the close rule in org/START.md.

## express

1. Confirm the ruling is R0 and the free band covers every decision
   in sight; otherwise convert to Standard now.
2. Do the work in one coherent run. Targeted checks: the affected
   tests plus lint and types on the touched scope.
3. Commit with a message that is the whole record, and self-merge. If
   a derived risk fact changed mid-run, stop and re-route instead.

## standard

1. Open or take the task record; declare facts, let the router rule.
2. Plan briefly inside the record's budget, implement with tests per
   org/TESTING.md, document in the same change.
3. Run the affected tests the map names, widening on low confidence.
4. Close: gate-time re-route against the actual diff, then merge on
   green. The task joins the sampled-review pool unless the routing
   reasons demand independent review.

## spike

1. Enter with the question, timebox and budget on the record; branch
   spike/T-####.
2. Explore freely inside the sandbox; checks may wait; nothing
   merges.
3. Exit on answer or timebox: discard, or harden.

## harden

1. Open a fresh task through the router for the spike's keeper.
2. An ORACLE session authors acceptance independently where the
   ruling demands it.
3. Reimplement or lift the spike's material to standard quality with
   full checks; the spike branch is deleted after harvest.

## high-assurance

1. The record states the invariants and the rollback plan before any
   work.
2. ORACLE authors and freezes the acceptance oracle first.
3. EXECUTOR implements to the frozen oracle; amendments only via the
   append-only workflow, never by the implementer.
4. REVIEWER judges at acceptance; R3 waits for the operator's
   recorded approval before anything irreversible.

## parallel (integrator)

1. Plan disjoint lanes; write and commit org/claims.json before any
   dispatch; each lane carries its own mode.
2. Dispatch lanes to worktrees or subagents. Refuse unscheduled
   sessions; quarantine their branches to adopt or discard, and never
   delete quarantined work without operator authority.
3. Per lane merge: verify the diff against the assigned claims, run
   affected plus shared contract tests, then rolling integration
   checks.
4. Regenerate every derived view; the full suite runs at release
   tier.

## wide build

For work wide enough to run several lanes at once, and only then. It is
a shape for the parallel wrapper above, not a new mode: every lane still
carries its own ruled mode and its own claim.

1. Rule the fork before anything is dispatched. The question is whether
   this work wants lanes at all, and
   `packs/agentic-swarm/guides/GD-SWARM-001-swarm-or-single-agent.md`
   answers it. Do not run wide over work one session already does well,
   and do not run wide over a chain.
2. Then run the method in org/GRAPH_BUILD.md: cut the partition, write
   the lane briefs, dispatch, merge, and what stops a run. That file is
   the executable half of `packs/agentic-swarm` compiled into this
   venture, and the procedure is written there and nowhere else, so
   there is one copy to keep true. The pack behind it holds the rules,
   the defaults and the evidence, including the evidence against
   running wide at all. Read the pack before the first partition.
3. Close by journalling the run: the partition, what each lane
   returned, and what the integrator had to repair. That journal is the
   only evidence the venture will have about whether running wide paid.

## hardening pass

Independent evaluators and test generators run against the
integrated result: mutation, property, contract, accessibility,
performance, security. They generate findings and tests only and
never change product behaviour; every finding routes back through
the owning lane for repair, then final acceptance.

## incident

1. Operator approval per event, recorded; open the append-only
   incident record before acting.
2. Smallest reversible containment (flag off, revert, scale to zero,
   rotate credentials), rollback path stated, four-hour default
   limit, extension re-approved.
3. Record every bypassed gate as bypassed.
4. After containment: a retrospective oracle by a non-implementer
   plus full validation before the fix becomes durable; the checker
   blocks closure until green. File the post-incident review task.

## upkeep

The fortnightly sweep: dependency updates within policy, expired
reviews flagged, the claim set current, derived views regenerated,
dead task records closed or discarded, spend noted. Nothing
behavioural changes here; discoveries become proposed task records.
A sweep that finds nothing still records checked and clean with the
date.

## retro

Monthly, on evidence: sample the review pool and the recorded tier
exceptions (one-off ones sit on the task records they lowered, standing
ones in the venture's decision records), read escaped defects, oracle
amendment frequency and ceremony spend against budgets. Tune the
sampling rate and the cadences; propose policy or doctrine changes
through the graded path (experimental edit, ADR); set one deliberate
experiment. The organisation edits itself here and nowhere else.

## stakeholder-update

Compile from records and git, never compose from memory: built,
blocked, changed, next; one page, sent by the operator. Anything
needing a stakeholder decision links a question.

## guard-validation-review

Quarterly: confirm the adapter validation report is current for the
mapping in force (any adapter or mapping change voids it), check
capability-profile expiry and evidence, and confirm the always-human
list still matches reality. Without a current report, guarded
classes are manual-only and the policy's guard.validated must say
false.
