---
summary: EOS v2.1, the Genesis blueprint phase, the exemplar-learning workflow, the agentic-swarm pack, hands-off ventures and staged verification
type: decision
tags: [eos]
status: accepted
decided_by: Daniel Parke
date: 2026-08-10
---

# ADR-0006: Genesis, exemplar learning and the swarm pack

The operator approved the v2.1 plan on 2026-08-10 and accepted this record in
principle before it was drafted, on the terms set out in that plan's
interview. This record is the authorisation for every protected-set
change the v2.1 build makes. ADR-0002 stands as the operative
architecture; this extends it and supersedes nothing.

## Context

Three findings drove this.

**v1 had a step v2 lost.** v1's PB-001, Genesis, turned a signed seed
into a buildable organisation: domain model, architecture, roadmap,
standards, decision records, full specifications and a foundation-first
backlog, with the acceptance walk-through written as a deliberately
failing suite that went green journey by journey. It ran for real twice.
v2 dropped it with no migration row, while `org/migration/MIGRATION_MAP.md`
claims nothing was dropped silently, and five live files still cite it. A
venture now falls from a signed seed straight into ad-hoc task intake.

**The learning loop only reads documents.** The evidence ledger, the
fragment import and the harvest playbook work, and one harvest has run
for real. But nothing can study a product, a repository, a game or a
postmortem; a rejected lesson leaves no trace, so it can be re-proposed
forever; contradictions are found after adoption rather than at intake;
and there is no lens contract, so nothing records what was studied and
what was deliberately not.

**Building with agent graphs is the method and it is undocumented.**
Twenty packs cover venture domains. None covers how we ourselves fan work
out over a dependency graph, which is now the primary way the estate is
built. Research for this decision gathered 232 sources; the strongest
finding is that structure pays and parallelism alone does not.

## Decision

1. **Genesis returns, scale-graded, as a compiled hand-off.**
   `inception/GENESIS.md` defines one phase, run in the venture repo
   after the seed gate, producing bounded research packets, a product
   map with a dependency graph and contracts, work packages with context
   packets and acceptance conditions, and a failing acceptance spine. Its
   templates compile into every seed; running it is the operator's launch
   decision, full form the ORG default and a lite form at S. The word
   Genesis means this and nothing else; the v1 sense is history and is
   glossed wherever it is cited.

2. **The Study workflow, PB-E11.** Lens contract before study; the study
   session is the only one that reads the raw source and freezes the
   corpus first; findings separate observation, sourced fact,
   interpretation, inference and recommendation, and are extracted as
   principles, patterns, techniques, failure modes, decision forks and
   reference material; a conflict pass against packs, registries,
   policies, governance, the inception process and prior lessons runs
   before the operator sees anything; his decisions become lesson rows.

3. **`registry/lessons.json` becomes canonical**, with
   `registry/LESSONS.md` derived. Rows carry an origin discriminator
   (study rows cite an evidence id and a lens; harvest rows name the
   venture), the lesson, evidence class, disposition, scope,
   applicability conditions, machine-readable links (`informs`,
   `conflicts_with`, `supersedes`, `superseded_by`), the decision date
   and the operator's reasoning. Rejections are retained with their reason.
   Dispositions: reference-only, dated-registry-fact, venture-ruling,
   worked-exemplar, implementation-reference, experimental-guidance,
   decision-guide, estate-default, binding-candidate, rejected,
   deferred. Binding is never a disposition the workflow assigns, only
   one it proposes, and the ladder in `GOVERNANCE.md` is unchanged.

4. **`packs/agentic-swarm/`, the twenty-first pack**, plus
   `kernel/templates/org/GRAPH_BUILD.tpl.md` compiling its executable
   half into ORG seeds. Its governing rule: fan out over a measured
   dependency graph with one integrator and an external verifier that
   predates the lanes. Its counter-evidence organ carries the results
   that argue against swarms, including a normalised ten-benchmark study
   in which five of six multi-agent systems scored below a single-agent
   baseline while burning 24 to 286 per cent more tokens. The existing
   agentic-development pack keeps its scope, agent systems built into
   venture products, and the two cross-link.

5. **Verification is staged by risk and measured stability, never by a
   completeness percentage.** Risk floors from day one; cheap executable
   checks always; contract tests when an interface is declared stable;
   the comprehensive harness assembled on stated stability signals,
   derived from the map and specifications rather than from the code,
   authored or reviewed independently of the implementing agent, and
   mutation-checked before it blocks. `packs/coding` B1 demotes from
   binding to default: no rule requires tests first. What binds is the
   remainder, and it is narrower and better evidenced: the artefact that
   decides whether a change is correct must not be authored by the agent
   holding that implementation in context. Prompting a model with the
   buggy implementation cuts bug-revealing tests by about two thirds
   against giving it the specification instead; forcing a frontier model
   to write tests across about 500 benchmark tasks changed the number
   resolved by zero. Ordering is ceremony; independence is not.

6. **The EOS hands off at venture birth.** It compiles a seed and a
   blueprint and stops. Ventures diverge freely. A venture-initiated
   check-in, PB-E12, returns findings and candidate lessons and applies
   nothing. The EOS never initiates. This is stated in `README.md`;
   `GOVERNANCE.md` is not changed by this record.

7. **Apache-2.0**, declared at the root and in `tools/pyproject.toml`,
   with a provenance sweep behind it: each pack's prose checked for
   carried expression beyond fair quotation, each cited source's licence
   confirmed as a recorded fact rather than a guess, a NOTICE file, and
   an honest residual list of sources whose licence is unknown or
   not-stated. No source is re-fetched wholesale and no licence is
   invented.

8. **The dead-weight cut.** Every mechanism found doing nothing is
   removed or honestly re-scoped, and every false statement found in the
   live tree is corrected. The per-file list is in the v2.1 plan and in
   the lane task records T-0014 to T-0025.

## Protected-set changes authorised

- `kernel/POLICY_SPEC.md`: the venture-stricter-factors sentence
  re-worded to describe what the router actually consumes.
- `org/policy.json`: the retired paths `doctrine/` and `GUIDE.md`
  removed from `path_patterns.reversible`; the two declared side effects
  that reach no factor (`writes-production-data`, `rollback-cost`) wired
  into the factor table in `tools/eos/router.py` and the spec's table.
- `packs/security-privacy/PACK.md`: B3 and the choices list re-pointed
  from the withdrawn exception ledger to the task record, matching
  ADR-0005's correction to the reviewer charter. No binding requirement
  changes meaning.
- `kernel/METADATA_SPEC.md`: a `conflicts_with` axis added, so a rule or
  lesson can name what it contradicts in machine-readable form. Adding a
  front-matter axis routes through the ADR path under ADR-0004.

The authority audit run under ADR-0008 never touches a safety floor:
`packs/security-privacy` B1 to B6 and the production-safety rules in
`packs/devops-reliability` stay binding whatever it finds elsewhere.

## Counter-evidence and applicability limits

The research behind decision 4 is not one-sided and the pack says so.
Multi-agent systems underperform strong single agents on a normalised
benchmark suite; per-agent reasoning goes thin beyond three or four
agents under a fixed budget; coordination cost grows superlinearly; once
a single agent already succeeds often, adding agents makes it worse; and
no public benchmark measures the specific architecture this decision
adopts, so the EOS's own runs will be the best evidence it has. The
decision rests on the narrower finding that cohesion-aware partitioning
over a real dependency graph with one integrator beats sequential work,
and on the fact that the estate's own two parallel builds worked.

Decision 5's staging is a default, reversible per venture, and its
stability signals are starting values rather than measured thresholds.
The claim that deferring breadth reduces waste without raising escaped
defects is a hypothesis this decision labels as one.

## Reserved

Release remains a separate approval under ADR-0007. Nothing here
authorises a write to a venture repository, a tag, or a push to main.
