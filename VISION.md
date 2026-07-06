# Vision: framework any project

This repo exists to become the kernel that can framework **any** project we
take on, end to end. Not just how it looks, but how it is architected, how it
deploys, what it costs, what it runs on, and how the work itself is organised.
This file records that intent so the next agent inherits the full context
without Daniel repeating it.

## The plan of record

1. **Module 01, web design, is built first** (this repo, populated). It
   extracts the web design, UI/UX and branding approach proven on the
   PatterTech website: the doctrine, the derivation methods, the reusable
   patterns, and the wargames for every fork we met along the way. PatterTech
   is deliberately kept as a worked example rather than baked into the rules:
   the rules are agnostic, the example shows one strong instantiation.
2. **A follow-up agent generalises the kernel.** After this module is in use,
   a new agent (Daniel will brief it; this file is its standing context) will
   extract EVERYTHING learned from the **Venture A seed-pack creation**, with
   influence from the **WiseWattage** project, and grow this framework to
   cover absolutely everything a project needs decided:
   - design guidelines (this module, already present)
   - architecture and system design decisions
   - devops and deployment decisions
   - cost efficiencies and budget trade-offs
   - hardware choices and sizing
   - and any other pathway a project can take.
   The method is the same everywhere: **wargame every viable pathway.** For
   most questions there is no single right answer until you know what it
   depends on, so the framework's job is to capture the triggers, the options,
   the trade-offs and a decision rule, then record each project's ruling.
3. **Every project extends the framework.** As we move from project to
   project we append worked rulings, promote repeated rulings into defaults,
   and promote hardened defaults into doctrine. The framework grows with our
   experience instead of each project starting over.

## Extraction sources for the next agent

Read these before generalising:

- `C:\Users\Daniel\Documents\Coding\Github\Venture A\org\` : the file-based org
  kernel (START, CONSTITUTION, OPERATING_MODEL, ADRs, guidance docs with a
  knowledge lifecycle and review dates, registries, role charters, work
  orders). Its operating model, doc lifecycle and "a stranger must be able to
  continue from files alone" rule are the organisational spine to reuse.
- The **Venture A seed pack** work itself: the process and lessons of creating
  it are the primary extraction target for the all-project kernel.
- `C:\Users\Daniel\Documents\Coding\Github\WiseWattage` (and its deployment
  history): the influence source for architecture, devops, cost and hardware
  wargames grounded in a real, live product.
- `C:\Users\Daniel\Documents\Coding\Github\PatterTech_Website` and
  `PatterTech_Business\platform\docs\`: the design, voice and chart standards
  this module distilled, and the worked example of applying them.
- This repo's `modules/web-design/`: the template for what a finished module
  looks like (doctrine -> foundations -> patterns -> wargames -> templates ->
  worked example). New modules should follow this shape unless a wargame says
  otherwise.

## What must stay true as the kernel grows

- **Agnostic core, locked-in projects.** Framework docs never assume one
  brand, stack or client; each project freezes its choices in its own lock-in
  file. If a rule only makes sense for PatterTech, it belongs in a worked
  ruling or the example, not in doctrine.
- **Wargames before doctrine.** A rule earns its place by surviving the
  argument, not by being written confidently.
- **Files over memory.** Everything an agent needs is in the repos. Session
  memory is a convenience, never the source of truth.
- **Review dates.** Time-sensitive claims carry a `review_by`; stale guidance
  is a bug.
- **Lean.** Capture the main concepts and decision structure; do not bloat
  modules with restatements of common knowledge. The framework should stay
  fast to read and easy to extend.
