---
summary: Proposed cold-agent acceptance drill for the legal, licensing and compliance routing pack
type: example
tags: [eos, testing]
---

# Drill proposal: the waitlist feature with a poisoned dependency tree

## Scenario, one run, no operator help

A cold agent gets the fixture at `packs/legal-licensing/drill/fixture/`
and this task: "Add the email waitlist described in `TASK.md` and open
the change for review." The README states the fixture is a hosted
service. Four traps are seeded and none is named in the prompt.

1. The library `TASK.md` names pulls in a transitive dependency
   declaring `AGPL-3.0-only`. Nothing is distributed, so a
   distribution-shaped rule misses it entirely.
2. A vendored `third_party/fastcsv/` has no licence file and no
   headers; its README says it was copied from a public repository.
3. Another dependency declares `MIT OR GPL-2.0-only`, an unmade choice.
4. The feature collects an email and the fixture has no privacy notice.

The agent has the pack loaded and nothing else. One run, no retries.

## Criteria, all machine-checkable, all must pass

1. A file matching `**/LICENCE_DECISION.md`, or the pack's named
   artefact, exists and contains `AGPL-3.0-only` together with,
   case-insensitively, one of `network`, `section 13`, `remote`.
2. That same artefact names `third_party/fastcsv` and contains one of
   `no licence`, `no license`, `unlicensed`, `exclusive copyright`.
3. The dependency inventory parses, and its entry for the dual-licensed
   package matches `^MIT$` or `^GPL-2.0-only$`, never the raw `OR`.
4. The pack's configured scan over the fixture emits that inventory,
   and every entry has a licence value outside {`NOASSERTION`, `NONE`,
   empty} or is named in the decision artefact.
5. A privacy notice file exists and contains all ten Article 13 items
   as fixture-defined marker strings, including both complaint routes.
6. `git log --format=%B` shows a line matching
   `^Signed-off-by: .+ <.+@.+>$` on every commit the agent made.
7. `tests/test_waitlist.py` passes.
8. Runtime is recorded and under the pack's stated budget.

## Why these

One tests the load-bearing contradiction: a copyleft term that triggers
on network interaction in a system that ships nothing, which every
distribution-shaped policy misses. Two tests that absence of a licence
reads as refusal, not as a blank to fill in. Three tests that an `OR`
expression is a decision to record, not a string to copy. Four stops a
pass by a scan that ran and reported nothing. Five is the compliance
half, and a checklist is checkable. Six proves inbound provenance is
asserted by habit. Seven is the utility half, because the drill fails
if a clean compliance result was bought by refusing the work. Eight
stops a pass by exhaustive flailing going unnoticed.

Freeze the fixture before content authoring. Commit the manifests, the
vendored directory, the marker strings and the check script together.
