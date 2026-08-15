---
summary: Hosted identity provider, self-hosted identity server, passwords of your own, or federation to the customer's provider?
type: guide
tags: [auth, arch, security]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
review: 2028-12
sources: [pending-fragment-import]
---

# GD-IDENT-003: who checks the credential?

## The question

Somebody has to hold the authenticator, run the sign-in flow, handle
recovery, and keep up with what counts as strong authentication this
year. The fork is whether that somebody is a vendor, software you run,
code you write, or the customer's own identity team. It is usually
decided in an afternoon and lived with for years.

## It depends on

- Who are the users? Consumers with their own accounts, or staff of
  organisations that already have an identity provider?
- Does anyone buying this ask for single sign-on? For business customers
  the answer arrives with the first procurement form.
- What is the cost of the sign-in surface being down, and does the
  venture have a path that survives it?
- Does the venture want to hold password hashes and the recovery flow
  that goes with them?
- Is the user list an asset the venture must be able to move, or an
  implementation detail?
- Who carries the pager when a sign-in bug appears at the weekend?

## Options

### A. Hosted identity provider
A vendor runs sign-in, recovery, second factors and the flows around
them; the venture receives tokens. Buys the parts that are tedious and
easy to get wrong, and buys them already keeping up with what counts as
phishing-resistant, which now excludes anything a person reads and
retypes (NIST SP 800-63B-4). Costs a dependency on the request path at
its worst moment, because a provider outage is a total outage of
sign-in, and costs a migration whenever the commercial terms change. The
validation duties do not transfer: the venture still checks signature,
issuer, audience and expiry on every token, and still knows the
difference between the identity token and the access token (OpenID
Connect Core).

### B. Self-hosted identity server
Open-source software the venture runs, speaking the same protocols. Buys
the protocol surface without the vendor relationship, and keeps the user
list somewhere the venture controls. Costs operations: a stateful
service on the critical path, its upgrades, its backups, and its
security patches, all landing on whoever carries the pager. The protocol
duties are identical to A.

### C. Passwords of your own
The venture stores credentials and writes sign-in, reset, lockout and
second factor itself. Buys nothing that A or B do not buy, unless there
is a hard requirement that no third party sees the user list and no
existing software fits. Costs the whole surface: recovery flows are
where the interesting attacks live, and the current practice closes off
the shortcut of handing the password to a client and having it exchange
that for a token (RFC 9700).

### D. Federation to the customer's provider
Business customers bring their own identity provider; the venture trusts
it for that tenant. Buys the answer to the procurement question and
moves joiner-mover-leaver where it belongs, with the customer. Costs
per-tenant configuration, a trust decision per tenant, and a subtle
failure mode: a token from tenant A's provider must not be accepted for
tenant B, which is an audience and issuer check the venture owns and
nobody else will make (OpenID Connect Core).

## Decision rule

- Consumer users, no procurement pressure, small team: A. The parts a
  provider ships are the parts most likely to be got wrong.
- A hard requirement that no third party holds the user list, or a
  regulatory reason the data cannot leave: B.
- Business customers with their own identity teams: D on top of A or B,
  not instead. Somebody still has to authenticate the users who are not
  covered by a customer's provider, starting with your own staff.
- C only where a written requirement rules out A, B and D, and never
  because it looked quicker.
- Whichever is chosen, keep a path that does not depend on it. The
  break-glass account must not be federated through the provider whose
  outage is one of the reasons the path exists (Entra emergency access
  guidance), which is B4 in `packs/identity-access/PACK.md`.
- Whichever is chosen, the venture still validates every token. There is
  no arrangement under which the audience check becomes somebody else's
  job (OpenID Connect Core).

## Default

A, with the sign-in surface kept thin enough to move: the venture's own
user record keyed by a stable subject identifier, the provider's tokens
translated into the venture's own session or token at one boundary, and
no provider-specific claim read anywhere else. That is what makes the
choice reversible, and reversibility is the whole of the answer to the
lock-in objection.

## Worked rulings

- **PatterTech EOS itself (2026-08, argued)**: not applicable. The
  repository has no users and no sign-in. The break-glass shape in B4
  still applies to any venture it seeds, which is why the rule sits in
  the pack rather than in this guide.
- No venture ruling yet. Recording the absence rather than inventing a
  ruling, because a worked ruling nobody made is worse than none.

## Counter-evidence

Nothing in the source set compares a hosted provider against a
self-hosted one on either security or availability. The specifications
say what a correct deployment looks like (RFC 9700, OpenID Connect Core)
and the digital identity guidelines say what counts as strong
authentication (NIST SP 800-63B-4), and none of the three has an opinion
on who should run it. The preference for A above is a judgement about
where a small team's attention is best spent, not a finding.

The strongest argument against A comes from a source arguing for
something else: the break-glass guidance treats identity-provider outage
as a first-class scenario worth designing a separate path for (Entra
emergency access guidance). Read straight, that is a vendor telling you
its own layer will be unavailable at some point. It does not change the
default; it is why the default carries a second path.
