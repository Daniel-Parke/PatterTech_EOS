---
summary: Activation, outcomes and decision map for the marketing-growth Doctrine and Wargames
type: pack
tags: [content, seo, pii, brand, voice]
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [publishes_public_content, collects_contact_details, sends_marketing_message, reports_channel_effect, plans_growth_spend]
activation_paths: [**/content/**, **/blog/**, **/robots.txt, **/sitemap*, **/*seo*, **/emails/**, **/campaigns/**, **/*landing*]
volatility: fast
review: none
sources: [EV-0022, EV-0041, EV-0055, EV-0059, EV-0060, EV-0095, EV-0225, EV-0241, EV-0353, EV-0354, EV-0355, EV-0356, EV-0357, EV-0358, EV-0359, EV-0360, EV-0361, EV-0362, EV-0363, EV-0364, EV-0365, EV-0366, EV-0367, EV-0368, EV-0369]
display_name: Marketing and Growth
category: product-commercial
id_namespace: MKTG
depends_on: [product-discovery, writing-content, legal-licensing]
---


# Marketing and Growth

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

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B1"></a>
- `B1` to [DOC-MKTG-001](doctrines/DOC-MKTG-001-the-lawful-basis-is-stored-with-the-address-not-asserted.md) (binding)
<a id="B2"></a>
- `B2` to [DOC-MKTG-002](doctrines/DOC-MKTG-002-every-marketing-message-carries-a-refusal-route-that-works.md) (binding)
<a id="B3"></a>
- `B3` to [DOC-MKTG-003](doctrines/DOC-MKTG-003-a-refusal-suppresses-before-the-next-send-mechanically.md) (binding)
<a id="D1"></a>
- `D1` to [DOC-MKTG-004](doctrines/DOC-MKTG-004-one-named-growth-philosophy-per-venture-recorded-before.md) (default)
<a id="D2"></a>
- `D2` to [DOC-MKTG-005](doctrines/DOC-MKTG-005-a-growth-plan-names-its-reinvestment-step.md) (default)
<a id="D3"></a>
- `D3` to [DOC-MKTG-006](doctrines/DOC-MKTG-006-effect-comes-from-a-randomised-holdout-or-the-number-is.md) (default)
<a id="D4"></a>
- `D4` to [DOC-MKTG-007](doctrines/DOC-MKTG-007-attribution-distributes-a-measured-total-it-never-produces.md) (default)
<a id="D5"></a>
- `D5` to [DOC-MKTG-008](doctrines/DOC-MKTG-008-a-funnel-number-ships-with-its-definition-as-configuration.md) (default)
<a id="D6"></a>
- `D6` to [DOC-MKTG-009](doctrines/DOC-MKTG-009-every-published-page-has-a-named-human-owner-and-a-stated.md) (default)
<a id="D7"></a>
- `D7` to [DOC-MKTG-010](doctrines/DOC-MKTG-010-structured-data-describes-what-the-reader-can-see.md) (default)
<a id="D8"></a>
- `D8` to [DOC-MKTG-011](doctrines/DOC-MKTG-011-crawler-directives-are-a-release-gated-artefact.md) (default)
<a id="D9"></a>
- `D9` to [DOC-MKTG-012](doctrines/DOC-MKTG-012-deliverability-is-a-preflight-gate-before-a-first-send.md) (default)
<a id="D10"></a>
- `D10` to [DOC-MKTG-013](doctrines/DOC-MKTG-013-reach-to-category-non-buyers-is-the-opening-bet-for-a-small.md) (default)
<a id="D11"></a>
- `D11` to [DOC-MKTG-014](doctrines/DOC-MKTG-014-each-activity-declares-a-time-horizon.md) (default)
<a id="D12"></a>
- `D12` to [DOC-MKTG-015](doctrines/DOC-MKTG-015-field-performance-is-a-marketing-constraint-on-public.md) (default)
- source `preferences:001` to [DOC-MKTG-016](doctrines/DOC-MKTG-016-channel-mix-and-whether-any-of-it-is-paid.md) (preference)
- source `preferences:002` to [DOC-MKTG-017](doctrines/DOC-MKTG-017-pull-rather-than-push-as-in-the-public-handbook-at-ev-0095.md) (preference)
- source `preferences:003` to [DOC-MKTG-018](doctrines/DOC-MKTG-018-publishing-the-marketing-handbook-itself-as-at-ev-0055-or.md) (preference)
- source `preferences:004` to [DOC-MKTG-019](doctrines/DOC-MKTG-019-taking-a-stance-rather-than-hedging-which-is-what-stops.md) (preference)
- source `preferences:005` to [DOC-MKTG-020](doctrines/DOC-MKTG-020-treating-documentation-and-marketing-content-as-one.md) (preference)
- source `preferences:006` to [DOC-MKTG-021](doctrines/DOC-MKTG-021-cadence-format-length-and-tone.md) (preference)
- source `preferences:007` to [DOC-MKTG-022](doctrines/DOC-MKTG-022-positioning-and-messaging-method.md) (preference)

## Decision map

| Fork | What it decides | Wargame |
| --- | --- | --- |
| Which growth philosophy does this venture run | Where budget and attention go, and what counts as progress | `packs/marketing-growth/wargames/WG-MKTG-001-growth-philosophy.md` |
| Where does a lawful address come from | Capture route, stored basis, what may be sent to it | `packs/marketing-growth/wargames/WG-MKTG-002-consent-route.md` |
| How is this channel's effect measured | What may be claimed, and what the claim costs | `packs/marketing-growth/wargames/WG-MKTG-003-effect-measurement.md` |
| Who owns a published page and why does it exist | Publishing rate, provenance and review | `packs/marketing-growth/wargames/WG-MKTG-004-content-provenance.md` |

Reference tables sit in `packs/marketing-growth/references/`: the consent
record, the send preflight, and the discovery surface. The pack applied
end to end is
`packs/marketing-growth/examples/EX-MKTG-001-launch-and-first-sequence.md`.
Evaluation criteria are in `packs/marketing-growth/CHECKS.md`.

## Failure modes and anti-patterns

- **Markup describing content no reader can see.** Rich-result
  eligibility goes (EV-0355).
- **Unsubscribe as a landing page with a confirm button.** The
  specification forbids the confirmation step on the one-click route,
  and a provider that never reaches the endpoint counts the complaint
  instead (EV-0359).
- **Lawful basis defaulted to legitimate interests for everything.** It
  has to be true per record, and PECR offers no such escape for
  marketing mail to an individual (EV-0361).
- **A conversion percentage with no holdout and no label.** It reads as
  measurement and is arithmetic (EV-0362).
- **A loop diagram with no reinvestment step.** An arrow drawn back to
  the start of a spending plan is not a loop (EV-0365).
- **Volume as strategy.** Named as scaled content abuse, and the test is
  purpose, not production method (EV-0354).
- **One global consent rule.** UK PECR is opt-in with a narrow soft
  opt-in, the US regime is opt-out, and EU states vary (EV-0361).
- **Crawler directives edited in a marketing console,** bypassing the
  release gate D8 exists to hold.
- **A retention-first plan for a brand with few buyers.** The double
  jeopardy evidence says that is close to backwards (EV-0368).
- **Inventing an optimisation workstream for AI answers.** The vendor
  states no new file or markup is needed for its own AI surfaces
  (EV-0357).
- **Suppression held inside one sending provider.** It does not survive
  the migration, and the first send from the next one mails the people
  who refused.
- **A keywords meta tag.** The index operator says it is unused
  (EV-0353).

## Open questions and counter-evidence

- **Acquisition against the installed base is unresolved.** The
  repeat-purchase tradition points budget at people who have never
  bought (EV-0368); loop thinking puts the engine inside the
  existing user base (EV-0365). Their evidence bases barely
  overlap, consumer panels on one side and software anecdote on the
  other. This pack makes the venture declare which world it is in and
  refuses to choose for it.
- **Optimising for AI answers is genuinely open.** The vendor denial
  (EV-0357) is self-interested and covers its own surfaces only. A
  live counter-practice, a machine-readable file for assistants, is
  being adopted with no measurement behind it. Neither side has
  evidence, and the pack records nothing as settled.
- **A venture that cannot afford a holdout has no documented answer.**
  Every serious measurement source assumes an experiment programme. This
  is the largest gap in the pack, and D3's labelling rule is a
  work-around rather than a solution. The field is also a spectrum
  rather than a prohibition: later work in the same journal treats
  non-experimental approaches more sympathetically than EV-0362
  does, which is why D3 is a default and not a binding rule.
- **Positioning has no evidence base here at all.** The well-known works
  are behind copyright and the research literature does not test them.
  It stays a preference until that changes.
- **Three sources were read at second hand.** The institute page is
  all-rights-reserved and paraphrase only, the IPA text and its
  commentary were paywalled, and direct access to the loop essay was
  refused at the cutoff (EV-0365, EV-0368, EV-0369). All
  three are directional, none is a measured finding, and only the naming
  discipline in D2 is carried from the last.
- **Attribution under widespread consent refusal is undocumented** by
  the vendors that model around it (EV-0364).
- **Whether machine-drafted content at volume is detectably worse,
  rather than merely against policy, is unmeasured.**
- **Refresh triggers.** Re-argue this pack on: any revision of the
  search guidance behind EV-0353 to EV-0357; a change to the
  sender requirements at EV-0360; an amendment to PECR regulation
  22; ICO guidance interpreting EV-0225; and the day the EV-0365,
  EV-0368 and EV-0369 primary texts become readable. Tactics
  here age faster than the rest of the estate, so every organ in this
  pack carries an event trigger rather than a distant date.
