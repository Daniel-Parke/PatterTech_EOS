---
summary: What a reviewer or a script can verify about marketing and growth work, split into executable today and judgement
type: guide
tags: [content, seo, pii, testing]
kind: guide
scope: estate
authority: default
basis: decision
evidence_grade: not-applicable
sources: [EV-0022, EV-0059, EV-0225]
review: on-change-of:PECR-reg-22-amendment
review_by: 2027-07
---

# marketing-growth pack checks

The evaluation criteria for work under
`packs/marketing-growth/PACK.md`. Each row names what is verified, how,
and whether a machine can do it today. A check that needs a person is
still a check; it is just someone's job.

## Executable today

These run in CI against the working tree and a fixture DNS zone, and
need no human input.

| Id | Verifies | How | Requirement |
| --- | --- | --- | --- |
| C-01 | Every contact record carries a lawful basis, a timestamp and a source | Schema validation over the contact store, basis restricted to the closed enum | B1 |
| C-02 | A soft opt-in claim is evidenced | A record with basis soft_opt_in and no transaction_ref fails validation, and a fixture proves the rejection fires | B1 |
| C-03 | Legitimate interests cannot be recorded as a marketing basis | The enum has three values; a fixture attempting a fourth fails | B1 |
| C-04 | One-click headers present and signed | Each message carries List-Unsubscribe with an HTTPS URI and List-Unsubscribe-Post, both names inside the DKIM signed-header list | B2 |
| C-05 | The unsubscribe token is validated | A tampered token is rejected, a valid token returns 2xx | B2 |
| C-06 | A visible in-body unsubscribe link exists | Assertion over the rendered message body | B2, D9 |
| C-07 | Refusal suppresses before the next send | A valid POST writes to the suppression store, and a later send attempt to that address exits non-zero | B3 |
| C-08 | Suppression survives re-import | An address in suppression that reappears in an import stays suppressed and the collision is recorded | B3 |
| C-09 | Preflight fails closed on each domain gate | Six negative fixtures for SPF, DKIM, DMARC, forward DNS, reverse DNS and TLS, six distinct non-zero exits | D9 |
| C-10 | Every published page has a named owner and a purpose | Manifest schema check, plus set equality with the page set asserted in both directions | D6 |
| C-11 | No page carries a keywords meta tag | Pattern scan over rendered pages | D6, preference on inert levers |
| C-12 | Structured data has zero orphan properties | Every markup property carrying user-facing text has a matching string in the rendered page of the same page | D7 |
| C-12b | Structured data is valid to the vocabulary | The index operator's own rich-result validator returns zero errors for each page carrying markup | D7 |
| C-13 | Crawler directives parse and the check discriminates | The file parses, is under 500 KiB, the production profile carries no blanket disallow, and a staging fixture carrying one fails the same test | D8 |
| C-14 | Sitemap agrees with the site | Every page appears exactly once, every listed URL returns 200, no listed URL is disallowed | D8 |
| C-15 | No bare effect number escapes | Every conversion or lift figure in the decision record carries a holdout design or the literal token UNVERIFIED | D3 |
| C-16 | Funnel definitions ship as configuration | Ordering mode, exclusion steps and conversion denominator stored machine-readably beside each number | D5 |
| C-17 | The philosophy record exists and cites evidence | The decision record names one philosophy from the guide list and one measurement method, each with at least one evidence id | D1 |
| C-18 | Field performance budget is measured, not asserted | Field data collected against a written budget for public surfaces | D12 |

## Judgement today

These need a person or a reviewing agent. Some may become executable
later; none is executable now.

| Id | Verifies | Who decides | Requirement |
| --- | --- | --- | --- |
| J-01 | The stored lawful basis is actually true of that capture | Reviewer, because a schema cannot see the form the person saw | B1 |
| J-02 | A soft opt-in transaction really was a sale or a negotiation with that person | Reviewer, and the similar-products scope is a judgement about what a buyer would expect | B1 |
| J-03 | The subscriber_type classification is right | Reviewer, since the individual and corporate line lives in regulator guidance rather than in the regulation | B1 |
| J-04 | The suppression store is genuinely portable | Reviewer, at any change of sending provider | B3 |
| J-05 | The chosen philosophy fits the category | Reviewer, against the fit conditions in the guide, which are argued and not measured | D1 |
| J-06 | The named reinvestment step is a mechanism rather than an arrow | Reviewer, and this is where a spending plan gets called a growth plan | D2 |
| J-07 | A page has a real reader | Reviewer, by name of need rather than by keyword | D6 |
| J-08 | Substantial automation is evident to the visitor | Reviewer, because the guidance is a questionnaire and two honest people can answer it the same way about very different pages | D6 |
| J-09 | Markup that passes the orphan check still describes the page honestly | Reviewer, since matching strings can be planted | D7 |
| J-10 | A labelled bookkeeping number is not being read as an effect anyway | Reviewer, and this is the failure the label exists to prevent and cannot itself stop | D3, D4 |
| J-11 | The declared time horizon matches the activity | Reviewer, because a brand activity judged on a four-week window will always look like a failure | D11 |
| J-12 | Guardrails block only on significant harm | Reviewer, on the thresholds themselves | D12 |

## How to read a failing check

C-01 through C-09 are the law floor. A failure there stops the send, and
no other result compensates. C-02, C-09 and C-13 are the checks that
prove the other checks work: each has a negative fixture, and a suite
where the negative fixtures pass is a suite that is not testing
anything.

C-10 through C-18 are defaults. A venture may depart with a recorded
reason in its lock-book, and the check then asserts the departure is
recorded rather than asserting the default.

Every J row is a place where a machine result is available and
insufficient. J-08 and J-10 are the two worth arguing about, because
both are judgements the pack's own evidence says nobody has yet
converted into a measurement.
