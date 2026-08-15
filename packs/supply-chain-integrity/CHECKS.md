---
summary: What a reviewer or a checker can verify about supply chain and release integrity work, executable today versus judgement
type: guide
tags: [security, delivery, testing, ci]
review: 2027-03
kind: record
scope: estate
---

# CHECKS: evaluating work under this pack

Every criterion states what it checks and how. Executable means a
script or an existing tool can rule on it today with no human reading.
Judgement means a reviewer has to read and decide, and the criterion
exists to tell them what to look for.

## Executable today

| # | Criterion | How it is checked | Binds to |
| --- | --- | --- | --- |
| C1 | Every third-party dependency resolves to a digest, not only to a version | Lock file parsed; any entry lacking an integrity hash fails | B1 |
| C2 | Every base image, downloaded binary and toolchain is named by digest | Container build files and fetch scripts scanned for a tag or a bare URL with no digest beside it | B1 |
| C3 | Every third-party build step is pinned to an immutable reference | Workflow files parsed; a step referenced by tag or branch fails, a full commit digest passes | B1 |
| C4 | The lock file and the manifest agree | Resolver run in check-only mode; a build that would rewrite the lock fails | B1 |
| C5 | A published artefact has a provenance statement bound to its digest | Statement fetched by digest; subject digest compared against the artefact's own | B2 |
| C6 | The provenance statement names the source revision that is actually tagged | Revision in the statement compared against the release tag in version control | B2 |
| C7 | The admission step fails closed | Verification deliberately fed a wrong digest and an absent signature; the build must fail in both cases, not warn | B3 |
| C8 | No unverified artefact entered the build | Build log scanned for fetches with no matching verification record | B3 |
| C9 | Publishing credentials and signing identity are scoped to the release path | Workflow permissions parsed; any job with publish or signing scope that also runs on a fork trigger, a shared runner or untrusted input fails | B4 |
| C10 | The default token starts read-only | Workflow permission block parsed; an absent or write-by-default block fails | B4 |
| C11 | The bill of materials was generated from the lock file | Generator invocation recorded; a scan-based generation without a recorded reason fails | Defaults |
| C12 | The bill of materials states its own completeness | Completeness or equivalent field present and not blanket-complete | Defaults |
| C13 | Every source cited resolves to a row in the evidence ledger | Each EV id in front matter looked up in `registry/evidence.json` | Pack hygiene |

## Judgement

| # | Criterion | What the reviewer looks for | Binds to |
| --- | --- | --- | --- |
| J1 | The pin is real, not decorative | Does the resolver actually use the digest, or is the digest recorded beside a name that is what really resolves? | B1 |
| J2 | The provenance claim is stated as narrowly as it is true | Release notes and documentation say where the artefact was built, not that it is safe or verified | B2 |
| J3 | Verification covers the artefacts that matter, not the easy ones | The transitive set, the base image and the toolchain, not only the top-level package | B3 |
| J4 | The exception list is short and argued | Each package exempted from the cooldown or from verification names why, and by whom | B3, Defaults |
| J5 | The blast radius was worked out, not assumed | A written answer to what a compromised build could reach: which secrets, which registries, which environments | B4 |
| J6 | The urgent release used the ordinary path | A hotfix published by hand, outside the release workflow, is the finding, however good the reason felt | B4 |
| J7 | The bill of materials is used for something | It is generated and read, or generated and filed. The second is a cost with no benefit | Defaults |
| J8 | Alerts were triaged, not counted | Findings have a disposition. A dashboard number with no dispositions is not triage | Defaults |
| J9 | A vendored tree has a reader | Somebody named reads the diff on every update, and there is evidence they did | B1, GD-SUPPLY-004 |
| J10 | Registry-specific gaps are named | Which of rollback, freeze and mix-and-match the venture's registry leaves open, and what is done about it | Open questions |
| J11 | Preferences are recorded as preferences | A taste choice presented as binding is a finding, and the reverse too | Pack hygiene |
| J12 | Thin evidence is admitted | Where the pack says the evidence is thin, work relying on it says so rather than borrowing confidence | Open questions |

## Not checkable, and why

Whether an artefact is safe. Nothing in this domain checks that, and
every framework behind this pack says so in its own words: provenance
describes production, a signature describes who published, a digest
describes bytes. A criterion phrased as "the dependency is trustworthy"
is unfalsifiable and none appears above.

Whether a maintainer intends harm. The SLSA threat model puts a
producer who deliberately ships bad code outside its scope, and so does
this file. The nearest usable signal, that the way a project publishes
changed between releases, is C-series adjacent but is a prompt to look
rather than a verdict, which is why it sits in the defaults and not in
the binding set.

Whether the cooldown window is the right length. There is no controlled
comparison behind any particular number, so a check on the number would
be enforcing an unevidenced default. The check that exists is that a
window is configured and its exceptions are argued.

## Failure severity

C1 through C10 are pass or fail and gate a release. C11 and C12 are
pass or fail but gate nothing on their own: a missing bill of materials
does not make an artefact untrustworthy, it makes it undescribed. C13
is pack hygiene. The J series produces findings with severity set by
the reviewer, and a J-series finding never downgrades a C-series
failure.

A frozen drill for this capability exists at
`benchmark/drills/supply-chain-integrity.md`. It was written before
this pack and was deliberately not read while this pack was authored,
so that it stays an independent oracle. Which of these rows it scores,
and in what order, is therefore not stated here and is the integrator's
to record after the first run.
