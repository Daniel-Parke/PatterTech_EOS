---
summary: The coding pack applied end to end to a webhook receiver that swallows a signature failure and returns success
type: example
tags: [delivery, testing]
kind: example
scope: estate
---

# EX-COD-001: The webhook that always said yes

A worked run of the coding pack against one concrete situation, from the
first read of the code to the merge. Every pack rule that fires is named
where it fires.

## The situation

A venture repo has a payment provider webhook receiver, about 120 lines,
written by an agent four months ago. It has no tests. Support reports
that some events never reach the ledger, but the provider dashboard
shows every delivery as a 200. Reading the handler shows a single
try block around the whole body with a bare catch-all that logs and
returns the success response. Signature verification failures, malformed
payloads and ledger write failures all land in the same place and all
look identical to the provider and to the operator.

## Step 1: activation and routing

The pack activates on `edits_source` and on `decides_merge`. The task is
a FIX.

The task record declares touches-auth, because signature verification is
an authentication surface, and writes-production-data, because the
handler writes to the ledger. Under `kernel/POLICY_SPEC.md` those are
two active factors with two floors, and the higher one wins:
writes-production-data is a declared source of the data-deletion factor,
floor R3, and touches-auth is a source of the auth surface factor, floor
R2. The router rules R3, with the data-deletion reason first and the
auth surface reason second. That factor is named for its derived half, a
deletion detected in the diff; a declared production-data write is the
other source on the same row, and it carries the same floor. Under Wargame
`packs/coding/wargames/WG-COD-002-review-gate.md` that means independent
human review at acceptance, the oracle frozen before implementation, and
the operator approving the merge because an R3 always takes a human.
Nobody argued the tier down. The diff size was never the input.

Worth noticing, because it is the part most runs get wrong: declaring
the ledger write is what took this from R2 to R3. Leaving it off the
record would have ruled R2 and looked tidier, and no detector would have
argued: the router derives nothing that says a diff writes production
data, so that declaration rests on the owner and on nobody else.

## Step 2: the oracle strategy

Wargame `packs/coding/wargames/WG-COD-001-oracle-strategy.md`. The code has
no specification and the task both moves behaviour and needs current
behaviour preserved for the well-formed path. The rule maps that to
option B then option A: characterise first, then the failing test for
the intended change.

Wargame `packs/coding/wargames/WG-COD-004-pin-then-change.md` gives the
commit order. Three commits, in order.

## Step 3: commit one, the pin

A test feeds three recorded well-formed provider payloads through the
handler and asserts the exact ledger rows and the exact response body
they produce today. It passes at the current commit, unchanged. That is
requirement B2 satisfied, and it is the thing that will later prove the
fix changed nothing for well-formed input.

Two of the three payloads produced timestamps, so those fields are
scrubbed before comparison, per the third rule in
`packs/coding/references/ORACLES.md`.

## Step 4: commit two, the failing test

Before deciding what the fix looks like, decide what callers may
distinguish. Wargame
`packs/coding/wargames/WG-COD-003-failure-mode-contract.md` rules option C
here, because the surface has a caller outside the module and because a
signature failure and a malformed payload need different responses: one
is rejected outright, the other is worth recording for investigation.

Two failure modes are named. A test asserts that an event with a bad
signature raises the signature failure to the caller and that the
response is a rejection rather than a success, and a second test asserts
that a malformed payload raises the payload failure. Both fail at the
current commit. That is requirement B1 satisfied on both clauses: the
expected values came from the provider's documented behaviour rather
than from the handler, and both tests have been seen red. The failing
run is recorded in the task before anything else is touched.

## Step 5: commit three, the fix

The bare catch-all goes. Signature verification failures are translated
into the declared signature failure with the original cause attached.
Payload parse failures are translated into the declared payload failure.
Ledger write failures are re-raised, because the caller is the provider's
retry mechanism and a retry is the correct recovery. Nothing is logged
and dropped. That is requirement B3 satisfied, against the three
outcomes listed in `packs/coding/references/ERROR_PATH.md`.

The two failure names go into the module docstring and into the
README, spelled identically in the module, the tests and the README.
That is requirement B4 satisfied, and B4 applies here rather than
default D9 because the caller is the payment provider, which the venture
does not control.

The handler previously repeated the same eight-line ledger-row builder
in two branches. Both branches now call one helper, so the duplicate
block count for the file went down rather than up. Nothing else was
tidied, because no pending change demanded it, which is default D5.

## Step 6: the gate

Requirement B5. The diff-aware policy run reports one blocking finding
and two monitoring findings. The blocking finding is a broad exception
catch left in a helper the agent had not noticed; it is fixed in the
same commit. The monitoring findings are pre-existing and go to retro.
The error-path scan returns clean over the changed file. The declared
name equality check passes across the module, the tests and the README.
The pin from commit one still passes, which is the evidence that
well-formed input behaves exactly as before.

## Step 7: review and merge

R3, so an independent person reads it and the operator signs before it
lands. They read the error paths first, per
`packs/coding/references/REVIEW_GATE.md`. They ask one question: whether
translating the ledger write failure would have been better than
re-raising it. The answer is no, because the provider retry is the
recovery, and re-raising is what triggers it. That is a design question
argued on engineering grounds, which is what review is for.

They do not comment on the helper's name. Naming uniformity is a
preference in this pack, not a gate.

Approved on the health gradient: the change definitely improves overall
code health, and it is not perfect. One reviewer, one iteration. The
operator reads the ruling and its two reasons off the record and
approves, which is what the R3 floor is for. Merged to trunk the same
day, which is default D3.

## What this run cost

Three commits, one blocking gate finding, one review question, and one
operator approval. The pin took a few minutes and is the reason anyone
can say with confidence that well-formed events still behave the same.

## What it would have looked like without the pack

One commit. The catch-all replaced with something narrower, tested by
hand against one payload, merged because the diff was small. The
well-formed path unverified, the failure names in the code and nowhere
else, and the next agent to touch the file with no way to tell what the
handler was supposed to do.
