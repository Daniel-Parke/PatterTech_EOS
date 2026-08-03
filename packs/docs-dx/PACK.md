---
summary: Documentation and developer experience, where a document's truth lives and which documents can be made to fail a build
type: playbook
tags: [content, voice, delivery, ci, tooling]
kind: rule
authority: binding
lifecycle: active
basis: empirical-evidence
evidence_grade: observational
scope: estate
applies_when: [publishes_docs, documents_executable_surface, emits_user_visible_failure, renames_or_deletes_documented_page]
volatility: slow
review: 2027-08
sources: [EV-0023, EV-0044, EV-0095, EV-0102, EV-0136, EV-0137, EV-0170, EV-0171, EV-0175, EV-0189, EV-0322, EV-0323, EV-0324, EV-0325, EV-0326, EV-0327, EV-0328, EV-0329, EV-0330, EV-0331, EV-0332, EV-0333, EV-0334, EV-0335, EV-0336]
---

# docs-dx

This pack covers documentation and the developer experience around it:
where a document's truth lives, which documents can be made to fail a
build, and what a failure message owes the person reading it. It
activates on any task that writes or changes documentation, renames or
deletes a documented page, cuts a release, or adds a user-visible
failure. Link integrity, snippet execution, generated reference and
error-message content bind. Prose style does not.

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

## Binding requirements

Six requirements bind. A run that breaks one fails, whatever else it
achieved. Each names its basis, because binding has to be earned. All
six exist because documentation failure decomposes into named,
detectable categories rather than being one quality judgement
(EV-0325), and a convention only binds once it is executable
(EV-0137).

**B1. Internal links and anchors resolve, checked in CI, blocking.**
The check runs offline over the repository, validates fragments and not
just paths, and distinguishes a broken link from a broken checker so a
tool failure is never read as a clean run (EV-0331). Basis: standard,
plus the exemplar at EV-0332 where the same check gates merges across
sibling repositories. Prevents the silent break: an internal
cross-reference to `#install-it` keeps pointing at nothing the moment
someone retitles the heading, and nobody notices until a reader does.
See `packs/docs-dx/refs/DOC_GATE.md`.

**B2. A renamed or deleted page leaves a redirect, or every reference
to it is updated in the same change.** One or the other, verified, in
the commit that does the moving (EV-0332). Basis: decision, taken on
that exemplar. Prevents the half-move, where the page is renamed, the
inbound links are found later, and the reader in between gets a
dead end with no clue what replaced it.

**B3. Every executable snippet either runs in CI or carries an explicit
declaration of why it does not.** A fenced block that names a command,
flag or API call is executed by the documentation gate, or it carries a
marker saying it is illustrative, environment-bound or expected to
fail. Absence of the marker is itself the failure (EV-0330). Basis:
standard, from a toolchain that has run this way for a decade. Prevents
the drifted quickstart: a flag is renamed, the shell block in the
quickstart still names the old spelling, and nothing anywhere knows.
Scope note: executing a snippet proves it runs, never that it is the
right snippet to show, and the prose around it stays unverified. See
`packs/docs-dx/guides/GD-DOCS-002-executable-examples.md`.

**B4. Generated reference is verified as regenerated, not hand-edited.**
Where reference material is produced from a schema, model or interface
document, CI regenerates it and fails on any difference (EV-0332,
EV-0102, EV-0023). Basis: standard. Prevents the patched artefact:
someone fixes a wrong line in the generated file, the generator keeps
producing the wrong line, and the next regeneration reverts the fix.
Annotations in code comments do not satisfy this, because proximity is
not accuracy and nothing fails when a docstring is wrong about the
function beneath it.

**B5. Every user-visible failure names the condition, the
caller-relevant identity, and what to do next.** The message says what
was wrong, shows or names the offending input, and points at the
accepted alternative. Detail beyond that goes behind an explicit
request rather than inline (EV-0328). Which failures a caller may tell
apart is an interface decision and is declared, not inferred
(EV-0175). Basis: empirical-evidence. Prevents the dead stop: a user
does the wrong thing, gets `error` and exit 1, and cannot tell whether
they mistyped, hit a bug or lack a permission. Scope note: the
read-rate and time-to-fix evidence is an eye-tracking study of 56
students fixing planted Java defects in Eclipse in 2017 (EV-0327). The
direction transfers, the percentages are not a target, and nothing
there tested an agent reader. See
`packs/docs-dx/guides/GD-DOCS-004-failure-messages.md`.

**B6. Every repository carries an agent entry file at the conventional
root path, and the commands it names are covered by B3.** The
convention fixes location and nothing else, which is why it was adopted
across vendors that agree on very little (EV-0044). Basis: decision.
Prevents an agent guessing at build and test commands, and the softer
failure where the file exists, is never checked, and confidently names
a command removed two releases ago. Adoption counts measure file
existence, so presence alone is worth nothing without the second half
of this requirement.

## Defaults

Each applies unless a venture's lock-book overrides it with a recorded
reason.

**D1. Use the four documentation forms as a diagnostic, never as a
folder layout.** When a page has become confusing, ask which of
tutorial, how-to, reference and explanation it is trying to be, and
split it (EV-0322). Reason: the load-bearing claim is that mixing forms
inside one page is what makes it unusable, because a reader trying to
get something done cannot use a page that keeps stopping to teach. The
framework has no research base beyond its author's practice, and four
empty directories on day one produce a tutorial nobody wrote (EV-0323).
See `packs/docs-dx/refs/DOC_FORMS.md`.

**D2. A README answers what it is, why it exists, how to use it, and
whether it is maintained.** Reason: sampled READMEs cluster on what and
how and systematically omit why and status, which are the questions a
reader cannot answer any other way (EV-0329). Scope note: that is a
descriptive study of open-source READMEs sampled before 2018, and it
never linked section presence to an outcome.

**D3. A curated changelog with a running Unreleased section.** One
entry per version, newest first, dated, grouped into added, changed,
deprecated, removed, fixed and security, with deprecations announced
before removal (EV-0333). Derive from commit history only where a
commit grammar is enforced at write time (EV-0170, EV-0171). Reason: a
consumer needs the consequence of upgrading, and a raw log is full of
merges and internal churn nobody can act on. Override for an internal
service whose only consumers are two other services of the same estate,
where a machine-readable compatibility diff (EV-0136) carries more than
prose. See `packs/docs-dx/guides/GD-DOCS-003-changelog-ownership.md`.

**D4. A failure that suggests a fix declares how confident it is.**
Four tiers work: safe to apply automatically, contains placeholders,
possibly wrong, unstated (EV-0328). Reason: a caller, human or agent,
needs to know whether to apply the suggestion without reading further.
Override where nothing can act on the suggestion automatically, in
which case the tier is decoration.

**D5. External link checking is advisory, never blocking.** Reason:
external checking fails against rate limits and transient outages, so
making it blocking buys false failures and then gets turned off
(EV-0331). The blocking half of the check runs offline over internal
links and anchors only, which is also what makes it reproducible.

**D6. Coverage before style.** When attention is scarce, a missing
install or deployment instruction outranks every style finding.
Practitioners rate absence as both the most damaging and the most
frequent documentation problem, ahead of prose quality (EV-0326).
Reason: a linter that consumes the attention which would have written
the missing runbook is a net loss. Scope note: that is perception data
from 146 practitioners across two surveys, a ranking of felt pain
rather than a measured defect rate.

**D7. Prose rules ship as suggestions and are promoted on evidence.** A
new house rule enters as a non-blocking severity, is observed against
real changes, and only then becomes an error (EV-0335). Reason: a rule
that blocks on its first day blocks the wrong things and teaches people
to route around the checker.

## Preferences

These are taste. Record them, do not gate on them, and override them
without asking.

- **House prose rules beyond the mechanical subset.** Second person,
  active voice, present tense, sentence case headings, code font for
  code, unambiguous dates and alt text on images are cheap to check and
  worth having (EV-0334). Everything past that is a preference, and
  that guide is American English written for a different house, so take
  the enforceable-subset principle rather than the guide.
- **Which static site generator, or none.** A repository of Markdown
  read on the forge is a legitimate documentation site.
- **Whether explanation lives beside reference or apart**, and which
  prose-linter severities apply to which rule (EV-0335).
- **Whether documentation lives with the code or in its own
  repository.** Edit-on-encounter (EV-0095) argues for beside the code
  and this repository takes that bet, but it is not evidenced.

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
