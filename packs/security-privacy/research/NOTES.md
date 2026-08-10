---
summary: Research synthesis for the security, privacy and safety pack, patterns, trade-offs and what should bind
type: example
tags: [eos]
---

# Security, privacy and safety: what the evidence supports

Research cutoff 2026-08-03. Fifteen new sources are proposed in
`sources.fragment.json`. Fifteen ledgered records already cover this
ground and are cited rather than re-recorded: EV-0034 and EV-0035
(ASVS 5.0 levels), EV-0036 (SAMM per-practice maturity), EV-0037
(SSDF outcomes not tools), EV-0038 (SLSA tracks and admission-time
verification), EV-0039 (OWASP cheat sheets as small indexed topics),
EV-0040 (NIST AI RMF functions), EV-0041 (ICO proportionality and
DPIA thresholds), EV-0068 (Sigstore, ephemeral identity plus
transparency log), EV-0069 (Scorecard, read the repo not its
self-description), EV-0070 (Semgrep, diff-aware blocking versus
monitor), EV-0071 (OPA, policy decoupled from the governed thing),
EV-0076 (guardrails in parallel with a tripwire), EV-0081 (per-action
risk analysis separated from the confirmation policy), EV-0011 (MCP
specification).

## The three philosophies, and when each fits

**One. Graded assurance levels.** ASVS 5.0 (EV-0034, EV-0035) grades
controls so the first tier is roughly a fifth of the catalogue and
deliberately cheap to enter, with the expensive defence-in-depth work
reserved for the top tier. SAMM (EV-0036) does the same per practice
rather than globally, so you can be mature in one area and immature in
another without a universal floor. This fits anything with a stable
control catalogue and a long life: the customer-facing product surface,
the release pipeline.

Trade-off: levels grade controls, not the reasoning behind them, and
tailoring needs documented exclusions or the level becomes theatre.
Anti-pattern: declaring a level and never testing against it, which is
what EV-0039 shows happening when an index still points at v4 mappings
long after v5 shipped.

**Two. Deterministic enforcement outside the model.** The 2026 adaptive
evaluation (FRAG-03) tested five out-of-band systems, capabilities,
information-flow labels and reference monitors, and found attack
success fell roughly sixfold and stayed low under a defence-aware
attack. CaMeL (FRAG-05) is the clearest instance: extract control flow
and data flow from the trusted request before untrusted data is seen,
then check capabilities at the point of tool invocation. Sandboxing
(FRAG-09) is the same idea at the operating-system layer, and its
strongest property is that the boundary holds regardless of what the
model chose to run.

Trade-off: it costs utility and generality. CaMeL solved 77 percent of
tasks against 84 percent undefended, and follow-up work reports the
static-planning strategy collapsing to zero utility on genuinely
open-ended tasks. Anti-pattern: applying it to a task class that cannot
be planned before the data arrives, then quietly widening the policy
until it permits everything.

**Three. Configuration rules that remove the precondition.** The lethal
trifecta (FRAG-08) says exfiltration needs private data, untrusted
content and outbound communication together, so forbid the combination
rather than filtering it. This is the cheapest control available to a
small venture and needs no model, no proxy and no budget. It fits
short-lived agent runs and one-off tooling.

Trade-off: it forbids configurations that a real policy layer could
make safe, so it costs capability rather than tokens. Anti-pattern:
treating a domain allowlist as satisfying the third leg when the
allowed domain is broad. The Claude Code docs (FRAG-09) state the
failure directly: the proxy decides from the client-supplied hostname
without inspecting TLS, so allowing `github.com` leaves an exfiltration
path open.

A fourth position exists and should be named to be rejected as a
primary control: **in-band detection**, meaning a classifier or a
prompt that asks the model to spot the injection. FRAG-04 bypassed all
eight defences it tested with over 50 percent success using adaptive
attacks. EV-0076 still earns its place as a cheap parallel tripwire,
but only above a real boundary, never instead of one.

## The disagreement that matters

FRAG-04 (2025) and FRAG-03 (2026) reach opposite-sounding verdicts on
whether prompt-injection defences work. They are reconcilable and the
reconciliation is the load-bearing principle: FRAG-04 broke defences
that ask the model to behave, FRAG-03 held up defences that do not
depend on the model behaving. The pack should not read this as
"injection is solved". FRAG-03's own authors call their result one
small-scale data point on one small model and one benchmark family.

The second disagreement is measurement. AgentDojo (FRAG-06) insists
security and utility be scored on the same runs, because a defence that
refuses work scores perfectly on attack success. Any pack criterion
phrased as a percentage of attacks blocked, with no utility number
beside it, is unfalsifiable in the direction that matters.

The third is scope. STRIDE (FRAG-13) is teachable and repeatable and
has no vocabulary at all for a model that follows instructions found in
the data it reads. Its six prompts still apply to the surrounding
system, so the pack should keep STRIDE for the system and add the
agentic catalogue (FRAG-02, FRAG-01) for the agent, rather than
choosing.

## What should bind, what should default, what is preference

**Binding.** These are cheap, checkable and their absence is a real
failure mode.

- No agent context holds private data, untrusted content and outbound
  network at once, unless a written exception names the mediating
  control (FRAG-08, FRAG-09).
- Filesystem containment and egress containment are enabled together or
  neither is claimed, because each alone is defeated by the other's gap
  (FRAG-09).
- Secret detection runs before the commit and again on the push path,
  and any bypass carries a stated reason and leaves an audit record
  (FRAG-10, FRAG-11).
- Credential files and secret environment variables are named in the
  deny list. There is no built-in default list, so unnamed means
  unprotected (FRAG-09).
- MCP and tool boundaries honour the specification's MUST clauses:
  no token passthrough, no session-as-authentication, per-client
  consent before proxying, exact command shown before local
  installation (FRAG-07, EV-0011).
- A named data protection complaints route exists and the lawful basis
  for each processing purpose is recorded (FRAG-14, EV-0041).

**Default, meaning do this unless the venture writes down why not.**

- ASVS level 1 as the entry bar, level 2 for anything holding personal
  data, with exclusions documented (EV-0034, EV-0035).
- One STRIDE pass per data-flow boundary at design time, timeboxed, plus
  an agentic pass against the ASI catalogue (FRAG-13, FRAG-02).
- Diff-aware static analysis split into blocking and monitor, with
  autofix only for mechanical findings (EV-0070).
- Verification at admission time against stated expectations rather than
  trust in the producing workflow, with signed provenance where the
  ecosystem supports it (EV-0038, EV-0068, EV-0069).
- Guardrails run in parallel as a tripwire above the enforcement
  boundary, never as the boundary (EV-0076, EV-0081).
- The NCSC five-topic baseline for the operating environment, on the
  grounds that a short list done beats a long list partly done
  (FRAG-15).

**Preference, meaning record the choice and move on.** Which secret
scanner, and note gitleaks is feature complete with a named successor
(FRAG-10). Which sandbox implementation. Whether threat models live as
diagrams or prose. Retention periods beyond any statutory floor.

## Anti-patterns to name in the pack

- Reporting a block rate with no utility number beside it (FRAG-06).
- Treating a percentage guardrail as protection. Ninety-five percent is
  a failing grade against an adversary who retries (FRAG-08).
- The hero threat modeller, and admiring the problem without fixing it
  (FRAG-12).
- A broad egress allowlist entry presented as network isolation
  (FRAG-09).
- Compliance documents that never get tested, the semantic staleness
  EV-0039 exhibits in its own index.
- Blanket licence assumptions. Licences here range across CC BY-SA 4.0,
  CC BY 4.0, MIT, Open Government Licence v3.0 and genuinely unknown,
  and reuse decisions turn on the exact one.

## Refresh triggers

Re-run this research on any of: a new OWASP GenAI list edition; ICO
publication of DUAA interpretive guidance, and note the ICO site
refused automated access at this cutoff so the Act itself is the
current primary (FRAG-14); an MCP specification revision; gitleaks
reaching end of life or Betterleaks shipping; a published adaptive
break of an out-of-band defence; a Claude Code sandbox release that
changes the TLS-inspection default.
