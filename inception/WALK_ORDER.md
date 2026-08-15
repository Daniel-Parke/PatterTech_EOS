---
summary: How Session 0 inherits Doctrine, pressure-matches Wargames and records every selection or omission
type: kernel
tags: [eos]
---

# WALK_ORDER

Phase C does not walk a directory. It inherits applicable Doctrine and
runs only the Wargames for which the venture has pressure. This file owns
the facts, the always-walk set, dependency order and the selection record.

## Build the facts

1. Translate the confirmed interview answers into the exact predicate
   names in `kernel/PREDICATES.md`. Record each known fact as `true` or
   `false`; use `unknown` only where the interview did not settle it.
2. Record `operator_requests_wargame` and
   `operator_requests_doctrine_review` as false unless the operator has
   explicitly asked for one. An explicit include still needs a reason.
3. Run `python -m tools.eos wargame match --facts <file>`. Doctrine and
   Wargame matching share one engine, so either public match command
   returns applicable Doctrine, required Wargames, candidates, unresolved
   facts, uncovered pressure and the dependency-ordered packs.
4. Ask about an unknown high-consequence pressure or include its Wargame.
   Show an unknown routine pressure as a candidate. A false pressure is
   omitted with the matcher reason.

The matcher classifies; it never chooses an option. The operator may
include or omit a scenario with a recorded reason. An override changes the
selection, not the Wargame's decision rule.

## Always walk

These decisions run even when their engagement predicates are false or
unknown.

1. `WG-EOS-001`, venture scale.
2. `WG-EOS-002`, repository shape.
3. The live security Wargames `GD-SEC-001` to `GD-SEC-004`. They exercise
   the injection, secret, assurance and external-action floors that no
   ordinary Ruling may waive.

The applicable security Doctrine also loads automatically. Always-walk
does not make every security option high consequence and does not lower a
manual-only action class.

## Dependency order

Pack order comes from each `PACK.md` `depends_on` list through the shared
resolver. Missing packs and dependency cycles fail the repository check.
Within a pack, sort Wargames by their immutable identity. A Wargame whose
metadata names a relation or another decision as an input runs after those
targets.

There is no second hand-maintained canonical list here. Adding a pack
without declaring its dependencies is an empty list, not permission for a
human to invent an order during Session 0.

## Record selection and Rulings

`docs/RULINGS.json` has two deliberately different lists.

- `selection_log` records every matched Wargame as selected, omitted or
  candidate, with the reason and the facts that mattered. Operator
  includes and omissions say so explicitly.
- `rulings` records one `RUL-*` object only when the venture executes a
  Wargame. It names the Wargame and applicable Doctrine, the decision,
  reasoning, departures and any proposed binding-scope change.

Inherited defaults need no empty Ruling. The EOS pin, adopted packs and
stack profiles already identify what was inherited. A departure from a
default needs a reason. A proposal to change binding scope needs an
accepted ADR or operator reference and cannot be authorised by the
Wargame itself.

Raw commercial, household, legal, authentication or personal context
stays in the venture. EOS harvests only a privacy-reviewed summary.

## Gaps

If a pressure is uncovered, make the venture decision through its local
ADR or operator route and record a sanitised gap in `docs/EOS_FEEDBACK.md`:
the question, stakes, options, cheapest test, fallback and revisit trigger.
Do not mint an EOS identity locally. A later EOS admission either assigns
a new `WG-*` identity or records that an existing relation covers it.

An uncovered high-consequence pressure blocks Phase C until it has a dated
fallback and an accountable owner. A routine gap does not block the
venture when the local decision and revisit trigger are explicit.

## Gate

Phase C is complete when:

- the always-walk set has argued Rulings;
- every required Wargame has a Ruling;
- every candidate has an include, omit or still-candidate reason;
- every unknown high-consequence fact was asked or included;
- every uncovered high-consequence pressure has a dated fallback;
- the selected packs are in resolver dependency order; and
- no outcome claims that a Wargame waived binding Doctrine.

Report four counts in `docs/COMPILE_REPORT.md`: required executed,
candidate included, candidate omitted and uncovered pressure. These are
coverage measures, not a file-count target and not a reason to rescale a
venture by themselves.
