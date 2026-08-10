---
summary: Research synthesis for the marketing-growth pack, four growth philosophies, the measurement floor, and what is law versus taste
type: example
tags: [eos, testing]
---

# marketing-growth research synthesis (cutoff 2026-08-03)

Purpose: let the pack produce marketing work without smuggling in one
growth religion as the default, while holding a compliance and
measurement floor that does not vary. Most of what marketing calls best
practice is convention. A small part of it is law, and a smaller part
still is measured. The pack has to keep those three apart.

## The floor that does not vary

1. **Consent provenance travels with the address.** PECR regulation 22
   (FRAG-MKTG-09) needs prior consent for marketing mail to an
   individual, with one narrow soft opt-in escape that requires all
   three of a prior sale or negotiation, similar products only, and a
   free refusal route at collection and in every message. You cannot
   reconstruct that later, so the lawful basis is a stored field on the
   contact, not a policy page. The Data (Use and Access) Act 2025
   (EV-0225) has already amended the regulation once, so this is a
   moving target with a named watch.
2. **Deliverability is a preflight gate, not a craft.** Gmail's sender
   guidelines (FRAG-MKTG-08) give numbers: SPF or DKIM for everyone,
   valid forward and reverse DNS, TLS, spam rate under 0.30 per cent,
   and above five thousand messages a day SPF and DKIM and DMARC plus
   From alignment and RFC 8058 one-click unsubscribe. RFC 8058
   (FRAG-MKTG-07) fixes the mechanics: HTTPS URI, List-Unsubscribe-Post,
   both DKIM-covered, no cookies, no confirmation page, an opaque
   hard-to-forge token the server validates. Every one of those is
   machine-assertable before a first send.
3. **Markup describes what a reader can see.** Google's structured data
   guidelines (FRAG-MKTG-03) are unusually clean: match visible content,
   do not block the crawler, and the penalty for breach is loss of
   rich-result eligibility rather than a ranking hit. Bounded blast
   radius plus a testable rule is the rare combination worth making
   binding. Schema.org itself (EV-0022) supplies the versioned
   vocabulary underneath.
4. **robots.txt is a release-gated artefact.** RFC 9309 (FRAG-MKTG-06)
   says a 5xx on robots.txt means the crawler must assume complete
   disallow, and that the protocol is not a security measure. A botched
   deploy is therefore a self-inflicted deindexing incident, and the
   file belongs in the release pipeline, not in a marketing console.
5. **A causal claim needs a holdout or a label.** Gordon and colleagues
   (FRAG-MKTG-10) ran fifteen randomised experiments at Facebook across
   about 500 million user-experiment observations and could not
   reproduce the experimental effects from observational estimators on
   the same, far richer, data. If the platform with the best data in the
   world cannot do it, a dashboard cannot. Any number not produced by a
   randomised holdout is reported as a bookkeeping convention.

## Four philosophies and when each fits

**Compounding organic asset.** Google Search Central (FRAG-MKTG-01,
FRAG-MKTG-04) plus PostHog's public marketing handbook (FRAG-MKTG-14,
EV-0095). Fits when the buyer already searches, the category has a
reading habit, and you can outlast a twelve-month payback. Signature
moves: publish in the open, take a stance rather than hedge, treat docs
and content as the same artefact, edit on encounter. Trade-off: slow,
and it produces nothing for a category whose buyers do not read.
Anti-pattern: volume as strategy. Google's spam policies (FRAG-MKTG-02)
name scaled content abuse and site reputation abuse precisely because
agents make volume cheap, and the test is purpose, not production
method, so a machine-written page with a real owner and a real reader is
fine while a hundred generated pages with neither are not.

**Reach-led brand building.** Ehrenberg-Bass (FRAG-MKTG-16) and Binet
and Field (FRAG-MKTG-17). Fits repeat-purchase categories, mass markets,
and anywhere most buyers are light buyers who are not in market today.
Signature moves: buy penetration among category non-buyers, budget by
time horizon rather than by blended ROI, accept that loyalty is largely
a consequence of size rather than a lever that creates it. Trade-off: it
needs money and patience, and the effect is invisible in a
weekly dashboard. Anti-pattern: a retention-first plan for a small
brand, which the double jeopardy evidence says is close to backwards.
Honest caveat: neither primary text was readable at this cutoff, so both
records are directional.

**Growth loops.** Balfour and colleagues (FRAG-MKTG-13). Fits products
where usage itself produces the next user, through content, invitation,
or public artefacts. Signature move: name the reinvestment step, the
point where output re-enters input. Trade-off: the essay is a
practitioner argument with no data, and it is a consultancy positioning
its own curriculum, so it earns the status of a useful question, not a
finding. Anti-pattern: calling a paid-acquisition budget a loop because
it has an arrow drawn back to the start. The usable rule survives the
weak evidence: a growth plan with no reinvestment step is a spending
plan, and should be described as one.

**Lifecycle and owned channel.** FRAG-MKTG-07, FRAG-MKTG-08,
FRAG-MKTG-09. Fits considered purchases with a gap between interest and
readiness, and any business that would be destroyed by losing a platform
account. Signature moves: consent captured with provenance, suppression
honoured mechanically, sending reputation treated as a production SLO.
Trade-off: the compliance surface is real and jurisdictional. Nothing in
the UK rules transfers to the US CAN-SPAM opt-out regime, so a single
global consent rule is wrong somewhere by construction.

## Where the sources actually disagree

- **Acquisition versus the installed base.** Ehrenberg-Bass
  (FRAG-MKTG-16) puts acquisition at roughly twice the weight of
  retention and points marketing at people who have never bought. Loops
  (FRAG-MKTG-13) put the engine inside the existing user base. These are
  not quite the same axis, but they pull budget in opposite directions,
  and their evidence bases barely overlap: repeat-purchase consumer
  panels on one side, software anecdote on the other. The pack should
  make the venture declare which world it is in rather than pick for it.
- **Whether measurement can be bought.** Google ships data-driven
  attribution as the GA4 default (FRAG-MKTG-12) while having deleted
  first-click, linear, time-decay and position-based models in November
  2023, an implicit admission that the heuristics were arbitrary.
  Gordon (FRAG-MKTG-10) says the whole observational family fails
  against experiment. Amazon's own paper (FRAG-MKTG-11) splits the
  difference and calibrates a model to randomised anchors. The
  reconcilable reading: attribution distributes an experimentally
  measured total, it never produces one.
- **The evidence under the 60:40 split.** Binet and Field's arithmetic
  rests on award-case ROI figures, which are observational, which is
  exactly the class Gordon found unreliable. The split may still be
  directionally right, but it is not measured in the way it is usually
  quoted.
- **Optimising for AI answers.** Google states plainly that no new file,
  markup or optimisation is needed for AI Overviews or AI Mode
  (FRAG-MKTG-05). A live counter-practice, llms.txt, is being adopted
  anyway. Google has a commercial interest in the denial, and the
  counter-practice has no measurement behind it. Genuine open question.

## Binding, default, preference

**Binding.** Lawful basis and consent provenance stored per contact.
RFC 8058 one-click unsubscribe with a validated opaque token. The Gmail
preflight numbers before any bulk send. Structured data matches visible
content. robots.txt changes go through the release pipeline. Every
published page has a named human owner and a stated purpose. No causal
claim without a holdout or an explicit unverified label.

**Default.** Experiment-first measurement, with every funnel definition
stored as configuration beside its number, because the same product
yields different conversion rates under sequential, strict and any-order
steps (FRAG-MKTG-15). Reach-led acquisition for a small brand. A named
reinvestment step in any growth plan. Time horizon declared per
activity. Core Web Vitals treated as a business measure rather than a
vanity one (EV-0241, EV-0060). Guardrail metrics that block only on
significant harm, borrowed from experiment practice (EV-0059).

**Preference.** Channel mix. Paid or not. Pull versus push. Tone,
format, cadence, and whether the handbook is public in the GitLab
(EV-0055) or PostHog (EV-0095) style.

## Open questions, honestly

- No evidence was found on what marketing measurement a venture with no
  budget for a holdout should do. Every serious source assumes an
  experiment programme.
- Positioning and messaging method has no primary evidence base in this
  set at all. The well-known works are books behind copyright and the
  research literature does not test them. This is currently taste, and
  the pack must say so rather than dress a framework as a finding.
- Whether agent-generated content at volume is detectably worse, rather
  than merely against policy, is unmeasured.
- Attribution under widespread consent refusal is undocumented by the
  vendors that model around it.

Refresh triggers: any revision of the Google Search Central pages named
above, a change to the Gmail sender requirements, an amendment to PECR
regulation 22, ICO guidance interpreting the Data (Use and Access) Act
2025, and the day the Reforge and IPA primary texts become readable.
