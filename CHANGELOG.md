---
summary: One entry per release tag, sectioned by area
type: governance
tags: [eos]
---

# CHANGELOG

Newest first. One entry per release tag; the Unreleased section
accumulates until the next tag. Sections: kernel, packs, governance,
inception, registry, org, tools, benchmark.

## Unreleased

ADR-0007 holds v2 unreleased and folds v2.1 into the same line, so
everything in this section ships as one release. All three entries stay,
newest first. Nothing in v2.1 supersedes the v2 record of how the
benchmark instrument was rebuilt, and that record is the reason the
gate table below reads the way it does.

### The release tidy

The last pass over the tree before the release commit. It added no
capability. It took out things that were not doing any work, fixed what
it found broken, closed the record, and rewrote the documentation
against the tree as it now stands. No benchmark run was made, because
ADR-0007 makes none, so nothing here is measured.

- **tools**: dead code out. A fallback import branch in
  `tools/eos/taskops.py` reimplemented `Finding` and `Findings` against
  the canonical module being missing. It sits in the same package and is
  never missing, so the branch could not run. `benchcli.runner` wrapped
  `benchmark/runner.py`, and the two benchmark ops the CLI exposes drive
  `harness.py` and `score.py`, so nothing but its own test reached it.
  Several functions had no caller in the tooling, kept alive by their
  own tests where they had any: `Findings.extend`, `to_json` and
  `exit_code`, and `branch_heads`, `changed_files` and `numstat` in
  `gitfacts.py` with the private helper only those three used. Two
  deliberate duplicates go with them. `migrate.py` carried its own
  front-matter reader, kept during the build to avoid coupling lanes
  that have since merged, and `router.py` and `contextgen.py` each
  carried a copy of the same git helper. Both now call the canonical one.
  Then three real bugs, all found by reading rather than by a failing
  test. `remote_tracking_heads` filtered the remote's symbolic HEAD on the
  short refname, which renders `refs/remotes/origin/HEAD` as plain
  `origin`, so the filter never matched once and the pointer entered
  the result as a remote with no branch. `migrate apply` took its seed
  path from a key the migration-state schema does not permit, so the
  documented invocation could never run and always refused; it now asks
  for `--seed` and says why. S009 read a month-only `next_due` as the
  first of that month, so a cadence due in a month reported overdue from
  the second day of it, which is every monthly row for most of its
  month. 504 tests, up from 464.
- **org**: org/QUEUE.md and org/CADENCE.md are deleted, so neither is a
  path any more. Each was a signpost to a signpost, pointing at the
  machine state that had already replaced it, and what they said past
  the pointer had gone stale: the cadence one described three rows where
  the file it pointed at now holds one. `org/cadence.json` is cut to that
  single monthly row, matching the one monthly pass ADR-0008 left
  standing. Twenty-one task records reach a terminal state, twenty done
  and T-0003 discarded with its reason, so every record under
  `org/tasks/` is now closed.
- **packs**: the delivery-testing decision map loses four forks that
  routed at v1 wargames this tree does not contain. Three are answered
  inside the pack instead, and the fourth, what visual regression
  covers, is answered by no pack in this estate and now says so. Five
  worked exemplars take the `EX-` ids the scheme requires:
  `EX-API-001`, `EX-API-002`, `EX-ARCH-001`, `EX-SEC-001` and
  `EX-UIUX-001`.
- **registry**: five evidence rows now carry what the swarm pack cites
  them for. Six of that pack's fifty-two research records matched a URL
  already in the ledger, so the import merged them into the older row
  and kept the older summary; for five of the six that summary did not
  contain the claim the pack rests on it. EV-0013, EV-0053, EV-0108,
  EV-0112 and EV-0244 carry both statements now. In the lessons ledger,
  LES-0012 and LES-0014 stop being deferred: the tasks they were waiting
  on, T-0005 and T-0006, landed in `inception/INCEPTION.md` and
  `inception/WALK_ORDER.md`, so both rows are pruned to provenance.
- **roots**: `README.md`, `TOUR.md` and `OPERATORS_GUIDE.md` rewritten
  against the settled tree. TOUR gains two things the repository was
  using and had defined nowhere: the words it uses in a particular way,
  and a table of the eleven lesson dispositions.

Nothing here settles the release gate. Of the five items ADR-0007
decision 5 names, three are in the tree to be checked: the suite is
green at 504, this section is the CHANGELOG, and the checker's remaining
errors are all derived views stale against their sources, which
regenerating clears. The other two, that no false statement about the
tree survives the final review and Daniel's approval under PB-E05, are
his alone.

### v2.1 · Genesis, the swarm pack and the de-restriction pass

Built under ADR-0006 (Genesis, the study workflow, the lessons ledger,
the swarm pack, staged verification, hands-off ventures, Apache-2.0 and
the provenance sweep), ADR-0007 (one release) and ADR-0008 (less law,
better kept). No benchmark run was made during this work, so nothing
below is measured against v2. What is claimed is what the tree now
does, not what it achieves.

- **kernel**: Genesis gets five blueprint templates in the seed:
  PRODUCT_MAP, ACCEPTANCE_SPINE, WORK_PACKAGE, RESEARCH_PACKET and
  LENS, with scale-matrix rows at S and ORG so a compiled seed carries
  the blank forms whether or not the operator runs the phase.
  `kernel/templates/org/GRAPH_BUILD.tpl.md` carries the swarm method
  into an ORG seed, ORG only, because it names `org/claims.json` as its
  mutex. The venture brief gains a material-workstreams section, which
  is what Genesis cuts its packages from. The metadata spec gains a
  ninth axis, `conflicts_with`, which names what an artefact contradicts
  and obliges a settling, and it tightens the authority test to match
  ADR-0008: `basis: decision` on its own no longer earns binding, and
  the two protected-set floors are exempt by where they sit rather than
  by what their basis field says. The policy spec's irreversible-action
  factor now names a declared rollback cost beside a declared
  irreversible action, and the seed rubric gains A15 and A16 for the two
  new seed checks. ADR-0008 decision 7 lands in the same file: the
  per-kind minima table shrinks to the axes that change what an agent
  does, `authority`, `applies_when`, `sources` and `review`, on top of
  the summary, type and tags E002 asks of every markdown file, and the
  derived-defaults table beside it is rewritten to match. Both tables
  now say which parts a check actually reads, because most of that spec
  is law here and unenforced.
- **inception**: Genesis returns as a defined phase in
  `inception/GENESIS.md`, and the word is glossed there because in v1 it
  named the AutoWatt origin story and a reader meeting both senses
  cannot tell which is meant. The launch decision sits at the gate:
  either Genesis runs, or the sign-off block carries one line saying why
  not. The templates ship in the seed either way, so a venture that
  declines can run the phase later without a recompile. The interview
  gains an eighteenth question, the material workstreams.
- **packs**: `packs/agentic-swarm` is the twenty-first pack: ten binding
  requirements, four guides, a risk register and a counter-evidence
  section running to a hundred lines, because the strongest result in
  its own corpus points away from swarms. On a normalised substrate,
  five of six multi-agent systems scored below a single-agent baseline
  while costing more, and the pack carries that in the body rather than
  a footnote. Verification is staged by risk and stability instead of by
  a completeness percentage, and the pack states plainly that the
  staging default is argued and never measured: no controlled comparison
  of building the comprehensive harness early against building it on
  stability signals was found. The coding pack splits B1. Oracle
  independence still binds. The ordering clause that made test-first
  doctrine is now a default, with a section saying what the demotion
  costs.
- **governance**: the ADR-0008 de-restriction pass. A rule stays binding
  only where it prevents a serious or hard-to-reverse failure and rests
  on law, a standard, empirical evidence or a protected-set floor.
  Every loosened rule names what catches the failure instead: claims
  scale with concurrency, and git history catches the solo case while
  the unchanged claim refusal still catches parallel lanes; task records
  are required for gate-bearing work, meaning R2 and above and anything
  touching the protected set, and the commit message is the record for
  the rest; four monthly cadences become one pass with four sections,
  and a skipped section is still a finding. Both loosenings are in the
  checker: E007 warns on a budgeted type over 150 lines whether or not a
  `length_waiver` is present, so the waiver names the reason rather than
  changing the severity; E009 warns on a tag outside the list, which is
  now the known set rather than the permitted set. The
  forty-line cap on `AGENTS.md` and `CLAUDE.md` stays an error on
  purpose, because that file sits in every agent's context and its cost
  is paid on every task. Untouched, and said so the loosening cannot be
  read as general: the safety floors, the derived-file rule, append-only
  decisions, bidirectional supersession and the promotion ladder. The
  repository is declared Apache-2.0, with `LICENSE` and `NOTICE` at the
  root and a provenance sweep of twenty-one packs behind it.
- **governance**: the authority audit ran over 109 binding requirements
  in seventeen packs and moved 48 of them to defaults. Thirty-four of
  the 48 keep their B numbers, in eight packs, because the checks,
  guides and exemplars cite them. The other fourteen were renumbered
  into their own pack's defaults block: ai-ml-llm, api-integration,
  architecture, business-logic-modelling, business-model-pricing and
  data-analytics each moved every rule it demoted, and updated the
  citations. Binding now, against what each pack carried before:
  agentic-development 4 of 7, ai-ml-llm 5 of 7, api-integration 4 of 6,
  architecture 3 of 5, business-logic-modelling 2 of 5,
  business-model-pricing 4 of 6, data-analytics 3 of 6,
  docs-dx 1 of 6, legal-licensing 4 of 7, native-client 3 of 7,
  product-discovery 2 of 8, support-operations 2 of 7, ui-ux 5 of 8,
  writing-content 5 of 10. Coding, delivery-testing and
  marketing-growth were audited and lost no whole requirement.
  `packs/pattertech-house` had none to test: no line in it was ever
  binding. `packs/security-privacy` B1 to B6 are excluded by name as
  protected-set floors. `packs/devops-reliability` was not audited, and
  the pack carries no note saying so: nobody ruled which of its seven
  count as the production-safety rules the exclusion protects, and four
  of them are process rules that would move on basis alone.
- **registry**: `registry/lessons.json` becomes the canonical lessons
  ledger, twenty-five rows, and `registry/LESSONS.md` becomes a derived
  view with a live generator. Rejections are retained rather than
  deleted, and the view has a section for each state: fifteen live, one
  rejected, nine pruned and, since the release tidy closed the last two,
  none deferred. A ledger that keeps only what it
  accepted cannot show what it turned down, which is how the same
  candidate gets argued twice. The evidence ledger grows from 449
  records to 504. `registry/LICENCE_RESIDUALS.md` is new: the cited
  sources whose licence is unknown or not stated, with what the
  provenance sweep confirmed and what it did not.
- **org**: two playbooks. PB-E11 studies an exemplar, starting from a
  lens contract agreed before anything is read, with lawfulness settled
  first and candidate lessons landing in the ledger. PB-E12 is the
  venture check-in, venture-initiated only: the EOS never schedules one
  and never offers one unasked, it returns findings and candidate
  lessons, and it changes nothing in the venture. The four monthly
  cadences collapse into one monthly pass with four sections, harvest
  first because the promotion review reads what the harvest queued.
  ADR-0006, ADR-0007 and ADR-0008 accepted.
- **tools**: five checks added. S018 makes a lesson that names a
  contradiction record how it was settled, so a ledger of decisions does
  not become a ledger of arguments nobody had. S019 validates the
  lessons ledger against its schema, requires unique ids and resolves
  every evidence id it cites. D010 fails an ORG seed that carries no
  file compiled from a Genesis blueprint, and stays quiet against a seed
  pinned before the templates existed. D011 reads whether a compiled
  acceptance spine still carries the marking an outstanding condition
  fails by, since a suite that cannot say a condition is outstanding
  reads as an acceptance walk already passed. E011 compares
  `org/TASKS.md` and `org/STATE.md` against the generator that owns
  them, which is the hole `packs/INDEX.md` sat in. Two checks removed:
  E010, which warned about a stale `active_session` in `org/STATE.md`,
  and S008, the opt-in canonical-fact check that had no subscribers and
  had never fired. `tools/import_fragments.py` gains a study
  subcommand for the intake PB-E11 writes. 464 tests, up from 395.
- **benchmark**: ADR-0007 settles the release gate, because the gate set
  ADR-0002 approved can no longer be computed. The context-token and
  wall-clock gates are struck with reasons, not met: on the reproducible
  2026-08-08 batch they came in at 9.1 per cent against a 30 per cent
  threshold and 4.6 per cent against 25, the system they were written to
  judge has since changed shape, and no run was made against v2.1. So no
  measurement of the evolved system exists, and a struck gate is not a
  met gate. Moving the thresholds to match the figures already achieved
  would be tuning the target to the result, which is the dishonesty the
  pre-release review removed. `SEALED-BENCH-2026-08` is retired
  unopened: it runs once, it needs Daniel's key, and it was authored for
  a frozen-v1 against final-v2 comparison this decision supersedes. It
  stays in the tree with its hashes, so the record of what was and was
  not measured survives. The pack-drill gate is not a release blocker
  and its 22 drills still hold 22 null verdicts. What the line offers as
  evidence is delivery quality on that batch, 50 of 50 v2 runs fully
  passing against 39 of 53 under v1. Efficiency is offered as unmeasured
  and safety and per-task regression as unmeasured, both of which
  depended on the sealed suite. That is a real reduction in assurance
  against the plan ADR-0002 approved, accepted knowingly.

### v2 · the overhaul

The v2 overhaul, built under ADR-0002 and corrected under ADR-0003.
Held at the release checkpoint.

The first gate run reported three of six numeric gates missed. The
2026-08-04 pre-release review found that no code computed any gate
figure, that one gate's verdict turned on an unwritten convention for
an undefined ratio, and that the freeze manifest failed its own hash
check. The 2026-08-08 review found something larger: nothing in the
repository ever made a run v1 or v2. `--variant` was a label
`score.py` wrote onto a ledger row and nothing upstream read, and ten
of the fourteen tasks use a fixture carrying no process files at all,
so both arms received a byte-identical tree and prompt. The sessions
behind those rows were driven by an orchestration wrapper that was
never committed. The 172 rows dated 2026-08-03 therefore cannot be
reproduced from this repository and are kept as history rather than as
the basis of any claim.

The instrument is rebuilt, the mechanism encoded, and a fresh grid run
under it: all 103 sessions, 53 under v1 and 50 under v2, every slot at
or above the protocol's floor of three trials a variant, so the
completeness gate passes for the first time. Ceremony falls 77.3 per cent against a 60 per cent
gate, and no longer turns on the undefined-ratio convention that
decided it before. Context tokens fall 9.1 per cent against 30 and
wall clock 4.6 per cent against 25, so both efficiency gates still
miss. The result that is not on the gate list: fifty-three v1 runs
produced fully passing work thirty-nine times, and fifty v2 runs
produced it fifty times. See org/reports/V2_FINAL_REPORT.md.

- **kernel**: ten-article constitution; EXECUTOR, ORACLE and REVIEWER
  replace the PLAN, WORK and VERIFY trinity; policy and cadence become
  JSON; the scale matrix moves to S and ORG, with a seed resolving
  whichever matrix its pinned commit carries. Ten v1 templates retired
  with every load-bearing rule's destination recorded.
- **packs**: doctrine becomes twenty progressive-disclosure packs across
  the estate's domains, each meeting an eleven-point definition of done.
  The house visual language becomes an opt-in preference pack, so a
  venture can choose another design philosophy without deviation
  machinery. WG-DEL-005 is written at last, with 006 and 007 beside it.
- **governance**: graded evidence path (experiment, ADR) replaces
  wargame-first; precedence scopes venture rulings locally and protects
  law and standard based rules from vote counts; the protected set
  narrows to ten items with security-privacy as canonical home for
  four of them.
- **tools**: one 445-line script becomes a tested package behind
  python -m tools.eos, with structural, semantic, seed and freshness
  checks, the deterministic router, the fail-closed guard, context
  packets, task and claim operations, migration and benchmark commands.
  395 tests on Python 3.11 and 3.14. The v1 checker is a forwarding shim.
- **benchmark**: a frozen suite of eleven tasks and three probes, an
  evidence ledger of 449 individually recorded sources, and a sealed
  final suite awaiting the operator's key. `gates.py` computes the
  gates from the ledger with its aggregation written down, including
  both conventions for an undefined ratio; check B001 verifies the
  freeze on every run; `score.py` records a scored-at clock and a
  sha256 per criteria script; `harness.py` prepares a run, places the
  variant's process surface, and emits the whole grid in a seeded
  counterbalanced order, which the protocol required and the first
  batch did not do. The process surfaces are the frozen paired seeds
  taken verbatim, so the ceremony difference between arms is whatever
  each version's kernel already produces rather than a choice made by
  whoever built the harness. Two gates were themselves wrong: the
  aggregate pass-rate gate was symmetric and failed a candidate for
  scoring better than its baseline, and `human_gates_pending` reads a
  file nothing in this repository writes, so every zero it has ever
  reported means "not measured".
- **governance**: ADR-0003 rules that retained material which misleads an
  agent is a defect, that the archive of record is a pushed tag rather
  than a directory, and that a file marked derived must have a live
  generator. packs/INDEX.md had listed eight of twenty packs, so twelve
  packs were unreachable through the sanctioned activation path;
  packs/GUIDE_INDEX.md had omitted 79 of 86 guides. Both now generate,
  scoped to live material. registry/coverage.json's twelve stale Wave B
  rows are repaired and S013 validates the matrix against its schema and
  against the packs on disk.
- **inception**: Session 0 becomes a pack activation walk with a risk
  surface map, plus an Express path for reversible S ventures.
- **org**: the EOS runs on its own v2 machinery: policy, task records,
  committed claims, generated views. v1 org files archived verbatim.
- **tools**: the repository hashes its own files, and it was hashing
  the checkout rather than the content. Merging v2 and checking out
  `main` turned a clean tree into 108 B001 errors on a repository
  where nothing had been edited: `core.autocrlf=true`, the default a
  Windows install sets, rewrites text files to CRLF on the way in, and
  the freeze verifier hashed the raw bytes. A fresh clone would have
  shown a new reader the same thing on their first command. Every one
  of the 130 frozen files was confirmed byte-identical to its recorded
  form once the checkout transform is undone, and none was modified.
  Three fixes, because one alone leaves a hole: `.gitattributes` pins
  the working tree to LF so a clone is the same on every platform, the
  freeze and drill hashers normalise line endings so the check
  survives a tree that predates it, and the manifest's 21 entries that
  had been recorded from a CRLF tree on 2026-08-08 are re-recorded on
  content. `write_indexes` compared derived files with `read_text`,
  which applies universal newlines, so a CRLF derived file read back
  equal to the LF text it generates and was never rewritten; it now
  compares and writes bytes.

## Superseded, towards v1.1.0 (never released)

- **roots**: GUIDE.md added, the all-in-one field guide. A teaching
  layer over the whole system (framework, the AutoWatt genesis, the
  development lifecycle) that cross-links to the canonical files rather
  than duplicating them, so it stays honest under the one-writer-per-fact
  rule. Session S-0020. Additive; the pointer lives in README.md.

## v1.0.0 · 2026-07-07

The founding release: the full kernel, the inception system proven by
a cold drill, five doctrine modules, the estate registries and the
check tool, built across sessions S-0001 to S-0018 per ADR-0001. The
folder rename to PatterTech_EOS, the private remote and the tag push
are the operator's manual close (OPERATORS_GUIDE troubleshooting has
the commands).

- **org**: ADR-0001 accepted, the v1.0 architecture. The EOS now runs on
  its own lite kernel (state, queue, cadences, playbooks, logs).
- **doctrine**: modules/ became doctrine/. Wargames renamed to
  module-prefixed IDs (WG-WEB-001 to 014). Cost and hardware stubs
  retired to roadmap rows. MODULE_SHAPE.md added. v4 web-design
  learnings captured (heading sweep, live rule, WG-WEB-013, WG-WEB-014).
  C2 populated the voice module: the seven-rule voice law with
  examples, the banned-list pattern, and WG-VOX-001 (audience register,
  default professional-calm), walked in every Session 0. F1 populated
  the architecture module: seven binding rules, eight WG-ARCH wargames
  argued from the estate's ADRs (boundary enforcement, ORM or raw SQL,
  derived state, job execution, the contract seam, proof of harmless
  change, vendor seams, database topology) and the ADR template. F2
  populated the delivery module: six rules including gate-is-a-rubric,
  and WG-DEL-001 to 004 (coverage ratchets, e2e weighting, VRT scope,
  flake policy). F3 populated the devops module: six rules (migrations,
  local parity, secrets, no console-clicking, proven restores, cost as
  design input) and WG-OPS-001 to 004 (hosting, containers, backups and
  restore, cost ceilings).
- **kernel**: created with the compile contract; LOCKBOOK.tpl.md
  migrated from the v0.1 project lock-in, full templates due in Phase B.
  D2's harvest amended two templates from reseed feedback: the
  constitution footer's AMENDMENT_HISTORY slot and the compile report's
  normalised and preserved ancestry row kinds.
  B1 landed the org templates from AutoWatt@d2e3250: the constitution
  (product-doctrine slot, Parts II and III renumbered per part), START
  and the three role charters, the three-strikes rule woven through,
  scale fences specified with a closing marker in kernel/README.md.
  B2 added the operating model (tiers and gates collapse at M scale),
  the canonical artefact formats including the M queue-row shape, STATE
  with the claim protocol and Resume Packet spec, the cadence schedule
  (founder update generalised to stakeholder update) and the questions
  queue. B3 added the venture router (compiled cap 40 lines, S points
  at the lock-book and worklog, M and L at the org), the operators
  guide with per-scale launcher libraries, and the playbook catalogue
  PB-001 to PB-051. B4 closed the phase: SCALE_MATRIX (S eight files, M
  eighteen, L nineteen plus empty dirs, trigger add-ons), SEED_RUBRIC
  (auto items A1 to A10 keyed to check IDs, human items H1 to H5 headed
  by the cold-start test), the lock-book rebuilt with the machine
  rulings header, and the venture brief, feedback, compile report,
  worklog, queue and NEXT templates.
- **inception**: shape fixed, system due in phases C and E. C1 landed
  COMPILE.md (prune, fill, distil, report, and the compiler's
  never-list) and WALK_ORDER.md (trigger-filtered walk, canonical
  module order, the draft-wargame escape, the twenty-ruling budget
  alarm). E1 completed the system: INCEPTION.md (phases A to E),
  INTERVIEW.md (twelve questions, three challenge steps), WG-EOS-001
  (venture scale, six triggers, argued rulings from AutoWatt and the
  website) and WG-EOS-002 (repo shape, default monorepo, estate
  rulings). E2 ran the S-scale drill cold and passed it: seed check
  green first run, the cold-start test passed live, and the findings
  fixed the lifespan clause, the spend and concrete-facts interview
  gaps and the walk budget, with S ergonomics and four house-brand
  default assumptions queued as E3 and E4. The canned brief lives at
  inception/briefs/BRIEF-S-brochure.md.
- **registry**: created; projects, vendors, lessons and the static web
  stack profile seeded. D1 updated the AutoWatt row: reseed compiled to
  a green seed check on branch reseed/eos-v1, awaiting the rubric
  signature.
- **tools**: eos_check.py added (checks E001 to E010, --repo and --seed
  modes, index generation).
- **roots**: AGENTS.md canonical with CLAUDE.md byte parity, START.md
  entry modes, GOVERNANCE.md, OPERATORS_GUIDE.md, evolved VISION.md.
