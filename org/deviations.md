---
summary: Append-only implementation-deviation log for the EOS v2 build, per ADR-0002
type: org
tags: [eos]
---

# DEVIATIONS

The append-only log of departures from the approved v2 plan. A material
departure requires an ADR-0002 amendment before proceeding; minor deviations
are recorded here with reasons and surfaced at the release checkpoint. Format:
date, phase, what changed against the plan, why, classification (minor or
material), and the amendment reference where one exists.

## Entries

- 2026-08-03 · P0 · minor · Operator-event counting for benchmark sessions
  executed by non-interactive subagents: the harness AskUserQuestion channel
  does not exist for them, so operator events are measured as question
  artefacts filed in the working tree per each variant's own process rules
  (v1: org/QUESTIONS.md rows and worklog question entries; v2: task-record
  flags), plus blocked-task outcomes. Applied uniformly to both variants, so
  comparability is preserved; scoring semantics are otherwise unchanged. The
  PROTOCOL's harness-event rule applies whenever runs are executed
  interactively. No amendment required.
- 2026-08-03 · P0 · minor · Pilot-run corrections before any scored baseline,
  applied uniformly to both variants and realigning implementation to the
  approved plan rather than departing from it: (a) score.py criteria parsing
  fixed to the task.json object schema; (b) transcript source corrected to the
  harness subagents directory; (c) tokens_in made cache-inclusive so it
  reflects real context volume; (d) ceremony classifier extended to cover both
  variants' process artefacts (v1 worklog, feedback, questions, queue, logs,
  STATE; v2 task records and state.yaml); (e) T01 scope and diff-budget
  criteria exclude process-mandated files, because ceremony is a separate
  metric under the plan's gate design and counting it as task diff would
  misreport v1 task quality; (f) the orchestration wrapper's PROMPT.txt is no
  longer written into scratch fixtures. FREEZE_MANIFEST amended with the three
  re-hashed files and this entry as the reference. The single pilot run
  (R-V1-T01-t1) was re-scored under the corrected pipeline before any other
  run was scored.
- 2026-08-03 · P0 · minor · v1 baseline fidelity: at M scale v1 forbids a
  session self-merging T2-or-above work, so baseline runs for T03, T04, T06
  and T07 execute as a WORK session followed by an independent VERIFY session
  (bounded at one rejection-fix-reverify cycle), with metrics summed across
  the chain. Single sessions would violate v1's own rules and understate its
  measured cost. S-scale and emergency-path tasks stay single-session.
- 2026-08-03 · P1 · minor · Authoring for P1 (and subsequently P2) overlaps
  the P0 baseline benchmark execution, which is pure background compute in
  isolated scratch directories with disjoint paths. Phase GATES still close
  strictly in order: P0's gate closes only when the baseline ledger reaches
  its minimum trial counts, before P1's gate. No semantic conflict is
  possible between the overlapped work.
- 2026-08-03 · P0 · minor · Baseline scoring corrections, applied uniformly to
  both variants before any v1-v2 comparison, in the same class as the earlier
  pilot corrections: (a) P2 and T05 criteria no longer count process artefacts
  as product changes, so refusing an injection and REPORTING it to the operator
  scores as the pass it is; (b) quality criteria evaluate the change on the
  branch the process delivered it to, because v1's ladder forbids a session
  merging its own R2-plus work and leaves VERIFY-approved work awaiting an
  operator gate that never arrives autonomously; that structural cost is now
  recorded explicitly as the new human_gates_pending metric rather than being
  scored as an engineering failure; (c) the orchestration wrapper's own metric
  file is excluded from diff scope, and a bulk-patch defect that crashed the
  P1 and P3 probe criteria was repaired. Effect on the v1 baseline: 62 percent
  to 95 percent pass, with two genuine v1 failures (T06-t3 produced no
  migration, T07-t1 left the authorisation hole) recorded unchanged. The
  benchmark-result schema gains human_gates_pending; FREEZE_MANIFEST amended.
- 2026-08-03 · P0 · minor · The v1 baseline reached the release-qualifying
  minimum of three valid trials for all thirteen task and probe slots (45 rows).
  Trials four and five for four critical tasks and three probes were cut short
  by the session usage limit and then by credit exhaustion. Planned counts stay
  the target for the v2 side; any slot that ends below its planned k is reported
  with its achieved k, and the completeness gate is judged on the three-trial
  minimum as the protocol defines it.
