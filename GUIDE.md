---
summary: The all-in-one guide to the EOS, the AutoWatt genesis and the development lifecycle
type: guide
tags: [eos]
review_by: 2027-01
---

# The PatterTech EOS Field Guide

One document that takes you from knowing nothing to working inside the
system with confidence. It teaches three things in order: what the
PatterTech Engineering Operating System is and how it thinks (Section
1), how a real venture called AutoWatt was born from it (Section 2),
and how you build a product inside it day to day (Section 3). AutoWatt
is the worked example throughout, so the ideas never stay abstract.

## How to use this guide

This guide teaches; it does not replace the files. The EOS has one iron
rule, "one writer per fact", so nothing here restates the reference
material that already lives in the repository. Instead each chapter
explains a concept and then points you to the canonical file where the
exhaustive detail lives and stays current. Read the guide to
understand; open the file it names when you need the last decimal
place.

There are two ways in:

- **New here?** Read start to finish. The chapters are ordered the way
  the system actually unfolds: the framework, then a venture's birth,
  then its build.
- **Looking something up?** Jump by the table of contents. Chapter 3 is
  the map of the whole repository; every later chapter tells you which
  file is the source of truth for its topic.

Throughout, callouts flag the things worth stopping for:

> [!TIP]
> A shortcut, or a piece of the machine that is easy to miss.

> [!IMPORTANT]
> A rule that will bite you if you skip it.

> [!WARNING]
> A common pitfall, with the way around it.

> [!NOTE]
> **Architecture note.** Why a thing is built the way it is, for
> readers who want the reasoning and not just the rule.

A glossary and a cross-reference appendix sit at the end. If a term
lands with no explanation, the glossary has it.

## Table of contents

**Section 1 · The PatterTech EOS framework**
- [Chapter 1 · What the EOS is, and the problem it solves](#chapter-1--what-the-eos-is-and-the-problem-it-solves)
- [Chapter 2 · The mental model: eight ideas that carry everything](#chapter-2--the-mental-model)
- [Chapter 3 · The map: seven concerns, the roots, and how to navigate](#chapter-3--the-map)
- [Chapter 4 · Doctrine and wargames: how the estate argues](#chapter-4--doctrine-and-wargames)
- [Chapter 5 · The kernel and the compile pipeline](#chapter-5--the-kernel-and-the-compile-pipeline)
- [Chapter 6 · How work happens: roles, orders, tiers, gates](#chapter-6--how-work-happens)
- [Chapter 7 · Governance and the check tool](#chapter-7--governance-and-the-check-tool)
- [Chapter 8 · The EOS runs itself](#chapter-8--the-eos-runs-itself)

**Section 2 · The AutoWatt seed pack and the genesis run**
- [Chapter 9 · Where AutoWatt came from](#chapter-9--where-autowatt-came-from)
- [Chapter 10 · Session 0 walked, step by step](#chapter-10--session-0-walked)
- [Chapter 11 · The compile in detail](#chapter-11--the-compile-in-detail)
- [Chapter 12 · What Genesis produced](#chapter-12--what-genesis-produced)
- [Chapter 13 · Nuances and lessons](#chapter-13--nuances-and-lessons)

**Section 3 · The development lifecycle**
- [Chapter 14 · The delivery loop](#chapter-14--the-delivery-loop)
- [Chapter 15 · Local-first setup](#chapter-15--local-first-setup)
- [Chapter 16 · A work order start to finish](#chapter-16--a-work-order-start-to-finish)
- [Chapter 17 · The road ahead for AutoWatt](#chapter-17--the-road-ahead-for-autowatt)
- [Chapter 18 · Operating a venture over time](#chapter-18--operating-a-venture-over-time)

**Back matter**
- [Glossary](#glossary)
- [Cross-reference: the canonical files](#cross-reference-the-canonical-files)

---

# Section 1 · The PatterTech EOS framework

## Chapter 1 · What the EOS is, and the problem it solves

**What you will learn:** what the system is for, the two-halves idea at
its heart, and why it exists at all. No file paths to open yet; this is
the concept before the mechanism.

The PatterTech Engineering Operating System (the EOS) is a repository
of documentation and process. It has no application to run and no
server to start. What it holds is the shared brain of an estate of
software ventures: the accumulated judgement about how to design,
build, test, ship and run software to a consistent standard, plus the
machinery to plant that judgement into a new venture and keep it
governed as the venture grows.

The problem it solves is the one every growing software effort hits.
Knowledge lives in people's heads and leaks when they leave. The same
decisions get re-argued from scratch on every project. Standards drift
because nothing checks them. A new project starts from a blank page
even though the last three projects already learned what it needs. The
EOS answers this by writing the judgement down as files, giving those
files a way to compound over time, and compiling a tailored copy of
them into each new venture at its birth.

> [!NOTE]
> **Architecture note.** The EOS is designed for AI agents as much as
> for people. An agent has no memory between sessions, so everything it
> needs must be on disk and findable. The whole system is shaped by
> that constraint: thin files that load on demand, a deterministic
> index to navigate by, and a house rule that if a thing is not written
> down, it is not decided. This is why the guide keeps pointing you at
> files. The files are the memory.

### The two halves

The EOS unifies two things that most teams keep separate and that,
kept separate, never reinforce each other.

- The **knowledge half** is what to decide and why: the design
  doctrine, the argued rules, the record of trade-offs. In this repo it
  lives in `doctrine/` and `registry/`.
- The **execution half** is how work actually happens: who does what,
  how a change moves from idea to shipped, what gates it passes. In
  this repo it lives in `kernel/` (the templates that carry it into
  ventures) and is demonstrated in `org/` (the EOS running the
  discipline on itself).

A venture gets both halves at once, sized to its needs, as a compiled
seed. That is the founding idea. Everything else in this guide is the
detail of how it is done.

### What "a venture" means here

A venture is one software project the EOS serves: a product, a site, a
tool. Two exist in the estate today. **AutoWatt** is a full product
build, used as the worked example from Section 2 onward.
**PatterTech_Website** is a smaller marketing and content site. The
registry lists them (see `registry/PROJECTS.md`); each carries a pinned
version of the EOS it was seeded from and never upgrades by accident.

---

## Chapter 2 · The mental model

**What you will learn:** the eight ideas that, once they click, make
the rest of the system obvious. Everything in later chapters is one of
these ideas made concrete.

1. **Files over memory.** If it is not written in a file, it is not
   decided. Anything you believe from training or a past conversation
   yields to what the files say. A decision left only in a chat is a
   decision lost. This is the rule that makes a stateless agent, or a
   new teammate, able to continue from where the last one stopped.

2. **The repository is the organisation.** State, knowledge, work,
   decisions and law are all versioned plain-text files. You reason
   about the organisation by reading it, and you change the
   organisation by editing it. There is no separate system of record.

3. **Compiled, not copied, never composed.** A venture does not
   hand-copy the framework, and an agent does not freely generate its
   files. A venture is compiled: hand-written templates are pruned to
   the venture's scale and have their blanks filled from the venture's
   own decisions, with a report proving every file's ancestry. The
   compiler is a mechanic, not an author (see Chapter 5).

4. **Ceremony tiers with risk and scale.** A weekend brochure site and
   a regulated platform should not carry the same process weight. The
   EOS sizes ceremony twice: once at birth by venture **scale** (S, M
   or L), and again per change by **risk tier** (T1 to T4). Small,
   reversible things stay cheap; large, irreversible things stay slow.

5. **Wargame first, doctrine later.** A rule is never just asserted.
   Before a rule exists, the argument that earns it exists: a
   **wargame** that states the fork, the options, and the decision
   rule. Rules are promoted from arguments that survived use, by
   counting evidence, not by opinion (see Chapter 4).

6. **Doctrine argues; registries date.** Timeless argued rules live in
   doctrine and change slowly. Time-sensitive facts (library versions,
   vendor choices, prices) live in registries and carry a review-by
   date. Keeping them apart is how doctrine avoids rotting.

7. **Verification everywhere, by someone else.** Nothing important is
   trusted because its author says it works. Automated checks are the
   floor; an independent reviewer in fresh context is the judgement
   layer; periodic audits keep both honest. No session approves its own
   work.

8. **Built for the weakest capable model.** Templates, checks and
   procedures are sized so a non-frontier agent can succeed from the
   files alone, and so a circuit breaker (the three-strikes rule)
   stops a failing loop rather than letting it grind. If the weakest
   capable worker can do it from the files, anyone can.

> [!TIP]
> If you remember only one of these, remember the first. "Files over
> memory" is the load-bearing idea. Every strange-looking discipline in
> the EOS (the session logs, the Resume Packet, the compile report, the
> derived index) exists to make that rule true in practice.

---

## Chapter 3 · The map

**What you will learn:** the shape of the repository, so you can find
anything. This chapter is the reference you will come back to; later
chapters name the specific files, and this is where they all sit.

The repository has seven top-level concerns. Each has one job.

| Directory | Its one job | Start file |
| --- | --- | --- |
| `kernel/` | The templates and rules compiled into ventures | `kernel/README.md` |
| `doctrine/` | The knowledge modules: argued rules and wargames | `doctrine/README.md` |
| `inception/` | The Session 0 system that seeds a new venture | `inception/INCEPTION.md` |
| `registry/` | Dated facts: projects, vendors, lessons, stack profiles | `registry/PROJECTS.md` |
| `org/` | The EOS running its own discipline on itself | `org/STATE.md` |
| `examples/` | Worked instantiations to learn from | `examples/autowatt-seed.md` |
| `tools/` | The single sanctioned executable, `eos_check.py` | `tools/eos_check.py` |

At the root sit the files every session may touch. The important ones:

- `AGENTS.md` and its byte-identical twin `CLAUDE.md` are the thin
  entry point, hard-capped at 40 lines. They name the three entry modes
  and a short never-list, and send you to `START.md`.
- `START.md` is the bootstrap: what to read, in what order, for your
  entry mode, plus the ground rules.
- `GOVERNANCE.md` is the law: the protected set, the front-matter
  schema, the tag vocabulary, the promotion numbers, versioning. When
  in doubt about a rule of the system itself, this is the source.
- `VISION.md`, `README.md`, `OPERATORS_GUIDE.md`, `CHANGELOG.md` and
  `MODULE_SHAPE.md` cover the north star, the outward summary, the
  human operator's manual, the release history, and the contract every
  doctrine module obeys.
- `INDEX.md` and `doctrine/WARGAME_INDEX.md` are **derived** files: one
  row per file, generated from front-matter. You do not edit them; you
  grep them. They are how an agent finds the right file without knowing
  the repo by heart.

> [!IMPORTANT]
> `INDEX.md` and `WARGAME_INDEX.md` are never hand-edited. They are
> regenerated by `python tools/eos_check.py --write-index`. Editing them
> by hand is a finding the check will flag (E001). If you add or retag a
> file, regenerate the index in the same change.

### The three entry modes

Every session begins by picking a mode. `AGENTS.md` states them;
`START.md` tells you what to read for each.

1. **Working on a venture.** Read that venture's lock-book first, then
   the doctrine and stack profiles its rulings cite. `INDEX.md` and
   `WARGAME_INDEX.md` are the maps.
2. **Working on the EOS itself.** Read `org/STATE.md`, take the top
   unblocked item in `org/QUEUE.md`, follow the playbook it names. This
   is the mode that built the whole system, and the mode this guide was
   written in.
3. **Starting a new venture (Session 0).** Run
   `inception/INCEPTION.md` end to end in the new venture's repo. This
   is Section 2 of this guide, walked in full.

---

## Chapter 4 · Doctrine and wargames

**What you will learn:** how the estate turns experience into rules
that hold, and how those rules earn their authority instead of being
declared. The canonical files are `GOVERNANCE.md` (the numbers) and
each module's `wargames/` directory (the arguments).

### The wargame: a pre-solved decision

A **wargame** is a decision procedure written down before you need it.
Its shape (fixed in `doctrine/web-design/templates/WG_TEMPLATE.md`) is
always the same: the question stated as a fork, what it depends on, the
options with their costs, a decision rule, a default for when the
triggers are silent, and a list of worked rulings from real ventures.

The value is that a fork gets solved once, with the reasoning attached,
and then every future venture facing the same fork applies the rule
instead of re-arguing it. There are 33 wargames today across five
modules. A few, to make it concrete:

- `WG-ARCH-003`: derived values, computed, cached, or stored as an
  immutable snapshot?
- `WG-OPS-001`: managed platform, a cloud estate, or self-hosting?
- `WG-WEB-001`: dark, light, or dual register for a web surface?
- `WG-VOX-001`: which register does this surface speak in?

### Argued versus inherited: the machinery of trust

When a venture applies a wargame, its ruling is marked one of two ways,
and the distinction is the engine of the whole knowledge system.

- **Argued** means the venture engaged the triggers afresh against its
  own facts and reasoned to the answer.
- **Inherited** means the venture took the default without new
  argument, which is legitimate when the triggers are silent.

Only argued rulings count as evidence, because only they represent a
fresh mind reaching the same conclusion. This one rule stops the
system's own defaults from laundering themselves into doctrine by
sheer repetition.

### How a rule climbs (and falls)

The promotion numbers live in `GOVERNANCE.md`. In plain terms:

- A wargame's **default** hardens when **two** concordant argued
  rulings from different ventures agree with no ruling against, or when
  one argued ruling is backed by strong external evidence.
- A default becomes binding **doctrine** when **three** concordant
  argued rulings across at least two venture scales agree, a fresh
  adversarial re-argument in a cold context fails to break it, and
  Daniel signs off.
- Rules fall the same way they rise. One contrary argued ruling marks a
  rule **contested**; two demote it automatically, doctrine back to
  default, default back to an open wargame.

> [!NOTE]
> **Architecture note.** This is a knowledge lifecycle with numbers
> attached. It is deliberately slow and deliberately evidence-bound.
> The point is that the estate gets monotonically smarter: a lesson is
> solved once, encoded, and never re-solved, and a rule that stops
> earning its place is demoted rather than defended. The monthly
> promotion review (playbook PB-E04) is where the counting happens.

### The five populated modules

Each doctrine module obeys `MODULE_SHAPE.md`: a README with activation
triggers, a `DOCTRINE.md` of binding rules, and a `wargames/`
directory. The five that exist:

| Module | Rules | Wargames | Activates when |
| --- | --- | --- | --- |
| web-design | 12 | 14 (WG-WEB) | any public web surface |
| voice | 7 | 1 (WG-VOX) | any written surface (so, always) |
| architecture | 7 | 8 (WG-ARCH) | server code, a database, a language boundary |
| delivery | 6 | 4 (WG-DEL) | any code with CI |
| devops | 6 | 4 (WG-OPS) | anything deployed or costing money |

Four more (data, security-compliance, product, hardware) are named as
roadmap rows in `doctrine/README.md`, to be extracted when a venture's
needs argue for them.

---

## Chapter 5 · The kernel and the compile pipeline

**What you will learn:** how a blank new repository becomes a
fully-formed venture, tailored to its size, with every file traceable.
The canonical files are `kernel/README.md`, `inception/COMPILE.md`,
`kernel/SCALE_MATRIX.md` and `kernel/SEED_RUBRIC.md`.

### Templates, slots and fences

The `kernel/templates/` directory holds hand-written templates: the
constitution, the role charters, the operating model, the venture
brief, the lock-book, and more. They are ordinary Markdown with two
special marks.

- A **slot** looks like `{{PRODUCT_DOCTRINE}}`. It is a blank the
  compiler fills from the venture's own decisions. A compiled file with
  an unfilled slot fails the seed check.
- A **scale fence** looks like `<!-- scale: M L -->` opening and
  `<!-- scale: end -->` closing. It wraps a section that only exists at
  the listed scales. The compiler keeps the section if the venture's
  scale is in the list and always removes the marker lines.

> [!NOTE]
> **Architecture note.** This is why the system is "compiled, not
> copied, never composed". Copying would drag every scale's ceremony
> into a tiny venture. Free generation would let an agent invent
> structure and drift from the estate's standard. Slot-filling and
> fence-pruning give a third path: one hand-written source of truth,
> mechanically tailored, with nothing invented.

### Scale: S, M and L

A venture's **scale** decides how much organisation it compiles. It is
ruled once at Session 0 by wargame `WG-EOS-001`, from six triggers:
lifespan, server state or auth, money, personal or regulated data, ops
burden, and a second human. The default is always the smallest scale
the triggers allow.

- **S** is about eight files: thin routers, a brief, a lock-book, a
  worklog, a feedback file. No organisation layer. A brochure site.
- **M** is about eighteen: S plus a lite organisation (a constitution,
  the three role charters, a single queue file, a few cadences),
  collapsed risk tiers.
- **L** is about twenty base files plus the directories Genesis fills:
  the full organisation with per-file work orders, playbooks, standards
  and knowledge shelves. AutoWatt is L.

`kernel/SCALE_MATRIX.md` is the machine-checked law of exactly which
files each scale gets, plus trigger add-ons (a compliance registry when
regulated data appears, an ops runbook when something deploys).

### The five compile steps

The compiler (an agent following `inception/COMPILE.md`) is a
slot-filler and pruner, never an author. It runs five steps:

1. **Prune** every scale-fenced section that the ruled scale excludes,
   and remove the fence markers.
2. **Fill** every slot from the lock-book and brief. No slot syntax may
   remain anywhere afterward, even inside code spans.
3. **Rewrite front-matter**: drop the template marks, add
   `compiled_from`, and write the lock-book's machine-readable rulings
   header.
4. **Assemble**: byte-copy `AGENTS.md` to `CLAUDE.md` last, create the
   empty directories the scale needs, and author any trigger add-ons
   from doctrine (the one sanctioned authoring, marked in the report).
5. **Distil** the venture-facing consequence of each argued ruling into
   the seed where templates leave room, quoting doctrine, never adding
   rules doctrine does not hold.

Then it fills the compile report and runs the gate.

> [!IMPORTANT]
> The compiler never touches protected template text (the
> constitution's Parts II and III, the role charters) except to prune
> fences, and never compiles from a dirty tree. The version it compiles
> from is a specific commit, not a moving branch. This is what makes a
> venture's `eos_pin` mean something exact.

### The seed rubric: the gate

Before a Session 0 closes, the compiled seed must pass
`kernel/SEED_RUBRIC.md`, which has two halves.

- **Auto items A1 to A10** are run by `eos_check.py --seed` and must be
  green: parseable front-matter, a lock-book header carrying version and
  scale and stack, every ruling marked argued or inherited, zero
  unfilled slots, zero leftover fences, every required file present,
  the compile report's ancestry complete, `CLAUDE.md` byte-identical to
  `AGENTS.md`, and the router within 40 lines.
- **Human items H1 to H5** are the operator's judgement, signed not
  delegated. The headline is **H1, the cold-start test**: a fresh
  session, given only the seed and its first task, completes that task
  with zero questions. If a stranger cannot start from the files alone,
  the seed is not done.

---

## Chapter 6 · How work happens

**What you will learn:** the execution half, the part that turns a
decision into a shipped, verified change. This is compiled into M and L
ventures from `kernel/templates/org/`; the reference is a venture's own
`org/OPERATING_MODEL.md` and its three role charters.

### Three roles, never mixed

Any capable worker can hold any role by loading its charter. There are
exactly three, plus you, the human operator.

- **PLAN** decides what and why. It writes specs, work orders, ADRs and
  the ordered queue. It never writes production code and never approves
  its own decisions into the protected set.
- **WORK** changes things. It takes one order at a time, works in an
  isolated branch, writes failing tests first where the type demands,
  and keeps an immaculate paper trail. Its cardinal sin is invention:
  a gap becomes a question, never a guess.
- **VERIFY** is the independent judgement. It reviews a change it did
  not write, in fresh context, and returns a verdict with evidence. It
  finds and reports; it does not fix.

> [!IMPORTANT]
> No session approves its own output. WORK does not merge its own
> sensitive work; VERIFY does not fix what it reviews; PLAN does not
> implement its own specs. This separation is the reason the system can
> be trusted without a human reading every line.

### The work order

Every change is a **work order**: one file (at L scale) stating its
type, risk tier, acceptance criteria as checkboxes, a test
specification, and what verification must confirm. Work enters through
exactly four doors and no others: human intent, a cadence finding, a
verification failure or incident, or a worker suggestion. Anything
noticed in passing becomes a suggestion, never silent extra scope.

There are eleven work types (FEAT, FIX, REFACTOR, PERF, MAINT, HARDEN,
COMPLY, RESEARCH, DOCS, OPS, SPIKE), each with its own definition of
done.

### Risk tiers and gates

A change's **risk tier** decides which **gates** it must pass.

- **T1** trivial and reversible: automated checks only (G1).
- **T2** a standard change: G1 plus independent review (G2).
- **T3** sensitive (schema, auth, money, public surfaces, personal
  data): G1, G2, and human approval (G3).
- **T4** constitutional or irreversible: all of the above plus a
  written ADR.

The gates themselves are G1 automated CI, G2 independent VERIFY review,
G3 human approval, G4 post-release checks, and G5 periodic audit. A red
gate is never bypassed.

### The three-strikes rule

If the same check or gate fails after three distinct fix attempts, the
worker stops. It records the attempts and its hypotheses, blocks the
item, flags it in the state file, and files a question if a human must
decide. It never weakens the check to pass it. This is the circuit
breaker that keeps a stuck agent from grinding or, worse, from quietly
lowering the bar.

> [!TIP]
> You will see this rule honoured for real in Chapter 16, where a
> reviewer rejects a change, the worker fixes the named findings rather
> than arguing, and the change passes on the second round. The system
> is built to make that the normal, unremarkable path.

---

## Chapter 7 · Governance and the check tool

**What you will learn:** the rules the system holds itself to, and the
single program that enforces the mechanical ones. The canonical files
are `GOVERNANCE.md` and `tools/eos_check.py`.

### What governance fixes

`GOVERNANCE.md` is the constitution of the EOS itself. It fixes:

- **The protected set:** the files that cannot change without an
  accepted ADR and Daniel's recorded approval (this includes the
  governance file, the constitution's organisational and change-control
  parts, the role charters, the module-shape invariants, and the
  wargame format).
- **The front-matter schema:** every file opens with YAML front-matter
  (summary, type, tags, and where relevant status and review-by). The
  types and required keys are listed there.
- **The tag vocabulary:** a controlled list, so the derived index stays
  greppable. A tag outside the list is a finding.
- **The ID schemes, line budgets, and the semantic versioning model**
  (patch for wording, minor for additive, major for breaking).

### The one executable

`tools/eos_check.py` is the only program in the repo, stdlib only. It
has ten stable checks, cited by ID so the three-strikes rule can name
them precisely:

| Check | Catches |
| --- | --- |
| E001 | a stale or hand-edited derived index |
| E002 | missing or malformed front-matter |
| E003 | `CLAUDE.md` not byte-identical to `AGENTS.md` |
| E004 | voice tells (em-dashes, exclamation marks, clichés) |
| E005 | bad or undefined wargame IDs |
| E006 | a file past its review-by date |
| E007 | a router over 40 lines, or a doctrine file over budget |
| E008 | an unfilled slot or a leftover scale fence |
| E009 | a tag outside the vocabulary |
| E010 | a stale session claim left in a state file |

It runs in three modes: `--repo` validates the EOS itself, `--seed
<path>` gates a compiled venture against the rubric, and
`--write-index` regenerates the two derived index files. Green means
zero errors; warnings are allowed and explained.

> [!TIP]
> Run `python tools/eos_check.py --repo` before you finish any change to
> the EOS. It is fast, it is the same gate the system holds itself to,
> and it catches the small things (a missing tag, a stale index) that
> are tedious to spot by eye. You will see it catch a real defect in
> Chapter 16 that two rounds of human review missed.

---

## Chapter 8 · The EOS runs itself

**What you will learn:** that the framework is not just described, it is
demonstrated, on itself, in the `org/` directory. This is the strongest
evidence that the system works, and the best worked example of the
execution half before you meet AutoWatt.

The `org/` directory is the EOS's own lite organisation. It has a
`STATE.md` (where the build is, and the Resume Packet a cold session
boots from), a `QUEUE.md` (the ordered work), a `CADENCE.md` (the
recurring maintenance), `PLAYBOOKS.md` (nine procedures, PB-E01 to
PB-E09), an `org/decisions/` folder with the founding ADR, and
`org/logs/` with one file per session.

The whole v1.0 framework was built this way, in nineteen logged
sessions across a single day (2026-07-07), each taking the top queue
item and closing out with a state update and a log. The phases:

- **Phase A** migrated the old v0.1 into the new shape and stood up the
  governance, registries, and the check tool.
- **Phase B** extracted the kernel templates from AutoWatt's own seed
  pack (AutoWatt is the kernel's ancestor; more on that in Chapter 9).
- **Phase C** wrote the compile rules and the voice module.
- **Phase D** reseeded AutoWatt and harvested the lessons.
- **Phase E** built the inception system and proved it with a cold
  drill: a fresh agent ran a full Session 0 against a canned brief and
  passed the rubric without charity.
- **Phase F** wrote the architecture, delivery and devops modules.
- **Release** tagged v1.0.0.

The full argument for every one of these choices is
`org/decisions/ADR-0001-eos-v1-architecture.md`, a thirteen-section
record that is worth reading once you have finished this guide. The
session logs in `org/logs/2026-07/` are the build narrative in the
system's own voice.

> [!NOTE]
> **Architecture note.** Running the framework on itself is called
> dogfooding, and it is not vanity. It is the first and hardest test:
> if the discipline is too heavy to bear, it shows up on the team that
> feels every gram of it first. The roughly eight files of self-ceremony
> in `org/` are the price, paid deliberately, of proving the system is
> livable before asking a venture to live in it.

This is the framework. Section 2 shows it giving birth to a venture.

---

# Section 2 · The AutoWatt seed pack and the genesis run

This section follows one venture, AutoWatt, from an empty organisation
to a complete, buildable one. It is chronological on purpose: the best
way to understand the machinery of Section 1 is to watch it run once.
AutoWatt lives in its own repository; this guide describes what
happened there and names the files, so you can open them alongside if
you have that repo, or follow the narrative if you do not. The
condensed worked example also lives at `examples/autowatt-seed.md`.

## Chapter 9 · Where AutoWatt came from

**What you will learn:** the unusual fact that makes AutoWatt the ideal
teaching case, and the shape of the venture itself.

AutoWatt is a lifecycle integrity platform for renewable energy assets.
In plain terms, it is the system of record for a solar or battery
installation: one canonical record per asset, holding its documents,
equipment, warranties, stewardship and inspection history, reachable by
the owner, an installer, an insurer, and the public through a QR plate
on the hardware. Its slogan, "records, not promises", is also its
engineering thesis: the records have to be genuinely unbreakable, or
they mean nothing.

The unusual fact is this. AutoWatt was seeded, by hand, before the EOS
v1.0 kernel existed. When the framework was generalised, AutoWatt's own
organisational files were the raw material the kernel templates were
extracted from. So AutoWatt is the kernel's ancestor. Reseeding it from
the finished kernel was therefore a round trip: the material that
taught the kernel came home through it, and doing so doubled as the
first real test of the whole compile pipeline at the largest scale.

> [!NOTE]
> **Architecture note.** This round trip is why Section 2 is such a
> clean example. The reseed was not a toy. It was a real venture, under
> a real six-week contract, compiled from the real kernel and graded by
> the real rubric. If the pipeline could reproduce its own ancestor to
> a passing grade, the pipeline worked.

AutoWatt runs under a genuine constraint that shapes everything: a
six-week trial sprint (6 July to 17 August 2026) between Daniel, the
technical co-founder candidate, and Garreth, the founder. That contract
sets the fence for what the MVP must be, which the venture captures as
an acceptance walk-through called §A5. Keep that walk-through in mind;
it becomes the spine of the entire build in Section 3.

## Chapter 10 · Session 0 walked

**What you will learn:** exactly what happens in an inception, step by
step, using AutoWatt's real rulings. The procedure is
`inception/INCEPTION.md`; the interview protocol is
`inception/INTERVIEW.md`; the wargame walk is
`inception/WALK_ORDER.md`.

A Session 0 runs five phases. Here they are, with what AutoWatt did in
each.

### Phase A: the interview and its challenges

The agent fills the venture brief from the operator's own words, then
must pass three mandatory challenge steps before the brief is accepted.
This is anti-sycophancy built into the process.

1. **Restate and be corrected.** The agent restates the venture; the
   operator corrects until it is right. AutoWatt's restatement stood
   after one correction round, with the founder's vocabulary made
   canonical.
2. **Name the three cheapest deaths.** Not the most dramatic failure
   modes, the cheapest. AutoWatt's were recorded verbatim: miss the
   acceptance walk-through and lose trust; breach the live legal
   complaints duty at launch; starve the website of its content.
3. **Propose the strictly smaller version.** The agent argues for a
   smaller scope than asked; the operator adopts or rejects it in their
   own words. AutoWatt's smaller version was superseded by the Heads of
   Terms, which fenced Oversight into the MVP.

### Phase B: scale and shape

The operator and agent walk `WG-EOS-001` and rule the scale. AutoWatt
fired all six triggers (money, personal data, auth and state, ops
burden, a second human, a multi-year lifespan), so it ruled **L**, and
that was argued, not inherited. They walk `WG-EOS-002` and rule the
repo shape: a monorepo, because three surfaces (api, app, website) ship
together under one contract.

### Phase C: the wargame walk

Now the agent compiles the venture's wargame walk from the index,
filtered to the domains its triggers touch, and rules each one into the
lock-book. AutoWatt walked seventeen wargames and recorded seventeen
rulings, nine of them argued. The rulings header in `docs/LOCKBOOK.md`
is machine-readable, one line each. The instructive ones:

- `WG-WEB-001` was **argued to B**, against the framework's dark-first
  default. The reasoning: AutoWatt is a print-native institutional
  brand whose one physical object is an etched metal plate. An
  insurer-facing registry has no business glowing. This is the system
  working at its best: the default held until a venture's facts argued
  it aside, and that argued ruling is now promotion evidence on the
  wargame.
- `WG-VOX-001` was argued to professional-calm, fitting a trust
  product.
- Eight wargames were **inherited**: their triggers were silent for
  AutoWatt, so it took the default without ceremony, and those rulings
  count for nothing in promotion. That is correct and honest.

> [!TIP]
> The argued-versus-inherited split is easiest to grasp here. Nine
> times AutoWatt had a real reason and reasoned to it; eight times it
> had no reason to depart and did not pretend to. The lock-book records
> both truthfully, and only the nine will ever move a rule.

### Phase D and E: compile and gate

Phase D compiles the seed (Chapter 11 covers this in detail) and Phase
E runs the gate: the auto rubric green, then the operator signs the
human items. One row is appended to the estate's `registry/PROJECTS.md`,
the single sanctioned cross-repo write.

## Chapter 11 · The compile in detail

**What you will learn:** what the compiler actually produced for
AutoWatt, and two real nuances that show the discipline under pressure.
The artefact is `docs/COMPILE_REPORT.md` in the AutoWatt repo.

The compile report is the proof that the seed was compiled, not
authored. Its heart is an **ancestry table**: one row per file, naming
its source. AutoWatt's has 23 rows. The categories tell the story:

- Most files trace to a kernel template with a count of slots filled.
- `CLAUDE.md` traces to `AGENTS.md` as a byte copy.
- The constitution's Part I (the product doctrine) was carried
  **verbatim** from AutoWatt's adopted original, because Part I is the
  venture's own law, not the kernel's. Parts II and III came from the
  kernel and were renumbered per part.
- Several pre-existing venture files (the product brief, the compliance
  registry, the two original ADRs, the Session 0 logs) were marked
  **preserved**: they gained front-matter and nothing else.

The report also records the distillations (venture-facing consequences
of argued rulings, condensed into the seed) and any deviations from the
scale matrix (none). Then it records the gate: `eos_check.py --seed`
returning **0 errors, 0 warnings** on the first full run, and the
sign-off block.

Two nuances are worth seeing, because they show what "discipline" means
in practice rather than in principle.

> [!NOTE]
> **The Garreth correction.** The seed carried the founder's name as
> "Gareth", one r. The Heads of Terms spelled it "Garreth". The repo
> was wrong, not the source. This surfaced under rubric item H2 (does
> the brief read true?) and was fixed in the current files, while the
> historical session logs kept the original spelling untouched. History
> is append-only; you correct forward, you do not rewrite the past.

> [!WARNING]
> **The mangled front-matter.** When Daniel signed the rubric in his
> editor, an autoformat quietly broke the compile report's YAML
> front-matter in the same save. The signature was his intent; the
> reflow was the tool's accident. The fix restored the valid committed
> structure and re-applied the signature, recording both facts in the
> sign-off block. The lesson: trust the committed structure over an
> editor's helpfulness, and record what you did and why.

Once signed, the reseed branch fast-forward merged to a single `main`,
and AutoWatt was a signed, seeded, single-branch organisation ready to
build.

## Chapter 12 · What Genesis produced

**What you will learn:** the difference between a seeded organisation
and a buildable one, and everything the Genesis run generated to bridge
that gap. The procedure is playbook PB-001; the output lives across
AutoWatt's `org/product/`, `org/decisions/`, `org/standards/` and
`org/work/`.

A seed is an empty, correct organisation. **Genesis** is the one-off
PLAN session that turns it into a complete, buildable one. It needs no
credentials, because it produces design and plans, not running code.
For AutoWatt, Genesis produced:

- **The product design set** in `org/product/`: a `DOMAIN_MODEL.md`
  (the entities and their invariants, and an eighteen-type event
  registry), an `ARCHITECTURE.md` (three container services, hexagonal
  layering, the authorisation choke point, the ports table), a
  `ROADMAP.md` (the four horizons from MVP to a two-year data moat, and
  the founder-input deadlines), a `BRAND.md`, and a
  `database/schema/SCHEMA.md`.
- **Three new ADRs** capturing the judgement calls: ADR-0003
  (local-first development with verified fakes), ADR-0004 (the API
  architecture and the Grant choke point), ADR-0005 (the evidence
  pipeline). These join the two that predated Genesis.
- **Five standards** in `org/standards/` (engineering, testing, API,
  security, data), each naming what enforces it.
- **Nine specifications**, SPEC-001 to SPEC-009, each with Given-When-
  Then behaviour, and each mapped to a step of the §A5 acceptance
  walk-through.
- **A 44-order backlog** in `org/work/items/`, ordered foundation-first
  in `org/work/NEXT.md`. Twenty-four are build orders; twenty are
  COMPLY orders, one per gap in the compliance registry.

> [!IMPORTANT]
> The acceptance walk-through, §A5, is the spine of the whole build.
> Genesis encoded it as a suite of tests written to fail from the
> start. A journey's tests go green only when that journey genuinely
> works end to end. This is the definition of done for the MVP, and it
> is a test the founder can run himself, not a feature list to take on
> trust.

### The compliance sweep

AutoWatt processes regulated UK data, so it carried a compliance
add-on: the registry `REG-COMP-UK-001.md`. Genesis turned every gap or
partial row in that registry into its own COMPLY work order. One of
them, OBL-030, the statutory data-protection complaints route, is a
live legal duty already in force, so it is a P0. Nobody can slip a
legal obligation, because each one is a tracked order with a
verification.

## Chapter 13 · Nuances and lessons

**What you will learn:** three things the genesis showed about how the
system behaves under real use, which you will not get from the
reference files.

**The feedback loop fires fast.** During the reseed, the compiler hit
two rough edges and banked them in the venture's `docs/EOS_FEEDBACK.md`:
a constitution template that hardcoded "amendment history: none" where
a reseeded venture has real history, and the WG-WEB-001 ruling worth
counting. Both were harvested the **same day** and changed the kernel:
the template gained a slot, and the wargame gained AutoWatt's argued
ruling. A venture that improves the framework on day one is the
compounding loop working exactly as designed.

**Sequencing defects are caught, not hidden.** Genesis is a large PLAN
session, and it made ordering mistakes. The first work order (the local
harness) was written with two acceptance boxes that actually needed the
second order's database schema to exist. Rather than fudge it, the
worker moved those boxes to the correct order with a note on both, and
recorded the Genesis sequencing defect openly. Getting it wrong and
correcting it in the open is the normal path, not a failure to hide.

**History keeps its errors.** You saw the Garreth correction in Chapter
11. The principle behind it is Part II Article 8: history is
append-only. The current files were corrected; the session logs that
recorded the original were left exactly as written. The estate would
rather carry an honest record of what happened than a tidy fiction.

> [!TIP]
> If you take one habit from Section 2, take this one: bank friction
> the moment it hurts. One line in the feedback file, dated, and the
> harvest will carry it home. The cost is trivial and the framework
> gets better within a cycle. AutoWatt changed the kernel twice on its
> first day precisely because someone wrote two sentences down.

Section 2 ended with AutoWatt buildable. Section 3 builds it.

---

# Section 3 · The development lifecycle

This section is the day-to-day: how a buildable venture becomes shipped
software, one verified change at a time. It follows AutoWatt's first
real work order in full detail, then shows the road ahead and how a
venture is operated over its life. Where Section 1 explained the
execution half and Section 2 set it up, Section 3 runs it.

## Chapter 14 · The delivery loop

**What you will learn:** the rhythm of building, and why it is shaped
the way it is. The reference is the venture's `org/OPERATING_MODEL.md`
and the role charters in `org/roles/`.

The loop is the three roles in sequence, over and over.

1. **PLAN** has already done its part at Genesis and does it again
   whenever the queue needs reshaping: it specs the work, writes the
   orders, and keeps `org/work/NEXT.md` ordered so the top item is
   always the right next thing.
2. **WORK** takes the top unblocked order, one at a time. It creates an
   isolated workspace (a git worktree on a short-lived branch), reads
   the order and everything it links, writes failing tests first where
   the type demands, implements to green, keeps commits small and
   citing the order, and runs the gates the tier requires.
3. **VERIFY** reviews the result in fresh context and returns a
   verdict. On approval, T2 work merges; higher tiers wait for human
   approval.

> [!NOTE]
> **Architecture note.** One item per session, in its own worktree, is
> not bureaucracy. It is what lets many workers run at once without
> stepping on each other, and it is what makes each change small enough
> to review honestly. The isolation comes from worktrees and path
> claims, never from lock files in a shared tree, because lock files go
> stale the moment a session crashes. The unit of work is deliberately
> small so that the unit of review can be thorough.

The work-in-progress limit is low on purpose (two concurrent workers at
most, to start), because the bottleneck is never how many agents you
can spawn. It is how much you can verify and merge without lowering the
bar. Scale is limited by verification bandwidth, and the system is
honest about that.

## Chapter 15 · Local-first setup

**What you will learn:** how to build and test the entire product on
your own machine, with no cloud accounts, and why that choice is a
force multiplier rather than a compromise. The canonical decision is
AutoWatt's `org/decisions/ADR-0003-local-first-development.md`.

AutoWatt's production stack is AWS and Clerk, and those credentials
arrive a week or two into the sprint. The venture cannot afford to wait
for them, so its architecture is designed so that not a single line of
application code cares whether it is running locally or in the cloud.
The trick is to sort every external dependency into one of two kinds.

- **Config-only boundaries** run the same adapter code in both worlds,
  changing only an environment value. Token verification points at a
  local issuer now and at Clerk later; blob storage points at a local
  MinIO now and at S3 later; the database points at a local Postgres
  now and at RDS later. Local runs the real adapter against a
  protocol-faithful server, never a hand-rolled fake.
- **Code ports** are the few places where local and production genuinely
  differ (sending email, reporting errors, the clock and id generators
  the tests need to freeze). These have a small interface and swappable
  implementations.

> [!TIP]
> The whole platform stands up with one command:
> `python ops/local/full_local_deploy.py`. It brings up Postgres,
> MinIO, Mailpit and a local token issuer, runs the migrations, loads
> golden seed data with three role logins, and health-checks the lot.
> What passes locally is what ships, because the same production
> container images run under the harness too.

The payoff comes at cutover. Because the boundaries are config-only,
the expected application-code change when the real credentials arrive
is zero on the backend and a single environment flag on the frontend.
The cutover checklists are written in week one, so the credential week
becomes a checklist to work through, not an integration crisis to
survive.

## Chapter 16 · A work order start to finish

**What you will learn:** the complete loop, on one real order, with
nothing smoothed over. This is the chapter to read if you learn best by
watching. The order is AutoWatt's WO-0001, the local harness itself,
and its record is `org/work/items/WO-0001-local-harness.md`.

Here is what actually happened, in order.

1. **Take the order.** A WORK session took WO-0001 from the top of
   `NEXT.md`, set it in progress, and created a worktree on a branch
   called `work/WO-0001`. It read the order and wrote a short execution
   plan into the order's notes.

2. **Verify the environment first.** Before building, it checked the
   toolchain: Docker running, the versions it needed present. This is
   the WORK charter's opening move, not an afterthought.

3. **Build.** It wrote the docker-compose harness (Postgres, MinIO with
   a stale-upload rule, Mailpit, and an RS256 token issuer with a
   committed key deliberately labelled a non-secret), the one-command
   bring-up script, a token minter for the three roles, and a webhook
   simulator. It proved the harness came up green from cold, twice, and
   that the pieces worked.

4. **Hit real problems, and record them.** Three things went wrong and
   were fixed in the open. A script named `token.py` shadowed a Python
   standard-library module and broke any script run from that folder,
   so it was renamed. The bucket-init container broke the compose
   wait-for-healthy logic, so it was moved behind a profile and run
   explicitly. The MinIO image shipped no curl, so liveness was probed
   from the host instead. Each was noted on the order.

5. **Submit to VERIFY, and get rejected.** A separate session, in fresh
   context, reviewed the change. It ran everything from cold itself, and
   went further than the author had: it tamper-tested the tokens and
   negative-controlled the webhook verifier. The harness was sound, but
   the reviewer found four real defects the author had shipped past
   himself, including a compiled cache file accidentally tracked in git
   and the repository having no `.gitignore` at all. Verdict: **reject**,
   with each finding named and evidenced.

6. **Fix the findings, do not argue them.** The author fixed all four,
   plus the fixable observations, and resubmitted. This is the
   three-strikes discipline in its healthy, everyday form: the check
   was right, so the work changed to satisfy it.

7. **Pass on the second round.** The reviewer re-checked the amended
   change against its own findings, confirmed each with evidence, and
   approved. Being a T2 change, it merged, squashed onto `main`, and the
   worktree and branch were retired.

8. **The deterministic gate catches the last one.** After the merge,
   the seed check found one more defect that two rounds of human review
   had missed: a README file with no front-matter. It was fixed in a
   final commit.

> [!IMPORTANT]
> Read step 5 again. The reject is not the system failing; it is the
> system working. A fresh-context reviewer caught defects the author
> genuinely could not see, precisely because it did not share the
> author's context or assumptions. Independent verification is the
> single most valuable habit in the whole loop, and it only works when
> the reviewer starts clean.

> [!NOTE]
> **Architecture note.** Notice the layering of defence. The author's
> own checks, then an independent human-judgement review, then a
> deterministic mechanical gate, each caught something the layer before
> it missed. No single layer is trusted to be complete. That is why the
> system holds up over time: the layers cover each other's blind spots.

The whole episode is written up in the session log
`org/logs/2026-07/S-0004-WORK.md`, and the verdicts are recorded on the
order itself. A stranger can reconstruct exactly what happened and why,
from the files alone.

## Chapter 17 · The road ahead for AutoWatt

**What you will learn:** how the rest of the build is sequenced, so you
can see where any given order fits. The plan is `org/work/NEXT.md`.

The backlog is ordered in lanes.

- **Week-one foundation**, all credential-free by design: the harness
  (done), the database schema, the API skeleton with its authorisation
  choke point, the failing acceptance suite, the evidence pipeline, the
  CI gates, and the app and website shells. This is the substrate
  everything else builds on.
- **The feature spine**, weeks two to five: the nine specifications
  turned into working journeys, in dependency order. The P0 legal duty
  (the complaints route) lands as early as its dependencies allow.
- **The cloud lane**, opening when the AWS account and budget are
  approved: the AWS baseline, the Clerk cutover, the S3 cutover, and
  staging end-to-end. These are safe to run in parallel because their
  file claims do not overlap the feature work.
- **The finish**, weeks five to six: hardening with a proven backup
  restore, and the handover documentation.

Threaded through all of it, the COMPLY orders close as their evidence
becomes real, and the §A5 acceptance journeys flip from failing to
passing one by one until the founder can run the whole walk-through
himself.

> [!TIP]
> To continue the build in a fresh session, you do not need this guide.
> You copy the L3-WORK launcher from AutoWatt's `OPERATORS_GUIDE.md`,
> which tells a WORK session to take the top unblocked item from
> `NEXT.md` and follow its charter. The launchers are tiny and stable
> on purpose; all the evolving detail lives in the files they point to.

## Chapter 18 · Operating a venture over time

**What you will learn:** what happens after the first build, when a
venture becomes a running concern. The reference is the venture's
`org/CADENCE.md` and the estate's `org/PLAYBOOKS.md`.

A venture is not just built, it is operated, and the operating is
mechanised as recurring sessions.

- **Weekly**, PLAN triages the queue and writes the stakeholder update
  (built, blocked, changed, next), and VERIFY clears the review queue.
- **Fortnightly**, a rotating practice audit samples the running system
  for drift between the docs and reality.
- **Monthly**, the compliance watch checks the regulator for change,
  knowledge is promoted up its ladder, and the retrospective improves
  the procedures themselves.
- **From the first production deploy**, a monthly restore test proves
  the backups actually restore, because a backup never exercised is a
  rumour.

Two of these loops reach back to the framework itself.

- **Harvest** (playbook PB-E02) is the estate pulling each venture's
  `docs/EOS_FEEDBACK.md` monthly, folding rulings into the wargames they
  answer and landing lessons in the registry. This is how one venture's
  hard-won lesson becomes every future venture's default.
- **Upgrade** (PB-E06) is the only sanctioned way a venture moves its
  EOS pin forward: by diffing the changelog between its pin and the
  target and applying what matters. Ventures never drift onto a new
  version by accident.

And when a venture's own nature changes (money arrives, personal data
appears, a second person joins), **rescale** (PB-E08) re-runs the scale
wargame and compiles the delta, so the ceremony grows to match the new
reality rather than being wrong in either direction.

> [!NOTE]
> **Architecture note.** The four horizons in AutoWatt's roadmap (MVP,
> then six months, one year, two years) are not just a plan, they are a
> reminder of why the discipline is worth it. The decisions made in
> week one, one asset to one immutable record, requirements held as
> data, equipment structured so any manufacturer fits, are what make
> the two-year data moat possible at all. You do not bolt integrity on
> at the end. You seed it at the start, which is the whole reason to
> build this way.

That is the lifecycle: born from the framework in Section 2, built
through the loop in Section 3, and operated by cadences that keep it
honest and feed its lessons back home. You now have the whole arc.

---

# Glossary

Terms are listed as they first matter. Where a term has a canonical
file, it is named.

- **ADR (Architecture Decision Record).** A dated record of a decision
  that closes a door: the options, why each lost, the consequences
  accepted. Immutable once accepted. Template in
  `doctrine/architecture/templates/ADR_TEMPLATE.md`.
- **Argued ruling.** A wargame ruling reached by engaging the triggers
  afresh. The only kind that counts as promotion evidence. Contrast
  inherited.
- **Cadence.** A recurring session (weekly, monthly, quarterly) that
  keeps a venture or the EOS honest. Defined in `CADENCE.md`.
- **Compile.** Turning kernel templates into a venture's seed by
  pruning fences and filling slots. Rules in `inception/COMPILE.md`.
- **Doctrine.** Binding, argued rules in a knowledge module. Contrast a
  wargame default, which is one step below doctrine.
- **Gate (G1 to G5).** A checkpoint a change passes: automated checks,
  independent review, human approval, post-release checks, periodic
  audit.
- **Genesis.** The one-off PLAN session (playbook PB-001) that turns a
  seeded organisation into a buildable one.
- **Inherited ruling.** A wargame ruling that took the default without
  new argument. Legitimate when triggers are silent; never promotion
  evidence.
- **Lock-book.** A venture's contract with the EOS: its scale, stack,
  pinned version, and rulings. Lives at `docs/LOCKBOOK.md` in a venture.
- **Playbook.** A versioned procedure for a category of session.
  EOS-side ones (PB-E01 to PB-E09) in `org/PLAYBOOKS.md`; venture-side
  ones compiled from the kernel catalogue.
- **Protected set.** The files that cannot change without an accepted
  ADR and human approval. Listed in `GOVERNANCE.md`.
- **Rescale.** Re-running the scale wargame when a venture's triggers
  change (playbook PB-E08).
- **Resume Packet.** The fixed-key block at the foot of a `STATE.md`
  that lets a cold session continue from the files alone.
- **Risk tier (T1 to T4).** How much ceremony one change carries, from
  trivial to constitutional.
- **Scale (S, M, L).** How much organisation a venture compiles, ruled
  by `WG-EOS-001`. Exact file lists in `kernel/SCALE_MATRIX.md`.
- **Seed.** The compiled set of files a venture starts life with.
- **Three-strikes rule.** Stop after three distinct failed fix attempts
  on the same check; record, block, flag, ask. Never weaken the check.
- **Wargame.** A pre-solved decision procedure. Format in
  `doctrine/web-design/templates/WG_TEMPLATE.md`; all of them indexed in
  `doctrine/WARGAME_INDEX.md`.
- **§A5 walk-through.** AutoWatt's acceptance test: the end-to-end
  journey the founder runs himself to call the MVP done.

# Cross-reference: the canonical files

The guide teaches; these files are the source of truth. When you need
the exhaustive, current detail on a topic, open its file.

| Topic | Canonical file |
| --- | --- |
| Entry modes and the never-list | `AGENTS.md`, `START.md` |
| The law of the system | `GOVERNANCE.md` |
| The human operator's manual | `OPERATORS_GUIDE.md` |
| Every file, one row, greppable | `INDEX.md` |
| Every wargame, one row | `doctrine/WARGAME_INDEX.md` |
| The compile contract and scale | `kernel/README.md`, `kernel/SCALE_MATRIX.md` |
| The compile steps | `inception/COMPILE.md`, `inception/WALK_ORDER.md` |
| The seed gate | `kernel/SEED_RUBRIC.md` |
| The Session 0 procedure | `inception/INCEPTION.md`, `inception/INTERVIEW.md` |
| A module's rules and wargames | `doctrine/<module>/DOCTRINE.md` and `wargames/` |
| The check tool | `tools/eos_check.py` |
| The founding argument | `org/decisions/ADR-0001-eos-v1-architecture.md` |
| The EOS's own live state | `org/STATE.md`, `org/QUEUE.md` |
| The EOS's procedures | `org/PLAYBOOKS.md` |
| The condensed AutoWatt example | `examples/autowatt-seed.md` |
| The venture directory | `registry/PROJECTS.md` |

For AutoWatt's own files (its constitution, domain model, ADRs,
standards, specs, work orders and session logs), open the AutoWatt
repository named in `registry/PROJECTS.md`. Section 2 and Section 3 of
this guide name the specific files as they come up.
