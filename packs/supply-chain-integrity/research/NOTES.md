---
summary: Research synthesis for supply chain and release integrity, the three philosophies, what should bind, and the predicates proposed
type: example
tags: [eos]
---

# Supply chain and release integrity: what the evidence supports

Research cutoff 2026-08-15. Fourteen new sources are proposed in
`sources.fragment.json`. Five ledgered records already cover adjacent
ground and are cited rather than re-recorded: EV-0038 (SLSA verifying
artifacts), EV-0068 (Sigstore), EV-0069 (OpenSSF Scorecard, read the
repository rather than its self-description), EV-0155
(SOURCE_DATE_EPOCH) and EV-0156 (Bazel hermeticity).

One source refused automated access. The CISA 2025 minimum elements for
a software bill of materials returned HTTP 403 at this cutoff, so the
pack's position on bill-of-materials content rests on the CycloneDX
specification and on the measurement study instead, and no claim about
the government list appears anywhere in the pack. That is the same
shape as the security pack's missing regulator guidance: the gap is
recorded, not papered over.

## The three philosophies, and when each fits

**One. Attest to the production, and verify at admission.** The build
platform emits a signed statement about what it built, from what, and
the consumer checks it before the artefact is allowed in. FRAG-01 sets
out the threat model this addresses and, more usefully, the threats it
does not: a producer who deliberately ships bad code, compromise of the
source-control platform, typosquatting at selection time, and build-time
dependency compromise are all outside the build track. FRAG-02 gives the
shape that makes an attestation portable, a signed envelope wrapping a
statement that binds subjects by digest to a predicate. FRAG-03 and
FRAG-07 are the same idea landed in two ecosystems.

This fits anything published to a registry that supports it, from a
hosted build platform, in the open. Trade-off: it describes the
production, never the contents, and both npm's documentation (FRAG-07)
and PEP 740 (FRAG-03) say so themselves. Anti-pattern: publishing
provenance and then advertising the package as verified, which converts
an honest narrow claim into a broad false one.

**Two. Make the identity short-lived and the record public.** Rather
than protecting a signing key for years, issue a certificate that lives
ten minutes, bind it to an identity from an identity provider, and log
its issuance publicly (FRAG-06). Key custody stops being a standing
liability. This fits any project publishing from a hosted platform that
can present an identity token, and it is what the registry mechanisms in
FRAG-03 and FRAG-07 are built on.

Trade-off: it moves the target rather than removing it. Whoever can
obtain a token for the publishing identity can obtain a certificate, and
verification after expiry depends on the log, so log availability
becomes load-bearing in a way a long-lived key never was. Anti-pattern:
adopting it for an artefact class the ecosystem cannot verify, so the
signature exists and nothing checks it.

**Three. Pin hard, move on a schedule, and let the ecosystem find the
bad release first.** No cryptography at all: resolve to exact versions,
verify by digest, and refuse anything published inside a cooldown window
(FRAG-08, FRAG-09). It costs nothing to install and works in every
ecosystem that has a lock file. FRAG-10 shows the strongest version of
the same idea, a lock file backed by a public checksum log, and is
explicit that this buys authenticity and not safety.

Trade-off: it is a straight trade of patch latency for exposure to
freshly published malicious versions, and npm's client makes you see it
by keeping the vulnerable version and exiting non-zero rather than
quietly resolving past the window. Anti-pattern: applying one cooldown
policy across ecosystems. Where tags are mutable, re-pushing an existing
tag restarts the clock, which the Renovate maintainers state outright,
so the control degrades to nothing exactly where container images live.

A fourth position exists and should be named to be rejected as a primary
control: **trust the registry**. FRAG-05 is the reason. A registry that
serves signed artefacts still permits serving an older signed release,
replaying stale metadata so a client never learns an update exists, and
mixing metadata from different moments. Those are the attacks the
four-role repository design exists for, and a venture consuming from
somebody else's registry inherits whatever that registry implements. The
useful reading is which attacks the registry leaves open, not a plan to
deploy the framework.

## The disagreement that matters

**Signing is widely recommended and, where measured, mostly broken.**
FRAG-12 measured four registries over a year. Where signing was
compulsory, presence was near-universal, about 97 percent on Maven
Central. Where it was not, presence was around one percent or below.
Validity was worse than presence: roughly 27 percent of Maven Central
signatures, 52 percent of PyPI signatures and 76 percent of Hugging Face
signatures failed verification, and over 99 percent of the Maven and
PyPI failures came down to public keys that were expired, revoked or not
findable. Mandates moved quantity, tooling moved quality, and publicised
attacks moved neither.

That is the reconciliation the pack has to carry. A signature is not a
control. A verified signature is a control, and the gap between the two
is where almost all of the observed failure sits. It also settles the
identity fork on evidence rather than fashion: the failure mode that
dominates the measurement is key custody, which is precisely what
short-lived identity removes.

**A bill of materials is not automatically evidence.** FRAG-13 generated
and scanned across 2,414 repositories and found the inventory
trustworthy mainly when derived from a lock file with a strong package
manager, then found the scanners on top of it reporting false positives
at about 92 percent in its case study, with reachability analysis
removing roughly 62 percent of those. So the ordering is pin first,
generate second, and treat the alert stream as a queue to triage rather
than a list of defects. The 92 percent is a case-study figure, not a
population estimate, and the pack says so where it uses it.

**Cheap signals beat expensive ones that nobody runs.** FRAG-14 measured
45,812 releases and found that watching how a release was published,
rather than what it contains, surfaced 204 discontinuities worth review,
with practitioner review of 30 core cases rating 20 as needing immediate
attention. The authors also state where it is blind: a compromise that
reuses the same publishing path leaves no discontinuity. A legitimate
workflow migration produces the same signal as a compromise, so it is a
prompt to look, never a verdict.

**What a compromised build system can reach is documented and mostly
ignored.** FRAG-11 says it in the platform's own words: anyone with
write access reads every secret, a step referenced by tag is mutable and
only a full commit digest is not, self-hosted runners give no isolation
guarantee, and the default token should start read-only. None of it is
enforced by anything. This is the part of the domain where the control
is configuration rather than cryptography, and it is the cheapest thing
on the list.

## What should bind, what should default, what is preference

**Binding.** Cheap, checkable, and the absence of each is a concrete
failure that is hard to reverse once an artefact is public.

- Every third-party artefact entering a build or a runtime is pinned to
  a digest, and the digest is what the build resolves (FRAG-10, FRAG-11).
- Anything published for others to install carries provenance from the
  system that built it, and the publish path is the only path that can
  sign (FRAG-01, FRAG-03, FRAG-07).
- A verification step exists on the consuming side and fails closed,
  because a signature nobody checks is not a control (FRAG-12).
- Publishing credentials and signing identity are reachable only from
  the release path, never from a workflow that untrusted input can
  influence (FRAG-11).

**Default, meaning do this unless the venture writes down why not.**

- A cooldown window before adopting a newly published version, with
  security fixes exempted deliberately rather than by accident
  (FRAG-08, FRAG-09).
- Generate the bill of materials from the lock file rather than by
  scanning a built tree, and record which branches are incomplete
  (FRAG-04, FRAG-13).
- Check the release path for discontinuity at admission, as a prompt to
  look (FRAG-14).
- Short-lived identity for signing wherever the ecosystem supports it,
  long-lived keys only where it does not (FRAG-06, FRAG-12).
- Reproducibility where the toolchain gives it cheaply, as the one check
  that does not depend on trusting the builder (EV-0155, EV-0156).

**Preference, meaning record the choice and move on.** Which bill of
materials format, given both are standardised and both round-trip
adequately. Where attestations are stored. Whether the cooldown lives in
the install client or the update bot. How long the window is, beyond
being non-zero.

## Anti-patterns to name in the pack

- Publishing provenance and describing the package as verified.
- Counting signatures rather than verifications (FRAG-12).
- A bill of materials generated by scanning a built image and presented
  as complete, with no statement of what it could not see (FRAG-04).
- Treating an alert count off a bill of materials as a defect count
  (FRAG-13).
- One cooldown policy applied across ecosystems where tags are mutable
  (FRAG-09).
- A release workflow that shares a runner, a token or a trigger with
  anything that reads untrusted input (FRAG-11).
- Vendoring to avoid a supply chain problem, then never diffing the
  vendored tree again. Vendoring moves verification to the moment the
  directory was generated (FRAG-10); if nobody reads that diff, it moves
  verification to nowhere.

## Predicates proposed

The vocabulary is integrator-owned, so these are proposals for
`kernel/PREDICATES.md`, not additions. Check S021 will fail against this
pack's front matter until they are added, which is the integrator's step.

Four existing predicates are reused rather than duplicated, and the pack
declares them: `publishes_code` and `ships_a_binary` for the publishing
side, `adds_dependency` and `vendors_code` for the consuming side. None
of the four needed a new spelling, and inventing one would have split
the estate the way `processes_personal_data` did.

Two facts are genuinely not in the vocabulary.

**`builds_release_artefact`**, settled by `task`, group "Code and how it
changes". True when the work produces an artefact meant to be installed
or run somewhere other than the machine that built it: a package, a
container image, an installer, a compiled binary, a signed bundle.

Why the existing names do not cover it. `publishes_code` and
`ships_a_binary` are venture facts settled once at interview question 5;
they say the venture distributes something, and stay true for its whole
life. They cannot tell you that *this* change cuts a release, which is
the moment the binding requirements about signing identity and publish
path actually apply. `deploys_to_environment` is the nearest running-it
predicate and is a different fact: a venture can deploy without ever
producing a distributable artefact, and can publish one without
deploying anywhere. `ships_code` in delivery-testing is broader still,
covering any code reaching somebody other than its author.

**`consumes_prebuilt_artefact`**, settled by `task`, group "Secrets and
reach outside itself" or "Code and how it changes", integrator's call.
True when the work brings in a binary, container image, archive, installer
or model file that nobody here built from source they can read.

Why `adds_dependency` does not cover it. That predicate is about
third-party *code*: something a resolver names, a lock file pins and a
reader can open. A base image, a downloaded toolchain, a driver blob or a
set of model weights is none of those. The distinguishing fact is not
provenance but readability: for a source dependency you can, in
principle, review the diff, and for a prebuilt artefact you cannot, so
the digest and the attestation are the only evidence available. That is a
different control set, which is what makes it a different predicate
rather than a shade of the same one.

If the integrator judges `adds_dependency` broad enough, the honest
consequence is that this pack loses the ability to activate on a change
that only bumps a base image tag, which is one of the two named cases in
the capability's own coverage row.

## Refresh triggers

Re-run this research on any of: a new SLSA specification version, and
particularly any change to which threats the build and source tracks
claim; an in-toto attestation specification v2; a CycloneDX or SPDX
release that changes the completeness model; the CISA minimum-elements
list becoming reachable; a package manager making a cooldown window
default-on; a published measurement of attestation verification rates,
as opposed to publication rates; and any incident where a short-lived
identity was abused through the identity provider rather than through a
stolen key.
