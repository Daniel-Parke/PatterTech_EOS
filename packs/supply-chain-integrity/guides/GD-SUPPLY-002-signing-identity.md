---
summary: No signature, a personal key, a custodied key, a short-lived identity certificate, or the platform's own signing?
type: guide
tags: [security, delivery, ci, tooling]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
review: on-change-of:EV-0068
sources: [EV-0068]
---

# GD-SUPPLY-002: short-lived identity or a long-lived key?

## The question

A signature says a particular identity stood behind these bytes. The
fork is what that identity is made of: a key somebody keeps for years,
or a certificate that exists for ten minutes and is bound to an account
that already has to be protected anyway. It looks like a cryptography
question and is really a custody question, which is where the measured
failures are.

## It depends on

- Can the publishing environment present an identity token to a
  certificate authority, or is it a laptop?
- Does the distribution channel mandate a particular signing scheme?
  App stores and operating systems do, and the choice is then made.
- Who is expected to verify: an automated client, or a person?
- What happens on the day the signer leaves, or the laptop dies?
- Is a public record of every signature acceptable, or does the fact
  that a release happened need to stay private until announcement?

## Options

### A. No signature
Rely on the registry account, transport security and the digest. Buys
simplicity and is honest about what is protecting the artefact, which is
the account. Costs any ability to distinguish a compromised account from
a compromised registry, and gives a consumer nothing to check.
Defensible for an internal artefact behind an authenticated boundary.
Not defensible for anything a stranger installs.

### B. A long-lived personal key
The maintainer holds a key and signs releases. Buys independence from
any platform and works offline. Costs the whole custody problem, and
this is where the evidence is loudest: in the four-registry measurement,
public-key problems accounted for over 99 percent of verification
failures on the two registries where failures were analysed, with keys
expired, revoked or simply not findable. The key also encodes a person,
so it becomes a succession problem the first time somebody leaves.

### C. A long-lived key held by a service
The same key material, generated and used inside a hardware module or a
managed key service, with only the release path able to invoke it. Buys
custody that does not depend on a human being careful, plus an audit
trail of use. Costs a service dependency, a cost line, and the fact that
whoever can invoke the signing operation can sign anything, so the
control collapses back onto access to that invocation.

### D. Short-lived identity certificates
The signer proves an identity to a certificate authority, receives a
certificate valid for about ten minutes, signs once, and discards the
private key; issuance is recorded in a public log so verification works
after expiry (EV-0068). Buys removal of custody as a standing problem,
which is the failure that dominates the measurement, and it binds the
signature to the workflow identity rather than to a person. Costs a
dependency on an identity provider and on the log staying available and
honest, and it makes every release publicly visible at the moment it
happens.

### E. Platform-managed signing
The store or the operating system signs, or requires a certificate it
issued. Buys the only thing that makes the artefact installable on that
platform at all. Costs are not really costs because there is no
alternative; the decision left is only how the credential is held, which
is C or D applied to the platform's certificate.

## Decision rule

- Publishing into an ecosystem that supports identity-based signing:
  D, and do not keep a long-lived key as a fallback. A fallback key is
  a second path with the same authority and less scrutiny.
- Publishing where D is not available and the artefact is public: C.
  Keep the key out of a person's hands from the start, because moving it
  later is a migration nobody schedules.
- B only where a person genuinely is the publisher and there is no CI,
  and then with a written succession plan and a published key location.
  Expect it to break, because it usually does.
- A only for artefacts that never leave an authenticated boundary, and
  say so in the lock-book rather than leaving it as a silence.
- E where the platform demands it, and then decide C or D for the
  credential underneath.
- Whichever is chosen, the signature is worth nothing until something
  checks it, which is binding requirement B3, not this guide's default.

## Default

D where the ecosystem supports it, C where it does not, and the release
path is the only thing that can invoke either.

## Worked rulings

- **PatterTech EOS (2026-08, argued)**: not applicable. Nothing is
  published from this repository, so no signing identity exists and none
  is described as existing.
- No venture ruling yet.

## Counter-evidence

Short-lived identity moves the target rather than removing it. Whoever
can obtain a token for the publishing identity can obtain a valid
certificate, and the ten-minute window bounds only how long that one
certificate is directly usable, not what it authorised. Anyone reading
option D as "no key to steal" has substituted one custody problem for an
identity-provider problem and should say which one they prefer and why.

The public log cuts both ways. It is what makes verification possible
after the certificate expires, and it is also a public record that a
release happened at a particular minute, which some ventures will not
want before an announcement.

Two operational facts about D are documentation rather than measurement:
the certificate lifetime is an operational parameter of a public shared
instance, and the availability guarantee of the log is a matter of who
runs it. Neither is a specification constant, and a venture depending on
either should record that it is depending on somebody else's
operations.
