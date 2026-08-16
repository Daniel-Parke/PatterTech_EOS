---
summary: The law of the EOS, the graded change path, precedence, promotion, the protected set, claims and records, ids, budgets
type: governance
tags: [eos]
---

# GOVERNANCE

How the EOS is allowed to change, and the contracts every file obeys.
This file is in the protected set: changing it needs an accepted ADR in
`org/decisions/` with the operator's approval recorded. The architecture it
governs is ADR-0002.

ADR-0008 is the de-restriction pass, and its test governs everything
below. A rule binds only where it prevents a serious or hard-to-reverse
failure and rests on law, standard, empirical evidence or a
protected-set floor. Everything else is a default: do it unless you
record why not. Where a rule was loosened, the sentence names what
catches the failure instead, because loosening without a replacement
catcher is how sixty-six false statements got into this tree once.

## The graded change path

Two rungs. Take the lower one that fits the change (ADR-0004).

1. **Experimental edit.** A reversible default, marked
   `lifecycle: experimental`, carrying its hypothesis in the body and an
   expiry no more than ninety days out. It expires by itself. The
   experiment sweep, section three of the monthly pass, closes or
   promotes it. Where the expiry is written into the `review` axis the
   checker also warns past the date (E006, F001); where it is only in
   the body, the sweep is the only thing that catches it, which is a
   reason to put the date in the axis.
2. **ADR.** For EOS architecture, for anything in the protected set, for
   any Doctrine that binds across the estate, for changes to the pack
   contract, knowledge naming, ID schemes or the front-matter schema, and for
   standing exceptions to the risk router. It states the change, the evidence, the
   counter-evidence and the applicability limits. ADRs are append-only in
   `org/decisions/`; the one sanctioned amendment to an accepted ADR is a
   `superseded_by` stamp.

There was a third rung, an evidence RFC under `org/rfcs/`. It is
withdrawn. In the whole v2 build not one was written and the directory
never existed, so what the rung bought was a plausible path nobody took.
Its work moved to the ADR path.

Wargames are written only for recurring forks: two occurrences across
the estate, or one plus a venture about to meet it. A Wargame written
for a fork that happened once is speculation with a filename.

The monthly pass samples five items: live experiments, recorded
exceptions, contested rules. Sampling is the check on the whole path, so
it is never skipped for being quiet.

## The cadence

One standing pass. It runs monthly in a single sitting with four
sections, harvest, promotion review, experiment sweep and hygiene, in
that order. It holds one row in `org/cadence.json` and its procedure is
`org/PLAYBOOKS.md`. A section that found nothing says so in one line; a
section that was skipped is a finding and records why.

Everything else fires on an event. The inception drill and the projects
review used to hold quarterly rows and neither had fired once since v1
(ADR-0008), so both are event-triggered now and hold no cadence row at
all. *Caught instead by*: the events each procedure names, a seed
compiled or a repository added, which is a trigger somebody actually
meets. A calendar trigger nobody honours is not a control, and leaving
it on the calendar only teaches a reader that overdue rows are normal.

## Claims and records

Two controls that used to apply to every session now scale with the
work.

**Claims scale with concurrency.** A claim is required when more than
one session may write at once. When lanes run in parallel the integrator
commits the claim set in `org/claims.json` before dispatch, lanes are
assigned claims and never acquire or mutate one, and none of that
changes: it is the only thing that stops two writers landing on one file
and the second silently dropping the first. A single session working
alone is implicitly claimed and need not hand-write a claim file first.
*Caught instead by*: git history, which shows exactly who wrote what
when there is only one writer.

The claim set is read at two points, both in the `task` command family.
`task new` and `task update` refuse a session that is not named in the
committed set. `task claims-verify` compares a lane's diff against its
claims and reports C001 to C005. Ordinary writes are not gated, so the
control bites where a record is written and again at integration. A
lane's claim over its product paths also covers its own record under
`org/tasks/`; the record still names its owner session, and the
integrator still owns every derived view.

**Task records are required for gate-bearing work.** That means R2 and
above, any diff touching the protected set, and anything a reviewer must
later be able to find. Ordinary R0 and R1 work records itself in the
commit message, which is what Express already did. *Caught instead by*:
git is the log, ruled in ADR-0002, and the close step of the standard
path in `org/PLAYBOOKS.md`, which re-routes against the actual diff and
opens a record when the work turns out to rule R2 or above. ADR-0008
named a sampled review of commits as the second catcher, and PB-E09 in
`org/PLAYBOOKS.md` is where it runs: one commit in five, in commit
order, against three questions. The failure this leaves open is a change
whose reasoning nobody can reconstruct. If a monthly pass finds one,
ADR-0008 is the suspect, and the fix is to raise the bar for what counts
as gate-bearing rather than to reinstate records everywhere.

## Precedence

1. A newer argued venture Ruling wins **inside that venture** and
   nowhere else. It does not amend the estate default by existing.
2. A venture Ruling marks an estate default `contested` only when the
   two applicability conditions overlap **and** a one-line
   generalisability note is recorded saying why the Ruling should travel.
   Without both, the default stands unmarked.
3. Contrary evidence against binding Doctrine triggers a **review**, never
   an automatic demotion. Counting Rulings cannot demote something that
   was promoted on evidence.
4. Doctrine atoms whose `basis` is law or standard are immune to vote counts.
   They change only through an ADR that cites the changed source,
   and they carry a versioned source with an on-change-of trigger or a
   dated review.
5. Where two live Doctrine atoms genuinely conflict and neither is law or
   standard, the stricter applies until the conflict is argued out.

## Promotion on the confidence ladder

The ladder is preference, advisory, default, binding. Authority is
earned, and the evidence for each step is named.

- **To default**: the proposition holds in practice and nothing contradicts it.
  Recorded with its basis and evidence grade.
- **To binding candidate**: two argued Rulings from two different
  ventures, or one argued Ruling plus a source with `basis: standard`
  or `evidence_grade: controlled`.
- **To binding**: an accepted ADR and the operator's approval. Binding also
  requires a basis of law, standard or empirical evidence, or an explicit
  protected-set floor, together with named sources and `applies_when`
  predicates. Decision-only and asserted-only material never binds unless an
  accepted ADR explicitly carries the exception.

Rulings count as promotion evidence only when marked argued. An
inherited Ruling took the default without engaging the fork and proves
nothing.

## The protected set

Changing any of these needs an accepted ADR and the operator (ADR-0002):

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

The pack contract, knowledge naming, the ID schemes and the front-matter schema
are no longer protected. They change through the ADR path, with the
argument and the migration in the record (ADR-0004). They are still
contracts, and the checker still enforces them.

## What the de-restriction did not touch

Stated here so the loosening above cannot be read as general.

- The safety floors. Prompt-injection resistance, secret protection,
  production safety, data protection and approval for consequential
  external actions are untouched, and the action-time guard still fails
  closed: with no validated host adapter, a guarded class stays
  manual-only.
- The derived-file rule below. It prevents a failure that has actually
  happened in this repository, twice.
- `org/decisions/` stays append-only, with the `superseded_by` stamp as
  the one sanctioned amendment.
- Supersession stays explicit and bidirectional, and the checker still
  enforces the pair.
- The promotion ladder. Authority is still earned, binding still needs an
  accepted ADR and the operator, and an argued Ruling still counts for more
  than an inherited one.
- The decision budget in `org/policy.json`, and its escalation band in
  particular: money, legal, personal-data ambiguity, the protected set,
  spend beyond budget, weakening any check, and conflict with stated
  intent all stop and ask.

## Metadata

Required on every Markdown file that carries front-matter: `summary`, `type`
and `tags`. E002 enforces those three, plus the status and review fields
required by particular file types. The canonical knowledge shapes use
matching `kind` and `type` values for Doctrine and Wargames; pack entry files,
pack checks and worked examples use the exact shapes in
`kernel/METADATA_SPEC.md`.

Required where they change what an agent does: `authority`,
`applies_when`, `sources` and `review`. Doctrine with no `applies_when`
gets applied where it does not belong, and binding Doctrine with no
`sources` cannot be argued with. The rest of the axes are optional and
derived where possible (ADR-0008). *Caught instead by*: nothing was
catching them before, so this makes the written rule match the enforced
one rather than shrinking real enforcement.

The axis definitions, canonical record shapes, enums and compatibility table stay in
`kernel/METADATA_SPEC.md`, where S001 checks the enums and F001 the
review axis. They are not restated here, because a rule written twice
goes stale in one of the two places. That file's per-kind minima table
now follows ADR-0008 decision 7.

## ID schemes

`kernel/NAMING_SPEC.md` is the complete naming contract. In brief:

- `DOC-<NAMESPACE>-NNN`: atomic Doctrine.
- `DREL-<NAMESPACE>-NNN`: typed Doctrine Relations.
- `WG-<NAMESPACE>-NNN`: Wargames. Every live Wargame uses this form.
- `RUL-<NAMESPACE>-NNN`: a Ruling unique within one venture's
  `docs/RULINGS.json`.
- `EX-<NAMESPACE>-NNN`: worked examples.
- `ADR-NNNN`, `EV-NNNN`, `LES-NNNN`, `LENS-NNNN` and `T-NNNN`:
  decisions, evidence, lessons, research lenses and tasks respectively.
- `PB-E<NN>`: EOS playbooks. `STACK-<slug>`: dated stack profiles.

New pack-owned IDs use the `id_namespace` in `PACK.md`. IDs are immutable and
never reused. Former Wargame identities resolve as direct aliases through
`registry/identifier-aliases.json`; they are not current definitions and no
new one is issued. A venture cites EOS `DOC-*`, `DREL-*` and `WG-*` identities
but mints none of them.

Old commits retain their own identities and paths. Current aliases preserve
identity, not latest-branch URLs, and the live tree carries no redirect files
at retired collection paths.

## Tag vocabulary

This list is the known set, not a wall. A tag outside it means look
before adding: either the file wants a tag that is already here, or the
estate has grown a subject and the list should grow with it. Add a tag
by editing this list in the commit that first uses it, with a one-line
reason in the commit message.

An unknown tag warns (ADR-0008). Check E009 parses this list live from
this file and flags any tag it cannot find, which is a prompt to look
rather than a refusal: the commit lands either way, and a tag added
without its entry shows up as a warning until somebody settles it.
*Caught instead by*: that warning, and hygiene in the monthly pass.

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

- `AGENTS.md` and `CLAUDE.md`: a hard cap of forty lines each, byte
  identical. This one stays an error, because that file sits in every
  agent's context and its cost is paid on every task. E003 compares the
  two files and E007 counts the lines.
- A pack `PACK.md` body stays under five hundred lines, and one Wargame
  under two hundred and twenty. There is no all-collections cap: nothing loads
  a whole pack, so total size never measured a cost anyone pays
  (ADR-0004). A pack holds as much atomic knowledge and supporting material as
  its domain earns.
- Types `doctrine`, `foundation`, `pattern`, `ux` and `implementation`:
  one hundred and fifty lines.
- A task record is capped at forty lines and a review verdict at ten.
  Nothing measures either, and a record is JSON under `org/tasks/`
  rather than prose. They are targets the review pass keeps.
- Registries and indexes are exempt. They must be complete rather than
  short.

Every budget but the router cap is a warning (ADR-0008), on the
argument that length is caught by the pruning test in
`packs/PACK_CONTRACT.md` and by the review passes. E007 enforces the
one-hundred-and-fifty-line warning for the five general budget types above,
the separate two-hundred-and-twenty-line threshold for `type: wargame`,
and the five-hundred-line threshold for `type: pack`. A `length_waiver` no
longer changes the
severity, only the wording. With one, the finding names the reason the
file is long. Without one, it says to prune the file or record a
reason. That is the distinction a review pass reads, an argued length
against one nobody has examined.

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
| `packs/DOCTRINE_INDEX.md` | `check --write-index` |
| `packs/WARGAME_INDEX.md` | `check --write-index` |
| `registry/DOCTRINE_PRESSURE_MATRIX.md` | `check --write-index` |
| `registry/IDENTIFIER_ALIASES.md` | `check --write-index` |
| `registry/CAPABILITIES.md` | `check --write-index` |
| `registry/LESSONS.md` | `check --write-index` |
| `org/TASKS.md` | `task views` |
| `org/STATE.md` | `task views` |

Every derived index is scoped to live material. Frozen trees, meaning
`archive/` and the benchmark fixtures, are checked and never indexed: a
fixture's Wargames are not EOS guidance, and an index that mixes them
with the real thing teaches an agent the wrong law.

Canonical machine files hold the truth; the Markdown beside them is a
view. `registry/evidence.json`, `registry/lessons.json`,
`registry/coverage.json`, `estate/repos.json`, `org/claims.json` and the
task records are canonical.

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
material, the fix is to write the Wargame in the pack, never to delete
the target and leave a dangling link.

## Versioning and release

Semver tags on this repo: patch for wording, minor for additive change,
major for a broken contract. Ventures pin the EOS commit they compiled
from and never auto-upgrade. A pin must resolve to a pushed tag or a
commit reachable from origin, and the checker enforces it. Release runs
through playbook PB-E05 and needs the operator's explicit approval.
