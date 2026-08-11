---
summary: The fixed shape of a discovery record, its sections, its line grammars, and what counts as a citable source
type: foundation
tags: [product, testing]
kind: fact
scope: estate
sources: [EV-0059]
volatility: slow
review: 2028-07
---

# The discovery record

Level-three material behind requirements B1 to B8 in
`packs/product-discovery/PACK.md`, of which B6 and B7 bind and the rest
are defaults after the 2026-08 audit. One record per decision, named
`discovery.md`, beside the work it decides. A record longer than two
screens is usually a research note that forgot to reach a verdict.

## The sections, in order

Headings are exact. A checker reads them literally, and a renamed
heading is a missing section.

```
## Problem
## Evidence
## Signal
## Risks
## Options
## Decision
```

`## Options` may be omitted when only one thing was ever on the table,
and the record says so in one line. Everything else is mandatory.

## Problem

What a person cannot do today, and what it costs them. Written so that
it stays true if the implementation changes completely.

Two rules, both from B2. The section does not contain the name of the
requested feature, because a problem section that names the solution has
not done any work. And it describes a person's situation rather than the
product's absence: "there is no bulk export" is a missing feature.

## Evidence

Where the claims come from. One line per source, naming the artefact,
what was read from it, and any filter applied to reach a count. The
filter is part of the claim: a count of tickets matching a search term
is a different claim from a count of tickets a person read and
classified, and the record says which.

Anything a model produced rather than a person supplied is labelled at
the point of use, per B6. The word is `unverified`, in the same line, so
that reading the citation and reading the caveat cannot come apart.

## Signal

The observations that would tell you whether this worked, fixed before
the work starts. One line each, in this grammar:

```
- signal: <the observation> | threshold: <what counts as firing> | source: <artefact>
```

The source is a file, a table, an export or a named instrument that
already exists. Naming a source you intend to build is how a record ends
up with a signal nobody reads. If the instrument does not exist yet,
building it is part of the work and the options section says so.

The order is the goals-signals-metrics ladder: state the goal, name the
observable signal, then pick the metric. A metric chosen before its goal
is a vanity metric by construction.

## Risks

Exactly four lines, one per risk, each with a written answer. None may
be blank and none may be merged.

```
- value: <would anyone choose it, and what says so>
- usability: <can they work it out, and what says so>
- feasibility: <can it be built with what is available>
- viability: <does it work for the business, including support and money>
```

Viability is the one a solo operator skips, so write it first. "Assumed
fine" is not an answer; "no recurring cost, no support surface,
reversible in an afternoon" is.

## Options

What else was considered, one line each, with what each buys and costs.
The point is that the chosen option was compared against something.

## Decision

The first non-blank line under the heading is exactly one of:

```
BUILD
TEST
KILL
```

Then the reason, in two or three lines, and the observation that would
overturn it. KILL is a successful outcome of a discovery. A record that
reaches KILL and says why is worth more than one that reaches BUILD by
not asking.

## The TEST verdict carries two extra lines

TEST means the next step is an experiment or a deliberately limited
release. Two lines are mandatory under the decision, per B7:

```
- stopping rule: <when you stop looking and what you do at each outcome>
- sample: <integer, the number of users or events the test will run over>
```

The sample cannot exceed the population that exists. A sample larger
than the product's user count is the clearest sign the record was
written without reading the numbers. The stopping rule is fixed before
data arrives, with the metric and the segmentation, and names what
happens on a positive, flat and negative result. The asymmetric shape is
the usable default: the goal metric drives the ship decision, guardrails
block only on significant harm (EV-0059, vendor documentation, so the
thresholds are conventions). See
`packs/product-discovery/refs/SAMPLE_AND_SIGNAL.md` for whether the test
can be powered at all.

## What counts as a citable source

- A file in the repository or the fixture, named exactly.
- A table, export or instrument that exists now.
- A dated conversation with a named person.
- An evidence-ledger row, cited by its id.

Not citable: a persona with no interview behind it, a number with no
base, a benchmark figure lifted from a population that is not yours, or
anything a model asserted about a group of people. Those may appear,
labelled `unverified`, and they may not carry the decision.

## Numbers

Every number either appears in a source or is derivable by counting from
a stated filter. There is no third category. An untraceable figure is
struck rather than softened, per B5, and "roughly" is not provenance.
