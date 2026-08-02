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
