# support-digest

The nightly job that reads yesterday's support transcripts, pulls a
structured complaint record out of each one, and rolls the week up into
a single report for Thursday's product meeting.

## Layout

- `transcripts/<date>/` one text file per closed conversation, dropped
  there by the helpdesk export at 03:10. Read only: the export rewrites
  the folder every morning and nothing in this repo should edit a
  transcript.
- `jobs/nightly.py` the runner. Walks one night's folder, calls the
  extractor on each transcript, appends to `state/complaints.jsonl`.
- `jobs/extract.py` the extraction step. One transcript in, one
  complaint record out.
- `schemas/complaint.schema.json` the shape an extraction has to match.
- `tools/validate_complaints.py` checks a complaints file against that
  schema and exits non-zero on the first bad record.
- `reports/` the weekly rollup, one file per ISO week. This is what the
  product meeting reads.
- `docs/runbook.md` how the job is run, and what to do when it stops.

## Where this is up to

There are about forty transcripts a night. The runner does them one at
a time in a single process, which takes long enough that a reboot on
the ops box loses the night and someone has to start it again from
nothing in the morning.

The weekly report is written by hand from `state/complaints.jsonl` by
whoever is on rota, and the pull request that lands it in this repo is
opened by hand too.

We want the agent runner to do both: the per transcript extraction and
the weekly write-up. Nobody has written down how that run should be
shaped, so nothing has been built yet.
