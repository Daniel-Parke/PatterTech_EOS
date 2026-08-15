---
summary: Activation, outcomes and decision map for the docs-dx Doctrine and Wargames
type: playbook
tags: [content, voice, delivery, ci, tooling]
kind: record
authority: none
lifecycle: active
basis: decision
evidence_grade: not-applicable
scope: estate
applies_when: [publishes_docs, documents_executable_surface, emits_user_visible_failure, renames_or_deletes_documented_page]
activation_paths: [**/README.md, **/docs/**, **/*.md, **/CONTRIBUTING.md, **/CHANGELOG.md, **/Makefile]
volatility: slow
review: none
sources: [EV-0023, EV-0044, EV-0095, EV-0102, EV-0136, EV-0137, EV-0170, EV-0171, EV-0175, EV-0189, EV-0322, EV-0323, EV-0324, EV-0325, EV-0326, EV-0327, EV-0328, EV-0329, EV-0330, EV-0331, EV-0332, EV-0333, EV-0334, EV-0335, EV-0336]
depends_on: [writing-content, coding]
---


# docs-dx

This pack covers documentation and the developer experience around it:
where a document's truth lives, which documents can be made to fail a
build, and what a failure message owes the person reading it. It
activates on any task that writes or changes documentation, renames or
deletes a documented page, cuts a release, or adds a user-visible
failure. Only one rule binds, that generated reference is regenerated
and never hand-edited. Link integrity, snippet execution and
error-message content are defaults. Prose style is taste.

## Activation

Load this pack when any of the following is true.

**Paths touched.** `README.md`, `AGENTS.md`, `CLAUDE.md`,
`CHANGELOG.md`, anything under a docs, doc, guides, site or handbook
tree, any other Markdown, AsciiDoc or reStructuredText file outside a
vendor directory, doc comments and docstrings, generated reference
outputs and the templates that produce them, documentation CI
configuration, and the handlers that produce user-visible failure text.

**Task types.** Writing or changing documentation. Renaming, moving or
deleting a documented page. Changing a flag, command, endpoint or
configuration key that documentation names. Cutting a release. Adding
or rewording a user-visible failure. Setting up a new repository. Any
task whose acceptance depends on a reader being able to follow written
instructions and succeed.

**Keywords, fallback only.** Readme, docs, changelog, release notes,
quickstart, tutorial, how-to, reference, docstring, onboarding, error
message, link check, style guide, redirect. Keywords are the weakest
signal and never override the predicates.

**Applicability predicates.**

| Predicate | True when |
| --- | --- |
| publishes_docs | the repository carries prose anyone outside the author reads |
| documents_executable_surface | documentation names a command, flag, endpoint or config key |
| emits_user_visible_failure | the software prints or returns a failure a person or agent sees |
| renames_or_deletes_documented_page | the change moves or removes a page something links to |
| releases_to_consumers | something outside the venture pins a version of this |
| has_generated_reference | reference material is produced from a machine-readable source |

A repository that trips a path trigger but satisfies no predicate loads
nothing beyond the first paragraph. Activation gives advice and never
permission: nothing here lowers a tier floor in `kernel/POLICY_SPEC.md`
or turns a manual-only action autonomous under `kernel/GUARD_SPEC.md`.

## Outcomes and non-goals

**Outcomes.** A reader who follows the written instructions gets the
result the instructions promised, and if they do not, a check failed
before they did. A cross-reference that stops resolving fails a build
rather than rotting quietly. Reference material that describes a
machine-readable artefact is derived from it. A failure tells its
reader what went wrong and what to do next, because that is the page
with the highest read rate in the system.

**Non-goals.** This pack does not set house prose style beyond a small
mechanical subset, and it does not own the voice law, which lives in
`GOVERNANCE.md`. API contract design and deprecation policy sit in the
api-integration pack, release mechanics and versioning in
devops-reliability and coding, agent instruction design in
agentic-development. It carries no site generator, no theme, and no
opinion about where explanation lives relative to reference. It does
not measure documentation with a productivity number, for the reason in
Open questions.

## Doctrine

Standing rules are atomic Doctrine files. The labels below are stable
compatibility anchors; they do not encode authority.

<a id="B1"></a>
- `B1` to [DOC-DOCS-001](doctrines/DOC-DOCS-001-internal-links-and-anchors-resolve-checked-in-ci-and-the-check-b.md) (default)
<a id="B2"></a>
- `B2` to [DOC-DOCS-002](doctrines/DOC-DOCS-002-a-renamed-or-deleted-page-leaves-a-redirect-or-every-reference-t.md) (default)
<a id="B3"></a>
- `B3` to [DOC-DOCS-003](doctrines/DOC-DOCS-003-every-executable-snippet-either-runs-in-ci-or-carries-an-explici.md) (default)
<a id="B4"></a>
- `B4` to [DOC-DOCS-004](doctrines/DOC-DOCS-004-generated-reference-is-verified-as-regenerated-not-hand-edited.md) (binding)
<a id="B5"></a>
- `B5` to [DOC-DOCS-005](doctrines/DOC-DOCS-005-every-user-visible-failure-names-the-condition-the-caller-releva.md) (default)
<a id="B6"></a>
- `B6` to [DOC-DOCS-006](doctrines/DOC-DOCS-006-every-repository-carries-an-agent-entry-file-at-the-conventional.md) (default)
<a id="D1"></a>
- `D1` to [DOC-DOCS-007](doctrines/DOC-DOCS-007-use-the-four-documentation-forms-as-a-diagnostic-never-as-a-fold.md) (default)
<a id="D2"></a>
- `D2` to [DOC-DOCS-008](doctrines/DOC-DOCS-008-a-readme-answers-five-questions-what-it-is-why-it-exists-how-to.md) (default)
<a id="D3"></a>
- `D3` to [DOC-DOCS-009](doctrines/DOC-DOCS-009-a-curated-changelog-with-a-running-unreleased-section.md) (default)
<a id="D4"></a>
- `D4` to [DOC-DOCS-010](doctrines/DOC-DOCS-010-a-failure-that-suggests-a-fix-declares-how-confident-it-is.md) (default)
<a id="D5"></a>
- `D5` to [DOC-DOCS-011](doctrines/DOC-DOCS-011-external-link-checking-is-advisory-never-blocking.md) (default)
<a id="D6"></a>
- `D6` to [DOC-DOCS-012](doctrines/DOC-DOCS-012-coverage-before-style.md) (default)
<a id="D7"></a>
- `D7` to [DOC-DOCS-013](doctrines/DOC-DOCS-013-prose-rules-ship-as-suggestions-and-are-promoted-on-evidence.md) (default)
- source `preferences:001` to [DOC-DOCS-014](doctrines/DOC-DOCS-014-house-prose-rules-beyond-the-mechanical-subset.md) (preference)
- source `preferences:002` to [DOC-DOCS-015](doctrines/DOC-DOCS-015-which-static-site-generator-or-none.md) (preference)
- source `preferences:003` to [DOC-DOCS-016](doctrines/DOC-DOCS-016-whether-explanation-lives-beside-reference-or-apart.md) (preference)
- source `preferences:004` to [DOC-DOCS-017](doctrines/DOC-DOCS-017-whether-documentation-lives-with-the-code-or-in-its-own-reposito.md) (preference)

## Decision map

| Fork | Guide | Default |
| --- | --- | --- |
| Where does this document's truth live? | `packs/docs-dx/guides/GD-DOCS-001-truth-location.md` | Generate it where a machine-readable source exists |
| How does a code example stop lying? | `packs/docs-dx/guides/GD-DOCS-002-executable-examples.md` | Run it in CI, or make it declare why not |
| Who writes the changelog? | `packs/docs-dx/guides/GD-DOCS-003-changelog-ownership.md` | Curated, with a derived first draft |
| What does a failure message owe its reader? | `packs/docs-dx/guides/GD-DOCS-004-failure-messages.md` | Condition, offending input, accepted alternative |
| Which documentation checks may block? | `packs/docs-dx/guides/GD-DOCS-005-blocking-checks.md` | Internal and structural block, prose and external advise |

Level-3 detail sits in `packs/docs-dx/refs/DOC_GATE.md` and
`packs/docs-dx/refs/DOC_FORMS.md`. The worked repair of a broken
quickstart is `packs/docs-dx/exemplars/EX-DOCS-001-stale-quickstart.md`.

## Failure modes and anti-patterns

- **The quickstart nobody has run.** Shell blocks correct when written
  and never executed since. The domain's characteristic failure, and B3
  exists for it (EV-0330).
- **A rename documented in the pages but not in the links.** The page
  moves, the references stay (EV-0331, EV-0332).
- **Hand-editing a generated file.** The edit looks like a fix and is a
  fork (EV-0102). Treating a docstring as generation is the same error
  with better manners.
- **`print("error")` and exit 1.** The most-read page in the system,
  left blank (EV-0327).
- **Four empty documentation directories.** Structure imposed before
  content exists, producing the wrong form in the right folder
  (EV-0322, EV-0323).
- **A style linter as the whole documentation gate.** Regex and word
  lists cannot tell you a page is wrong, incomplete or badly organised,
  which is where the reported cost sits (EV-0335, EV-0326).
- **Blocking on external links.** Buys false failures, then gets
  disabled, and takes the internal check down with it (EV-0331).
- **A documentation backlog.** Work never scheduled is not a plan. Fix
  the page in the change that made it wrong (EV-0095).
- **An agent entry file nobody checks.** Adoption is not accuracy
  (EV-0044).

## Open questions and counter-evidence

**Who curates release notes is genuinely contested.** The changelog
specification states flatly that generating from commit diffs fails
(EV-0333), while a commit grammar exists precisely to make the
changelog, the version bump and the release trigger derivations
(EV-0170). Both cannot be default. D3 reconciles them by constraining
the input at write time so the derivation is not noise, but the
residual disagreement is real: derived notes describe changes, curated
notes describe consequences, and only the second answers a consumer
asking whether to upgrade.

**Style enforcement versus coverage.** Executable prose rules are real
governance and one large exemplar makes them blocking (EV-0332,
EV-0335). Practitioners rank missing content far above style (EV-0326).
D6 takes the coverage side and D7 permits promotion, which is a
judgement rather than a finding.

**Documentation as a multiplier is plausible and unproven.** The
headline claim in the field is that teams with better documentation get
larger gains from adopting other capabilities (EV-0324). It is
cross-sectional self-report where documentation quality and capability
adoption come from the same respondent, the direction of the arrow is
not established, and mature teams plausibly write better documentation
because they are mature. Treat the direction as a working hypothesis
and do not quote the numbers.

**Onboarding time has no evidence here.** No source in this set links
documentation to time-to-first-commit, and the developer-experience
framework nearest the question does not carry onboarding time as a
headline measure at all (EV-0336). Instrument it locally if the estate
wants it, and heed the caution that framework states against its own
interest: measure throughput only when counterbalanced, never as a
target, never tied to reward.

**Human reader or machine reader.** Nothing here tests whether
documentation written for a person also serves an agent. The four
forms, the README taxonomy and the agent entry file are three different
answers and none is evidenced (EV-0322, EV-0329, EV-0044). Where
retrieval rather than navigation is how documents are reached,
architecture may matter less to the reader than to whatever ingests the
text, and that argument was speculation when it was made (EV-0323).

**Tool behaviour needs confirming before it blocks.** Vale exit-code
and severity behaviour was not verifiable from its repository landing
page and must be confirmed against the current release before any prose
rule blocks (EV-0335). The link checker's exit codes and fragment
behaviour are stated by its own documentation and are pinned by version
in the gate (EV-0331).

**Refresh triggers.** Re-argue this pack on: a changelog specification
release beyond 1.1.0; the agent entry file convention gaining a schema
or a conformance definition; a Vale major release changing severity
semantics; a link-checker release changing exit codes or fragment
handling; any controlled study linking documentation to a delivery or
onboarding outcome.
