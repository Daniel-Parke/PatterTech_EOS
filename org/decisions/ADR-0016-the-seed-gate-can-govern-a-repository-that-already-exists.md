---
summary: The seed gate judges what is in the repository, honours the reseed ancestry kinds it already documents, and stops failing open at the host hook
type: decision
tags: [eos, delivery, security]
status: accepted
decided_by: Daniel Parke
date: 2026-08-22
---

# ADR-0016: the seed gate can govern a repository that already exists

Venture D asked to adopt the EOS. It is the first repository the EOS has been
asked to govern that predates it, and the seed gate could not do it: `check
--seed` reported roughly 660 errors against a tree that has 378 commits, CI,
an enforced ring architecture and daily commercial use. None of those errors
described anything wrong with the venture.

## Context

Everything the EOS had seeded before was new. Venture A, Venture C and Project
Guth were compiled into empty or near-empty trees, where "every markdown file
in this tree is either a matrix file, an add-on, or unaccounted for" is a true
statement. PatterTech_Website was adopted rather than seeded, and its row says
so: pre-EOS, no pin, aligning to a compiled seed "when that work settles, no
earlier". Nobody had yet tried to compile a seed into a repository with a
history.

The templates anticipated this. `kernel/templates/COMPILE_REPORT.tpl.md` says
reseeds add two ancestry row kinds, `normalised` for pre-EOS files that gained
front-matter only and `preserved` for venture content the compile did not
touch. The checker did not implement them. `seed.py` read the compile report
*after* the per-file loop and used the row kinds for D003 alone, so a
`preserved` file still failed E002 for having no front-matter, which is the
defining property of being preserved, and a `normalised` file still failed
D001 for having no `compiled_from`, when by definition there is no template
behind it to name. Neither row kind had a test. The escape hatch existed on
paper and nowhere else.

Three further defects compounded it.

The walk had no `.gitignore` awareness. `SKIP_DIRS` was `.git`,
`__pycache__`, `.pytest_cache` and `node_modules`, so a virtualenv, a scratch
directory and a backups folder were all swept in. On Venture D roughly half
the files the gate judged were not in the repository at all, which means a
`uv sync` that pulled a dependency carrying a README would have changed a
governance verdict. A gate whose result depends on a dependency tree is not
measuring the venture.

A missing lock-book produced no finding at all. The lock-book carries the
scale, the scale gates twelve of the twenty checks, and the check that would
have reported it, E008 required-files, is itself gated on the scale only the
lock-book supplies. So a run without one reported a pile of errors while
twelve checks silently never executed, and exited 1 as though the seed had
failed its rubric rather than 2 as a run that could not happen.

And a blank source cell in a hand-maintained ancestry table raised an
uncaught `IndexError` out of `run_seed`, which is precisely the failure shape
the CLI's error handling exists to prevent.

Separately, and found in the same pass: the shipped Claude Code adapter could
not be wired. Its `hook_entry` was `guard eval --tool $TOOL --input $INPUT`,
where neither variable exists in a hook environment and `--input` expects a
file path. Had it run, `guard eval` returns 1 for a blocking verdict, and
Claude Code blocks on 2 and treats every other non-zero exit as a
non-blocking error it shows nobody. The one adapter the EOS ships would have
failed open on every manual-only and deny ruling.

## Decision

1. **The reseed ancestry kinds work.** The compile report is read before the
   per-file checks, and its row kinds govern them. A `preserved` file is
   exempt from the front-matter rules entirely, because the compile did not
   touch it. A `normalised` or `authored` file still owes `summary`, `type`
   and `tags`, but not a `compiled_from`, because no kernel template stands
   behind it. The exemption is scoped to what the compile report declares: a
   file with no ancestry row is still unaccounted for, which is what D003 is
   for.
2. **The walk judges the repository, not the disk.** When the seed is a git
   work tree, the markdown it walks is `ls-files -co --exclude-standard`,
   which is tracked files plus untracked ones that are not ignored. That is
   exactly "in the repository, or a candidate to be". Trees that are not git
   repositories, including the frozen fixtures, keep the old walk.
3. **A missing lock-book is a run that did not happen.** It reports, and it
   joins the cannot-run pairs, so the command exits 2 and says why on its
   first line rather than presenting a partial run as a rubric failure.
4. **A blank ancestry source is a row without a kind, not a crash.**
5. **The host hook speaks the host's contract.** A new `guard hook`
   subcommand reads the PreToolUse event as JSON on stdin, resolves the
   nearest venture policy at or above the event's `cwd` rather than always
   the EOS's, and exits 2 for manual-only, for deny, and for any action it
   cannot judge. `guard eval` keeps its own exit contract unchanged, because
   a caller that can read three codes should keep getting three.

## Consequences

Venture D's gate goes from roughly 660 findings to a run that exits 2 with
one line naming the missing lock-book, which is the honest state of a venture
that has been registered but not yet seeded. What remains after a lock-book
lands is real work the venture owes: ancestry rows for its own content, a
router within the cap, and the byte-identical pair E003 wants.

Fourteen tests cover the new behaviour, six of which fail against the code
this record replaces. The seventh guards a regression the fix must not cause:
untracked files that are not ignored are still judged.

This does not lower any bar. No check is weakened, no severity is reduced and
nothing is waived. Each change makes a check measure what it was written to
measure. The one bar that moves is the guard's, and it moves upward: rulings
that were silently discarded now block.

Not settled here: whether a venture that predates the EOS should compile a
full seed at all, or whether adoption at registration level with a pin is a
first-class state rather than a waiting room. `registry/PROJECTS.md` now holds
two rows of the second kind, PatterTech_Website and Venture D, and neither has
a `packs_adopted` list. That is a question for the estate, not for the
checker, and it wants its own record.
