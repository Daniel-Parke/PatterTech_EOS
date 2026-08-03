---
summary: Bootstrap for every session, read order per entry mode and the ground rules
type: root
tags: [eos]
status: archived
---

# START

The bootstrap for any agent or person working with the EOS. Read this
first, every time. AGENTS.md told you your entry mode; this file tells
you what to read for it.

## Read order by entry mode

**Mode 1, working on a venture:**

1. The venture's lock-book (in the venture repo). It wins on specifics.
2. The doctrine and stack profiles its rulings cite, found via `INDEX.md`.
3. If you hit a fork the lock-book does not answer: find the wargame in
   `doctrine/WARGAME_INDEX.md`, apply its decision rule, record the
   ruling in the lock-book (marked argued or inherited). No wargame
   covers it: draft one in the venture's `docs/EOS_FEEDBACK.md` with
   your ruling as its first worked entry, then carry on.

**Mode 2, working on the EOS itself:**

1. `org/STATE.md`: where the build is, and whether another session is
   active. If `active_session` is set and fresh, stop and tell Daniel.
2. `org/QUEUE.md`: take the top unblocked item.
3. `org/PLAYBOOKS.md`: follow the playbook the item names.
4. `GOVERNANCE.md` before touching anything in the protected set.

**Mode 3, Session 0 for a new venture:**

1. `inception/INCEPTION.md` and run its phases in order.

## Ground rules

- **Files over memory.** If it is not written down, it is not decided.
  Write down what you decide.
- **A stranger must be able to continue from files alone.** Never leave
  a decision only in a conversation.
- **Wargame first, doctrine later.** To change a rule, first write or
  extend the wargame that argues it. Doctrine edits without a wargame
  are reverted on sight.
- **Check currency.** Time-sensitive files carry `review_by` dates. Past
  the date, verify before relying.
- **Three strikes.** If the same check or gate fails after three distinct
  fix attempts, stop. Record the attempts and your hypotheses, block the
  item, flag it in the relevant STATE file, and file a question if a
  human decision is needed. Never weaken a check to pass it.
- **Close out properly.** Update the state file you own, write the
  session log, and leave a Resume Packet a cold session can boot from.
- **Voice.** Plain, spoken, British spelling, no em-dashes, no
  exclamation marks, no AI clichés, no two-fragment antithesis.
