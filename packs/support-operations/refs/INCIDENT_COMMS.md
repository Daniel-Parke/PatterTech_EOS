---
summary: The customer-facing update contract, the honesty rules including bypassed checks, audiences, cadence and the communication log shape
kind: fact
scope: estate
sources: [EV-0122, EV-0200]
volatility: slow
review: 2027-08
type: implementation
tags: [ops, voice, delivery]
---

# Incident communication

Reference for PACK.md B3 and B4. Communication during a customer-visible
incident is a job with an owner, and the owner is not the person
changing the system.

## The honesty rules

These are the whole point of the file. They mirror the kernel rule that
a bypassed gate is recorded as bypassed and that no emergency overlay
lowers a floor (`kernel/GUARD_SPEC.md`).

1. **A bypassed check is never reported as passing.** If a gate was
   skipped, waived, or run under an emergency route to get the fix out,
   the incident record and every customer-facing message that follows
   say so in those words.
2. **An all-clear names what was verified and how.** "Resolved" on its
   own is a claim with no evidence behind it. If the usual verification
   did not run, the message says the fix is live and unverified, and
   says when verification will follow.
3. **No message asserts a cause the record does not support.** "Cause
   unknown" and "not yet verified" are legal things to publish, and
   they age better than a guess.
4. **Nothing is quietly corrected.** A later update that changes an
   earlier claim says that it changes it.
5. **Severity is not revised downwards after the fact to make the
   record look calmer.** The argument about the band goes in the
   postmortem (PACK.md B2).

The reassuring all-clear is the failure these prevent. It is common
because it feels kind at the moment it is written, and it costs
everything the second time it turns out to be wrong.

## Audiences

Every entry in the log names its audience, because the same fact is a
different message to each:

| Audience | What they need |
| --- | --- |
| affected customers | what is broken, what to do meanwhile, when the next update comes |
| all customers | whether this affects them, in one sentence |
| internal | current state, who owns what, what is unverified |
| the record | timestamps, decisions, and what was not checked |

## Cadence and the log

At least three entries per customer-visible incident: one at
declaration, one while it is open, one at resolution. Timestamps
strictly increase. The first entry lands before the incident is
resolved, which is the whole distinction between telling people and
issuing a report afterwards.

Each entry carries: timestamp, audience, the message sent, and the
channel. Where the product surfaces machine-readable error identifiers,
quoting the identifier lets a customer match what they saw to what is
being said (EV-0122).

If the next update slips, the slip is itself an update. "Still working,
nothing new, next update at half past" is a real message and takes
thirty seconds.

## Handover

Command and communication ownership transfer by explicit statement with
acknowledgement, recorded in the log. A handover nobody acknowledged
did not happen.

## After

`postmortem_due` is set at resolution with a named owner (PACK.md D9,
EV-0200). Anything published from the postmortem carries ids rather
than customer names (PACK.md B6).
