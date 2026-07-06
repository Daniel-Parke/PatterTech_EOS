# START

The bootstrap for any agent or person working with this framework. Read this
first, every time.

## Read order

1. `VISION.md` : what this repo is becoming and the standing mandate for the
   next generalisation pass.
2. The relevant module's `DOCTRINE.md` (for web work:
   `modules/web-design/DOCTRINE.md`). Doctrine is binding.
3. If you are working **on a project**: that project's lock-in file (copied
   from `templates/PROJECT_LOCKIN.md`, usually living in the project repo's
   docs). The lock-in wins on specifics; doctrine wins on principles.
4. If you are **making a decision** the lock-in does not cover: find the
   wargame (`modules/*/wargames/`), apply its decision rule, and record the
   ruling in the project lock-in (and append it to the wargame's worked
   rulings).
5. Foundations and patterns as needed while executing.

## Ground rules

- **Files over memory.** If it is not written down here or in the project's
  lock-in, it is not decided. Write down what you decide.
- **A stranger must be able to continue from files alone.** Borrowed from the
  AutoWatt org kernel, and it applies here: never leave a decision only in a
  conversation.
- **Wargame first, doctrine later.** To change a rule, first write or extend
  the wargame that argues it, then change the rule. Doctrine edits without a
  wargame are reverted on sight.
- **Check currency.** Wargames and time-sensitive guidance carry `review_by`
  dates. If a doc is past review, verify its claims before relying on them.
- **Projects feed back.** Each project appends worked rulings. Repeated
  rulings become defaults; hardened defaults become doctrine.
- **Voice.** Framework prose follows the same writing law as the projects:
  plain, spoken, British spelling, no em-dashes, no exclamation marks, no AI
  clichés, no two-fragment antithesis.

## Starting a new web project (the short version)

1. Copy `modules/web-design/templates/PROJECT_LOCKIN.md` into the new repo,
   and write the narrative brief first: it drives everything else.
2. Walk the wargames it cites (WG-001 register, WG-002 archetypes, WG-005
   light budget, WG-007 stack, WG-009 accents, WG-010 type, WG-011
   reactivity, WG-012 imagery) and fill in the rulings.
3. Derive the brand tokens with the foundations docs; stand up the styleguide
   page before any real page (it is the acceptance surface).
4. Build with the patterns; hold the QC gates
   (`modules/web-design/implementation/QC_GATES.md`).
5. When the project teaches you something, bring it back here.
