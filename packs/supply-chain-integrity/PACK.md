---
summary: Whether an artefact is what it claims to be, covering provenance, signing identity, bill-of-materials shape, pinning cadence and the reach of a compromised build system
type: guide
tags: [security, delivery, ci, tooling]
kind: rule
authority: binding
lifecycle: active
basis: standard
evidence_grade: observational
scope: estate
applies_when: [publishes_code, ships_a_binary, builds_release_artefact, consumes_prebuilt_artefact, adds_dependency, vendors_code]
activation_paths: [**/*.lock, **/package-lock.json, **/pnpm-lock.yaml, **/go.sum, **/requirements*.txt, **/Dockerfile, **/Containerfile, **/vendor/**, **/third_party/**, .github/workflows/**, **/.gitlab-ci.yml, **/*.cdx.json, **/*.spdx.json, **/sbom*.json, **/*.intoto.jsonl, **/*.sigstore, **/renovate.json, **/dependabot.yml, **/.goreleaser.yaml, **/release/**]
volatility: fast
review: 2027-06
sources: [EV-0038, EV-0068, EV-0069, EV-0155, EV-0156, EV-0549, EV-0550, EV-0551, EV-0552, EV-0553, EV-0554, EV-0555, EV-0556, EV-0557, EV-0558, EV-0559, EV-0560, EV-0561, EV-0562]
---

# Supply chain and release integrity

This pack owns whether an artefact is what it claims to be: provenance,
signing identity, bill-of-materials shape, pinning cadence, and what a
compromised build system can reach. It activates when the venture
publishes something anyone installs, or when a change pulls in a
third-party binary, image or dependency. Licensing belongs to
`legal-licensing`, rollout to `devops-reliability`. Four binding
requirements, a short set of defaults, and four decision guides.

## Activation

**Path triggers.** Lock files of any ecosystem, dependency manifests,
container build files, a vendored or third-party tree, release and
publish workflow configuration, update-bot configuration, and any
artefact of the integrity machinery itself: bill-of-materials documents,
attestation bundles, signature files.

**Task-type triggers.** Cutting a release. Publishing to a registry, a
store or a download page. Adding, bumping or removing a dependency.
Pulling in a base image, a toolchain, a driver blob or a set of model
weights. Vendoring third-party code. Changing who or what is allowed to
publish. Adding a step to a build that runs code somebody else wrote.

**Keyword fallback**, used only when paths and task type miss:
provenance, attestation, SBOM, signing, cosign, sigstore, SLSA,
in-toto, lockfile, pinning, digest, transitive dependency, base image,
release, registry.

**Applicability predicates.** The six in the front matter:

- `publishes_code`: the venture's code is available to others.
- `ships_a_binary`: the venture distributes something that is installed.
- `builds_release_artefact`: this work produces an artefact meant to run
  somewhere other than the machine that built it.
- `consumes_prebuilt_artefact`: this work brings in a binary, image,
  archive or model file nobody here built from readable source.
- `adds_dependency`: this work brings in third-party code.
- `vendors_code`: third-party code is copied into the tree.

The first two are venture facts, settled at interview question 5. The
last four are task facts, settled from the change. None true means the
pack stays at level 1 and costs one paragraph. A binding requirement
whose own predicate is false does not apply, and each requirement names
the predicate it needs.

`builds_release_artefact` and `consumes_prebuilt_artefact` are proposed
to `kernel/PREDICATES.md` rather than declared by this pack, and the
argument for each is in
`packs/supply-chain-integrity/research/NOTES.md`. Until the integrator
adds them, this pack's front matter fails check S021, which is the
honest state to be in and not a thing to work around by borrowing a
predicate that means something else.

**Policy routing.** These triggers do not set a tier. Publishing to a
destination outside the repository is boundary contact and is already a
guarded class under `kernel/GUARD_SPEC.md`; signing identity is key
material and floors at R3 under `kernel/POLICY_SPEC.md` through the
security pack. This pack adds no tier of its own and lowers none.

## Outcomes and non-goals

Outcomes this pack is accountable for:

- Every third-party artefact a build or a runtime consumes is named by
  digest, and that digest is what actually resolves.
- Anything published for others to install can be traced to the build
  that produced it, by somebody who does not trust us.
- Verification happens on the consuming side and fails closed. A claim
  nobody checks is not a control.
- The set of things a compromised build can reach is written down, and
  is smaller than the set of things the repository holds.
- What the venture publishes about its own artefacts is narrow and
  true, so nobody reads a provenance statement as a safety claim.

Non-goals. This pack does not decide what a licence permits, which is
`legal-licensing`. It does not decide rollout, canaries, rollback or
environment promotion, which is `devops-reliability`. It does not
choose a vulnerability scanner or run a vulnerability programme; it
says what a bill of materials has to be for one to mean anything. It
does not do application cryptography, and it does not defend against a
maintainer who deliberately ships bad code, which every framework in
this space states is outside its scope and which this pack repeats
rather than quietly inheriting.

## Binding requirements

Four. Each names the failure it prevents, the predicate it needs, and
the evidence behind it. Basis is standard: the SLSA threat model, the
in-toto attestation shape, PEP 740, the CycloneDX specification and The
Update Framework, plus the measurement in the signing study for the
verification requirement. None is taste, and each prevents a failure
that is public and irreversible the moment it happens.

**B1. Third-party artefacts resolve by digest.** Every dependency,
base image, toolchain and downloaded binary that reaches a build or a
runtime is pinned to a content digest, and the build resolves that
digest rather than a name that can be re-pointed. A workflow step
referenced by tag is mutable; only a full commit digest is not.
Predicate: `adds_dependency` or `consumes_prebuilt_artefact`. Prevents:
the same identifier resolving to different bytes tomorrow, with nothing
in the tree recording that it changed. Evidence: the platform's own
hardening guidance on mutable tags, and the checksum-database design
that makes a hash hard to rewrite after the fact (EV-0038).

**B2. Published artefacts carry provenance from the system that built
them.** Anything the venture publishes for others to install carries a
statement, generated by the build platform rather than typed by hand,
binding the artefact digest to the source revision and the build that
produced it. Predicate: `builds_release_artefact` together with
`publishes_code` or `ships_a_binary`. Prevents: an artefact appearing
under our name with no way for anyone outside to tell where it came
from. Evidence: the SLSA build track and its verification guidance
(EV-0038), the in-toto statement shape, and the two registry
mechanisms built on them.

**B3. Verification exists on the consuming side and fails closed.**
Where an artefact we consume offers a signature, an attestation or a
published digest, a step checks it, and a failed or missing check stops
the build rather than logging a warning. Predicate:
`consumes_prebuilt_artefact` or `adds_dependency`. Prevents: the
observed failure mode of this whole domain, which is not absent
signatures but unchecked ones. In the four-registry measurement, a
majority of the signatures present would not verify on two of the four,
and better than a quarter would not on a third; over 99 percent of the
failures on the two that were analysed came down to keys that were
expired, revoked or unfindable. Nobody was looking.
See `packs/supply-chain-integrity/refs/admission-checklist.md`
for what a check consists of per ecosystem.

**B4. The publish path is separate, and nothing untrusted shares it.**
Publishing credentials and signing identity are reachable only from the
release path. No workflow that reads untrusted input, runs a fork's
code, or executes on a shared or self-hosted runner has access to them,
and the default token starts read-only. Predicate:
`builds_release_artefact`. Prevents: a compromised build signing a real
release, which is the one failure that defeats every other control in
this pack at once, because the signature will verify. Evidence: the
platform's own statement that anyone with write access reads every
secret, that self-hosted runners give no isolation guarantee, and that
untrusted pull-request text reaches shell context.

## Defaults

Do these unless the venture writes down why not, and its lock-book is
where that goes.

| Default | Reason | Evidence |
| --- | --- | --- |
| A cooldown window before adopting a newly published version, with security fixes deliberately exempted | Compromised releases are usually caught in hours; a window trades patch latency for that head start, and the trade should be made on purpose | npm and Renovate release-age documentation |
| Generate the bill of materials from the lock file, not by scanning a built tree | The measurement study found lock-file generation accurate and consistent where other routes were not | Zhou et al. 2026 |
| Record what the bill of materials could not see | The format carries a completeness model and a reader who is not told about a gap will read it as an absence | CycloneDX 1.7 / ECMA-424 |
| Short-lived signing identity where the ecosystem supports it | Key custody is the dominant observed failure, and a ten-minute certificate removes the thing that fails | Sigstore (EV-0068), signing measurement |
| Check the release path for discontinuity at admission | Publisher, repository and workflow changing between releases is a cheap signal with usable precision | Santos-Grueiro 2026 |
| Reproducibility where the toolchain gives it cheaply | It is the only check that does not require trusting the builder | EV-0155, EV-0156 |
| Read the repository, not its self-description, before depending on it | A project's own claims about its practices are not evidence about its practices | EV-0069 |
| One release path, used for every release, including the urgent one | A second path exists precisely so it can be used under pressure, which is when it is least reviewed | Derived from B4 |

## Preferences

Taste. Record the choice and move on. None of these bind.

- Which bill-of-materials format. Both major ones are standardised and
  both round-trip adequately for our purposes.
- Where attestations are stored, so long as a consumer can find them
  from the artefact digest alone.
- Whether the cooldown sits in the install client or the update bot.
- How long the window is, beyond being non-zero and written down.
- Whether release notes list dependency changes, or a generated diff
  does.

## Decision map

| Fork | Guide | Default |
| --- | --- | --- |
| What provenance to generate, and who verifies it | GD-SUPPLY-001 | Build-platform provenance at publish, digest-and-signature verification at admission |
| Short-lived identity or a long-lived key | GD-SUPPLY-002 | Short-lived identity where the ecosystem supports it, a custodied key only where it does not |
| How far to pin, and how often to move | GD-SUPPLY-003 | Exact pins with digests, batched moves on a schedule, a cooldown window, security fixes exempt |
| Vendor it or depend on it | GD-SUPPLY-004 | Depend with a pin; vendor only for a named reason with a named person reading the diff |

Guides sit in `packs/supply-chain-integrity/guides/`. Level-three
detail sits in two refs: what a check at admission consists of, in
`packs/supply-chain-integrity/refs/admission-checklist.md`, and what a
compromised build can reach, in
`packs/supply-chain-integrity/refs/build-system-reach.md`. The worked
example is
`packs/supply-chain-integrity/exemplars/EX-SUPPLY-001-first-published-release.md`.

## Failure modes and anti-patterns

- Publishing provenance and then describing the package as verified.
  The mechanism proves where the artefact was built. Both npm's
  documentation and PEP 740 say in their own words that it proves
  nothing about the contents, and repeating their narrow claim broadly
  is how a true statement becomes a false one.
- Counting signatures instead of counting verifications. This is the
  measured failure of the domain, not a hypothetical one.
- A bill of materials produced by scanning a built image, presented as
  complete, with no statement of what the scanner could not see.
- Treating an alert count off a bill of materials as a defect count. In
  the case study behind this pack, about 92 percent of what the
  scanners reported was false, mostly code that was present and never
  called.
- One cooldown policy applied across ecosystems. Where tags are
  mutable, re-pushing an existing tag restarts the clock, so the
  control degrades to nothing exactly where container images live.
- A release workflow sharing a runner, a token or a trigger with
  anything that reads untrusted input.
- Vendoring to escape a supply chain problem and then never reading the
  vendored diff again. Vendoring moves verification to the moment the
  directory was generated; if nobody reads that diff, it moves
  verification to nowhere.
- Assuming one licence covers the sources. Of the fourteen this pack
  adds, three were verified from a licence file, nine state a licence
  that was not opened, one states none at all, and one carries terms
  that grant a reader no reuse right whatever. The per-source list is
  in `packs/supply-chain-integrity/research/provenance.fragment.json`.
  The frozen source batch and the synthesis are in
  `packs/supply-chain-integrity/research/sources.fragment.json` and
  `packs/supply-chain-integrity/research/NOTES.md`.

## Open questions and counter-evidence

**The frameworks say what they do not cover, and it is a lot.** The
SLSA threat model names, as outside its scope, a producer who
deliberately ships bad code, compromise of the source-control platform
itself, typosquatting at package selection, insecure use of a correct
artefact, and build-time dependency compromise, which it addresses only
by suggesting the framework be applied recursively to every dependency.
A venture that reaches build level 3 has bought a narrow and real
guarantee about tamper resistance during the build, and nothing else.
Anyone who reads it as supply chain security is reading it wrong.

**Provenance mechanisms are honest about themselves and are still read
too broadly.** PEP 740 records that attestations neither raise nor
lower trust in the index, because a dishonest index can alter what it
serves or simply omit the attestation; a verifier that accepts
unattested artefacts therefore gains nothing from the attested ones.
npm's documentation states that provenance does not mean the package is
free of malicious code. These are the mechanisms' own words about their
own limits and they are the strongest counter-evidence available.

**Signing measures far worse than it is described.** The four-registry
study is the counter-evidence to almost every recommendation in this
space, including some of ours. Presence tracked mandates and not
danger: publicised attacks moved adoption not at all. Validity was the
worse half. Read it as a reason to verify rather than a reason not to
sign, and note that the dominant failure it found, key custody, is
precisely the one short-lived identity removes, which is why B3 is
binding and the identity choice is only a default.

**Where the evidence is thin.** No source we found measures how often
consumers actually verify, only how often producers sign, so B3 rests
on the shape of the failure rather than on a measurement of the
remedy. The 92 percent false-positive figure is from a case study
inside a larger paper, not a population estimate. The release-path
discontinuity signal has practitioner review of 30 cases behind it and
no more. The cooldown default rests on maintainer documentation and on
incident timelines, not on a controlled comparison, and its own sources
say a cooldown does nothing against ordinary vulnerabilities in code
that was never malicious.

**One source refused automated access.** The CISA 2025 minimum
elements for a bill of materials returned HTTP 403 at the research
cutoff, so no claim in this pack rests on it and the defaults above
lean on the specification and the measurement instead.

**Refresh triggers.** A new SLSA specification version, especially any
change to which threats the tracks claim. An in-toto attestation
specification v2. A bill-of-materials release that changes the
completeness model. The minimum-elements list becoming reachable. A
package manager making a cooldown default-on. A published measurement
of verification rates rather than publication rates. Any incident where
a short-lived signing identity was abused through the identity provider
rather than through a stolen key.
