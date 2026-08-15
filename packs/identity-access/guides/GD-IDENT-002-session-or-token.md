---
id: GD-IDENT-002
summary: Server-side session in a cookie, bearer token, token in a cookie behind a front end, or a sender-constrained token?
kind: wargame
type: wargame
tags: [auth, eos, security, state, wargame]
scenario_modes: [selection, exception]
applicable_doctrines: [DOC-IDENT-015]
applies_when: [authenticates_people]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0524, EV-0525, EV-0526, EV-0527]
review: 2028-11
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# GD-IDENT-002: how does the venture remember who this is?

## Decision question and stakes

Authentication happens once and the request happens a thousand times.
Something has to carry the answer between them, and the fork is what
that something is: state the server holds and a key to it, or a signed
statement the client holds and presents. The choice decides how
revocation works, where the credential can be stolen from, and what
happens on the day you need to sign everybody out.

## Doctrines or coverage gap under pressure

- `DOC-IDENT-015` (default): Server-side sessions in cookies for a first-party browser surface; tokens for anything else.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Who is calling? A browser the venture also serves, a browser it does
  not, a native client, or another service?
- Same site, or cross-origin? Cookies are automatic within a site and
  awkward outside one.
- Does anything need to be revoked before it expires? A ban, a password
  change, a stolen laptop.
- How many services accept this credential? One, or several that do not
  share a database?
- Can the client hold a private key, or is it script running in a page
  where anything script can read is already lost?

Applicability is `authenticates_people`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Server-side session, key in a cookie
The server holds the session; the cookie holds an opaque identifier.
Buys revocation that actually works, because the state is yours to
delete, and it buys a credential that page script cannot read when the
cookie is marked accordingly. The property list is short and cheap:
enough entropy from a cryptographic generator, the secure and
script-inaccessible flags, a cross-site restriction, a fresh identifier
whenever privilege changes, an idle limit and an absolute limit both,
and invalidation on the server at logout rather than deletion on the
client (OWASP session guidance). Costs server state, which has to be
shared or sticky across instances, and it fits a browser far better than
anything else.

### B. Bearer token in an authorisation header
The client holds a signed statement and presents it. Buys statelessness
and works for native clients, other services and cross-origin calls
where cookies are a fight. Costs revocation: the token is valid until it
expires, so either the lifetime is short and a refresh token carries the
risk instead, or a check against a revocation list puts the state back
and removes the reason for choosing this. It costs storage safety too,
because the browser places to put it are the places script can read,
which the guidance is direct about (OWASP session guidance). And a
bearer token is a password with an expiry: whoever holds it is the user
(RFC 9700).

### C. Token behind a front end, cookie to the browser
The browser gets a session cookie; a server-side component holds the
tokens and calls the downstream services. Buys both halves: the
credential the browser holds cannot be read by script and can be
revoked, and the services still see a token they can validate. Costs a
component that has to exist, be deployed and be kept in step, and it
reintroduces server state for the browser leg.

### D. Sender-constrained token
The token is bound to the client that was issued it, by mutual TLS or by
proof of possession, so a stolen token alone is not enough. This is
where the current practice points (RFC 9700). Buys the one property
bearer tokens lack. Costs client capability: something has to hold a key
and sign, which rules out the cases where the token was attractive
because the client was simple.

## Failure premises

### Premortem for A. Server-side session, key in a cookie

Assume `A. Server-side session, key in a cookie` was selected and the outcome failed. Test this option's stated failure mechanism first: server state, which has to be shared or sticky across instances, and it fits a browser far better than anything else.

### Premortem for B. Bearer token in an authorisation header

Assume `B. Bearer token in an authorisation header` was selected and the outcome failed. Test this option's stated failure mechanism first: revocation: the token is valid until it expires, so either the lifetime is short and a refresh token carries the risk instead, or a check against a revocation list puts the state back and removes the reason for choosing this. It costs storage safety too, because the browser places to put it are the places script can read, which the guidance is direct about (OWASP session guidance). And a bearer token is a password with an expiry: whoever holds it is the user (RFC 9700).

### Premortem for C. Token behind a front end, cookie to the browser

Assume `C. Token behind a front end, cookie to the browser` was selected and the outcome failed. Test this option's stated failure mechanism first: a component that has to exist, be deployed and be kept in step, and it reintroduces server state for the browser leg.

### Premortem for D. Sender-constrained token

Assume `D. Sender-constrained token` was selected and the outcome failed. Test this option's stated failure mechanism first: client capability: something has to hold a key and sign, which rules out the cases where the token was attractive because the client was simple.

## Decision rule

- First-party browser surface, one origin, one venture: A. It is the
  cheapest thing that revokes.
- Native client, another service, or a public API: B, and constrain the
  token to the client wherever the client can hold a key, which is D.
- A browser talking to services that also serve non-browser clients: C,
  rather than putting a token where page script can reach it.
- Anything needing revocation faster than the token lifetime: A, or B
  with a short lifetime and a rotating refresh token, and say out loud
  which one you chose.
- Public client holding a refresh token: bind it or rotate it on every
  use. Not optional in the current practice (RFC 9700).
- Never the password grant, and never tokens returned directly in an
  authorisation response (RFC 9700).
- Never the identity token as a credential to an API. It is a statement
  to one named client that somebody authenticated, and the client is the
  one required to check the audience (OpenID Connect Core).

## Safe default

A for a first-party browser surface, B constrained per D for everything
else. Both limits on every session, idle and absolute, sized against the
graded ranges: a month is defensible for a low-assurance surface, a day
for one holding somebody's account, hours for anything administrative
(NIST SP 800-63B-4).

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Who is calling? A browser the venture also serves, a browser it does not, a native client, or another service?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** A for a first-party browser surface, B constrained per D for everything else. Both limits on every session, idle and absolute, sized against the graded ranges: a month is defensible for a low-assurance surface, a day for one holding somebody's account, hours for anything administrative (NIST SP 800-63B-4).

**Exit condition:** Stop or roll back the selected branch when server state, which has to be shared or sticky across instances, and it fits a browser far better than anything else, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Who is calling? A browser the venture also serves, a browser it does not, a native client, or another service?

## Counter-evidence and transfer limits

The session property list and the storage warning are practitioner
consensus with no measurement behind them (OWASP session guidance), and
the graded session limits come from a federal risk framework whose
assurance levels map onto federal impact categories rather than onto a
venture's threat model (NIST SP 800-63B-4). Taking the numbers wholesale
imports a process most ventures do not have, so they are used here as
ranges rather than as thresholds.

The one position in this guide that is genuinely normative rather than
advisory is the OAuth current practice (RFC 9700), and it is normative
only for OAuth deployments. It does not say whether to use OAuth at all,
sets no token lifetime, and says nothing about authorisation beyond the
scope carried in the token. The choice between A and B is therefore ours
to argue and nobody's to settle.
### Historical ruling boundary

The baseline file carried 2 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
