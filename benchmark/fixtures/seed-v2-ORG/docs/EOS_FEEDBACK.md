---
summary: FieldKit feedback file, the one channel back to the EOS, harvested monthly
type: template
tags: [eos]
compiled_from: kernel/templates/EOS_FEEDBACK.tpl.md
---

# EOS feedback

The venture's channel back to the shared brain. One writer per repo per
concern: the venture writes here at will; the EOS harvest (PB-E02)
reads it monthly and never writes here. Nothing in this file blocks the
venture; it banks what the estate should learn.

Entry format, newest first, one dated entry per item:

- `YYYY-MM-DD · friction` · a template, playbook or rule that fought
  you, with the file and the moment it hurt.
- `YYYY-MM-DD · ruling-report` · a wargame ruled here worth counting
  early, or a default that felt wrong when argued.
- `YYYY-MM-DD · draft-wargame` · a fork no wargame covered. State the
  question, the options you saw, the decision rule you used, and your
  ruling as the first worked entry.
- `YYYY-MM-DD · ceremony-complaint` · ceremony that cost more than it
  protected, with the evidence.
- `YYYY-MM-DD · lesson` · anything the estate would pay to know.

## Entries

- `2026-08-03 · lesson` · rubric item A10 (the seed check's D004) says
  every `set at first build` deferral must have an open item
  scheduling the lock-in. At ORG the check never runs: the queue-file
  map in tools/eos/checks/seed.py still reads S, M and L, so ORG has
  no entry and seventeen deferrals passed unchecked. This seed points
  them all at org/tasks/T-0001.json by hand, but a rubric item that
  silently does not apply is worse than one that fails loudly.
- `2026-08-03 · friction` · kernel/templates/LOCKBOOK.tpl.md still
  tells the reader that the first-build lock-in "notes it in the
  worklog or queue". Neither file exists at v2: S keeps docs/TASKS.md
  and ORG keeps task records with a derived org/TASKS.md. The sentence
  is unfenced template prose, so the compiler had to leave it while
  pointing every deferral at org/tasks/T-0001.json instead. Update the
  sentence to name the v2 surfaces.
- `2026-08-03 · friction` · kernel/templates/org/cadence.tpl.json
  demands a stakeholder-update frequency and first due date, and the
  Session 0 interview answers neither: FieldKit has one operator and
  its users are the firm's own staff. Rather than invent a cadence the
  compile set the row to on-demand with no due date and recorded Q-003
  in org/QUESTIONS.md. A template that forces a value the interview
  never asks for pushes a compiler towards inventing one.
- `2026-08-03 · friction` · kernel/templates/org/policy.tpl.json ships
  the Express admission thresholds (`max_diff_lines` 100,
  `max_files` 5) as fixed values with no slot, so a compile cannot tune
  them to the venture even though the policy schema says the capability
  profile tunes exactly those numbers. This seed left them at the
  template's values. Either give them slots or say in COMPILE.md that
  they are never venture-tuned at Session 0.
- `2026-08-03 · friction` · the same template's `GUARD_MAPPING_REF`
  and `CAPABILITY_PROFILE_REF` slots want repo-relative paths to
  records that no matrix row ships, so a truthful compile has nothing
  to point at. This seed filled the capability profile with the level
  id `conservative` (the schema allows an id) and the mapping ref with
  `org/guard-mapping.json`, the path the mapping must land at before
  `guard.validated` can turn true. Neither file exists yet, which is
  why every guarded class is manual-only and why Q-004 is open.
- `2026-08-03 · lesson` · the v1 M-scale seed shipped its first item as
  a queue row with no work order behind it, which is a Part II Article
  4 problem the moment a session takes it: nothing declared the facts,
  so nothing routed. This seed ships org/tasks/T-0001.json instead, a
  record valid against kernel/schemas/task-record.schema.json with its
  declaration, its ruling and its reasons list. It cost one file and it
  removes the whole class of failure.
