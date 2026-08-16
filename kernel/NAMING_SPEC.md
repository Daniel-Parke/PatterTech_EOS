---
summary: The current terminology, identifiers, pack presentation and file naming contract
type: kernel
tags: [eos]
---

# NAMING_SPEC

The current EOS uses one name for each knowledge class and one canonical
location for each collection. Names should tell a reader what something is
without turning presentation labels into machine identity.

## Knowledge language

Capitalise these terms when they name an EOS class:

- **Doctrine** is one atomic standing proposition. Its authority is binding,
  default, advisory or preference.
- **Wargame** is one recurring decision procedure used when Doctrine is under
  pressure, alternatives need selection, an exception is proposed or coverage
  is missing.
- **Wargaming** is the act of applying a Wargame.
- **Relation** is one typed conditional edge involving Doctrine.
- **Ruling** is one venture's execution of one Wargame.

Lowercase `guide` remains available for a genuine document description, such
as the operator guide or a style guide. It is not a synonym for Wargame.
`example` is the current term for a worked application. `reference` is the
current term for supporting material.

## Identifier schemes

| Form | Meaning and scope |
| --- | --- |
| `DOC-<NAMESPACE>-NNN` | Estate-wide Doctrine identity |
| `DREL-<NAMESPACE>-NNN` | Estate-wide Relation identity; new records use the owning Doctrine's namespace |
| `WG-<NAMESPACE>-NNN` | Estate-wide Wargame identity |
| `RUL-<NAMESPACE>-NNN` | Ruling identity, unique within one venture's `docs/RULINGS.json` |
| `EX-<NAMESPACE>-NNN` | Worked example identity |
| `ADR-NNNN` | Decision record |
| `EV-NNNN` | Evidence-ledger row |
| `LES-NNNN` | Lesson-ledger row |
| `LENS-NNNN` | Research lens contract |
| `T-NNNN` | Task record |
| `PB-E<NN>` | EOS playbook |
| `STACK-<slug>` | Dated stack profile |

Identifiers are immutable and never reused. New pack-owned identifiers use
the `id_namespace` declared by that pack. Historical Relation namespaces stay
unchanged when a Relation now sits in another pack.

Every live Wargame uses `WG-*`. Former decision-procedure identities are
direct aliases in `registry/identifier-aliases.json`; they are not live
definitions and no new one is issued. The generated reader view is
`registry/IDENTIFIER_ALIASES.md`.

The resolver canonicalises an alias before comparison, selection, omission,
always-walk enforcement and Ruling validation. With `--commit`, it resolves
the identity and path from that Git tree rather than falling forward to the
current worktree. Retired identities remain reserved and cannot be selected
as live Rulings.

Aliases preserve identity, not branch-relative paths. Old Git commits retain
old paths. The current tree carries no redirect files for retired collection
names, so an external URL that assumes the latest branch and an old path must
be updated.

## Pack names

A pack has three independent names:

- its lowercase kebab-case directory, a stable machine key;
- `display_name`, a concise reader-facing domain name;
- `id_namespace`, the short uppercase token used in new pack-owned IDs.

`display_name` does not add `Pack`, `EOS` or a category prefix. Directory names
do not change merely to improve presentation. Pack namespaces and display
names are unique.

`category` is one of six navigation keys:

| Key | Reader label |
| --- | --- |
| `data-ai` | Data and AI |
| `engineering` | Engineering |
| `experience-content` | Experience and Content |
| `practice-governance` | Practice and Governance |
| `product-commercial` | Product and Commercial |
| `reliability-trust` | Reliability and Trust |

Categories group `packs/INDEX.md`. They do not affect pack identity,
activation or dependency order. Each `PACK.md` heading exactly matches its
`display_name`.

## Collections and files

The canonical pack collections are `doctrines/`, `wargames/`, `examples/`,
`references/` and `research/`, plus `relations/` when needed. Their contracts
are in `packs/PACK_CONTRACT.md`.

Entity filenames start with the canonical identity and use a descriptive
lowercase kebab-case slug. A Doctrine basename is at most 72 characters and
ends at a whole-word boundary. Moving or shortening a file does not change its
identity or proposition.

Repository entry points, contracts and generated catalogues use short
uppercase filenames such as `README.md`, `PACK.md`, `CHECKS.md`,
`PACK_CONTRACT.md` and `WARGAME_INDEX.md`. Metadata keys use `snake_case`.
Current prose and code cite canonical paths; compatibility aliases appear only
where resolution or migration is the subject.

## Metadata names

The outer record shape describes the artefact, not its authority:

- `PACK.md`: `kind: record`, `type: pack`;
- `CHECKS.md`: `kind: record`, `type: checks`;
- Doctrine: `kind: doctrine`, `type: doctrine`;
- Wargame: `kind: wargame`, `type: wargame`;
- worked example: `kind: example`, `type: example`.

`kernel/METADATA_SPEC.md` defines the remaining axes and their enforcement.

## Historical executable snapshot

`tests/test_ontology_oracle.py` is the byte-preserved T-0026 executable
snapshot. The current suite excludes it because it asserts the superseded
identity and collection contract. Run it only in a worktree at its recorded
historical commit. `tests/test_naming_oracle.py` is the active naming oracle.
