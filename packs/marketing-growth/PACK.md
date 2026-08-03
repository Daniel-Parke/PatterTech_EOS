---
summary: How a venture reaches and keeps people, four growth philosophies over one consent, refusal and measurement floor
type: playbook
tags: [content, seo, pii, brand, voice]
kind: rule
authority: binding
lifecycle: active
basis: law
evidence_grade: observational
scope: estate
applies_when: [publishes_public_content, collects_contact_details, sends_marketing_message, reports_channel_effect, plans_growth_spend]
volatility: fast
review: on-change-of:PECR-reg-22-amendment
sources: [EV-0022, EV-0041, EV-0055, EV-0059, EV-0060, EV-0095, EV-0225, EV-0241]
---

# marketing-growth

This pack covers how a venture reaches people who are not yet customers
and keeps the ones it has: published pages, search discovery, lifecycle
mail, campaign planning and the numbers used to judge any of it. It
activates on any task that publishes public content, collects contact
details, sends a marketing message or reports a channel's effect.
Consent and refusal bind, because the law says so. Channel, tactic and
tone are chosen per venture and written down.

## Activation

**Paths.** Anything under a site, www, marketing, content, posts, blog,
landing, campaigns, lifecycle, emails or newsletters directory. Crawler
and discovery files, sitemaps, structured-data templates and page
metadata partials. Analytics, tag-manager, email-service-provider and
CRM configuration. Signup, contact and subscribe handlers and their
stores.

**Task types.** Launch or change a public surface. Publish or update
content. Plan or run a campaign. Build or change a lifecycle sequence.
Import or capture contact details. Set up or change analytics and
attribution. Report a channel's or a campaign's effect. Decide where
growth effort goes.

**Keywords, fallback only.** SEO, search, ranking, content, blog,
newsletter, subscriber, unsubscribe, opt-in, consent, campaign, funnel,
conversion, attribution, growth, acquisition, retention, brand, launch,
landing page. Keywords never override the predicates.

**Applicability predicates.**

| Predicate | True when |
| --- | --- |
| publishes_public_content | the task creates or changes something readable by people outside the venture |
| collects_contact_details | the task stores a way to reach an identifiable person |
| sends_marketing_message | the task sends or schedules an electronic message whose purpose is marketing |
| reports_channel_effect | the task produces a number crediting an outcome to a channel or campaign |
| plans_growth_spend | the task allocates money or effort across channels |

A task that trips a marketing path and satisfies no predicate loads
nothing beyond the first paragraph. Restyling a component under a site
directory is interface work and belongs to `packs/ui-ux/PACK.md`.

Activation gives advice, never permission. Nothing here lowers a tier
floor set by `kernel/POLICY_SPEC.md` or turns a manual-only action
class in `kernel/GUARD_SPEC.md` into an autonomous one. A bulk send, a
list import and a DNS change stay guarded whatever this pack says.

## Outcomes and non-goals

**Outcomes.** Every address the venture can mail carries a recorded
reason it is lawful to mail it. A person can stop the mail in one
action, and it stops. Every published page has a named owner and a
reason to exist. The venture can say which growth philosophy it runs
and why, instead of inheriting one from whoever wrote the last plan.
Any number offered as an effect is either measured against a holdout or
labelled as bookkeeping.

**Non-goals.** No house tone, palette, channel mix or content calendar.
Not pricing or packaging. Not the interface, which is
`packs/ui-ux/PACK.md`. Not data protection in general, which is
`packs/security-privacy/PACK.md`; this pack owns the marketing consent
surface only. Not product analytics instrumentation depth. Not
positioning or messaging method, which has no primary evidence in this
pack's source set and is stated as taste.

## Binding requirements

Three requirements bind. All three are law, or the standard by which a
legal duty is discharged. Everything else here is a default or a
preference, which is the honest shape for a domain where most published
practice is convention rather than finding.

**Evidence note.** Ids of the form FRAG-MKTG-NN are rows in this pack's
evidence fragment at
`packs/marketing-growth/research/sources.fragment.json`, each carrying
its version, licence, access date, maintenance state and review
trigger. The integrator imports that fragment into
`registry/evidence.json` and assigns final EV ids; until it runs, the
fragment ids are the citable form, and every EV id used here already
exists in the ledger.

**B1. The lawful basis is stored with the address, not asserted about
the list.** `collects_contact_details`. Every contact record carries a
basis from a closed enum, a timestamp and the collection source,
written at capture; a record claiming soft opt-in also carries a
reference to the sale or negotiation it rests on. Prevents the one
failure that cannot be repaired afterwards. PECR regulation 22 requires
prior consent for marketing mail to an individual subscriber, with a
single narrow escape needing all three of details obtained in the
course of a sale or negotiation, similar products only, and a free
refusal route at collection and in every later message (FRAG-MKTG-09).
Provenance cannot be rebuilt from a table of addresses six months on,
and UK statute now expects a recorded lawful basis rather than a
privacy notice (EV-0225). Basis: law. See
`packs/marketing-growth/refs/CONSENT_RECORD.md`.

**B2. Every marketing message carries a refusal route that works
without a conversation.** `sends_marketing_message`. Mail carries a
`List-Unsubscribe` header with an HTTPS URI and
`List-Unsubscribe-Post: List-Unsubscribe=One-Click`, both inside the
DKIM signed-header list, with an opaque hard-to-forge token the server
validates, no cookies, no HTTP authentication and no confirmation page
(FRAG-MKTG-07). A visible in-body link stands beside it (FRAG-MKTG-08).
Prevents a refusal route that exists on paper and fails in the hand,
which is what PECR asks for at collection and in every message
(FRAG-MKTG-09). The token closes the mirror failure, an unsubscribe
endpoint anyone can forge into a denial-of-subscription hole. Basis:
standard, discharging a legal duty. See
`packs/marketing-growth/refs/SEND_PREFLIGHT.md`.

**B3. A refusal suppresses before the next send, mechanically.**
`sends_marketing_message`. A valid unsubscribe request writes to a
suppression store; the send path reads that store and fails closed on
any address in it. Suppression survives list re-import and a change of
provider. Prevents the usual shape of a breach, which is not a missing
link but a link whose effect never reached the sending system. RFC 8058
fixes the signal and says nothing about how fast the effect must land
(FRAG-MKTG-07), so this pack rules the timing: before the next send,
not on a nightly job. Basis: law, because a refusal with no effect is
the same as no refusal.

## Defaults

Followed unless the venture's lock-book records a reason to depart.

**D1. One named growth philosophy per venture, recorded before spend.**
Chosen from the four in
`packs/marketing-growth/guides/GD-MKTG-001-growth-philosophy.md`, with
at least one evidence id per choice. Reason: the four pull budget in
genuinely different directions, no evidence ranks them, so the choice
has to be argued rather than absorbed.

**D2. A growth plan names its reinvestment step.** The place where an
output re-enters as an input. A plan with none is a paid-acquisition
budget and is described as one (FRAG-MKTG-13). Reason: the source is a
practitioner essay with no data, and this rule survives the weak
evidence because it is a naming discipline, not a claim about results.

**D3. Effect comes from a randomised holdout, or the number is
labelled.** Any conversion or lift figure carries a holdout design or
the literal token UNVERIFIED. Reason: across fifteen randomised
experiments and roughly 500 million user-experiment observations,
observational estimators on far richer data than a venture will ever
hold failed to reproduce the randomised estimates (FRAG-MKTG-10). Scope
note: one platform, one era, mostly large advertisers with small
percentage effects. It does not show observational methods failing
everywhere, and it says nothing about a venture that cannot afford a
holdout. See
`packs/marketing-growth/guides/GD-MKTG-003-effect-measurement.md`.

**D4. Attribution distributes a measured total, it never produces
one.** Any percentage split across touchpoints is a declared reporting
convention. Reason: the dominant analytics vendor deleted first-click,
linear, time-decay and position-based models from its own product in
November 2023 (FRAG-MKTG-12), and the platform paper defending
attribution anchors its model to randomised trials rather than
replacing them (FRAG-MKTG-11).

**D5. A funnel number ships with its definition as configuration.**
Step ordering mode, exclusion steps and the conversion denominator sit
in machine-readable form beside the number. Reason: the same product
yields different rates under sequential, strict-order and any-order
steps, and two teams quoting different conversion rates are usually
quoting different parameter sets (FRAG-MKTG-15).

**D6. Every published page has a named human owner and a stated
purpose,** recorded in a manifest the page set is checked against.
Reason: the index operator's spam policies name scaled content abuse
and site reputation abuse, and the test is purpose rather than
production method (FRAG-MKTG-02), so a machine-drafted page with a real
owner and a real reader is fine while a hundred with neither are not.
The helpful-content guidance asks that substantial automation be
evident to the visitor (FRAG-MKTG-04). See
`packs/marketing-growth/guides/GD-MKTG-004-content-provenance.md`.

**D7. Structured data describes what the reader can see.** Every markup
property carrying user-facing text has a matching string in the
rendered page (FRAG-MKTG-03), against the versioned vocabulary at
EV-0022. Reason: the penalty is bounded, loss of rich-result
eligibility rather than a ranking hit, and the rule is testable.

**D8. Crawler directives are a release-gated artefact.** The robots
file ships through the same pipeline as code, with a test asserting the
production profile carries no blanket disallow and a staging fixture
that fails the same test. Reason: a 5xx on that file means a conforming
crawler must assume complete disallow (FRAG-MKTG-06), so a botched
deploy is a self-inflicted deindexing incident. It is not a security
control and never names a secret path.

**D9. Deliverability is a preflight gate before a first send.** SPF or
DKIM, forward and reverse DNS, TLS and RFC 5322 conformance for every
sender; above five thousand messages a day, SPF and DKIM and DMARC with
From alignment plus one-click unsubscribe; spam rate under 0.30 per
cent (FRAG-MKTG-08). Reason: published numbers a machine can assert
before anything ships. Scope note: one mailbox provider's rules for its
own inboxes. Others publish overlapping but different thresholds, and
at least one computes the spam-rate denominator differently, so no
single number is universal. See
`packs/marketing-growth/refs/SEND_PREFLIGHT.md`.

**D10. Reach to category non-buyers is the opening bet for a small
brand.** Reason: the repeat-purchase tradition puts acquisition at
roughly twice the weight of retention and finds loyalty largely a
consequence of brand size rather than a lever that produces it
(FRAG-MKTG-16). Scope note: consumer goods and mass-market services
panels, thin on business software and subscription products where
negative churn is a real mechanism, and the record is an institute
summary rather than the underlying papers.

**D11. Each activity declares a time horizon.** Reason: brand-building
and sales activation behave differently in time, and one blended return
number will always select activation (FRAG-MKTG-17). The quoted 60:40
split is not adopted: it rests on self-selected award case studies, the
observational class FRAG-MKTG-10 found unreliable. The horizon
declaration survives; the ratio does not.

**D12. Field performance is a marketing constraint on public
surfaces** (EV-0241, EV-0060), with any revenue claim from it settled
by experiment rather than by quoting a case study, and guardrail
metrics that block only on significant harm (EV-0059).

## Preferences

Taste. Depart freely, no reason needed.

- Channel mix, and whether any of it is paid.
- Pull rather than push, as in the public handbook at EV-0095, where the
  audience has a reading habit. It transfers badly to a category whose
  buyers do not read (FRAG-MKTG-14).
- Publishing the marketing handbook itself, as at EV-0055 or EV-0095.
- Taking a stance rather than hedging, which is what stops
  machine-drafted content reading like everyone else's.
- Treating documentation and marketing content as one artefact.
- Cadence, format, length and tone.
- Positioning and messaging method. No framework in common use has
  primary evidence in this pack's source set, so a framework here is a
  preference wearing a diagram.

## Decision map

| Fork | What it decides | Guide |
| --- | --- | --- |
| Which growth philosophy does this venture run | Where budget and attention go, and what counts as progress | `packs/marketing-growth/guides/GD-MKTG-001-growth-philosophy.md` |
| Where does a lawful address come from | Capture route, stored basis, what may be sent to it | `packs/marketing-growth/guides/GD-MKTG-002-consent-route.md` |
| How is this channel's effect measured | What may be claimed, and what the claim costs | `packs/marketing-growth/guides/GD-MKTG-003-effect-measurement.md` |
| Who owns a published page and why does it exist | Publishing rate, provenance and review | `packs/marketing-growth/guides/GD-MKTG-004-content-provenance.md` |

Reference tables sit in `packs/marketing-growth/refs/`. The pack applied
end to end is
`packs/marketing-growth/exemplars/EX-MKTG-001-launch-and-first-sequence.md`.
Evaluation criteria are in `packs/marketing-growth/CHECKS.md`.

## Failure modes and anti-patterns

- **Markup describing content no reader can see.** Rich-result
  eligibility goes (FRAG-MKTG-03).
- **Unsubscribe as a landing page with a confirm button.** The
  specification forbids the confirmation step on the one-click route,
  and a provider that never reaches the endpoint counts the complaint
  instead (FRAG-MKTG-07).
- **Lawful basis defaulted to legitimate interests for everything.** It
  has to be true per record, and PECR offers no such escape for
  marketing mail to an individual (FRAG-MKTG-09).
- **A conversion percentage with no holdout and no label.** It reads as
  measurement and is arithmetic (FRAG-MKTG-10).
- **A loop diagram with no reinvestment step.** An arrow drawn back to
  the start of a spending plan is not a loop (FRAG-MKTG-13).
- **Volume as strategy.** Named as scaled content abuse, and the test is
  purpose, not production method (FRAG-MKTG-02).
- **One global consent rule.** UK PECR is opt-in with a narrow soft
  opt-in, the US regime is opt-out, and EU states vary (FRAG-MKTG-09).
- **Crawler directives edited in a marketing console,** bypassing the
  release gate D8 exists to hold.
- **A retention-first plan for a brand with few buyers.** The double
  jeopardy evidence says that is close to backwards (FRAG-MKTG-16).
- **Inventing an optimisation workstream for AI answers.** The vendor
  states no new file or markup is needed for its own AI surfaces
  (FRAG-MKTG-05).
- **Suppression held inside one sending provider.** It does not survive
  the migration, and the first send from the next one mails the people
  who refused.
- **A keywords meta tag.** The index operator says it is unused
  (FRAG-MKTG-01).

## Open questions and counter-evidence

- **Acquisition against the installed base is unresolved.** The
  repeat-purchase tradition points budget at people who have never
  bought (FRAG-MKTG-16); loop thinking puts the engine inside the
  existing user base (FRAG-MKTG-13). Their evidence bases barely
  overlap, consumer panels on one side and software anecdote on the
  other. This pack makes the venture declare which world it is in and
  refuses to choose for it.
- **Optimising for AI answers is genuinely open.** The vendor denial
  (FRAG-MKTG-05) is self-interested and covers its own surfaces only. A
  live counter-practice, a machine-readable file for assistants, is
  being adopted with no measurement behind it. Neither side has
  evidence, and the pack records nothing as settled.
- **A venture that cannot afford a holdout has no documented answer.**
  Every serious measurement source assumes an experiment programme. This
  is the largest gap in the pack, and D3's labelling rule is a
  work-around rather than a solution. The field is also a spectrum
  rather than a prohibition: later work in the same journal treats
  non-experimental approaches more sympathetically than FRAG-MKTG-10
  does, which is why D3 is a default and not a binding rule.
- **Positioning has no evidence base here at all.** The well-known works
  are behind copyright and the research literature does not test them.
  It stays a preference until that changes.
- **Three sources were read at second hand.** The institute page is
  all-rights-reserved and paraphrase only, the IPA text and its
  commentary were paywalled, and direct access to the loop essay was
  refused at the cutoff (FRAG-MKTG-13, FRAG-MKTG-16, FRAG-MKTG-17). All
  three are directional, none is a measured finding, and only the naming
  discipline in D2 is carried from the last.
- **Attribution under widespread consent refusal is undocumented** by
  the vendors that model around it (FRAG-MKTG-12).
- **Whether machine-drafted content at volume is detectably worse,
  rather than merely against policy, is unmeasured.**
- **Refresh triggers.** Re-argue this pack on: any revision of the
  search guidance behind FRAG-MKTG-01 to FRAG-MKTG-05; a change to the
  sender requirements at FRAG-MKTG-08; an amendment to PECR regulation
  22; ICO guidance interpreting EV-0225; and the day the FRAG-MKTG-13,
  FRAG-MKTG-16 and FRAG-MKTG-17 primary texts become readable. Tactics
  here age faster than the rest of the estate, so every organ in this
  pack carries an event trigger rather than a distant date.
