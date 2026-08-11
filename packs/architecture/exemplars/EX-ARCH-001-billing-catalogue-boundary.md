---
summary: The pack applied end to end to a two-module Python repo where billing may read the catalogue and the catalogue must never know about billing
kind: exemplar
scope: estate
type: example
tags: [arch, tooling, ci]
---

# EX-ARCH-001: billing reads the catalogue, never the reverse

The situation. An empty Python repository with two modules, billing
and catalogue, plus a shared package. One instruction: stand up the
architecture record and boundary enforcement, billing may read the
catalogue, the catalogue must never know about billing, then add a
price lookup in billing that uses the catalogue.

This is the drill in `benchmark/drills/architecture.md`. What follows
is the pack applied in order, with the reasoning shown.

## Step 1: read the fork before reaching for a tool

Two modules, one owner, boundaries not yet proved stable under change.
GD-ARCH-001 rules option B, module-shaped: one deployable, one store,
boundaries enforced in the build. No DORA-shaped signal exists here,
so nothing justifies a second deployable or a second database. That
ruling is worth stating out loud, because proposing separate services
is one of the drill's named failure conditions.

WG-ARCH-001 then rules how the boundary is held. One consumer of a
shared layer and an agent writing the code means at least option B, a
machine contract, from the first week. No behaviour canary exists yet,
so option C, the tree as architecture, waits.

## Step 2: declare the public interface before the contract

A forbidden contract that names a private submodule only works if
there is a public one to prefer. The catalogue exposes one module and
keeps the rest to itself.

```
catalogue/
  __init__.py
  api.py          # the public interface: get_product, list_products
  internal/
    __init__.py
    repository.py # storage detail, off limits to outsiders
    pricing.py    # calculation detail, off limits to outsiders
billing/
  __init__.py
  price_lookup.py
shared/
  __init__.py
  money.py
```

Deciding this first is what makes criterion 10 of the drill passable.
An agent that writes the contract first tends to forbid nothing but
the obvious direction and leaves the internals open.

## Step 3: write the contract

Three contracts, in `.importlinter`, following
`packs/architecture/refs/boundary-tooling.md`:

```ini
[importlinter]
root_packages =
    billing
    catalogue
    shared

[importlinter:contract:catalogue-independent]
name = The catalogue must never know about billing
type = forbidden
source_modules =
    catalogue
forbidden_modules =
    billing

[importlinter:contract:public-interface-only]
name = Billing reaches the catalogue only through its public interface
type = forbidden
source_modules =
    billing
forbidden_modules =
    catalogue.internal

[importlinter:contract:layering]
name = Layering
type = layers
layers =
    billing
    catalogue
    shared
```

The first contract is the instruction, stated in the direction it was
given. The second is the one nobody asks for and everybody needs. The
third stops shared reaching upward.

## Step 4: prove the check actually checks

Run `lint-imports`. Expect exit 0. Then add `import billing` to a
catalogue module, run again, and expect a non-zero exit naming the
catalogue-independent contract. Revert, run again, expect exit 0.

Four commands. Without them the contract file is a claim, and B1 of
`packs/architecture/PACK.md` binds the check, not the file.

## Step 5: wire it into the build

A contract nothing runs is the first failure condition in the drill.
Both places, calling the identical command:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: lint-imports
        name: import boundaries
        entry: lint-imports
        language: system
        pass_filenames: false
```

```yaml
# CI workflow
jobs:
  boundaries:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install import-linter
      - run: lint-imports
```

## Step 6: record the decision

A door is being closed: the direction of the dependency, and the tool
that holds it. That is D11 territory. The record lands in
`docs/decisions/` using the MADR headings from
`packs/architecture/refs/architecture-description.md`, and it must
carry three things the drill checks and one it does not:

- `## Considered Options` with three real options: convention and
  review, import-linter contracts in CI, and the directory tree with
  the contract on top.
- `## Decision Outcome` naming the chosen option and why the other two
  lost. Convention loses because an agent crosses it without noticing.
  The tree loses for now because no canary exists to prove the move
  neutral, and it is named as the next step rather than discarded.
- The tool named in the text, and the direction stated in words:
  billing may import the catalogue's public interface, the catalogue
  may import neither billing nor its own future consumers.
- The anti-pattern guarded against, which is a shared package growing
  into a bidirectional dependency.

A single-option record here would pass a file check and fail the
point.

## Step 7: draw what is now true

D4 asks for a container view. Structurizr DSL, one model, both modules
named, regenerated rather than hand-edited. Where a Structurizr
toolchain is more machinery than the repository earns, a Markdown file
carrying a `Container diagram` or `Building Block View` heading and
naming both modules discharges the same obligation, and a checker can
find it.

## Step 8: write the feature the instruction actually asked for

The price lookup lives in billing and imports the catalogue's api
module only. Never the internal repository, never the internal pricing
module. The second contract now earns itself: an agent reaching for
the repository to save a hop gets a red build with the contract name
in the failure message, which is the cheapest possible explanation of
why the boundary exists.

## What this example is not

It does not prove the boundary holds at runtime. Everything above is
static import analysis, which cannot see reflection, dependency
injection or string-keyed lookup. In a repository this size that gap
is acceptable and worth knowing about, and the pack says so in its
open questions rather than pretending otherwise.
