---
summary: The v2 intake protocol, eighteen questions, the risk-surface set and the three challenge steps
type: kernel
tags: [eos]
---

# INTERVIEW

Phase A of Session 0. The operator talks; the agent transcribes,
structures and challenges. Nothing here is invented: an unanswered
question is a recorded question, never a guess, and it lands in
docs/TASKS.md at S or org/QUESTIONS.md at ORG. One sitting where
possible. The output fills docs/VENTURE_BRIEF.md, the trigger list for
the pack walk, the risk-surface map phase B turns into policy, and the
list of material workstreams Genesis later cuts its work from.

## The venture set

Thirteen questions, asked in this order, following up until each
answer would satisfy a stranger.

1. What is it, in one paragraph, in your words?
2. Who is it for, and who pays (if anyone)?
3. Why now, and what agreement or deadline sits behind it?
4. How long should it live: a weekend, a quarter, years?
5. What surfaces exist: site, app, api, hardware, documents?
6. Does anything persist or log in (server state, auth)?
7. Does money change hands under this venture's name?
8. What may this venture spend, and who approves spend (hosting,
   tools, services)? A number or "nothing without me", never silence.
9. Does it touch personal or regulated data, anyone's?
10. What has to be deployed, monitored or backed up?
11. Who besides you holds any decision?
12. What does success look like in ninety days?
13. What is explicitly out of scope?

Question 8 is the one that goes missing, because a venture with nothing
to sell reads as a venture with nothing to spend. It carries real money
either way, so ask it even when the venture looks free to run. The
canned drill brief went without an answer to it until 2026-08-11.

Answers to 4 through 11 become the trigger list for WG-EOS-001 and the
pack walk. Vague answers on server state, money or personal data are
resolved now rather than later; they carry legal weight and they set
the policy.

## The risk-surface set

Five more questions, asked once the venture set has landed. The first
four become the path patterns in the venture's policy file at phase D,
so they need paths and not adjectives. The fifth names the work.

14. Where in the tree will each risky thing live: the money code, the
    auth code, the personal data, the deploy configuration? Directory
    names are enough; a venture with no code yet answers from its stack
    profile.
15. What must never change without you in the room?
16. What can be undone in a minute by anyone, without asking?
17. What can this venture reach outside itself (payment providers,
    email, hosting, an app store), and may an agent act there
    unattended?
18. What are the material workstreams: the parts of this venture that
    somebody has to sit down and build? A list, one line each, in the
    operator's own words. Not a plan and not an estimate.

Question 17 sets the guard posture. Until a validated adapter mapping
exists, the honest answer compiles as manual-only for every guarded
class, per kernel/GUARD_SPEC.md.

Question 18's list lands in the brief as its own short section, and it
is what inception/GENESIS.md cuts its research packets and work packages
from. Three to eight lines is the usual shape. A venture that cannot
name its workstreams is not ready for a blueprint, and saying so at the
interview is cheaper than finding out at Genesis.

## The challenge steps (mandatory, in order)

Anti-sycophancy by design. Session 0 does not proceed past any step
until it lands.

1. **Restate and be corrected.** The agent restates the venture in two
   or three sentences of its own words. The operator corrects until
   they say it is right. The final corrected restatement opens the
   brief.
2. **The three cheapest deaths.** The agent names the three cheapest
   ways the venture dies, the cheapest rather than the most dramatic.
   The operator amends or replaces them. They land in the brief
   verbatim; they are the risk register at birth.
3. **The strictly smaller version.** The agent proposes the smallest
   version that still serves the stated audience, smaller than the
   operator asked for. The operator explicitly adopts or rejects it and
   the verdict is recorded in their words. Adoption reshapes the brief;
   rejection with a reason is promotion-grade evidence that the scope
   is deliberate.

## Closing the interview

Read the trigger list back as plain yes-or-no facts, then the
risk-surface map back as paths, then the workstreams back as a list and
take a yes on each. Collect the concrete facts the compile
prints: the venture name as it appears in public, contact details for
any contact surface, the domain if one is owned, brand assets if any
exist. Confirm the operator's availability for phase B now and phase E
later. Then move to WG-EOS-001 with the triggers in hand.
