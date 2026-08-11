---
summary: What a reviewer or checker can verify about architecture work, split into what is executable today and what stays a judgement call
kind: record
scope: estate
type: example
tags: [arch, ci, tooling]
sources: [EV-0097, EV-0159]
---

# Architecture pack checks

Evaluation criteria for work in this domain. Each check names what it
verifies and which requirement it serves. The split that matters is
the last column: a check that needs a person is not a gate, and
calling it one is how a pack starts lying about its own coverage.

## Executable today

These need no judgement. A script or a CI step decides.

| Id | Verifies | How | Serves |
| --- | --- | --- | --- |
| A-01 | A boundary contract file exists and parses | run the tool's own config parse | B1 |
| A-02 | The contract contains at least one directional rule for each declared boundary | parse the contract, compare against the declared boundaries | B1 |
| A-03 | The boundary command exits 0 on the delivered tree | run it | B1 |
| A-04 | The boundary command exits non-zero when a violation is injected, and 0 again when reverted | inject, run, revert, run | B1 |
| A-05 | The same command is invoked from a committed CI workflow or pre-commit config | grep both files for the command string | B1 |
| A-06 | A decision record exists for each door-closing change in the diff | path match against the decisions directory | D11 |
| A-07 | Each decision record carries a considered-options heading with two or more options and a decision-outcome heading | heading and list-item parse | D11 |
| A-08 | Each decision record names the enforcement tool and states the dependency direction | string presence of the tool name plus a direction phrase | D11 |
| A-09 | A container-level view artefact exists and names every module in the contract | parse the DSL or the Markdown heading, compare module names | D4 |
| A-10 | Two independent builds of the same source produce identical bytes | build twice, compare hashes | D12 |
| A-11 | Build tools are pinned by version or hash rather than taken from the host | manifest and lockfile inspection | D12 |
| A-12 | Committed generated artefacts match a fresh generation from source | regenerate into a temp dir, diff | B4 |
| A-13 | Every generated client call site checks the response succeeded | pattern scan of the generated client surface | B4 |
| A-14 | Webhook handlers read the raw body before any parse, and verify before any use | call-order scan of the handler module | B5 |
| A-15 | Webhook verification uses a non-zero recency tolerance | config or constant inspection | B5 |
| A-16 | Every migration adding a table has a matching consumer and retention note | migration file and table registry comparison | D9 |
| A-17 | No new deployable or datastore appears without a decision record naming the signal that justified it | manifest delta plus record lookup | D1, D8 |
| A-18 | Every module named in the contract resolves in the source tree | resolve each source and forbidden module against the package tree; an unresolved name fails | B1 |

A-01 to A-05, A-07 and A-09 are exactly the shape of criteria 1 to 9
in `benchmark/drills/architecture.md`, so a pack that passes the drill
passes most of this column by construction.

A-18 is here because this pack shipped a skeleton forbidding
`catalogue.repository`, a module that was never in the tree, and A-01
through A-04 all passed over it: it parses, it names a direction, the
run is green, and an injected violation of a different rule still trips.
A rule pointed at nothing is the one shape that column cannot see. It is
also what a package rename leaves behind, which is the common case.

## Judgement, not executable

These decide whether the work was any good. A reviewer answers them,
and the answers belong in the review record rather than in a gate.

| Id | Question | Serves |
| --- | --- | --- |
| J-01 | Is the declared decomposition the right one, or merely enforced? No tool in the ledger can answer this, and all three say so | B1 |
| J-02 | Does the decision record's losing option represent a case someone would actually argue, or a straw one? | D11 |
| J-03 | Is the boundary crossed at runtime through dependency injection, reflection or string-keyed lookup, where no static check can see it? | B1 |
| J-04 | Does the adapter interface model the venture's need, or the current vendor's shape? | D7 |
| J-05 | Is the exit route written down specific enough to cost, naming what replaces the vendor and what migrates? | D7 |
| J-06 | Does each view answer a named concern of a named stakeholder, or is it a diagram with no defence? | D4 |
| J-07 | Was a split justified by a measured signal, or by a preference for the shape? | D1, D2 |
| J-08 | Does a port exist where no second driver or device is plausible? | preference on ports |
| J-09 | Is a stored derived value a genuine snapshot or a cache with no invalidation owner? | D5 |
| J-10 | Has a default been departed from without a recorded reason? | all defaults |

## What is not checkable yet, and why

- **Runtime boundary conformance.** The only public prior art is a
  call-graph tool that is not public (EV-0159). Until an equivalent
  exists, J-03 stays a question a person asks.
- **Whether the boundary helped.** No source in the ledger measures
  outcomes for machine-enforced boundaries in a codebase of one or two
  people. A-01 to A-05 verify the mechanism, not the benefit, and this
  pack does not claim otherwise.
- **Decision quality.** EV-0097 records that there is no measured
  evidence that decision records improve outcomes. A-06 to A-08 check
  the shape of an argument, never its strength.

## Using this file

At review time, run the A column and answer the J column in the review
record. A pull request that passes every A check and fails J-01 is
correctly enforced and possibly wrong, which is the honest state of
the art rather than a gap in the checking.
