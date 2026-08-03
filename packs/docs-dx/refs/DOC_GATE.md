---
summary: The documentation gate reference, what runs, in what order, blocking or advisory, and how to prove each step works
type: foundation
tags: [content, delivery, ci, tooling]
kind: fact
scope: estate
sources: [EV-0102, EV-0136, EV-0170, EV-0189, EV-0330, EV-0331, EV-0332, EV-0335]
volatility: slow
review: on-change-of:lychee-exit-codes-or-fragment-checking
review_by: 2028-05
---

# Documentation gate reference

Level 3 material behind binding requirements B1 to B4 and guide
`packs/docs-dx/guides/GD-DOCS-005-blocking-checks.md`. Read this when
wiring or debugging a documentation gate.

## The steps, in order

Order matters, because the cheap deterministic steps should fail before
the expensive ones run.

| Step | Checks | Blocking | Needs network |
| --- | --- | --- | --- |
| 1 | Structural lint over Markdown | yes | no |
| 2 | Internal links and anchors resolve | yes | no |
| 3 | Redirect or reference update for every moved or deleted page | yes | no |
| 4 | Generated reference regenerates with no diff | yes | no |
| 5 | Fenced blocks execute, or carry a declared skip marker | yes | no |
| 6 | Prose rules | no, advisory | no |
| 7 | External URLs reachable | no, advisory | yes |

Steps 1 to 5 must run with no network access. That is not an
optimisation. It is what makes the gate reproducible and what stops
somebody else's outage turning into your red build (EV-0331).

## Step 2: links and anchors

The two properties that matter.

**Fragments are checked, not just paths.** A link to
`docs/quickstart.md#install-it` must fail when the heading is renamed
to `## Installing`. Path-only checking passes that link forever, and
internal cross-references break silently on a heading rename more often
than they break on a file move (EV-0331).

**Exit codes are distinguished.** A checker that exits non-zero for
both "a link is broken" and "I could not start" lets a broken tool read
as a broken document, or worse, lets a crashed tool read as a clean
run. The checker this pack's evidence describes is lychee, which
reports 0 for success, 1 for a runtime failure, 2 for a link failure
and 3 for a configuration error, and validates fragments as well as
paths (EV-0331). Any checker with those two properties will do; the
tool choice is a preference and the properties are not. Wire the
pipeline so 2 fails the documentation step and 1 or 3 fails loudly as a
tooling problem.

**Pin the version.** The invocation names an exact release, not a
floating tag. A checker that silently gains a rule is a build that
fails on an unrelated day, and a checker that silently loses one is a
gate that stopped working without telling you.

**Separate the internal and external invocations.** Two commands, two
configurations, two exit-code handlers. Sharing one invocation is how
the external flakiness takes the internal check down with it.

## Step 3: redirect on rename

When a page moves or is deleted, one of two things must be true in the
same change: a redirect exists at the old path, or every reference to
the old path has been updated. Verify it rather than trusting it
(EV-0332). Step 2 catches the in-repository half. The redirect half
matters wherever a published URL exists, because a reader's bookmark is
a reference you cannot grep for.

## Step 4: regenerated reference

Run the generator, then fail on any difference against the committed
output (EV-0332, EV-0102). Three notes.

- Pin the generator version alongside the checker, or the diff will
  fire on formatting churn.
- Where the source of truth is an interface document, the same document
  supports a breaking-change diff (EV-0136) and property-based
  conformance testing (EV-0189). One artefact, three checks.
- A code comment is not a generated artefact. Nothing regenerates it,
  and nothing fails when it disagrees with the code beneath it.

## Step 5: executing snippets

The mechanics that make this work rather than merely exist.

**Extract by fence language.** Nominate the languages the gate
executes, for example `bash`, `sh` and the repository's primary
language. Everything else is untouched.

**Run each block in a clean working directory** seeded from the
repository at that commit, with no network and no credentials. A block
needing either belongs in the skip category.

**Fail the step on any non-zero exit** from any executed block, and
report which file and which block.

**Require a declaration on every unexecuted block.** The marker names
one of: illustrative, needs credentials, needs network, environment
specific, expected to fail. A block with neither execution nor a marker
is the finding, which is the whole design (EV-0330).

**Prove the step with drift.** Add a block that calls the documented
tool with a flag that does not exist, run the gate, and confirm it goes
red. A snippet gate that has never been shown to fail is not known to
work.

## Step 6: prose rules

Rules arrive at a non-blocking severity and are promoted only after
observation (EV-0335). Confirm exit-code and minimum-alert-level
behaviour against the release you pin before wiring any promotion,
because that behaviour was not verifiable from the tool's landing page
and must be checked rather than assumed.

Surface findings as annotations on the change under review rather than
only in a log (EV-0332). A finding in a log is a finding nobody reads.

## What the gate cannot do

It verifies that links resolve, snippets run, generated files are
current and prose matches a word list. It cannot tell you a page is
correct, complete, well organised, or that the snippet shown is the one
a reader needed. Those are the judgement rows in
`packs/docs-dx/CHECKS.md`, and they stay a person's job.
