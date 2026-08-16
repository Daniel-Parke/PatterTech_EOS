---
id: WG-DOCS-002
summary: How a code example in documentation stops lying, and what to do with the ones that cannot run
kind: wargame
type: wargame
tags: [ci, content, delivery, eos, testing, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-DOCS-003]
applies_when: [publishes_docs]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0189, EV-0326, EV-0330, EV-0331, EV-0332]
review: on-change-of:rustdoc-doctest-semantics
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-DOCS-002: How does a code example stop lying?

## Decision question and stakes

Documentation contains a command, a snippet or a call. The underlying
thing changes. Nothing in the repository knows the two are connected.
The fork is what mechanism, if any, ties the example to the code, and
what happens to the examples that mechanism cannot cover.

## Doctrines or coverage gap under pressure

- `DOC-DOCS-003` (default): Every executable snippet either runs in CI or carries an explicit declaration of why it does not.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Will a reader paste this and run it?
- Can the example run without a network, a credential or a live
  service?
- Does the toolchain already have first-class support for executing
  examples?
- How expensive is a false failure in this repository, given who is on
  call for the documentation build?

Applicability is `publishes_docs`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Toolchain doctests

The language runs every fenced example in a doc comment as part of the
test suite (EV-0330). Buys: no separate harness, examples live next to
the thing they document, and the escape hatches are already designed.
Costs: only available where the toolchain has it, and it covers doc
comments rather than standalone Markdown pages.

### B. A documentation gate that executes fenced blocks

CI walks the documentation tree, extracts fenced blocks of the
languages you nominate, and runs each one in a clean working directory,
failing the step on any non-zero exit. Buys: works for standalone
Markdown, works in any language, and catches the renamed flag in a
quickstart, which doctests never see. Costs: you write and maintain the
extractor, and you need a sandbox that makes execution safe and
repeatable.

### C. Declared skip markers, checked

Every fenced block either runs or carries a marker saying why it does
not: illustrative, needs credentials, expected to fail, environment
specific. A checker fails on any block with neither (EV-0330). Buys:
the absence of a declaration becomes the finding, so nothing silently
opts out. Costs: a convention to teach, and markers rot into a blanket
exemption if nobody audits how many blocks carry one.

### D. Review discipline only

A human is expected to notice. Buys: nothing to build. Costs: it is the
status quo that produced the problem, and it fails exactly when the
change is small and the reviewer is the author.

## Failure premises

### Premortem for A. Toolchain doctests

Assume `A. Toolchain doctests` was selected and the outcome failed. Test this option's stated failure mechanism first: only available where the toolchain has it, and it covers doc comments rather than standalone Markdown pages.

### Premortem for B. A documentation gate that executes fenced blocks

Assume `B. A documentation gate that executes fenced blocks` was selected and the outcome failed. Test this option's stated failure mechanism first: you write and maintain the extractor, and you need a sandbox that makes execution safe and repeatable.

### Premortem for C. Declared skip markers, checked

Assume `C. Declared skip markers, checked` was selected and the outcome failed. Test this option's stated failure mechanism first: a convention to teach, and markers rot into a blanket exemption if nobody audits how many blocks carry one.

### Premortem for D. Review discipline only

Assume `D. Review discipline only` was selected and the outcome failed. Test this option's stated failure mechanism first: it is the status quo that produced the problem, and it fails exactly when the change is small and the reviewer is the author.

## Decision rule

- The toolchain has doctests and the examples live in doc comments:
  **A**, and stop there for those examples.
- Documentation is standalone Markdown naming commands a reader will
  run: **B**, always, plus **C** for the blocks B cannot execute.
- The example calls a live service or needs a credential: **C** with the
  reason named, and cover the same path with a contract or conformance
  test elsewhere (EV-0189) rather than pretending the snippet is
  covered.
- **D** alone is never sufficient where `documents_executable_surface`
  is true.

## Safe default

B plus C. Execute what can be executed, and force everything else to
declare itself. B and C together are what turn B3 from an aspiration
into a gate: a block calling a flag that no longer exists fails the
build on the run that introduces it. B3 is a default rather than a
binding requirement, so a repository may decline the gate, and then it
writes down which blocks it has stopped checking.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Will a reader paste this and run it?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** B plus C. Execute what can be executed, and force everything else to declare itself. B and C together are what turn B3 from an aspiration into a gate: a block calling a flag that no longer exists fails the build on the run that introduces it. B3 is a default rather than a binding requirement, so a repository may decline the gate, and then it writes down which blocks it has stopped checking.

**Exit condition:** Stop or roll back the selected branch when only available where the toolchain has it, and it covers doc comments rather than standalone Markdown pages, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Will a reader paste this and run it?

## Counter-evidence and transfer limits

### Evidence boundary

EV-0330 is a working toolchain that has run this way for years, which
is existence proof and not comparative evidence. Nothing in this set
measures how many documentation defects an execution gate catches, or
what it costs to run. EV-0332 shows one organisation choosing a similar
split with a large CI budget and a dedicated writing function, so the
cheap parts transfer and the expensive parts do not.
### Preserved reasoning: Making the gate honest

Three properties decide whether this survives contact with a real
repository.

**It must run offline.** A gate that needs the network is a gate that
fails for reasons unrelated to the documentation, and that is how gates
get switched off (EV-0331). Examples that need a service go to C.

**The drift test is the real test.** The check has value only if
introducing a wrong example makes it fail. Prove that once, by adding a
block that calls the tool with a flag that does not exist and watching
the step go red. If it does not, the gate is decoration.

**A skip marker is a cost, not a free pass.** Count them. A repository
where most blocks carry a marker has a checker and no coverage, and
coverage is what practitioners actually rate as damaging when it is
missing (EV-0326).
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
