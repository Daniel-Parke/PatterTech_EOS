---
id: WG-EOS-001
summary: What scale of organisational machinery does this venture compile, S or ORG?
kind: wargame
type: wargame
tags: [eos, wargame]
scenario_modes: [selection, gap]
gap_domain: inception
applies_when: [runs_agents]
engages_when: [operator_requests_wargame]
consequence: high
relations: []
always_walk: true
scope: eos-internal
authority: default
basis: local-observation
evidence_grade: observational
volatility: slow
sources: [kernel/SCALE_MATRIX.md]
review: 2027-07
lifecycle: active
generated_by: tools.eos.migrate_wargames
---

# WG-EOS-001: What scale of organisational machinery does this venture compile?

## Decision question and stakes

Every Session 0 compiles a seed from the kernel, and the seed's size is
the single largest ceremony decision the venture ever takes. Too small
and legal duties or coordination fail silently; too large and the
ceremony kills small work (the failure mode the EOS was built against).
The scale is ruled once at inception and re-ruled only through rescale
when a trigger changes.

## Doctrines or coverage gap under pressure

This inception fork covers a gap before pack Doctrine is activated. It is always walked because venture scale and repository shape decide which later rules can be loaded safely.

## Preconditions and engagement triggers

- Lifespan: a weekend artefact or a going concern?
- Server state or auth: does anything persist or log in?
- Money: does money change hands under this venture's name?
- Personal or regulated data: does the law watch this venture?
- Ops burden: does anything need deploying, monitoring, backing up?
- A second human: does anyone besides the operator hold decisions?

Applicability is `runs_agents`. Engagement is `operator_requests_wargame`. This is an always-walk decision.

## Options

### S. Fourteen files, no org
Routers, operators guide, brief, lock-book, feedback, compile report,
policy and task list, plus the five blank Genesis forms. Seven of the
fourteen are operating surface; kernel/SCALE_MATRIX.md holds the list
and the accounting. One human, one task surface, no charters, no
integrator tooling. Costs nothing to run; offers no separation of
duties and no compliance machinery.

### ORG. The full shape
Twenty-five files. Adds the constitution, the boot file, the testing
law, the artefact shapes, the questions file, the playbooks, the
wide-build file, the three situational charters (EXECUTOR, ORACLE,
REVIEWER), the cadence file and the claims file. Work becomes task
records with derived views; separation of duties exists where the
router asks for it. Verification bandwidth becomes the limiting
resource.

## Failure premises

### Premortem for S. Fourteen files, no org

Assume `S. Fourteen files, no org` was selected and the outcome failed. Test this option's stated failure mechanism first: nothing to run; offers no separation of duties and no compliance machinery.

### Premortem for ORG. The full shape

Assume `ORG. The full shape` was selected and the outcome failed. Test this option's stated failure mechanism first: Twenty-five files. Adds the constitution, the boot file, the testing law, the artefact shapes, the questions file, the playbooks, the wide-build file, the three situational charters (EXECUTOR, ORACLE, REVIEWER), the cadence file and the claims file. Work becomes task records with derived views; separation of duties exists where the router asks for it. Verification bandwidth becomes the limiting resource.

## Decision rule

All six triggers silent: S. Any one of server state or auth, money,
personal or regulated data, standing ops, or a second human holding
decisions: ORG. Lifespan is the sixth and never forces a scale by
itself: a long-lived venture with no other trigger stays S with its
rescale conditions written in. What lifespan does is make those rescale
conditions mandatory, because a venture that lives will eventually trip
one. Trigger add-ons attach regardless of scale (a compliance file the
moment regulated data appears; see the matrix). Torn between the two,
take S and write the rescale condition into the lock-book; rescale is
cheap and deliberate, over-ceremony is a standing tax.

## Safe default

The smallest scale the triggers allow. Ceremony must be earned by
risk, never by ambition.

## Cheapest discriminating test

Settle this question with the smallest representative probe: **Lifespan: a weekend artefact or a going concern?** Compare only the option branches that answer changes, using the decision rule above as the oracle. Stop when the result rules at least one credible option in or out.

## Fallback, exit and revisit

**Fallback `safe-default`:** The smallest scale the triggers allow. Ceremony must be earned by risk, never by ambition.

**Exit condition:** Stop or roll back the selected branch when nothing to run; offers no separation of duties and no compliance machinery, or when its stated preconditions cease to hold.

**Revisit trigger:** Run this Wargame again when the answer to this question changes: Lifespan: a weekend artefact or a going concern?

## Counter-evidence and transfer limits

### Preserved reasoning: Why two options and not four

v1 offered S, M and L. The live matrix, kernel/SCALE_MATRIX.md, carries
S and ORG only, so the fork is two-way and an existing M or L venture
reads as ORG at its next recompile. The trigger set and the decision
rule below are unchanged; only the destination of the heavier answers
moved. That is why two of the worked rulings still say L and M.
### Historical ruling boundary

The baseline file carried 3 worked ruling notes. They are not copied into this live Wargame because they record a selection but do not carry both a privacy-reviewed harvest and an independently verifiable execution outcome. The immutable source remains available at commit `7f56e4e22378323cf58318fe051d26b5afa8c35f` for historical provenance. No `RUL-*` record was admitted from this procedure.
### Transfer limit

Use this decision rule only where its applicability holds and the representative test matches the venture's users, scale and failure cost. The cited evidence and prior arguments establish decision factors, not a universal outcome. Revisit on contrary evidence, a changed pressure fact or a changed Doctrine lifecycle.
