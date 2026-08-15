---
summary: Test timing by change class.
type: doctrine
tags: [eos]
id: DOC-DEL-007
statement: Test timing by change class.
kind: doctrine
authority: default
basis: empirical-evidence
evidence_grade: controlled
scope: estate
applies_when: [ships_code]
challenge_triggers: [operator_requests_doctrine_review]
sources: [EV-0006, EV-0007]
review: 2028-02
lifecycle: active
verification_refs: [packs/delivery-testing/CHECKS.md]
migration_sources: [packs/delivery-testing/PACK.md:defaults:002]
generated_by: tools.eos.migrate_doctrines
---

# DOC-DEL-007

The `statement` field is the canonical standing proposition.

## Reasoning and limits

and this is a default set rather
  than law:

  | Change class | Default timing |
  | --- | --- |
  | FIX | Failing reproduction first, kept forever |
  | Invariants, money, security, personal data, irreversible operations, public contracts | Acceptance authored independently and frozen before implementation, at any tier |
  | FEAT at R2 | Oracle from the specification, frozen before implementation, same session permitted |
  | FEAT at R3 | Oracle authored by a separate session and frozen |
  | FEAT at R0 or R1 | Oracle from the spec, written before or beside the code, never read off it |
  | REFACTOR | Behaviour pinned before structure moves |
  | DOCS, MAINT | No behavioural tests; link, snippet and schema checks only |

  Reason: the load-bearing property is independence, not ordering
  (EV-0007), and mandating more agent-written tests reshapes cost
  rather than quality (EV-0006, scoped to SWE-bench Verified runs). The
  timing ablation ran on 2026-08-03 and settled the cells: all three
  timings passed six of six on three tasks, so timing did not separate
  quality on that work, while implement-then-harden cost about 65 per
  cent more tokens and 50 per cent more wall clock than the other two.
  The results are in `org/reports/V2_FINAL_REPORT.md`. Where a policy
  sets `test_timing` to `per-profile`, this table is what that resolves
  to; the capability-profile record decides the level, its expiry and
  what regresses it, and nothing else. Ours is
  `org/capability-profile.json`. So the cells stand on cost rather than
  on fault-finding, every arm passed, and nothing here says which timing
  catches more faults. Neither test-first nor end-stage testing is
  doctrine. The second row is unchanged by any of that, because it is a
  risk floor rather than a timing preference. Argued in WG-DEL-007.

## Migration provenance

This Doctrine was reviewed from the following frozen source blocks:

- `packs/delivery-testing/PACK.md:defaults:002`, lines 165-193, SHA-256 `1517cd493dc46b7764782d7a2e9b49f77662a6d68f12c767cc9d66cecdc5cb30`.
