---
summary: A checksums file, build-platform provenance, a self-hosted attestation chain, or an independently reproduced build?
type: guide
tags: [security, delivery, ci, tooling]
kind: guide
scope: estate
authority: default
basis: standard
evidence_grade: observational
review: 2027-04
sources: [EV-0038, EV-0155, EV-0156]
---

# GD-SUPPLY-001: what provenance do we generate, and who verifies it?

## The question

Somebody downloads a thing with our name on it. What can they establish
about where it came from, without trusting us, and what does it cost us
to give them that? The fork is not whether to produce provenance. It is
how much of the production to describe, and who is on the other end
checking, because provenance nobody checks is a build step that only
adds time.

## It depends on

- Does the ecosystem you publish into have a verification path a
  consumer will actually use without being told to? Most do not.
- Is the repository public? Several registry mechanisms require it.
- Does the build run on a hosted platform that can present an identity,
  or on your own machine?
- Who is the consumer: an installer resolving automatically, a person
  downloading a file, or another one of your own systems?
- Is the toolchain reproducible cheaply, or would making it so be the
  project?

## Options

### A. A published digest list beside the artefact
A checksums file on the release page. Buys the ability to tell a
corrupted or swapped download from a good one, costs nothing, and works
in every ecosystem including a plain download page. Costs everything the
moment the attacker can write to the release page, because they can
rewrite the list too. It is an integrity control against accident and
transport, not against an adversary with publish rights.

### B. Build-platform provenance
The hosted build platform generates a signed statement binding the
artefact digest to the source revision and the workflow that produced
it, and the registry serves it beside the package. Buys a claim a
stranger can check against a public log, with a verification path that
already exists in the client. Costs a hosted build, a public repository
in some ecosystems, and acceptance of the platform's own trust root.
Its scope is narrow and stated: it describes production, not contents.

### C. A self-hosted attestation chain over more than the build
Several statements about one digest: that the source was reviewed, that
the tests ran, that a scan passed, that this is what was built. Each is
a predicate bound to the same subject digest, and a policy at admission
says which must be present before the artefact is allowed in. Buys a
control that can encode your own release conditions rather than the
platform's. Costs a policy engine, somewhere to store and find
statements, and the discipline to keep predicates meaningful once
somebody is being blocked by them.

### D. Independently reproduced builds
Make the build deterministic, publish the inputs, and let a second party
rebuild and compare digests. Buys the only guarantee in this list that
does not require trusting the builder at all, which is why it is the one
worth reaching for when the builder is the threat (EV-0155, EV-0156).
Costs a hermetic toolchain, elimination of every source of nondeterminism
including timestamps and paths, and somebody willing to do the second
build. For most ventures that last item does not exist.

## Decision rule

- Publishing into an ecosystem with a provenance mechanism: B, always,
  and take the platform's trust root as given rather than pretending to
  audit it. Add A because it costs a line and covers the plain download.
- Publishing a binary or an installer with no registry mechanism: A
  plus a signature under GD-SUPPLY-002, and say plainly on the download
  page how to check it.
- Consuming: verify at admission against a stated expectation rather
  than trusting the producing workflow, which is what the specification
  guidance actually asks for (EV-0038). The check belongs in the build,
  failing closed, not in a runbook.
- C only when a specific release condition needs enforcing and a person
  is going to maintain the policy. A policy that always passes is worse
  than none, because it reads as a control.
- D when the toolchain is already close to deterministic, or when the
  artefact is important enough that a second party will genuinely
  rebuild it. Do not start a reproducibility programme to satisfy a
  framework level.
- Never describe B as verification of the artefact. The mechanisms say
  so themselves and repeating their limit is free.

## Default

B at publish, digest-and-signature verification at admission, A
alongside. C and D are earned by a named need, not adopted by default.

## Worked rulings

- **PatterTech EOS (2026-08, argued)**: none of these apply today. This
  repository publishes no artefact, so the predicates are false and the
  guide is recorded for the first venture that publishes rather than
  applied here. Saying so is the point: a control described but not
  built is the thing the house rules forbid.
- No venture ruling yet.

## Counter-evidence

The strongest argument against investing here is that almost nobody
verifies. Measurement across four registries found signing present at
roughly one percent or below wherever it was not compulsory, and where
it was present, verification failed for a substantial fraction. That is
evidence about producers, and we found no measurement at all of how
often consumers check. So option B's value to a stranger is partly
theoretical, and the honest reason to do it anyway is that it is close
to free on a hosted platform and it is the only thing that makes an
independent check possible later.

The argument against D is its own literature: determinism is achievable
and the second builder usually is not. A reproducible build with no
rebuilder is an expensive property nobody exercises.
