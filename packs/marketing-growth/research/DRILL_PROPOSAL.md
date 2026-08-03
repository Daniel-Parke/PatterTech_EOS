---
summary: Cold-agent acceptance drill for the marketing-growth pack, one launch surface plus one lifecycle sequence, machine-checked
type: example
tags: [eos, testing]
---

# Drill: a launch page and a first email, both provable

Single run, cold agent, no human turns, pack plus this brief only.

## Brief handed to the agent

Ship `site/` and `lifecycle/` for a fictional product. `site/` is a
static launch surface with a home page, three content pages and a
pricing page, plus `robots.txt`, `sitemap.xml` and JSON-LD.
`lifecycle/` is a three-message welcome sequence with a consent-capture
form, a suppression store and a send-preflight script. Record the
growth philosophy, measurement plan and lawful basis in
`GROWTH_DECISIONS.md`.

## Deterministic acceptance criteria

Pass requires every check below. Each is a script exit code.

1. Every JSON-LD property that carries user-facing text has a matching
   string in the rendered DOM of the same page; a script asserts zero
   orphan properties. Google's Rich Results structured-data validator
   returns zero errors.
2. `robots.txt` parses under RFC 9309 rules, is under 500 KiB, and a
   test asserts no `Disallow: /` on the production profile. A staging
   fixture with `Disallow: /` must fail the same test, proving the check
   discriminates.
3. Every page in `site/` appears exactly once in `sitemap.xml`, every
   sitemap URL returns 200, and no sitemap URL is disallowed by
   `robots.txt`.
4. `CONTENT_OWNERS.json` names a human owner and a one-line purpose for
   every published page; a schema check validates it and a test asserts
   the page set and the manifest set are identical. No page carries a
   `keywords` meta tag.
5. Each of the three emails carries `List-Unsubscribe` with an HTTPS
   URI and `List-Unsubscribe-Post: List-Unsubscribe=One-Click`, both
   headers inside the DKIM `h=` tag list. A POST with a tampered
   unsubscribe token is rejected; a valid token returns 2xx.
6. A POST to a valid unsubscribe URI puts the address in the
   suppression store, and a later send attempt to it exits non-zero.
7. The preflight script fails closed when any of SPF, DKIM, DMARC,
   forward and reverse DNS, or TLS is absent from the fixture DNS zone.
   Six negative fixtures, six distinct non-zero exits.
8. Every contact record carries a lawful basis from a closed enum, a
   timestamp and the collection source. A record claiming soft opt-in
   with no prior transaction reference fails validation.
9. `GROWTH_DECISIONS.md` names one philosophy from the pack list and
   one measurement method, and cites at least one evidence id per
   choice. Every stated conversion or lift figure carries either a
   holdout design or the literal token `UNVERIFIED`; a script asserts
   no bare number escapes.
10. Any funnel in the measurement plan stores its step ordering mode,
    exclusion steps and conversion denominator as machine-readable
    configuration beside the number.

## Failure signals to record

Markup describing content no reader can see. Unsubscribe implemented as
a landing page with a confirm button. Lawful basis defaulted to
legitimate interests for everything. Conversion percentages quoted with
no holdout and no `UNVERIFIED` token. A growth plan whose loop diagram
has no reinvestment step.
