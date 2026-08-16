---
summary: What a verification step actually consists of per ecosystem, and what each check does and does not establish
type: guide
tags: [security, delivery, ci, tooling]
kind: fact
scope: estate
volatility: fast
review: on-change-of:EV-0038
sources: [EV-0038]
---

# Reference: what a check at admission consists of

Level 3 detail behind binding requirement B3, which says verification
exists on the consuming side and fails closed. B3 is the requirement.
This file is what satisfying it looks like in the ecosystems a venture
is likely to meet, and what each step does and does not establish.

The order matters and is the same everywhere: identify the artefact by
digest, then check any claim about that digest, then check the claim
came from an identity you expected. Skipping the first step makes the
rest theatre, because a claim that verifies against the wrong artefact
verifies perfectly.

## The four steps

**One, resolve to a digest.** The thing you are about to trust is a
sequence of bytes, not a version string and not a tag. If the resolver
gives you a name, get the digest before you get anything else.

**Two, check the bytes match.** A lock-file hash, a published checksum
or a registry-side integrity field. This is the only step that is
always available, and it is the one that fails silently if the
integrity field is missing rather than wrong. Absent must fail.

**Three, check any claim about those bytes.** A signature, an
attestation, a provenance statement. The subject digest inside the
claim must equal the digest from step one. A claim whose subject is a
different digest is not a weaker claim, it is a claim about something
else.

**Four, check the claim's identity is the one you expected.** Not that
a valid signature exists, but that it was made by the identity you
wrote down in advance: this repository, this workflow, this publisher.
Skipping this accepts anything anyone signed.

## Per ecosystem, what is available

| Ecosystem | Digest available | Claim available | The trap |
| --- | --- | --- | --- |
| Package registries with a lock file | Integrity hash per entry | Registry attestations where the publisher opted in | The lock file is only checked if the resolver runs in check-only mode. A normal install may rewrite it and report success |
| Container registries | Image digest, always | Signatures and attestations stored alongside | A tag is not an identifier. Pull by digest or you have checked nothing |
| Hosted build steps and actions | Commit digest | The source repository | A tag or branch reference is mutable by the action's owner |
| Downloaded binaries and installers | Whatever the publisher chose to publish | Detached signature if any | Both the checksum and the signature usually live on the same page as the download, so both fall together |
| Compiled toolchains | Vendor-published digest | Vendor signature, platform-specific | Fetched by a script during the build, and therefore invisible to every dependency tool you own |
| Model weights and data files | File digest, if the host publishes one | Rare | Frequently fetched at runtime rather than build time, so admission control has to exist at a layer nobody thinks of as a build |

## What each check does not establish

- A matching digest proves the bytes are the bytes you recorded. It
  says nothing about whether those bytes were ever safe.
- A valid signature proves an identity signed. It does not prove the
  identity was not compromised, and it does not prove the signer read
  what they signed.
- Provenance proves where an artefact was built. Both of the registry
  mechanisms behind this pack say in their own documentation that it
  does not mean the contents are free of malicious code.
- A published bill of materials proves what the generator found. Where
  it was produced by scanning rather than from a lock file, the
  measurement behind this pack found that unreliable.

## Failing closed

The check has to stop the build. Three phrasings fail in practice and
all three are common:

- Warn and continue. Nobody reads build warnings after the first week.
- Check in a scheduled job rather than in the build. The artefact is
  already in production by the time it runs.
- Check only when the claim is present. This is the important one. If
  an absent attestation passes, an attacker publishes without one and
  the whole mechanism is bypassed by omission. PEP 740 makes exactly
  this point about a dishonest index: the omission attack is the one
  that costs an attacker nothing.

The expectation is therefore written positively and in advance: this
artefact must carry a claim of this type from this identity. Anything
else, including nothing at all, fails.

## Verify against a stated expectation, not against the workflow

The specification guidance is explicit that trust in the producing
workflow is not evidence about the artefact (EV-0038). The consumer
writes down what it expects before it looks, and compares. A check
that reads the provenance and then decides the provenance looks fine
has verified nothing except that the file parses.
