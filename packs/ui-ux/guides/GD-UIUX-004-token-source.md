---
id: GD-UIUX-004
summary: Where do tokens live and how do they reach each platform?
kind: wargame
type: wargame
tags: [brand, colour, eos, tooling, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-UIUX-006]
applies_when: [has_user_interface]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0030, EV-0064, EV-0065, EV-0227, EV-0228, EV-0229]
review: on-change-of:DTCG-format-module
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-UIUX-004: Where do tokens live and how do they reach each platform?

## Decision question and stakes

Named values are what let two surfaces with different philosophies stay
one product underneath. The fork is which artefact is the single source
and how derivations reach CSS, native platforms, documentation and
design tools. PACK.md B6 already binds define-once-and-generate; this
guide decides where the once is.

## Doctrines or coverage gap under pressure

- `DOC-UIUX-006` (binding): Tokens are defined once and generated; derived files are never hand-edited.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- **How many platforms consume the values.** One web app has a much
  weaker case for a build step than web plus two native apps.
- **Who edits values.** Designers in a tool, or engineers in a repo.
- **Whether a vendor system is already in play**, since it arrives with
  its own token layer.
- **Rebrand frequency.** A multi-brand estate pays for aliasing early.
- **Review appetite.** A generated file in a pull request is noise
  unless the diff is readable.

Applicability is `has_user_interface`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Source file in the repo, generated per platform
One token file in the DTCG shape (EV-0030) with a build producing each
platform's output (EV-0065). Buys one reviewable source, aliasing,
per-platform transforms, and outputs that are reproducible from source.
Costs a build step and a habit of never touching the outputs.

### B. Design tool as source, exported into the repo source
The tool exports into the DTCG file, which then generates as in A.
Buys designer ownership of values and fewer transcription errors. Costs
a coupling to the tool's export shape, and a review surface that is
hard to read when the tool renames things.

### C. Vendor system tokens with one thin settings layer
Consume a system's tokens through functions and one settings layer, so
the structure stays invariant while the palette varies (EV-0064,
EV-0227). Buys a maintained scale and documentation for free. Costs
freedom: departures fight the system, and a rebrand is bounded by what
the settings layer exposes.

### D. Platform-native token systems bridged from one source
Values land in each platform's own mechanism, custom properties for the
cascade, asset catalogues and resource files for native, produced from
one source with a test pinning each pair (EV-0229). Buys native tooling
and native performance on every platform. Costs the most machinery, and
it only earns its keep across three or more platforms.

### E. No token layer, values written in components
Named here to be excluded. B6 in PACK.md forbids it wherever tokens
exist, because a value re-typed inside a component passes every import
rule and quietly makes a shared kit wear one brand's colour.

## Failure premises

### Premortem for A. Source file in the repo, generated per platform

Assume `A. Source file in the repo, generated per platform` was selected and the outcome failed. Test this option's stated failure mechanism first: a build step and a habit of never touching the outputs.

### Premortem for B. Design tool as source, exported into the repo source

Assume `B. Design tool as source, exported into the repo source` was selected and the outcome failed. Test this option's stated failure mechanism first: a coupling to the tool's export shape, and a review surface that is hard to read when the tool renames things.

### Premortem for C. Vendor system tokens with one thin settings layer

Assume `C. Vendor system tokens with one thin settings layer` was selected and the outcome failed. Test this option's stated failure mechanism first: freedom: departures fight the system, and a rebrand is bounded by what the settings layer exposes.

### Premortem for D. Platform-native token systems bridged from one source

Assume `D. Platform-native token systems bridged from one source` was selected and the outcome failed. Test this option's stated failure mechanism first: the most machinery, and it only earns its keep across three or more platforms.

### Premortem for E. No token layer, values written in components

Assume `E. No token layer, values written in components` was selected and the outcome failed. Test this option's stated failure mechanism first: Named here to be excluded. B6 in PACK.md forbids it wherever tokens exist, because a value re-typed inside a component passes every import rule and quietly makes a shared kit wear one brand's colour.

## Decision rule

If one web surface and no near-term native plans, choose A. If
designers own the palette and the tool is already the working source of
truth, choose B on top of A. If a vendor system is already adopted for
components, choose C and do not run a second parallel source. If three
or more platforms consume the values, choose D. Never choose E.

## Safe default

A. It is the cheapest route that satisfies B6, it keeps the source
reviewable as text, and it upgrades into B or D without changing the
source shape.

## Cheapest discriminating test

Settle this question with the smallest representative probe: ****How many platforms consume the values.** One web app has a much weaker case for a build step than web plus two native apps.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A. It is the cheapest route that satisfies B6, it keeps the source reviewable as text, and it upgrades into B or D without changing the source shape.

**Exit condition:** Stop or roll back the selected branch when a build step and a habit of never touching the outputs, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: **How many platforms consume the values.** One web app has a much weaker case for a build step than web plus two native apps.

## Counter-evidence and transfer limits

### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
