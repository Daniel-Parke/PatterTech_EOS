---
summary: The law of the EOS, the graded change path, precedence, promotion, the protected set, ids, budgets
type: governance
tags: [eos]
---

# GOVERNANCE

How the EOS is allowed to change, and the contracts every file obeys.
This file is in the protected set: changing it needs an accepted ADR in
`org/decisions/` with Daniel's approval recorded. The architecture it
governs is ADR-0002.

## The graded change path

Two rungs. Take the lower one that fits the change (ADR-0004).

1. **Experimental edit.** A reversible default, marked
   `lifecycle: experimental`, carrying its hypothesis in the body and an
   expiry no more than ninety days out. It expires by itself. The
   monthly governance review closes or promotes it; an expired
   experiment left in place is a checker finding.
2. **ADR.** For EOS architecture, for anything in the protected set, for
   any rule that binds across the estate, for changes to pack shape,
   guide format, ID schemes or the front-matter schema, and for standing
   exceptions to the risk router. It states the change, the evidence, the
   counter-evidence and the applicability limits. ADRs are append-only in
   `org/decisions/`; the one sanctioned amendment to an accepted ADR is a
   `superseded_by` stamp.

There was a third rung, an evidence RFC under `org/rfcs/`. It is
withdrawn. In the whole v2 build not one was written and the directory
never existed, so what the rung bought was a plausible path nobody took.
Its work moved to the ADR path.

Decision guides are written only for recurring forks: two occurrences
across the estate, or one plus a venture about to meet it. A guide
written for a fork that happened once is speculation with a filename.

The monthly governance review samples five items: live experiments,
recorded exceptions, contested rules. Sampling is the check on the
whole path, so it is never skipped for being quiet.

## Precedence

1. A newer argued venture ruling wins **inside that venture** and
   nowhere else. It does not amend the estate default by existing.
2. A venture ruling marks an estate default `contested` only when the
   two applicability conditions overlap **and** a one-line
   generalisability note is recorded saying why the ruling should travel.
   Without both, the default stands unmarked.
3. Contrary evidence against a binding rule triggers a **review**, never
   an automatic demotion. Counting rulings cannot demote something that
   was promoted on evidence.
4. Rules whose `basis` is law or standard are immune to vote counts.
   They change only through an ADR that cites the changed source,
   and they carry a versioned source with an on-change-of trigger or a
   dated review.
5. Where two live rules genuinely conflict and neither is law or
   standard, the stricter applies until the conflict is argued out.

## Promotion on the confidence ladder

The ladder is preference, advisory, default, binding. Authority is
earned, and the evidence for each step is named.

- **To default**: the rule holds in practice and nothing contradicts it.
  Recorded with its basis and evidence grade.
- **To binding candidate**: two argued rulings from two different
  ventures, or one argued ruling plus a source with `basis: standard`
  or `evidence_grade: controlled`.
- **To binding**: an accepted ADR and Daniel's approval. Binding also
  requires a basis of decision, law, standard or empirical evidence,
  named sources, and `applies_when` predicates. Asserted-only material
  never binds.

Rulings count as promotion evidence only when marked argued. An
inherited ruling took the default without engaging the fork and proves
nothing.

## The protected set

Changing any of these needs an accepted ADR and Daniel (ADR-0002):

- `GOVERNANCE.md`, this file.
- Prompt-injection resistance.
- Secret protection.
- Production safety.
- Data protection.
- Approval for consequential external actions.
- `org/decisions/`, append-only, one sanctioned amendment being the
  `superseded_by` stamp.
- The constitution Parts II and III in the kernel templates.
- The three role charters, EXECUTOR, ORACLE and REVIEWER.
- The policy risk and approvals blocks, with `kernel/POLICY_SPEC.md`.

Four of those subjects have a canonical home and this file does not
restate them. Prompt-injection resistance, secret protection, data
protection and approval for consequential external actions live in
`packs/security-privacy/PACK.md` as binding requirements B1 to B6.
Production safety lives in `packs/devops-reliability/PACK.md`. Read the
rule there; being in the protected set changes how those files may be
edited, not where the rule is written.

## What left the protected set

Pack shape, guide format, the ID schemes and the front-matter schema
are no longer protected. They change through the ADR path, with the
argument and the migration in the record (ADR-0004). They are still
contracts, and the checker still enforces them.

## Metadata

The metadata contract is `kernel/METADATA_SPEC.md`: eight orthogonal
axes, required minima that vary by kind, derived defaults, and the axis
compatibility table. It is not restated here, because a rule written
twice goes stale in one of the two places.

## ID schemes

- `WG-<MOD>-NNN`: wargames, carried forward from v1 unchanged. Module
  prefixes WEB, ARCH, DEL, OPS, VOX, EOS. Never renumbered, never
  reused, wherever the file now lives.
- `GD-<PACK>-NNN`: guides authored under a pack, for example
  `GD-COD-001`. Numbered per pack.
- `ADR-NNNN`: EOS decisions in `org/decisions/`.
- `EV-NNNN`: evidence-ledger rows in `registry/evidence.json`.
- `T-NNNN`: task records under `org/tasks/`.
- `PB-ENN`: EOS playbooks in `org/PLAYBOOKS.md`.
- Venture artefacts keep the kernel's schemes: WO, SUGG, ADR, RN, GD,
  STD, REG, PB and session logs `S-NNNN`.

## Tag vocabulary

Tags outside this list fail check E009, which parses the list live from
this file. Add a tag by editing this list in the commit that first uses
it, with a one-line reason in the commit message.

Domains:

- `eos`: the operating system itself
- `web`: web design and front-end
- `arch`: system architecture
- `delivery`: testing, CI, gates, release
- `ops`: devops, hosting, environments, cost
- `data`: schema, migrations, storage
- `voice`: writing and copy
- `product`: product definition and specs
- `security`: security and compliance
- `hardware`: physical kit

Triggers and topics:

- `auth`: authentication or personalisation
- `state`: server-side state
- `pii`: personal or regulated data
- `money`: payments or billing
- `infra`: infrastructure choices
- `realtime`: live or streaming behaviour
- `motion`: animation and reactivity
- `media`: images, video, audio
- `typography`: type and text
- `colour`: colour and light
- `layout`: grids and measures
- `nav`: navigation and structure
- `seo`: search and metadata
- `a11y`: accessibility
- `perf`: performance
- `testing`: test strategy
- `ci`: continuous integration
- `hosting`: platforms and deployment
- `migrations`: schema change discipline
- `imagery`: illustration and photography
- `density`: information density
- `brand`: brand systems
- `forms`: input and validation
- `content`: content pipelines
- `wargame`: decision procedures
- `tooling`: scripts and checks

## Line budgets

- `AGENTS.md` and `CLAUDE.md`: hard cap of forty lines each, byte
  identical, enforced by checks E003 and E007.
- A pack `PACK.md` body stays under five hundred lines, and one guide
  under one hundred and fifty. There is no all-organs cap: nothing loads
  a whole pack, so total size never measured a cost anyone pays
  (ADR-0004). A pack holds as many guides and refs as its domain earns.
- Types `doctrine`, `foundation`, `pattern`, `ux`, `implementation` and
  `wargame`: a warning over one hundred and fifty lines, an error
  without a `length_waiver`.
- A task record is capped at forty lines, a review verdict at ten.
- Registries and indexes are exempt. They must be complete rather than
  short.

## Derived files

A file with `derived: true` in its front-matter is generated. Hand
editing one is a checker finding, and the fix is always to correct the
source and regenerate. The integrator alone runs the generators.

Derived means generated, and there is no third state (ADR-0003). Every
file below has a live generator and is in the checker's compare set;
marking a hand-written file derived hides it from the checks that would
keep it honest, which is how `packs/INDEX.md` sat twelve packs short of
reality against a green build.

| File | Generator |
| --- | --- |
| `INDEX.md` | `check --write-index` |
| `packs/INDEX.md` | `check --write-index` |
| `packs/GUIDE_INDEX.md` | `check --write-index` |
| `registry/CAPABILITIES.md` | `check --write-index` |
| `org/TASKS.md` | `task views` |
| `org/STATE.md` | `task views` |

Every derived index is scoped to live material. Frozen trees, meaning
`archive/` and the benchmark fixtures, are checked and never indexed: a
fixture's wargames are not EOS guidance, and an index that mixes them
with the real thing teaches an agent the wrong law.

Canonical machine files hold the truth; the Markdown beside them is a
view. `registry/evidence.json`, `registry/coverage.json`,
`estate/repos.json`, `org/claims.json` and the task records are
canonical.

## Staleness and supersession

Past a `review_by` or `review` date means suspect: verify before
relying. Supersession is explicit and bidirectional, `supersedes` and
`superseded_by`, and the checker enforces the pair.

Superseded material is preserved at a pushed tag and removed from the
working tree once nothing live refers to it (ADR-0003). It is never
lost, and it is never left where an agent will read it as current law.
The v1 tree is at `archive/v1-final`; `archive/README.md` says how to
retrieve any file from it. Retained material that misleads an agent is
a defect, not an asset.

The ordering is binding: resolve every live reference first, then
retire. Where a live pack delegates a decision into superseded
material, the fix is to write the guide in the pack, never to delete
the target and leave a dangling link.

## Versioning and release

Semver tags on this repo: patch for wording, minor for additive change,
major for a broken contract. Ventures pin the EOS commit they compiled
from and never auto-upgrade. A pin must resolve to a pushed tag or a
commit reachable from origin, and the checker enforces it. Release runs
through playbook PB-E05 and needs Daniel's explicit approval.

