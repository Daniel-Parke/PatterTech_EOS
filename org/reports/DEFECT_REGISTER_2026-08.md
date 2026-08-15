---
summary: Every defect and contradiction the audit raised, what it turned out to be, and where each one now stands
type: org
tags: [eos]
---

# Defect register, August 2026

Raised by the audit pass that opened `eos/audit-research-expansion` and
kept current through it. Four of the seventeen opening findings did not
survive checking, and they are kept here with what was actually true,
because a register that quietly drops its wrong entries teaches nobody
anything.

Status vocabulary: **fixed**, **disclosed** (the gap stands and is now
stated where a reader looks), **wontfix** (with the reason), **wrong**
(the finding itself was not true), **open** (scheduled, named here).

## Fixed

| Id | Defect | Resolution |
| --- | --- | --- |
| F2 | All 22 drills carried `pass: null`, and their stored reasons named grader paths that now hold graders | 22 rows appended 2026-08-15 with real verdicts. The ledger is append-only, so the old rows stand as history and the README says which is which |
| F4 | A derived view could record "Git facts unavailable in this working copy" from a git working copy, invisible to E011 and S007 | Check S020, five tests, one asserting the blindness directly |
| F6 | CI installed `jsonschema pytest` unpinned while the repo maintained a hash-locked file README told readers to use | CI installs from the lock. The cause was deeper than CI, see N1 |
| F8 | `claim_expiry_hours` and `renewal_window_hours` read by nothing, and undisclosed beside a `max_lanes` that was disclosed | Stated in `OPERATORS_GUIDE.md` |
| F9 | `seed-v2-S` was the one seed fixture no test ran the seed series over, and the worked example pointed readers at it | Tested, and the example explains why nine files against a fourteen-row matrix is correct |
| N1 | The lockfile carried one hash per package, so `--require-hashes` failed on three of the four platforms CI builds | `gen_lock.py` downloads per target and carries every hash. Proven before and after, not assumed |

## Disclosed, not closed

| Id | Defect | Where it now says so |
| --- | --- | --- |
| F1 | Routing at record creation reads declarations and no diff. 21 of 25 records ruled R0 from an empty fact set; on 22 the ruled tier came out below the proposed tier | `task new` separates "nothing declared" from "nothing fired", surfaces a proposal the facts do not carry, and names the merge gate as a command somebody runs. Whether that gate becomes a check binds across the estate and needs an ADR |
| F13 | Only S006 checks a pack, and only that three organs exist. Six of the eleven definition-of-done points are review-held | `org/reports/CONTROL_ENFORCEMENT.md` |

## Wontfix, with the reason

| Id | Defect | Why it stands |
| --- | --- | --- |
| F3 | `INDEX.md` summarises two frozen drills as "Proposed". Both are frozen with hashes and one is a Wave A independent oracle | The index is derived and correct; the stale word is inside the spec's own front-matter, and the spec's hash is the independence guarantee. Breaking a Wave A hash to fix one word is the wrong trade |
| F10 | There is no seed compiler in code. `inception/COMPILE.md` is a prose spec an agent executes | Out of scope for this mission and recorded as such. The detective control, D001 to D011, catches what matters |

## Wrong

| Id | What was claimed | What is true |
| --- | --- | --- |
| F7 | The single SLSA evidence record was likely stale, since slsa.dev shows v1.0 retired and v1.2 current | `EV-0038` already reads `SLSA v1.2`, `v1.2 (approved; v1.0 retired)`, accessed 2026-08-02. The finding was inferred from a web fetch without reading the record. Its real weakness is a dated review of `2028-08` on a spec line that moved twice, which is freshness work, not a version fix |
| F5 | The ablation files say the overlay is not wired while eight ledger rows carry the `v2-no-router` variant | Not a contradiction. All eight are dated 2026-08-03, inside the batch the changelog already keeps as history, and `--variant` was a label nothing upstream read. Recorded on the file through a freeze amendment |
| F15 | `counter_evidence` is null on 208 of 504 records, against definition-of-done point 10 | Point 10 is a pack-level requirement, not a per-record one. Of 149 empirical records, 23 carry a null. The other 185 nulls sit on standards and vendor documentation, where no counter-evidence is frequently the honest answer |
| N5 | `api-integration` c1 passes an untouched tree, so it fails to discriminate | It is a regression guard on a file the drill hands the agent to edit. Three other passing criteria are prohibitions an idle agent has not breached. No grader was demoted |

## Open, and where each is scheduled

| Id | Defect | Scheduled |
| --- | --- | --- |
| N2 | `packs_adopted` is `[]` in both seed fixtures and "None" for all three ventures. The pack-adoption path has never run end to end, so activation is proven only against diffs in this repository | Activation machinery |
| N3 | `licence` carries 249 distinct values across 504 evidence records, including three spellings of Apache-2.0. Realised taxonomy drift, with a single writer | Research programme |
| N4 | `GOVERNANCE.md` says the checker enforces bidirectional supersession. S002 reads markdown front-matter only; the evidence ledger has no supersession fields | Research programme |
| F11 | Session 0 pack selection is a by-hand walk. `eos context` evaluates activation globs against a diff in this repository and has no brief mode | Activation machinery |
| F12 | `packs/INDEX.md` carries `applies_when` but not `activation_paths`, which is the half that is evaluated | Activation machinery |
| F14 | No pack owns data engineering, database and storage selection, migration and compatibility, identity and authorisation, observability and SLOs, local-first, or reproducible computing. In the ledger: SLSA 1 record, sigstore 1, in-toto 0, SBOM 0, CycloneDX 0, TUF 0 | Knowledge-base expansion |
| F16 | `delivery-testing` has zero `GD-` guides. `agentic-swarm`, the pack the estate itself runs on, has no frozen drill | Knowledge-base expansion |
| F17 | Every prose count is hand-written and unchecked: "513 tests" appears four times, "504 rows" five, "twenty-one packs" five. All are accurate today | 1.0 gate. Generated or checked, or it rots |
| F7b | 22 evidence rows are `stale` and one is `url-dead`. 268 of 504 carry an `on-change-of:` review that F002 skips by design, so nothing watches them | Research programme |
