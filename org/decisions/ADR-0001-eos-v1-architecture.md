---
summary: The founding decision, PatterTech EOS v1.0 architecture and the argument for it
type: decision
tags: [eos]
status: accepted
decided_by: Daniel Parke
date: 2026-07-07
---

# ADR-0001: PatterTech EOS v1.0 architecture

This record is the comprehensive architecture proposal for v1.0 and the
decision that adopted it. It supersedes the v0.1 plan of record in
VISION.md and satisfies the wargame-first rule for the migration itself:
the argument is written down before the rules changed.

## Context

PatterTech_Framework v0.1 held one populated module (web-design) and a
standing mandate to grow into a kernel that can run any project. Daniel
commissioned the full generalisation: an AI-native Engineering Operating
System, the single source from which a capable agent, given only a
high-level venture description, can plan, architect, implement, test,
document, deploy and evolve a project to PatterTech standards with
minimal human input. The prompt explicitly invited a redesign from first
principles rather than preservation of existing structure.

## 1. Critical review of v0.1

What earned its keep:

- **The wargame format** (question, triggers, options, decision rule,
  default, worked rulings) is ahead of industry practice. The closest
  public analogues are ADRs, which record decisions after the fact, and
  golden paths, which offer one pre-made choice. A wargame is a pre-solved
  decision procedure. It stays.
- **The knowledge lifecycle in miniature**: ruling to default to doctrine,
  gated by argument. Right idea, no numbers attached.
- **Files over memory, the stranger rule, review_by dates, the house
  voice.** All kept, several promoted to kernel law.
- **The module shape** (doctrine, foundations, patterns, wargames,
  templates, example) proved itself on web-design.

What failed or was missing:

- **No execution half.** The framework said what to decide and never how
  work happens. Roles, work orders, gates, cadences and session discipline
  lived in Venture A's org kernel, a separate repo, unconnected.
- **No meta-layer.** No promotion criteria, no staleness or supersession
  rules, no doctrine-exception mechanism, no module-shape rules for
  non-design domains, no versioning, no release model.
- **Copy-based consumption.** Projects copied PROJECT_LOCKIN.md by hand.
  Nothing stamped which framework version a project used, and nothing
  defined how lessons flowed back.
- **No deterministic navigation.** An agent had to know the repo to find
  the right file.
- **Stub modules that were not domains.** Cost is a trigger in nearly
  every architecture and devops decision, not a domain that owns
  decisions. Hardware has no venture demanding it yet.

## 2. Research findings

External survey, July 2026. Sources at the end of this section.

- **Spec-driven development works and over-reaches.** GitHub reports an
  order of magnitude fewer regenerate-from-scratch cycles with Spec Kit,
  and the same tooling turns a small bug fix into sixteen acceptance
  criteria. Uniform ceremony is the failure mode; unmaintained specs
  become lies that misguide later sessions. Ceremony must tier with the
  size of the thing being built.
- **Root agent files must be small and hand-written.** The AGENTS.md
  standard (Linux Foundation since December 2025) converges on files
  under 150 lines; measured studies found LLM-generated instruction files
  reduce task success. The always-loaded surface is precious.
- **Long-running agent harnesses converge on the same organs.** Anthropic's
  published harness uses an initialiser agent, then a coding agent per
  session, a granular pass/fail feature list, a progress file, git as the
  state spine, one feature per session, and verification before building.
  Venture A's kernel arrived at the same shape independently: work orders
  with acceptance boxes, STATE.md, session logs, one WO per session.
- **Context is the binding constraint.** Performance degrades as the
  window fills. Progressive disclosure (a name and one line always
  visible, the body loaded on demand) is the load-bearing pattern, and a
  deterministic index file beats vector search at repo scale.
- **Named failure modes to design against**: context rot, instruction
  drift, spec drift, sycophantic confirmation, silent failure, premature
  completion, degeneration loops on a failing check.
- **Roles as personas add ceremony without value.** BMAD-style agent
  casts are criticised for role-play overhead. Venture A's practices are
  bodies of knowledge in files, loadable by any model. That is the better
  call and the kernel keeps it.
- **ADRs matter more for agents than for people**, because agents have no
  memory between sessions and the record carries the why.

Sources: martinfowler.com on spec-driven tools (Kiro, spec-kit, Tessl);
github.blog and github.github.com/spec-kit; agents.md and the AAIF
donation notes; anthropic.com/engineering on effective harnesses for
long-running agents; code.claude.com best-practices; llmstxt proposals
and index-file write-ups; BMAD-METHOD documentation and critiques;
adr.github.io.

## 3. Architectural principles

1. **Context is the constraint.** Thin routers, deterministic index,
   progressive disclosure. Nothing loads that does not pay rent.
2. **Doctrine argues; registries date.** Timeless argued rules in
   doctrine. Time-sensitive facts in registries with review_by dates.
3. **Compiled, not copied, never composed.** Seeds are slot-filled and
   pruned from hand-written templates, with a compile report proving
   ancestry. The compiler is a mechanic, not an author.
4. **Ceremony tiers with risk.** Venture scale S, M or L at inception.
   Risk tiers T1 to T4 per work order. Only triggered wargames are walked.
5. **One writer per repo per concern.** Ventures write feedback at home;
   the EOS pulls it on a cadence.
6. **The EOS runs itself on its own kernel.** Its own state, queue,
   cadences, decisions and logs. The first dogfood.
7. **Verification everywhere.** Executable gates with rubrics, independent
   review in fresh context for anything above trivial, drills as the
   standing eval harness.
8. **Built for the weakest capable model.** Templates and checks sized so
   a non-frontier model succeeds from files alone. Circuit breakers over
   open-ended retries.

## 4. Proposed structure

Seven top-level concerns:

- `kernel/`: the material compiled into ventures. Templates with explicit
  slots and scale markers, the scale matrix, the seed rubric. Nothing here
  is read at project runtime; projects get compiled copies.
- `doctrine/`: the knowledge modules. web-design (populated), then
  architecture, delivery, devops, voice. Each module owns its wargames
  with globally unique module-prefixed IDs (WG-WEB-001). A derived
  WARGAME_INDEX gives inception one surface to walk.
- `inception/`: the Session 0 system. Interview protocol, scale wargame,
  walk order, compile rules.
- `registry/`: estate facts. Projects, trusted vendors, lessons, stack
  profiles. Everything carries review_by.
- `org/`: the EOS's own lite kernel instance. State, queue, cadences,
  playbooks, decisions, logs.
- `examples/`: worked instantiations.
- `tools/eos_check.py`: the single sanctioned executable. Stdlib only.
  Generates and verifies the indexes, validates front-matter against the
  schema, checks voice, IDs, budgets and staleness. Two modes: --repo for
  this repo, --seed for compiled seed packs.

Wargames stay per-module because colocation preserves progressive
disclosure; prefixed IDs kill collisions; the derived index gives
inception its single surface. Stack profiles are central in the registry
because a stack couples frontend, backend, testing and hosting, and
because a stack profile is dated fact, not argued doctrine.

## 5. Documentation taxonomy

Every markdown file opens with YAML front-matter validated against the
schema in GOVERNANCE.md: summary (one line, feeds the index), type (one
of the artefact types), tags (from the controlled vocabulary), and where
the artefact is time-sensitive, status and review_by, plus supersedes and
superseded_by when lineage exists. INDEX.md and WARGAME_INDEX.md are
derived pipe-tables, one row per file, regenerated and verified by
eos_check.py. Doctrine and wargame files carry a 150-line budget,
enforced as a warning that becomes an error without a length_waiver;
registries, kernel templates and org files are exempt by type; root
routers are hard-capped at 40 lines.

## 6. Agent lifecycle

Idea, then Session 0, then Genesis where scale demands it, then the
delivery loop, then operations, then evolution.

The delivery loop is the Venture A machinery, adopted unchanged: PLAN,
WORK and VERIFY roles with separation of duties; four intake doors
(human intent, cadence findings, verification failures, suggestions);
typed work orders whose risk tier decides the gate ladder; worktrees and
path-glob claims for parallelism; cadences that outrank new low-priority
work; append-only session logs; STATE.md as the handoff spine, closing
with a fixed-key Resume Packet. The three-strikes rule binds all roles:
when the same check fails after three distinct attempts, stop, record
the attempts and hypotheses, block the item, flag the state, and file a
question if a human decision is needed. Never weaken a check to pass it.

Evolution has four organs: the venture retro (the only place a venture
edits its own org), rescale (re-run the scale wargame when triggers
change), upgrade (move the EOS pin forward by changelog diff), and
harvest (the EOS pulls feedback and rulings monthly).

## 7. Session 0 methodology

One session in the new venture repo, human present at the start and the
gate. Five phases:

- **A. Interview.** The agent fills the venture brief. Three challenge
  steps are mandatory before the brief is accepted: restate the venture
  and be corrected; name the three cheapest ways it dies; propose the
  strictly smaller version and have it explicitly rejected or adopted.
  This is anti-sycophancy by design.
- **B. Scale ruling.** Walk WG-EOS-001. Triggers: lifespan, server state
  or auth, money, personal or regulated data, ops burden, a second human.
  Default is the smallest scale the triggers allow.
- **C. Wargame walk.** Compile the walk from the wargame index filtered
  by the venture's triggered domains. Rule each wargame into the
  lock-book, marked argued or inherited. A fork with no wargame files a
  draft wargame in the venture's feedback file, ruling attached.
- **D. Seed compile.** Prune scale-marked sections, fill slots from the
  lock-book, distil the venture's standards from the doctrine the rulings
  cite, write the compile report.
- **E. Gate.** eos_check --seed all green, then the human signs the
  rubric's judgement items, headed by the cold-start test: a fresh WORK
  session must be able to complete the first work order with zero
  questions. One row is appended to the EOS projects registry.

## 8. Seed pack pipeline

Scales: S is roughly six files (thin routers, brief, lock-book, worklog,
feedback; no org). M is roughly fifteen (adds a lite org: constitution
with the product-doctrine slot filled, collapsed tiers, a single-file
queue, three cadences). L is roughly twenty-five, the full Venture A
shape. Add-ons attach by trigger regardless of scale: a compliance
registry when personal data appears, ops runbooks when anything deploys.
The lock-book header is machine-readable YAML: eos_root, eos_version and
commit, scale, stack profile, and the rulings table. Ventures pin their
EOS version and never auto-upgrade.

## 9. Knowledge management

One pipeline, two scopes. Inside a venture: L0 research, L1 guidance, L2
standard, L3 automated check, with review_by expiry, exactly as the
Venture A kernel defines. Across ventures: worked rulings accumulate on
wargames, harden into defaults, and defaults harden into doctrine, with
the numbers in GOVERNANCE.md. Harvest is pull-based and monthly; a
silent month still records checked, clean. Lessons land in the registry
ledger with a disposition: ruling appended, wargame filed, default
changed, or declined with a reason.

## 10. Governance

- **Promotion.** Ruling to default: two concordant argued rulings from
  different ventures with none contrary, or one argued ruling plus strong
  cited external evidence. Default to doctrine: three concordant argued
  rulings across at least two scales, plus a fresh adversarial
  re-argument in a cold context that fails to break it, plus human
  sign-off. Inherited rulings never count, which stops the compiler's own
  defaults laundering themselves into doctrine.
- **Demotion.** One contrary argued ruling marks the rule contested and
  schedules a re-argument. Two demote automatically: doctrine falls to
  default, default falls to open wargame.
- **Staleness and supersession.** Past review_by means suspect: verify
  before relying. Supersession is explicit and bidirectional in
  front-matter; nothing is silently deleted.
- **Exceptions.** A venture deviates from doctrine only through a
  lock-book deviation entry citing the trigger, human-approved.
  Deviations are harvested as contrary rulings.
- **Precedence.** Venture lock-book on specifics, then kernel
  constitution, then module doctrine, then defaults, then guidance. The
  owning module wins across modules; the stricter rule applies until a
  joint wargame resolves a conflict.
- **Versioning.** Semver tags. Patch is wording, minor is additive, major
  is breaking. The upgrade playbook is the only path forward for a
  pinned venture.
- **Protected set.** GOVERNANCE.md, the kernel constitution Parts II and
  III, the role templates, the module-shape invariants, the wargame
  format, the ID schemes, and org/decisions/. Changes require an EOS ADR
  with recorded human approval.

## 11. Migration from v0.1

Executed at this decision's date: branch renamed to main; modules moved
to doctrine with git mv (history follows); devops-deployment renamed
devops; the worked example, static stack profile and lock-in template
lifted to examples/, registry/stacks/ and kernel/templates/; cost and
hardware stubs retired to roadmap rows; fourteen wargames renamed to
WG-WEB IDs with every reference updated; root files rewritten; the
governance layer, registries, org instance, check tool and indexes
created. The folder rename to PatterTech_EOS is deliberately last, run
by Daniel after closing sessions rooted in the repo, followed by fresh
creation of the private GitHub remote and the first push. Two external
references in PatterTech_Website are updated at the same time.

## 12. Roadmap

Phase A (this session): migration, roots, governance, registries, org
instance, check tool. Phase B: kernel extraction from the Venture A seed
at commit d2e3250, scale matrix, seed rubric; four to five sessions and
the highest-value writing in the plan. Phase C: compile rules and the
voice module. Phase D: the Venture A reseed, which doubles as the L-scale
drill; Daniel ruled that Venture A reseeds from the new kernel before
Genesis runs, so phases B to D are front-loaded to keep sprint delay
small. Phase E: the full inception system and an S-scale drill. Phase F:
architecture, delivery and devops doctrine modules, then the v1.0.0 tag.
Data, security-compliance, product and hardware are roadmap rows with
extraction mandates for v1.1 and beyond.

## 13. Risks and trade-offs

Index drift (generated, checked, swept monthly). Doctrine bloat (line
budgets, the pruning test, promotion bars). Compiled seeds drifting into
generated mush (slot-fill only, compile reports, the rubric, drills).
Version skew between EOS and ventures (pins, quarterly review, cheap
upgrades). Over-ceremony for small ventures (S capped near six files,
smallest-fitting default, ceremony complaints are harvest input).
Sycophantic inception (mandated challenge steps, human gate).
Harvest starvation (a due cadence outranks new low-priority work).
Sprint pressure from the early Venture A reseed (front-loaded phases,
slotting its existing content rather than rewriting it). Single-machine
bus factor (GitHub push at the tag, stranger rule applied to the EOS
itself). Accepted impurities: one Python script in a docs repo, a
derived index to maintain, and roughly eight files of self-ceremony in
org/, the price of dogfooding.

## 14. Additional concepts adopted with this decision

- **The guardrail review.** Six proposed guardrails were validated rather
  than accepted wholesale. Adopted: the compile gate (mechanical seed
  validation before Session 0 closes), strict columnar indexes with a
  controlled tag vocabulary, and the Resume Packet. Adopted in substance
  but rerouted: the escalation gate became the three-strikes rule through
  existing organs rather than a new HELP.md file. Rejected: dot-notation
  sub-wargame IDs (split, don't nest) and .eoslock files (worktrees and
  claims are the isolation mechanism; lock files in a shared tree are
  racy and go stale, which the estate's own job queue already learned).
- **The drill as eval harness.** A canned brief run cold through Session
  0 on a quarterly cadence, graded against the rubric. The EOS tests
  itself the way it tests ventures.
- **Argued versus inherited rulings**, making promotion evidence
  machine-countable across the estate.
- **The weakest-capable-model principle**, recorded above as principle 8.

## Alternatives considered

- **Adopt an external meta-framework** (BMAD, Spec Kit). Rejected: both
  impose uniform ceremony, neither carries our doctrine or voice, and
  both would put the decision library outside our governance.
- **Keep two repos**, framework for knowledge and a per-project org
  kernel with no shared source. Rejected: that is the v0.1 status quo,
  and it is why the two halves never compounded.
- **A monorepo of all ventures plus the EOS.** Rejected: ventures have
  different lifespans, remotes and contractual boundaries; the estate
  convention is a repo per venture with the EOS as the shared brain.

## Decision

Adopt the architecture above as PatterTech EOS v1.0. Accepted by Daniel
on 2026-07-07 after plan review, three scope rulings (staged build,
Venture A reseed before Genesis, rename to PatterTech_EOS) and the
guardrail amendment round.
