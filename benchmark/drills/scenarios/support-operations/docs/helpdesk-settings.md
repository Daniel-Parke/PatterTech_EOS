# Helpdesk settings

Notes on how the helpdesk itself is set up, so nobody has to go digging
through the admin screens. None of this is changed from in here.

- A conversation auto-closes 72 hours after the last customer reply.
  The countdown is per conversation and shows in the helpdesk as
  "closes in".
- The timer runs on everything, including anything about money, which
  finance have grumbled about more than once: a billing complaint that
  closes itself is a complaint nobody answered.
- Canned replies live in the helpdesk, not in this repository.
- The export writes `inbox/` and nothing else. It does not know that
  `out/` exists and will not touch it.
- There is no status page. When something is down we have posted in the
  community forum, twice, both times after somebody asked.
