---
summary: Where do tokens live and how do they reach each platform?
kind: guide
authority: default
basis: standard
evidence_grade: observational
scope: estate
sources: [EV-0030, EV-0064, EV-0065, EV-0227, EV-0228, EV-0229]
review: on-change-of:DTCG-format-module
type: guide
tags: [tooling, brand, colour]
review_by: 2027-12
---

# GD-UIUX-004: Where do tokens live and how do they reach each platform?

## The question

Named values are what let two surfaces with different philosophies stay
one product underneath. The fork is which artefact is the single source
and how derivations reach CSS, native platforms, documentation and
design tools. PACK.md B6 already binds define-once-and-generate; this
guide decides where the once is.

## It depends on

- **How many platforms consume the values.** One web app has a much
  weaker case for a build step than web plus two native apps.
- **Who edits values.** Designers in a tool, or engineers in a repo.
- **Whether a vendor system is already in play**, since it arrives with
  its own token layer.
- **Rebrand frequency.** A multi-brand estate pays for aliasing early.
- **Review appetite.** A generated file in a pull request is noise
  unless the diff is readable.

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

## Decision rule

If one web surface and no near-term native plans, choose A. If
designers own the palette and the tool is already the working source of
truth, choose B on top of A. If a vendor system is already adopted for
components, choose C and do not run a second parallel source. If three
or more platforms consume the values, choose D. Never choose E.

## Default

A. It is the cheapest route that satisfies B6, it keeps the source
reviewable as text, and it upgrades into B or D without changing the
source shape.

## Worked rulings

- **ui-ux pack exemplar (2026-08, argued)**: one DTCG source, two
  generated platform outputs, regeneration asserted to produce no diff,
  and both surfaces consuming semantic names only. The two surfaces
  differ in spacing density and type scale by consuming different
  semantic sets over the same primitives. See
  `packs/ui-ux/exemplars/two-surfaces-one-spine.md`.
- **PatterTech Website (2026-07, inherited)**: one home for tokens with
  a mirroring contract across code, styleguide and documentation, and a
  test that fails the build on any re-typed raw value. Recorded in
  `archive/v1-final:doctrine/web-design/implementation/TOKENS.md` and carried into
  `packs/ui-ux/refs/TOKEN_PIPELINE.md`.
