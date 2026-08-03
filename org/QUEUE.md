---
summary: Pointer, the queue is now per-task records in org/tasks with a derived TASKS view
type: org
tags: [eos]
---

# QUEUE

The v1 queue is archived at `archive/v1/org/QUEUE.md`. Work now lives
as per-task JSON records in org/tasks/, one T-#### file each, with a
derived TASKS view regenerated only by the integrator. Two v1 items
survive as records: T-0002, the test-doubles decision guide, its
scheduling hold lifted by ADR-0002 for the v2 build only, and T-0003,
the hexagonal boundary statement, still held pending Venture A W1
(Daniel, 2026-07-07). A session not named in `org/claims.json` may not
create records or modify product files; unscheduled work is refused.
