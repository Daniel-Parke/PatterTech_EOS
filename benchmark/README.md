---
summary: How to run and score one benchmark session, the run_meta.json contract, and the honesty rules
type: example
tags: [eos, testing]
---

# Benchmark harness

This directory holds the harness for the v1 versus v2 comparison. The
frozen rules live in `PROTOCOL.md`. This file covers the mechanics of
one session.

## Running one session for a task

1. Materialise the fixture into a scratch directory outside the repo:

   ```
   python benchmark/runner.py materialise --fixture app-static \
       --dest /path/to/scratch --task benchmark/tasks/T03
   ```

   This copies the fixture (holdout material excluded), initialises a
   git repo with an initial commit, applies the task's `break.patch`
   if there is one, and prints the task prompt.

2. Start a fresh agent session in the scratch directory, per the
   settings in `PROTOCOL.md`, and give it the printed prompt verbatim.
   Capture the session transcript as JSONL.

3. When the session ends, score it (see below). Use
   `python benchmark/runner.py prompt --task <dir>` if you only need
   the prompt again.

## Scoring

`score.py` takes the task, the scratch directory, the transcript and
run labels:

```
python benchmark/score.py --task benchmark/tasks/T03 \
    --scratch /path/to/scratch --transcript /path/to/transcript.jsonl \
    --variant v2 --run-id T03-v2-r1
```

It works in this order:

1. Parses the transcript: counts Read tool uses as files_read and
   Write and Edit uses as files_written, sums token usage, takes wall
   clock from the first and last timestamps, counts AskUserQuestion
   entries as operator_events, and counts assistant turns. Written
   paths matching ceremony patterns (org/logs, STATE, session-log,
   resume-packet) have their written lines summed as ceremony_lines.
2. Writes `run_meta.json` into the scratch directory (contract below),
   before any criteria script runs.
3. Runs every criteria script for the task against the scratch
   directory. Each script prints one JSON object:
   `{"id": ..., "pass": true or false, "reason": ...}`.
4. Appends exactly one row to `results/ledger.json`.

## The run_meta.json contract

Before running any criteria script, `score.py` writes `run_meta.json`
into the scratch directory so criteria scripts, probe criteria in
particular, can consume transcript-derived facts without parsing the
transcript themselves. The shape is:

```json
{
  "operator_events": 0,
  "commands": ["every Bash or shell command string from the transcript"],
  "files_written": ["paths written during the session"]
}
```

- `operator_events` is the count of AskUserQuestion tool_use entries.
- `commands` lists every shell command string found in the transcript,
  in order.
- `files_written` lists the file paths of Write and Edit tool uses.

Criteria scripts receive the scratch directory as their first argument
and can read `run_meta.json` from its root.

## Ablation overlays

`ablations/` declares four policy overlays as JSON. In P0 they are
declarations only; they get wired to the policy engine in P2.

## Honesty rules

- The ledger is append-only. `score.py` refuses a duplicate run_id and
  rewrites nothing. Bad rows are corrected by appending a new row and
  noting the supersession, never by editing history.
- v1 failures are recorded unchanged and never fixed. Fix-and-restart
  applies to v2 runs only.
- The diagnostic holdout is visible to the build side. That is a known
  limitation and is recorded as one wherever holdout-scored numbers
  are reported.
- Perceived speed is never accepted as evidence. Only measured wall
  clock, tokens and harness-counted operator events count.
