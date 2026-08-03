---
summary: The pack applied end to end, a five-page launch surface and a three-message welcome sequence with consent, suppression and preflight proved
kind: exemplar
scope: estate
type: example
tags: [content, seo, pii, forms]
---

# Worked example: a launch surface and a first sequence

The situation. A two-person venture is launching a scheduling tool for
independent physiotherapists. It has a static site to build and an
audience of nobody. Somebody will ask, within a month, whether the
launch worked. This is the pack applied in order, with the decisions
written down as they were taken.

## 1. Activation

The task creates public pages, stores addresses from a signup form, and
sends mail. So `publishes_public_content`, `collects_contact_details`
and `sends_marketing_message` are all true, and
`reports_channel_effect` becomes true the moment anyone asks how it
went. `plans_growth_spend` is false: there is no budget to allocate.

## 2. Philosophy, argued before spend

Ruled with `packs/marketing-growth/guides/GD-MKTG-001-growth-philosophy.md`
and recorded in `GROWTH_DECISIONS.md`.

Chosen: **A, compounding organic asset**, with **D, lifecycle and owned
channel** beside it. The buyers search, because a physiotherapist
looking for scheduling software types that in, and the category has a
reading habit around practice management. Evidence cited: FRAG-MKTG-01
and FRAG-MKTG-14.

Rejected: **B, reach-led brand building**, for want of budget rather
than want of evidence. That reason is written down, because the day
there is budget the decision changes, and FRAG-MKTG-16 says reach is
where a small brand's growth comes from.

Rejected: **C, growth loops**, because the reinvestment step could not
be named without drawing it. Scheduling software does not make the next
physiotherapist. Under PACK.md D2, the plan is therefore described as
what it is: a publishing plan plus a sequence, not a growth engine.

## 3. The launch surface

Five pages: home, three content pages, one pricing page.

**Ownership (D6, guide GD-MKTG-004, option A).** A manifest names a
human owner and a one-line purpose for each of the five. The test
asserts set equality in both directions, so a page with no entry fails
and an entry with no page fails. Both directions matter: only checking
one way lets the manifest rot.

**Structured data (D7).** Each page carries markup for what the page
actually is. A script walks every markup property that carries
user-facing text and asserts a matching string exists in the rendered
page. Zero orphan properties. The first run found three: a review count
on the pricing page, an author on a content page written by nobody, and
an aggregate rating invented wholesale. All three were removed rather
than made visible, because none of them was true.

**Crawler directives and sitemap (D8).** The robots file ships in the
release pipeline. Two profiles exist: production, and a staging fixture
carrying a blanket disallow. The test asserts production has no blanket
disallow and asserts the staging fixture fails the same test. A check
that cannot fail proves nothing, so the negative fixture is the point.
The sitemap lists each of the five exactly once, every URL returns 200,
and no listed URL is disallowed.

**What was not done.** No keywords meta tag, because the index operator
says it is unused (FRAG-MKTG-01). No machine-readable file for AI
assistants, because the operator states none is needed for its surfaces
and nothing measures the counter-practice (FRAG-MKTG-05). Both
omissions are recorded, so the next person knows they were decisions.

## 4. Consent capture

Ruled with `packs/marketing-growth/guides/GD-MKTG-002-consent-route.md`.
Route A, explicit opt-in, at an unticked box on the signup form.

Each record carries the fields in
`packs/marketing-growth/refs/CONSENT_RECORD.md`: address,
subscriber_type, lawful_basis, captured_at, source and capture_wording.
The enum is closed at three values and legitimate interests is not one
of them.

The `soft_opt_in` value is in the schema and unused in live data. It is
exercised by two fixtures: one with a transaction reference that
validates, one without that is rejected. The rejection is a hard
failure, not a warning, because a basis you cannot evidence is not a
basis.

## 5. The three messages

**One-click unsubscribe (B2).** Each message carries `List-Unsubscribe`
with an HTTPS URI and `List-Unsubscribe-Post`, both inside the DKIM
signed-header list, plus a visible in-body link. The URI carries an
opaque token the server validates. Tests: a tampered token is rejected,
a valid one returns 2xx.

**Suppression (B3).** A valid POST writes to the suppression store
before returning, and a later send attempt to that address exits
non-zero. The store lives with the venture, not with the sending
provider, so the second provider inherits it. A re-import containing a
suppressed address leaves it suppressed and records the collision.

**Preflight (D9).** The script checks SPF, DKIM, DMARC, forward DNS,
reverse DNS and TLS against the zone, and fails closed on any absence.
Six negative fixtures, six distinct non-zero exits, so a failure names
itself instead of reporting a generic red. Details in
`packs/marketing-growth/refs/SEND_PREFLIGHT.md`.

## 6. Measurement

Ruled with `packs/marketing-growth/guides/GD-MKTG-003-effect-measurement.md`.
Chosen: **D, funnel diagnostics with the definition attached**. There is
no volume for a holdout, and pretending otherwise would produce the
exact number FRAG-MKTG-10 says cannot be trusted.

The one funnel, visit to signup to first booking, stores its three
parameters as configuration beside the number: ordering mode
`sequential`, exclusion steps `[]`, denominator `first_step`. Without
those three the rate means nothing, because the same product yields
different rates under different parameter sets (FRAG-MKTG-15).

Every rate in `GROWTH_DECISIONS.md` carries the literal token
UNVERIFIED. A script asserts no bare percentage escapes the document.
When someone asks in a month whether the launch worked, the honest
answer is a labelled bookkeeping number and a named reason it is not an
effect.

## 7. What this example does not prove

It shows the pack producing a compliant, checkable launch. It shows
nothing about whether the launch grows the business, because that would
need the holdout the venture cannot afford. That gap is the pack's
largest open question, and this example does not close it: it labels it.
