---
summary: The six binding delivery rules, test-first by type, ratchets, rubric gates, determinism
type: doctrine
tags: [delivery, testing, ci]
status: archived
---

# Delivery doctrine

Binding on every venture with code. The wargames beneath these rules
carry the arguments; the kernel's playbooks (PB-010 to PB-013) carry
the per-type procedures these rules assume.

1. **Test-first where the type demands.** A FIX starts with the
   failing reproduction and keeps it forever. A FEAT starts from its
   test specification, acceptance-level skips lifted only when green
   end to end. A REFACTOR pins behaviour before touching structure
   (WG-ARCH-006). Types whose Definition of Done says nothing about
   tests (DOCS, MAINT) earn no ceremony.

2. **Ratchets only tighten.** Coverage floors, type allowlists, token
   and breakpoint gates move upwards in the change that earned the
   movement, and never down without a ruled deviation (WG-DEL-001).
   Big-bang strictness on an existing tree is forbidden; allowlists
   grow module by module.

3. **A gate is a rubric, not a vibe.** Every gate states its pass
   criteria measurably, in the file that defines it: the command, the
   threshold, the evidence a verdict cites. A gate whose pass cannot
   be stated is review theatre; this rule exists because the v0.1
   design system shipped gates as commands with no rubric for judging
   their output.

4. **Determinism is budgeted, not hoped for.** Every external
   dependency has a synthetic or offline mode CI uses; rendering is
   pinned before pixels are compared; blocking gates run zero retries
   (WG-DEL-003, WG-DEL-004). The stack profiles carry the estate's
   paid-for fixes; new flake classes land there as constraints.

5. **The trunk takes assembled proof.** Fast suites gate every change;
   the end-to-end acceptance journeys block `main` (WG-DEL-002). Where
   an agreement defines acceptance (a §A5-style walk-through), that
   walk-through is the suite, written failing at Genesis.

6. **A red gate is never negotiated.** Never weakened, skipped or
   deleted to pass; a gate believed wrong is escalated as a question
   with the evidence (constitution Part II Article 6, the
   three-strikes rule). Flakes are contained by quarantine with
   deadlines, never by retries on blocking gates.
