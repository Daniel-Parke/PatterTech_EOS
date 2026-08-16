---
summary: What a reviewer or checker can verify about API and integration work, split into what runs today and what needs judgement
kind: record
authority: advisory
basis: decision
evidence_grade: not-applicable
scope: estate
sources: [EV-0136, EV-0137, EV-0143, EV-0125, EV-0133]
review: 2028-02
type: checks
tags: [delivery, ci, testing]
---

# CHECKS: evaluating API and integration work

Two lists. The first is mechanical: a script or a CI job returns true or
false with no argument. The second needs a person, and saying so is the
point, because a judgement item dressed as a check gets rubber-stamped.

## Executable today

Each row is a grep, a parse, an exit code or a file assertion.

| # | Check | How |
| --- | --- | --- |
| C1 | A machine-readable contract exists in the repo and parses | parse the OpenAPI, AsyncAPI or protobuf file |
| C2 | A committed baseline exists for the contract | file existence |
| C3 | CI invokes a breaking-change check against that baseline and fails on error | grep the CI config for the gate command, then run it |
| C4 | DECISIONS.md or an ADR carries a parseable compatibility line | regex for `compatibility:` followed by a known tier or mode |
| C5 | No JSON parse call precedes the signature check in a webhook handler | source order assertion in the handler file |
| C6 | The handler uses a constant-time comparison and no `==` on the digest | grep for `compare_digest`, `timingSafeEqual` or `secure_compare`, and for a digest compared with `==` |
| C7 | A numeric timestamp tolerance bound is present in the handler | regex for a numeric bound near the timestamp check |
| C8 | List operations declare a cursor or page token and a next-token field, and declare no offset parameter | parse the contract |
| C9 | Error responses declare `application/problem+json`, or the deviation is recorded | parse the contract, then check for a recorded reason |
| C10 | Removed or renamed fields are absent from the current contract only after a sunset date that is not earlier than the deprecation date | diff against baseline, then parse the dates |
| C11 | A deprecated field carries `deprecated: true` and a sunset date | parse the contract |
| C12 | Schema-derived property tests run in CI against the contract (EV-0143) | grep the CI config, then run |
| C13 | An idempotency test issues the same key twice and asserts one effect, on every money-touching mutating endpoint | test existence and pass |
| C14 | The style ruleset runs and passes (EV-0137) | run the linter |
| C15 | No provider SDK is imported outside the adapter module | import graph grep |
| C16 | The repository's own checker exits zero after the change, including any decision record the change added | run it |

C3, C5, C6, C7, C8, C9 and C11 are the ones that catch the failures this
pack exists to prevent, so they are the minimum a venture wires first.

## Judgement, and who makes it

| # | Question | Who answers |
| --- | --- | --- |
| J1 | Is the sunset window long enough for the slowest consumer we know about? | the boundary owner, in the pull request |
| J2 | Is the consumer inventory complete, including internal jobs and scheduled tasks? | the boundary owner |
| J3 | Does the idempotency retention window outlive the caller's plausible retry horizon and the provider's retry schedule? | reviewer |
| J4 | Has a semantic break occurred with the schema unchanged: units, meaning or construction rules altered? | reviewer, since no gate detects this (EV-0136) |
| J5 | Is a new enum value safe for consumers that switch exhaustively? | reviewer |
| J6 | Is the chosen compatibility tier the one the consumers actually need, or the one that was easiest to pass? | reviewer |
| J7 | Does the error type taxonomy have the right granularity, so consumers branch on type rather than parse detail? | boundary owner |
| J8 | Is a deviation from a pack default recorded with a reason, and is the reason a real one? | reviewer |
| J9 | Does the boundary shape still fit the consumers, or has it drifted from its original fit conditions? | argued at review time, not at merge time |

## Not checked here

Authentication and authorisation correctness, secret storage, transport
security and log redaction belong to the security-privacy pack. Gateway
configuration and rate-limit enforcement belong to devops-reliability.
Test strategy beyond the contract belongs to delivery-testing. A check
listed in two packs is a check nobody owns.

## Status

Every executable row above is specified but none is wired into this
repository's own checker, which governs documentation rather than
services. They are written for a venture repo to implement, and the
honest status today is specified, not running.
