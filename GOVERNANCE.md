---
summary: The law of the EOS, schema, tags, promotion numbers, precedence, versioning, protected set
type: governance
tags: [eos]
---

# GOVERNANCE

How the EOS itself is allowed to change, and the contracts every file
obeys. This file is in the protected set: changing it requires an
accepted ADR in `org/decisions/` with Daniel's approval recorded.

## Protected set

- `GOVERNANCE.md` (this file)
- `kernel/templates/org/CONSTITUTION.tpl.md` Parts II and III
- `kernel/templates/org/roles/` (all three charters)
- The module-shape invariants in `doctrine/MODULE_SHAPE.md`
- The wargame format (`doctrine/web-design/templates/WG_TEMPLATE.md`)
- The ID schemes and front-matter schema below
- `org/decisions/` (append-only, no retro-edits)

Emergency clause, borrowed from the kernel: anything may be fixed to
restore a broken repo state first, paperwork immediately after, but the
protected set is never touched under the emergency clause.

## Front-matter schema

Every markdown file opens with YAML front-matter. `tools/eos_check.py`
validates it (check E002). Keys:

| Key | Required | Notes |
| --- | --- | --- |
| `summary` | always | One line, feeds INDEX.md |
| `type` | always | One artefact type from the list below |
| `tags` | always | Inline list from the tag vocabulary, `[web, motion]` |
| `status` | wargame, decision, stack, registry | draft, active, contested, superseded, accepted, proposed |
| `review_by` | wargame, stack, registry, guide | YYYY-MM |
| `supersedes` / `superseded_by` | when lineage exists | Bidirectional |
| `template` | kernel templates | `true`, exempts slot checks in --repo mode |
| `derived` | generated files | `true`, hand-editing is a finding |
| `length_waiver` | over-budget files | The reason, one line |
| `extracted_from` | kernel extractions | e.g. `Venture A@d2e3250` |

Artefact types: `root`, `governance`, `decision`, `doctrine`,
`foundation`, `pattern`, `ux`, `implementation`, `wargame`, `template`,
`example`, `registry`, `stack`, `playbook`, `org`, `kernel`, `guide`,
`index`.

## Tag vocabulary

Tags outside this list fail check E009. Add a tag by editing this list
in the same commit that first uses it, with a one-line reason in the
commit message. One flat vocabulary, grouped for reading.

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

## ID schemes

- Wargames: `WG-<MOD>-NNN`, module prefixes WEB, ARCH, DEL, OPS, VOX,
  EOS. Globally unique, numbered per module, never reused.
- EOS decisions: `ADR-NNNN` in `org/decisions/`.
- EOS playbooks: `PB-ENN` in `org/PLAYBOOKS.md`.
- Venture artefacts keep the kernel's schemes: WO, SUGG, ADR, RN, GD,
  STD, REG, PB, session logs `S-NNNN`.

## Line budgets

- `AGENTS.md` and `CLAUDE.md`: hard cap 40 lines each (check E007).
- Types `doctrine`, `foundation`, `pattern`, `ux`, `implementation`,
  `wargame`: warning over 150 lines, error without a `length_waiver`.
- All other types exempt. Registries must be complete rather than short.

## Knowledge promotion and demotion

Rulings on wargames are marked `argued` (engaged the triggers afresh) or
`inherited` (took the default without new argument). Only argued rulings
are promotion evidence.

- **Ruling to default**: two concordant argued rulings from different
  ventures with zero contrary rulings, or one argued ruling plus strong
  cited external evidence. Applied by editing the wargame's Default
  section, citing the rulings.
- **Default to doctrine**: three concordant argued rulings across at
  least two venture scales, plus a fresh adversarial re-argument of the
  wargame in a cold context that fails to break it, plus Daniel's
  sign-off. The wargame stays alive beneath the doctrine as its argument
  of record.
- **Demotion**: one contrary argued ruling marks the default or doctrine
  `contested` and schedules a re-argument at the next promotion review.
  Two contrary argued rulings demote automatically: doctrine falls to
  default, default falls to open wargame.
- Promotion and demotion run through playbook PB-E04 on the monthly
  cadence, counting rulings from lock-book headers across the estate.

## Staleness and supersession

Past `review_by` means suspect: verify the claims before relying, and
the hygiene cadence queues expired items as work. Supersession is
explicit and bidirectional (`supersedes` / `superseded_by`); the
superseded file keeps its place for one release cycle, then the release
playbook archives it. Silent deletion of guidance is a finding.

## Doctrine exceptions

A venture deviates from doctrine only through a Deviations entry in its
lock-book citing the trigger that justifies it, approved by Daniel.
Deviations are harvested and count as contrary rulings. If no wargame
covers the fork, the deviation must file a draft wargame with its ruling
as the first worked entry.

## Conflict precedence

1. The venture lock-book, on specifics.
2. The kernel constitution articles.
3. Module doctrine.
4. Wargame defaults.
5. Guidance.

Across modules, the module that owns the decision (per the wargame
index) wins. A discovered conflict is queued and resolved by a joint
wargame; until resolved, the stricter rule applies. Doctrine may never
contradict kernel constitution Parts II or III.

## Versioning and release

Semver tags on this repo: patch for wording and fixes, minor for
additive change (new wargames, rulings, modules, stack profiles), major
for breaking change (template contracts, ID schemes, doctrine
reversals). Release is playbook PB-E05: checks green, CHANGELOG entry,
tag, push. Ventures pin `eos_version` plus commit in their lock-book and
never auto-upgrade; PB-E06 is the only upgrade path. The quarterly
registry review flags ventures more than one minor version behind.
