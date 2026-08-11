---
summary: Contract shapes, config skeletons and known blind spots for import-linter, dependency-cruiser and ArchUnit, plus how each is wired into a build
kind: fact
scope: estate
sources: [EV-0146, EV-0147, EV-0148, EV-0159]
volatility: fast
review: 2026-11
type: example
tags: [arch, tooling, ci]
---

# Boundary tooling reference

Level 3 material for B1 and D3 of `packs/architecture/PACK.md`. Read
this when writing or reviewing a contract file, not before.

## The three contract shapes

Every tool here expresses the same three ideas under different names
(EV-0147 is where they are cleanest):

- **layers**: an ordered stack; a higher layer may import a lower one,
  never the reverse.
- **forbidden**: this package must never reach that one. Directional.
- **independence**: these siblings must not know each other at all.

Most real rules are a layers contract plus one or two forbidden
contracts for the crossings that matter most.

## Python: import-linter (EV-0147, BSD-2-Clause)

Config lives in `.importlinter`, `setup.cfg` or `pyproject.toml`. The
command is `lint-imports`, exit 0 clean, non-zero on any violation.

The skeleton below is written against this tree, and every module it
names exists in it:

```
billing/       __init__.py, price_lookup.py
catalogue/     __init__.py, api.py            # api is the public interface
catalogue/internal/  __init__.py, repository.py, pricing.py
shared/        __init__.py, money.py
```

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

Layers are listed highest first. A forbidden contract naming a
submodule is how a public interface is enforced: the package exposes
one module, and everything else is off limits to outsiders.

**Name only modules that exist.** This skeleton used to forbid
`catalogue.repository` alongside `catalogue.internal`, and no such
module was ever in the tree; the private repository sits at
`catalogue.internal.repository`. A pack acceptance drill found it. A
contract naming a module outside the graph protects nothing, and what
you see depends on the version: some raise an invalid-contract error
and some report the contract kept, which reads as a green check. The
second is worse, and it is the usual shape of this failure after a
rename rather than a typo.

That is the argument for step 4 of
`packs/architecture/exemplars/EX-ARCH-001-billing-catalogue-boundary.md`:
add the forbidden import on purpose and watch the run go red before you
trust it. B1 binds the check, not the file, for exactly this reason.

**Blind spots, stated by the project.** Static imports only. Runtime
imports, plugin registries, dependency-injection containers and
string-based dynamic loading are invisible. The contract file must be
kept in step with package renames by hand.

## TypeScript and JavaScript: dependency-cruiser (EV-0148, MIT)

Config lives in `.dependency-cruiser.json` or its JS equivalent. The
same rule engine emits the dependency graph as dot, mermaid, json or
html, so the enforced architecture and the drawn architecture come
from one source.

```json
{
  "forbidden": [
    { "name": "no-circular", "severity": "error",
      "from": {}, "to": { "circular": true } },
    { "name": "catalogue-independent", "severity": "error",
      "from": { "path": "^src/catalogue" },
      "to":   { "path": "^src/billing" } },
    { "name": "no-reaching-inside", "severity": "error",
      "from": { "path": "^src/billing" },
      "to":   { "path": "^src/catalogue/(?!index)" } }
  ]
}
```

Rule classes worth having by default: no cycles, no orphans, no
production code importing dev or optional dependencies, and no
reaching into another module's internals.

**Blind spots.** Module graphs only. It detects structural violations
and says nothing about whether the decomposition is sound. Large
monorepos need explicit include and exclude tuning or run time becomes
the problem.

## JVM: ArchUnit (EV-0146, Apache-2.0)

Rules are ordinary unit tests over compiled bytecode, so they fail the
normal build with no new CI surface. Layered architecture, slice
independence and cycle bans are all first-class.

**Blind spots.** Bytecode only. Dynamic dispatch through reflection,
string-keyed service locators and configuration-driven wiring are
invisible, so a rule can pass while a runtime boundary is crossed.

## Wiring it into the build

A contract file nothing runs is the drill's first named failure
condition. Wire it in both places if you can, and at least one:

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
# CI workflow step
- name: Import boundaries
  run: lint-imports
```

The CI step and the hook must call the same command, so a green local
run means the same thing as a green pipeline.

## The dynamic gap

All three tools state the same limitation. Shopify's answer
(EV-0159) was call graphs captured from CI runs, scored per component,
which catches what static analysis cannot. That tool is in-house and
not public, and a score that tolerates violations is a migration
tactic for legacy mass rather than a rule for new code. Until
something better exists, the honest position is that static checking
is the cheap default and dynamic wiring is a known gap to be watched
by hand.

## Verifying the check actually checks

Any contract file should be proved once, not trusted:

1. Run the command on a clean tree. Expect exit 0.
2. Add the forbidden import to a source file in the source package.
3. Run again. Expect a non-zero exit naming the contract.
4. Revert. Expect exit 0.

That four-step proof is what separates an enforced boundary from a
documented one, and it is the shape of criterion 4 in
`benchmark/drills/architecture.md`.
