---
summary: Server-side session in a cookie, bearer token, token in a cookie behind a front end, or a sender-constrained token?
type: guide
tags: [auth, security, state]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
review: 2028-11
sources: [pending-fragment-import]
---

# GD-IDENT-002: how does the venture remember who this is?

## The question

Authentication happens once and the request happens a thousand times.
Something has to carry the answer between them, and the fork is what
that something is: state the server holds and a key to it, or a signed
statement the client holds and presents. The choice decides how
revocation works, where the credential can be stolen from, and what
happens on the day you need to sign everybody out.

## It depends on

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

## Default

A for a first-party browser surface, B constrained per D for everything
else. Both limits on every session, idle and absolute, sized against the
graded ranges: a month is defensible for a low-assurance surface, a day
for one holding somebody's account, hours for anything administrative
(NIST SP 800-63B-4).

## Worked rulings

- **PatterTech EOS itself (2026-08, argued)**: not applicable. The
  repository authenticates nobody. Recorded so that nobody reads the
  pack's activation on `**/*session*` as a claim that this repository
  has sessions.
- No venture ruling yet. The archetype in the coverage row is a hosted
  web application with a browser front end, which lands on A, and it
  will meet B on the first integration that is not a browser.

## Counter-evidence

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
