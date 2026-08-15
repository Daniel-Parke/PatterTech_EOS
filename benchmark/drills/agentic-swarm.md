---
summary: Single-run cold-agent acceptance drill for the agentic swarm pack, cutting a partition on the dependency graph rather than on the backlog
type: example
tags: [eos]
---

# Drill: cut the partition on the graph, not on the backlog

## Scenario

A cold agent is given the agentic swarm pack and a seeded repository for
a small metering service. The tree holds:

- `meter/registry.py`, a name to handler map every module imports.
- `meter/schema.json`, the shared reading record every module reads.
- `meter/ingest/reader.py` and `meter/ingest/normalise.py`.
- `meter/pricing/tariff.py` and `meter/pricing/rounding.py`.
- `meter/reporting/render.py` and `meter/reporting/export.py`.
- `meter/reporting/wording.md`, the customer-facing summary copy.
- `meter/tests/e2e/test_pipeline.py`, the only check in the repository.
  It runs ingest, pricing and reporting end to end, and gates every
  change.
- `GRAPH.md`, the measured import graph. Inside each of ingest, pricing
  and reporting the modules depend on one another. Across those three
  groups nothing depends on anything except `meter/registry.py` and
  `meter/schema.json`, which every module imports.

`BACKLOG.md` holds seven items:

- I1, half-hourly readings in `meter/ingest/reader.py`, registered in
  `meter/registry.py`.
- I2, reject malformed timestamps in `meter/ingest/normalise.py`, with a
  new field in `meter/schema.json`.
- I3, publish a `normalised_reading` accessor from
  `meter/ingest/normalise.py`.
- I4, consume `normalised_reading` in `meter/pricing/tariff.py` in place
  of the private lookup it uses today. Needs I3.
- I5, correct the half-penny rounding in `meter/pricing/rounding.py`.
- I6, add a CSV export to `meter/reporting/export.py`, registered in
  `meter/registry.py`.
- I7, rewrite the customer-facing summary in `meter/reporting/wording.md`
  so it reads better.

`TASK.md` asks for a partition and a dispatch plan. Plan only, writing
nothing under `meter/`. It fixes the return contract and leaves every
judgement to the agent:

- `swarm-out/partition.json`, an object carrying `lanes`, `hub`,
  `manual_gate`, `verification` and `merge_order`. Each entry in `lanes`
  carries `id`, `owns`, `consumes`, `publishes` and `depends_on`. `hub`
  lists what the integrator owns and no lane may write. `manual_gate`
  lists backlog ids whose acceptance no script can decide.
  `verification` carries `per_lane_checks`, a map from lane id to the
  path of the check that decides that lane.
- `swarm-out/packets/<lane id>.md`, one per lane, under the nine level
  two headings `Objective`, `Write set`, `Read set`, `Return contract`,
  `Tool set`, `Budget`, `Stop condition`, `Acceptance condition` and
  `Escape`.
- `swarm-out/RUN.md`, carrying `token_ceiling`, `per_node_cap` and
  `delegation_depth`, each followed by an integer.

`TASK.md` also gives the four terminal statuses as a closed vocabulary:
`nothing-to-do`, `needs-decision`, `check-failed` and `killed`.

One run, no human turns. Nothing below asks whether the cut was a wise
one. That is judgement, and no criterion here claims it.

## Deterministic pass criteria

Every check must return true. Each is a file existence, exit code or
parse assertion, no judgement.

1. `swarm-out/partition.json` exists and parses as JSON. The top-level
   object carries `lanes`, `hub`, `manual_gate`, `verification` and
   `merge_order`, and every entry in `lanes` carries `id`, `owns`,
   `consumes`, `publishes` and `depends_on`, with `owns` a non-empty
   list.
2. `lanes` holds between two and five entries inclusive. Seven lanes,
   one per backlog item, fails here.
3. The `owns` lists are pairwise disjoint. No path appears in the `owns`
   of two lanes.
4. Prohibition. Neither `meter/registry.py` nor `meter/schema.json`
   appears in any lane's `owns`, and both appear in `hub`.
5. Let A be the lane whose `owns` holds `meter/ingest/normalise.py` and
   B the lane whose `owns` holds `meter/pricing/tariff.py`. Both files
   are owned by some lane, and either A and B are the same lane, or B's
   `depends_on` names A's id and `merge_order` lists A before B.
6. Prohibition. No lane's `owns` holds any path under `meter/tests/`,
   and `meter/tests/e2e/test_pipeline.py` appears in `hub`.
7. The key set of `verification.per_lane_checks` equals the set of lane
   ids exactly, no two lanes are given the same check path, and no lane
   is given `meter/tests/e2e/test_pipeline.py`.
8. Prohibition. `meter/reporting/wording.md` appears in no lane's
   `owns`, and `I7` appears in `manual_gate`.
9. For every lane id there is a file `swarm-out/packets/<lane id>.md`,
   and each holds all nine headings as level two headings, each with a
   non-empty body.
10. In every packet, the paths listed under `Write set` are set-equal to
    that lane's `owns` in `swarm-out/partition.json`, and the `Escape`
    section contains at least one of the four status tokens verbatim.
11. `swarm-out/RUN.md` holds a line matching `token_ceiling:` followed
    by an integer, and the same for `per_node_cap:` and
    `delegation_depth:`. All three are present and all three parse as
    integers.
12. Prohibition. Every file under `meter/` in the delivered tree matches
    the fixture by sha256, and no path under `meter/` has been added or
    removed.

## Scoring

Twelve binary checks, pass threshold 12 of 12. Partial credit is
recorded for diagnosis only and is not a pass.
