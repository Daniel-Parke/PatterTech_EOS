---
summary: A worked repair of a quickstart that stopped working, applying the pack from activation through to the gate that stops it recurring
kind: example
scope: estate
sources: [EV-0175, EV-0327, EV-0328, EV-0330, EV-0331, EV-0332, EV-0333]
type: example
tags: [content, delivery, ci, tooling]
---

# EX-DOCS-001: the quickstart that stopped working

A small command-line tool ships with a `README.md`, a
docs/quickstart.md, a docs/reference.md and a `CHANGELOG.md`. A
user follows the quickstart, it fails, and they cannot tell why. There
is no documentation CI at all. This is that repository, repaired, in
the order the pack asks for.

## 0. What is actually wrong

Three separate defects, and it is worth naming them apart because they
have three different fixes.

- docs/quickstart.md has a shell block calling `--outdir`. The flag
  was renamed to `--out-dir` two releases ago. Nothing ever runs the
  block.
- `README.md` links to docs/setup.md, which was renamed to
  docs/quickstart.md. docs/reference.md links to
  `docs/quickstart.md#install-it`, and that heading is now
  `## Installing`. A path-only link check would catch the first and
  miss the second.
- The tool rejects an unknown flag with `print("error")` and exit 1, so
  the user who mistyped had nothing to go on.

The user's report is one symptom of all three at once.

## 1. Activation

Paths touched are `README.md` and `docs/`, so the path trigger fires.
Predicates: `publishes_docs` is true, `documents_executable_surface` is
true because the quickstart names a flag,
`emits_user_visible_failure` is true because the tool prints a rejection
message, and `renames_or_deletes_documented_page` is true for the
setup-to-quickstart move that was never finished. Four predicates, so
the pack loads in full.

## 2. Fix the text, but do not stop there

Correct the flag in docs/quickstart.md to `--out-dir` and grep the
whole tree for the old spelling, including `README.md`. Fix the two
links: repoint `README.md` at docs/quickstart.md, and repoint the
anchor at `#installing`.

That is the whole of the textual fix and it is worth about a week. The
same defect returns with the next rename. Requirement B3 exists because
this step is not the job.

## 3. Make the class of failure impossible to reintroduce silently

Three gate steps, all offline, all blocking, per
`packs/docs-dx/references/DOC_GATE.md`.

**Link and anchor checking (B1).** Add a CI step invoking a pinned link
checker with fragment checking switched on over the repository, with
the internal invocation kept separate from any external one. Verify
both directions: it exits clean on the repaired tree, and it exits with
the link-failure code against the commit before the repair (EV-0331).
A check that has never been shown to fail is not known to work.

**Snippet execution (B3).** Add a step that extracts every fenced
`bash` block under `docs/` and runs it in a clean directory with no
network, failing on any non-zero exit, and that fails any block
carrying neither execution nor a declared skip marker (EV-0330). Prove
it: add a temporary block calling the tool with `--bogus`, watch the
step go red, then remove it. That is the drift oracle, and without it
the step is decoration.

**Rename discipline (B2).** The setup-to-quickstart rename is the
original sin here. Going forward, a move either leaves a redirect or
updates every reference in the same change, and step 2 of the gate
verifies the second half (EV-0332).

Nothing in this gate touches the network. That is deliberate: an
external link check would make the build fail on somebody else's
outage, so if one is added at all it reports without failing (EV-0331).
A link to a host that does not resolve must not turn this build red.

## 4. Fix the message the user actually read

The user hit `print("error")`. Requirement B5 sets the floor at naming
the condition, showing the offending input and pointing at the accepted
alternative. So the rejection becomes, on the failure path:

- what happened: the flag was not recognised
- the offending input, quoted: `--outdir`
- the accepted alternative, named in full: `--out-dir`

Lower case, no trailing full stop, identifiers in backticks (EV-0328).
Exit code stays non-zero, and the failure is one the caller can
distinguish from a usage error with a valid flag, which is an interface
decision and is written down rather than inferred (EV-0175). A user who
mistypes now fixes it without opening the documentation at all, and
that is the cheapest documentation in the repository, on the page with
the highest read rate (EV-0327, scoped: the read-rate evidence is a
2017 eye-tracking study of students in one IDE, so take the direction
and not the numbers).

## 5. Record the consequence

`CHANGELOG.md` already has a running `Unreleased` section, so the entry
lands there under Changed, naming `--out-dir` and the old spelling it
replaces (EV-0333). Default D3: the entry describes what a consumer has
to do, not which commits happened. Cutting the release later is a
rename of that heading rather than an archaeology exercise.

## 6. What was deliberately not done

- **No prose linter.** Nothing in the user's report was about style,
  and a blocking style rule installed today would consume the attention
  that just fixed the content. If one is added it arrives advisory, per
  `packs/docs-dx/wargames/WG-DOCS-005-blocking-checks.md`.
- **No four-folder restructure.** The quickstart is a tutorial and
  reads as one. There is nothing confusing to diagnose, so the four
  forms have no work to do here.
- **No external link checking made blocking.** Advisory or absent.
- **No hand-written reference regeneration story**, because this tool
  has no generated reference yet. When it grows one, B4 turns on.

## 7. What a reviewer checks

The executable rows in `packs/docs-dx/CHECKS.md` cover the gate. The
two judgement rows that matter here: whether the corrected quickstart
is the sequence a new user actually needs, which no checker can judge,
and whether the changelog entry states a consequence rather than
restating the diff.
