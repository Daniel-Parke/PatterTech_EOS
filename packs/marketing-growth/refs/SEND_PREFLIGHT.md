---
summary: The gates a sending domain and a message pass before a first bulk send, and the one-click unsubscribe mechanics
kind: fact
scope: estate
sources: [EV-0225]
volatility: fast
review: on-change-of:Gmail-sender-guidelines-requirements
type: implementation
tags: [pii, tooling, ci]
---

# Send preflight

Reference for PACK.md B2, B3 and D9. Every item here is machine-
assertable before a first send, which is the point: deliverability
becomes a gate rather than a craft.

## Domain gates

Six checks, each with its own non-zero exit so a failure names itself.

| Gate | Requirement | Applies to |
| --- | --- | --- |
| SPF | published and passing | every sender |
| DKIM | signing key published, signature verifies | every sender |
| DMARC | policy published, From aligned with the SPF or DKIM domain | above the bulk threshold |
| Forward DNS | sending host resolves | every sender |
| Reverse DNS | pointer record resolves back to the host | every sender |
| TLS | connection negotiated for transmission | every sender |

The bulk threshold at the cutoff is five thousand messages a day to one
mailbox provider, and the same provider holds the spam rate under 0.30
per cent measured through its own postmaster tooling (EV-0360).

**Scope note, and it matters.** Those are one mailbox provider's rules
for its own inboxes. Others publish overlapping but not identical
thresholds, and reporting at the cutoff says at least one computes the
spam-rate denominator from inbox-delivered mail rather than all
delivered mail. Assert the union of the published requirements, and
never treat one provider's number as universal.

## Message gates

- RFC 5322 conformance.
- `List-Unsubscribe` present, carrying an HTTPS URI.
- `List-Unsubscribe-Post: List-Unsubscribe=One-Click` present.
- Both header names inside the DKIM signed-header list, so neither can
  be stripped or rewritten in transit (EV-0359).
- A visible unsubscribe link in the body, beside the header route.

## One-click mechanics

The specification is narrow, and each clause exists to close a hole
(EV-0359).

- The URI encodes the recipient and the list identity, so the server
  needs nothing else to act.
- The URI carries an opaque, hard-to-forge component that the server
  validates. Without it the endpoint is a denial-of-subscription hole
  anyone can walk into.
- No cookies and no HTTP authentication. The mailbox provider posting on
  the recipient's behalf has neither.
- No confirmation page. A landing page with a confirm button is not
  one-click, and the provider counts a complaint instead.
- The POST carries `List-Unsubscribe=One-Click` as its body.

## The preflight contract

The script fails closed. Absent evidence is a failure, not a pass:

- Six negative fixtures, one per domain gate, each producing a distinct
  non-zero exit.
- A tampered unsubscribe token is rejected; a valid one returns 2xx.
- A valid POST writes to the suppression store before the response is
  returned, and a later send attempt to that address exits non-zero.

## What this file does not settle

How fast suppression must take effect. The specification is silent on
it, so PACK.md B3 rules it: before the next send. Nor does it settle
warm-up schedules, sending volume ramps or content filtering, none of
which has a published number in this pack's source set. Those are
craft, and the pack does not pretend otherwise.
