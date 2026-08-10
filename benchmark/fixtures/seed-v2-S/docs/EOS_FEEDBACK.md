---
summary: Herbfield Lane feedback file, the one channel back to the EOS, harvested monthly
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

- `2026-08-03 · friction` · the seed check's D004 refuses this seed
  because it looks for the first-build lock-in item in
  docs/WORKLOG.md. The v2 matrix has no WORKLOG at any scale; the S
  work surface is docs/TASKS.md, and that file carries the lock-in as
  its top open item. The queue-file map in tools/eos/checks/seed.py
  still reads S, M and L, so at S it names a deleted file and at ORG
  it names nothing, which means ORG deferrals are never checked at
  all. Nothing a seed can do about either.
- `2026-08-03 · friction` · kernel/templates/LOCKBOOK.tpl.md still
  tells the reader that the first-build lock-in "notes it in the
  worklog or queue". Neither file exists at v2: S keeps docs/TASKS.md
  and ORG keeps task records with a derived org/TASKS.md. The sentence
  is unfenced template prose, so the compiler had to leave it while
  pointing every deferral at docs/TASKS.md instead. Update the
  sentence to name the v2 surfaces.
- `2026-08-03 · friction` · kernel/templates/OPERATORS_GUIDE.tpl.md
  ends with a Troubleshooting section that is not fenced by scale but
  names the ORG launchers RESUME and RUN. Compiled at S the section
  survives, so this guide tells the operator to run two launchers its
  own library does not carry. The compiler does not reword template
  text outside slots, so the text stands as compiled. The fix is a
  scale fence around those two sentences, or launcher-neutral wording.
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
  `docs/guard-mapping.json`, the path the mapping must land at before
  `guard.validated` can turn true. Neither file exists yet, which is
  why every guarded class is manual-only.
- `2026-08-03 · friction` · the canned brief
  (inception/briefs/BRIEF-S-brochure.md) pins the venture name Ashdown
  Joinery, but the compile instruction for this seed named the venture
  Herbfield Lane. The instruction was followed: venture name Herbfield
  Lane, every other fact from the brief, contact facts adapted to
  `workshop@herbfieldlane.example` and `01444 000000`. A drill brief
  and a compile instruction should not disagree on the name.
