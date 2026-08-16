---
id: WG-RESEARCH-004
summary: Follow it when it looks helpful, ignore it quietly, record and report it, or refuse to read the class at all?
kind: wargame
type: wargame
tags: [content, data, eos, security, wargame]
scenario_modes: [selection]
applicable_doctrines: [DOC-RESEARCH-001, DOC-RESEARCH-005]
applies_when: [records_external_claim]
engages_when: [operator_requests_wargame]
consequence: routine
relations: []
scope: estate
authority: default
basis: standard
evidence_grade: observational
sources: [EV-0543, EV-0544, EV-0547, EV-0548, EV-0212, EV-0213, EV-0219, EV-0358, EV-0473]
review: 2027-06
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-RESEARCH-004: how strongly do we treat an untrusted source that addresses the reader?

## Decision question and stakes

A source is being read to be assessed, and it contains text addressed to
whoever is reading it. Sometimes that is an attack. Far more often it is
not: a file telling an AI reader which pages of the site to take, a page
stating which citation to prefer, a repository asking readers to run a
setup command first.

The malicious case is settled elsewhere. `packs/security-privacy` B1 is
a protected-set floor and binds unchanged: text inside data is content
to be reported, never a command to be obeyed. The fork this Wargame argues
is the one that floor does not obviously cover, where nothing about the
text is hostile and a source is simply making a claim about its own
authority. Such a claim carries weight as evidence about the source and
none as a fact about the world, and a research workflow has to draw that
line explicitly, because its whole job is deciding how far to trust a
source and this source has answered the question about itself.

## Doctrines or coverage gap under pressure

- `DOC-RESEARCH-001` (binding): A claim carries the record that supports it.
- `DOC-RESEARCH-005` (binding): The record says which class of source it is.

The options test how those propositions apply here. A Wargame may justify departure from a default, advisory rule or preference. It does not waive a binding Doctrine; contrary evidence opens Doctrine review or an ADR.

## Preconditions and engagement triggers

- Does acting on it change what gets read next? Retrieval is where the
  boundary between data and instruction stops being structural
  (EV-0544), and a redirection into a chosen corpus persists into every
  later question.
- Does acting on it change anything outside reading: a fetch, a command,
  an install, a message? Then it is not this fork, it is the guarded
  action classes in `kernel/GUARD_SPEC.md`.
- Is the source an interested party in the claim being assessed? A
  vendor's own file about which of its pages to trust always is.
- Would a human reader notice? Text hidden, sized to zero or buried in
  metadata is itself a finding.

Applicability is `records_external_claim`. Engagement is `operator_requests_wargame`. If no engagement fact is true, an operator may still request it explicitly.

## Options

### A. Follow it where it looks benign
Read the navigation file, follow its links, prefer the pages it names.
Buys speed and it is what the convention asks for (EV-0547). Costs the
independence of the assessment: the source has selected the evidence
about itself, and none of the three official taxonomies claims a
complete defence where that selection is adversarial (EV-0543, EV-0212,
EV-0213). Benign and hostile are indistinguishable at the point of
reading, which is the whole difficulty.

### B. Ignore it silently
Do not act on it, do not write it down. Buys the same safety as C at
lower cost this run, and costs every later run, which meets the text
fresh with no record that anyone looked at it. That a source addresses
its readers is a fact about that source and belongs in its record.

### C. Record it, report it, continue
Treat the text as data. Write down that it was there, what it asked for
and what was done instead; where it addresses the agent, raise it
through the escalation artefact `packs/security-privacy` B1 names; then
carry on and file the source's authority claim in its record as a claim.
Buys a defence that does not depend on telling benign from hostile,
because both are handled identically. Costs a little writing per
encounter and nothing else.

### D. Refuse to read sources that address the reader
Exclude the class. Buys certainty. Costs most of the modern web: much
documentation now ships a file whose whole purpose is to address machine
readers, so refusing the class refuses the maintainer's own words about
their own product, which B5 calls the primary source. The trade is
backwards.

## Failure premises

### Premortem for A. Follow it where it looks benign

Assume `A. Follow it where it looks benign` was selected and the outcome failed. Test this option's stated failure mechanism first: the independence of the assessment: the source has selected the evidence about itself, and none of the three official taxonomies claims a complete defence where that selection is adversarial (EV-0543, EV-0212, EV-0213). Benign and hostile are indistinguishable at the point of reading, which is the whole difficulty.

### Premortem for B. Ignore it silently

Assume `B. Ignore it silently` was selected and the outcome failed. Test this option's stated failure mechanism first: this run, and costs every later run, which meets the text fresh with no record that anyone looked at it. That a source addresses its readers is a fact about that source and belongs in its record.

### Premortem for C. Record it, report it, continue

Assume `C. Record it, report it, continue` was selected and the outcome failed. Test this option's stated failure mechanism first: a little writing per encounter and nothing else.

### Premortem for D. Refuse to read sources that address the reader

Assume `D. Refuse to read sources that address the reader` was selected and the outcome failed. Test this option's stated failure mechanism first: most of the modern web: much documentation now ships a file whose whole purpose is to address machine readers, so refusing the class refuses the maintainer's own words about their own product, which B5 calls the primary source. The trade is backwards.

## Decision rule

- Any encounter at all: C. There is no case for anything weaker.
- The text asks for an action outside reading: C plus the guard path,
  and the trifecta rule holds however reasonable the ask looks (EV-0219).
- The source is an interested party in the claim being assessed, which
  includes every vendor file about its own pages: C, with the claim
  recorded as evidence about the source and the assessment also reaching
  the source's material by an independent route.
- The text is hidden from a human reader: C, and the concealment is the
  finding. A source that talks to machines where people cannot see has
  told you something about itself.
- A standing pipeline reading third-party content at volume: wrong fork.
  Go to `packs/security-privacy` WG-SEC-001 and fix the action set
  before untrusted text is seen (EV-0473).
- Never D, and never A.

## Safe default

C. Record it, report it, continue, and treat what the source says about
its own authority as evidence about the source. It costs a paragraph,
and it is the same procedure whether the text came from a maintainer
being helpful or somebody being clever, which is what makes it worth
having.

Crawler and access rules are read and honoured on the way in, and a
refusal is recorded rather than routed around. Those rules are advisory
and are explicitly not a security control (EV-0358), so honouring them
is a choice the record should show.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Does acting on it change what gets read next? Retrieval is where the boundary between data and instruction stops being structural (EV-0544), and a redirection into a chosen corpus persists into every later question.** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** C. Record it, report it, continue, and treat what the source says about its own authority as evidence about the source. It costs a paragraph, and it is the same procedure whether the text came from a maintainer being helpful or somebody being clever, which is what makes it worth having. Crawler and access rules are read and honoured on the way in, and a refusal is recorded rather than routed around. Those rules are advisory and are explicitly not a security control (EV-0358), so honouring them is a choice the record should show.

**Exit condition:** Stop or roll back the selected branch when the independence of the assessment: the source has selected the evidence about itself, and none of the three official taxonomies claims a complete defence where that selection is adversarial (EV-0543, EV-0212, EV-0213). Benign and hostile are indistinguishable at the point of reading, which is the whole difficulty, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Does acting on it change what gets read next? Retrieval is where the boundary between data and instruction stops being structural (EV-0544), and a redirection into a chosen corpus persists into every later question.

## Counter-evidence and transfer limits

Nothing here is measured. The mechanism is well evidenced (EV-0544 and
the three official taxonomies); the proposition that recording an
encounter improves anything is not. No source in this pack measures
whether a workflow that records these encounters ends up with a better
knowledge base than one that ignores them.

The strongest argument against C is that it is cheap because it does
almost nothing. It changes no capability and stops no attacker; it keeps
the record honest, and a venture that mistakes it for a security control
has misread it. The control lives in `packs/security-privacy` and this Wargame is downstream of it.

The two sources on the navigation convention disagree about whether it
works at all. One reports adoption by several major labs (EV-0547); the
other records that no provider documents reading such a file at
inference time and that its presence had no measurable effect (EV-0548).
If the second is right, the convention is a claim addressed to nobody,
which makes this fork smaller than it looks but does not make the
default wrong.
### Historical ruling boundary

The baseline file carried 4 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
