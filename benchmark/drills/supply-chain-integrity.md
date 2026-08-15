---
summary: Single-run cold-agent acceptance drill for the supply-chain and release-integrity capability, frozen before any pack for it was authored, with deterministic machine-checkable criteria.
type: example
tags: [eos]
---

# Drill: publish an artefact a stranger can verify

## Scenario

A cold agent is given the supply-chain and release-integrity pack, once
one exists, and a seeded repository for `feedmill`, a small command-line
tool published as a wheel. Nothing else. This spec was frozen against
the capability row in `registry/coverage.json` before any of that pack's
content was authored, so it cannot have been written to suit the pack.

The seeded tree holds:

- `src/feedmill/cli.py` and `src/feedmill/render.py`, the code.
- `pyproject.toml`, declaring four runtime dependencies by version
  range, plus a build backend by version range.
- `requirements.txt`, resolved to exact versions on one maintainer's
  laptop, carrying no digests and no record of the platform it was
  resolved on.
- `.github/workflows/release.yml`, a single job that installs the
  dependencies, runs the build, then uploads the wheel to a package
  index using a token from the workflow's secret store.
- `scripts/fetch-vendor.sh`, called during the build, which downloads a
  compiled helper binary from a release URL and copies it into the wheel
  without checking what arrived.
- `dist/`, empty.

`TASK.md` is the change request: ship 1.4.0, and make the release
verifiable by somebody who downloaded the wheel from the index, did not
build it, and does not trust our build system. It says to record the
release facts in `RELEASE.json` at the tree root, and to put the single
command such a person runs in its `verify_command` field. It names none
of the defects above.

One run, no human turns.

No criterion below names a tool, a vendor or a format. Each names a
property, and any implementation that carries the property passes.

## Deterministic pass criteria

Every check must return true. Each is a file existence, exit code or
parse assertion, no judgement.

1. `RELEASE.json` parses as JSON and carries non-empty `artefact`,
   `artefact_sha256`, `provenance`, `signature`, `trust_root` and
   `verify_command`. Every path it names resolves to a file in the tree,
   and the grader's own sha256 of the file named by `artefact` equals
   `artefact_sha256`.
2. The file named by `provenance` parses, the digest it records for its
   subject equals the digest from criterion 1, and it names both the
   commit `git rev-parse HEAD` returns in the tree and the build entry
   point that produced the artefact.
3. Every entry in the resolved dependency file carries at least one
   cryptographic digest. The count of entries carrying none is zero, and
   the helper binary that `scripts/fetch-vendor.sh` fetches is one of
   the entries.
4. The set of name-and-digest pairs the provenance record lists as build
   inputs equals the set the resolved dependency file carries. Either
   one being a subset of the other fails: a signature over an input the
   record does not pin proves nothing about that input.
5. The set of platform tags the release configuration builds for is a
   subset of the set of platform tags the resolved dependency file
   carries digests for. A lock resolved on one platform and consumed on
   another fails here.
6. A component inventory file exists and parses as JSON or XML. Every
   component in it carries a name, a version and at least one digest,
   and the set of component names equals the set in the resolved
   dependency file.
7. A committed file records, for the pinned set, an owner and a
   next-refresh date, and that date parses and falls after the run date.
8. Copying every file `RELEASE.json` names into an otherwise empty
   directory and running `verify_command` there exits zero.
9. Flipping one byte of the copied artefact and re-running
   `verify_command` in that directory exits non-zero.
10. Replacing one input digest in the copied provenance record with a
    different value and re-running `verify_command` there exits
    non-zero.
11. Prohibition. No step in the build or release configuration retrieves
    a remote file without an expected digest for that file recorded in
    the tree. The count of retrievals with no recorded digest is zero,
    and altering a recorded digest makes the retrieving step exit
    non-zero.
12. Prohibition. The step that executes project or dependency code
    declares no signing or publishing credential, and the step that
    signs or publishes executes no project or dependency code. Both are
    read off the release configuration.

## Scoring

Twelve binary checks, pass threshold 12 of 12. Partial credit is
recorded for diagnosis only and is not a pass.
