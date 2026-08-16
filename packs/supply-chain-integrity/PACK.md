---
summary: Activation, outcomes and decision map for the supply-chain-integrity Doctrine and Wargames
type: pack
tags: [security, delivery, ci, tooling]
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [publishes_code, ships_a_binary, builds_release_artefact, consumes_prebuilt_artefact, adds_dependency, vendors_code]
activation_paths: [**/*.lock, **/package-lock.json, **/pnpm-lock.yaml, **/go.sum, **/requirements*.txt, **/Dockerfile, **/Containerfile, **/vendor/**, **/third_party/**, .github/workflows/**, **/.gitlab-ci.yml, **/*.cdx.json, **/*.spdx.json, **/sbom*.json, **/*.intoto.jsonl, **/*.sigstore, **/renovate.json, **/dependabot.yml, **/.goreleaser.yaml, **/release/**]
volatility: fast
review: none
sources: [EV-0038, EV-0068, EV-0069, EV-0155, EV-0156, EV-0549, EV-0550, EV-0551, EV-0552, EV-0553, EV-0554, EV-0555, EV-0556, EV-0557, EV-0558, EV-0559, EV-0560, EV-0561, EV-0562]
display_name: Supply Chain and Release Integrity
category: reliability-trust
id_namespace: SUPPLY
depends_on: [security-privacy, devops-reliability]
---


# Supply Chain and Release Integrity

This pack owns whether an artefact is what it claims to be: provenance,
signing identity, bill-of-materials shape, pinning cadence, and what a
compromised build system can reach. It activates when the venture
publishes something anyone installs, or when a change pulls in a
third-party binary, image or dependency. Licensing belongs to
`legal-licensing`, rollout to `devops-reliability`. Four binding
requirements, a short set of defaults, and four Wargames.

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

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B1"></a>
- `B1` to [DOC-SUPPLY-001](doctrines/DOC-SUPPLY-001-third-party-artefacts-resolve-by-digest.md) (binding)
<a id="B2"></a>
- `B2` to [DOC-SUPPLY-002](doctrines/DOC-SUPPLY-002-published-artefacts-carry-provenance-from-the-system-that.md) (binding)
<a id="B3"></a>
- `B3` to [DOC-SUPPLY-003](doctrines/DOC-SUPPLY-003-verification-exists-on-the-consuming-side-and-fails.md) (binding)
<a id="B4"></a>
- `B4` to [DOC-SUPPLY-004](doctrines/DOC-SUPPLY-004-the-publish-path-is-separate-and-nothing-untrusted-shares.md) (binding)
- source `defaults:001` to [DOC-SUPPLY-005](doctrines/DOC-SUPPLY-005-a-cooldown-window-before-adopting-a-newly-published.md) (default)
- source `defaults:002` to [DOC-SUPPLY-006](doctrines/DOC-SUPPLY-006-generate-the-bill-of-materials-from-the-lock-file-not-by.md) (default)
- source `defaults:003` to [DOC-SUPPLY-007](doctrines/DOC-SUPPLY-007-record-what-the-bill-of-materials-could-not-see.md) (default)
- source `defaults:004` to [DOC-SUPPLY-008](doctrines/DOC-SUPPLY-008-short-lived-signing-identity-where-the-ecosystem-supports.md) (default)
- source `defaults:005` to [DOC-SUPPLY-009](doctrines/DOC-SUPPLY-009-check-the-release-path-for-discontinuity-at-admission.md) (default)
- source `defaults:006` to [DOC-SUPPLY-010](doctrines/DOC-SUPPLY-010-reproducibility-where-the-toolchain-gives-it-cheaply.md) (default)
- source `defaults:007` to [DOC-SUPPLY-011](doctrines/DOC-SUPPLY-011-read-the-repository-not-its-self-description-before.md) (default)
- source `defaults:008` to [DOC-SUPPLY-012](doctrines/DOC-SUPPLY-012-one-release-path-used-for-every-release-including-the.md) (default)
- source `preferences:001` to [DOC-SUPPLY-013](doctrines/DOC-SUPPLY-013-which-bill-of-materials-format.md) (preference)
- source `preferences:002` to [DOC-SUPPLY-014](doctrines/DOC-SUPPLY-014-where-attestations-are-stored-so-long-as-a-consumer-can.md) (preference)
- source `preferences:003` to [DOC-SUPPLY-015](doctrines/DOC-SUPPLY-015-whether-the-cooldown-sits-in-the-install-client-or-the.md) (preference)
- source `preferences:004` to [DOC-SUPPLY-016](doctrines/DOC-SUPPLY-016-how-long-the-window-is-beyond-being-non-zero-and-written.md) (preference)
- source `preferences:005` to [DOC-SUPPLY-017](doctrines/DOC-SUPPLY-017-whether-release-notes-list-dependency-changes-or-a.md) (preference)

## Decision map

| Fork | Wargame | Default |
| --- | --- | --- |
| What provenance to generate, and who verifies it | WG-SUPPLY-001 | Build-platform provenance at publish, digest-and-signature verification at admission |
| Short-lived identity or a long-lived key | WG-SUPPLY-002 | Short-lived identity where the ecosystem supports it, a custodied key only where it does not |
| How far to pin, and how often to move | WG-SUPPLY-003 | Exact pins with digests, batched moves on a schedule, a cooldown window, security fixes exempt |
| Vendor it or depend on it | WG-SUPPLY-004 | Depend with a pin; vendor only for a named reason with a named person reading the diff |

Wargames sit in `packs/supply-chain-integrity/wargames/`. Level-three
detail sits in two references: what a check at admission consists of, in
`packs/supply-chain-integrity/references/admission-checklist.md`, and what a
compromised build can reach, in
`packs/supply-chain-integrity/references/build-system-reach.md`. The worked
example is
`packs/supply-chain-integrity/examples/EX-SUPPLY-001-first-published-release.md`.

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
