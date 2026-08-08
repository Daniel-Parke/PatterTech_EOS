---
summary: The error-path reference, what counts as handled, how failures are declared, and the checks that catch a swallow
type: foundation
tags: [delivery, testing]
kind: fact
scope: estate
sources: [EV-0011, EV-0023, EV-0025, EV-0061, EV-0171, EV-0174, EV-0175]
volatility: stable
review: 2028-02
---

# Error path reference

Level 3 material behind binding requirement B3 and guide
`packs/coding/guides/GD-COD-003-failure-mode-contract.md`. Read this
when writing or reviewing a handler.

## Why the error path gets its own rules

A retrospective analysis of 198 randomly sampled user-reported
production failures across five distributed systems found that 92 per
cent of the catastrophic ones came from incorrect handling of non-fatal
errors the software had already explicitly signalled, and about a third
of those were trivial mistakes visible to plain code inspection with no
system knowledge (EV-0174). Most reproduced on three nodes or fewer.

Scope: Java-heavy distributed data systems, 2014. The proportion belongs
to that corpus. What transfers is the direction of attention. The error
path deserves more review and test effort than the happy path, and a
large share of the damage is catchable by reading the handler.

## What counts as handling

A caught error must end in exactly one of these:

1. **Handled.** The failure is recovered from, and the recovery is
   itself observable, usually by a test.
2. **Translated.** The failure is converted into one of the module's
   declared failure modes, with the original cause attached, and raised
   or returned.
3. **Re-raised.** The failure passes through unchanged.

Anything else is a swallow. Logging and continuing is a swallow with a
receipt.

## Rejected constructs

- A bare catch-all with no exception type.
- A catch of the broadest type whose body is a pass, a continue, or a
  return of a default value.
- A handler that records the failure and then returns the success shape,
  so the caller cannot tell.
- A retry loop with no terminal failure, which turns an error into a
  hang.
- Catching to convert a signalled failure into a silently dropped row,
  record or message. Dropping is a decision, and a decision the caller
  cannot see is a bug.

## The declaration rule

The set of failures a caller may tell apart is contract surface. Once a
module documents that a caller can inspect a particular failure, it must
always be returned that way, on every path (EV-0175). Adding a
distinguishable failure is a minor change; removing or renaming one is a
major change (EV-0171).

Write the declaration in three places and keep the names identical
across them, character for character:

- the module or its public docstring,
- the tests that assert the failure reaches the caller,
- the README or interface documentation the caller reads.

Synonyms across those three are the failure this rule exists to stop. A
caller who matches on the name in the README and gets a different name
at runtime has no recovery.

## How the rule expresses itself per language

- **Exception languages.** Declare a module-level base failure and the
  small set of subclasses callers may distinguish. Attach the original
  cause rather than discarding it. Never catch the language's root
  exception type in library code.
- **Go and similar.** Wrap when the caller should be able to react to
  the cause, and convert without wrapping when the cause is an
  implementation detail you refuse to commit to. Inspection goes through
  chain-aware predicates rather than equality on a concrete type
  (EV-0175).
- **Result and Either types.** Enumerate the failure variants in the
  type. The compiler then does the check this reference is asking a
  reviewer to do.
- **Over a transport.** Put the taxonomy in the schema, so remote
  callers see the same set as local ones (EV-0023 for HTTP surfaces,
  EV-0025 for the payload shape). Version it by date with per-consumer
  pinning if semantic compatibility judgements are more than you want to
  own (EV-0061, EV-0011).

## Mechanical checks

These run in CI and need no judgement:

- A pattern scan for bare catch-alls and for catch bodies that are only
  a pass or a continue, over changed files.
- A test that asserts the declared failure reaches the caller for each
  declared mode.
- A string-equality check that every declared failure name appears in
  the module, the tests and the interface documentation.

The judgement-bound part is whether a translation lost information the
caller needed. A reviewer reads that; no scanner does.

## Licence note

EV-0175 is vendor documentation and EV-0174 is a published paper. Both
are read here for their principles. No prose from either is reproduced.
