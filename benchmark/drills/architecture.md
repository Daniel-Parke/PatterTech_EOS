---
summary: Single-run cold-agent acceptance drill for the architecture pack, with deterministic machine-checkable criteria
type: example
tags: [eos]
---

# DRILL-ARCH-001: boundary declared, enforced and proved

## Scenario

A cold agent is given the architecture pack and an empty Python
repository with two toy modules, `billing/` and `catalogue/`, plus a
`shared/` package. The prompt is one line: "Stand up the architecture
record and boundary enforcement for this repo. Billing may read the
catalogue; the catalogue must never know about billing. Then add a
price lookup in billing that uses the catalogue."

Single run, no follow-up prompts. Pass requires all ten criteria;
each is a file check or an exit code.

## Deterministic criteria

1. `.importlinter` (or `setup.cfg`/`pyproject.toml` equivalent) exists
   and parses.
2. It contains at least one contract of type `forbidden` whose source
   is the catalogue package and whose forbidden target is the billing
   package.
3. `lint-imports` exits 0 on the delivered tree.
4. The harness injects `import billing` into a catalogue module;
   `lint-imports` then exits non-zero. Reverting restores exit 0.
5. The boundary check is wired into a committed CI workflow or
   pre-commit config file that references the same command.
6. An ADR exists at a path matching `**/[Aa][Dd][Rr]*-*.md` or
   `docs/decisions/*.md`.
7. That ADR contains MADR headings `## Considered Options` and
   `## Decision Outcome`, and lists two or more options.
8. The ADR text cites the enforcement tool by name and states the
   direction of the allowed dependency.
9. A C4 or arc42 artefact exists (a `.dsl` file parsed by the
   Structurizr CLI, or a Markdown file containing a `Building Block
   View` or `Container diagram` heading), and it names both modules.
10. The delivered price lookup imports only from the catalogue's
    declared public interface module, not from a private submodule
    (checked by an added `forbidden` contract in the harness, which
    must exit 0).

## Fail conditions worth logging separately

- Contract file present but not run anywhere (5 fails while 1 to 3
  pass): the pack taught documentation, not enforcement.
- ADR present with a single option (7 fails): the pack taught the
  template, not the argument.
- Agent proposes separate services or a second database: the pack
  failed to carry the one-deployable default.

## Freeze note

Criteria 1 to 10 are frozen before content authoring. The toy repo,
the injected violation in criterion 4 and the harness contract in
criterion 10 are fixed inputs and are stored with the drill.
