---
summary: Cadence template, the recurring session schedule and the rules that keep it honest
type: template
tags: [eos]
template: true
extracted_from: Venture A@d2e3250
---

# CADENCE · Recurring sessions

The heartbeat. The operator (later: a scheduler) launches whatever is
due; the running session updates `last_run` and `next_due`. Frequencies
are starting values, tuned only via the retrospective.

<!-- scale: M -->
| Cadence | Role | Frequency | last_run | next_due |
| --- | --- | --- | --- | --- |
| Triage and queue ordering: reorder `org/QUEUE.md`, promote or decline suggestions, check what is due below | PLAN | Weekly | | |
| Stakeholder update: built, blocked, changed, next | PLAN | Weekly or per agreement | | |
| Retrospective and freshness sweep: what dragged, expired `review_by` items, EOS feedback filed | PLAN | Monthly | | |
<!-- scale: end -->
<!-- scale: L -->
| Cadence | Role · Playbook | Frequency | last_run | next_due |
| --- | --- | --- | --- | --- |
| Triage and queue ordering | PLAN · PB-050 triage | Weekly | | |
| Stakeholder update: built, blocked, changed, next | PLAN · PB-051 | Weekly or per agreement | | |
| Verification sweep (clear `in_verification`) | VERIFY · PB-030 | Weekly or on demand | | |
| Practice audit, rotating | VERIFY · PB-022 | Fortnightly | | |
| Compliance and regulation watch | WORK · PB-021 | Monthly | | |
| Maintenance sweep (deps, archives, expiry flags) | WORK · PB-013 | Fortnightly | | |
| Knowledge promotion and freshness | PLAN · PB-040 | Monthly | | |
| Retrospective and org self-improvement | PLAN · PB-050 | Monthly | | |
| Backup restore test (prove, don't assume) | WORK · ops runbook | Monthly from first production deploy | | |
| Deep review: roadmap, metrics, budget, WIP, tier tuning | PLAN with HUMAN | Quarterly | | |
<!-- scale: end -->

Rules: a due cadence outranks new P2 and P3 work. Every run leaves a
session log. A cadence that finds nothing still records checked, clean,
sources and date; silence is not evidence.
