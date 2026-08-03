---
summary: Single-run cold-agent acceptance drill for the support-operations pack, with deterministic machine-checkable criteria
type: example
tags: [eos, testing]
---

# Drill: run one inbox week and one customer-visible incident

## Scenario

A cold agent, given only this pack and a seeded fixture, is told: this
is the support inbox for a paid product with 60 customers, triage it,
run the outage that is in it, and turn the week into backlog items. One
run, no human hints. The fixture supplies `inbox/` with 40 numbered
items in fixed order (24 questions, 8 bug reports, 5 feature requests,
2 billing complaints, 1 outage at item 17 that four later items repeat
independently), a `customers.csv`, an empty `out/`, and a fixed clock.
Items 9, 22 and 31 lack any reproduction detail. The agent produces
`out/severity_policy.md`, `out/triage.json`, `out/incident-0001.json`,
`out/comms.log` and `out/synthesis.json`.

## Machine-checkable criteria and scoring

Pass requires 12 of 12; criteria 2, 5, 8, 10 and 12 are fatal. Every
check is a script over the produced tree, no judgement calls.

1. `triage.json` parses and holds exactly 40 records, one per item id,
   no duplicates, no extras.
2. Every record has non-empty `kind`, `priority`, `queue` and
   `triage_state` (`accepted` or `needs-info`), and `queue` partitions
   into at least `incident` and `request` with no record in both.
3. Items 9, 22 and 31 are `needs-info` and each carries a
   `next_action_due` date strictly after the run date.
4. Both billing complaints have `acknowledged_at` set and neither
   carries an auto-close timer field.
5. Item 17 and its four duplicates reference one shared `incident_id`,
   equal to the id in `incident-0001.json`.
6. `severity_policy.md` defines three or more ordered bands each with a
   written impact criterion, states the take-the-higher rule, and names
   one band that changes the response mode, not only the wording.
7. `incident-0001.json` has keys `severity`, `declared_at`,
   `declared_by`, `comms_owner`, `fix_owner`, `customers_affected`,
   `resolved_at`, `postmortem_due`; `severity` is a band defined in
   `severity_policy.md`; `postmortem_due` is at most five days after
   `resolved_at`.
8. `comms_owner` and `fix_owner` are separate non-empty fields, even
   when the values are equal.
9. `comms.log` has three or more entries with strictly increasing
   timestamps, the first before `resolved_at`, each naming an audience.
10. No file under `out/` contains a key or heading matching
    `mean_time|avg_.*_time|MTTR`; any duration reported carries a
    percentile label or is a raw count.
11. `synthesis.json` has `denominator`, `coding_stance` and a `themes`
    array; every theme has `count` and `item_ids`, every id exists in
    `triage.json`, `count` equals the length of `item_ids`, and the
    distinct ids number at most 40.
12. `python tools/eos_check.py --repo` exits zero, and no customer name
    or email from `customers.csv` appears under `out/` except in hashed
    or id form.
