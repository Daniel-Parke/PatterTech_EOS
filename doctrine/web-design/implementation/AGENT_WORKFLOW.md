# Agent workflow

How an agent executes web work on this framework without supervision.

## Before touching code

1. Read the project's lock-in file, then the module docs it cites. The
   lock-in wins on specifics; doctrine wins on principles.
2. If the task forks on a question the lock-in does not answer, find the
   wargame, apply its decision rule, record the ruling.
3. Locate the styleguide route and the QC scripts; they are your acceptance
   surface and gates.

## Executing a change

- **New vocabulary lands as new files**; existing components are restyled in
  place or replaced, and legacy pieces are deleted only after their last
  importer migrates. The build stays green after every phase.
- **Every new component carries its law in a JSDoc header**: what it is for
  and what it must never do (width-agnostic, grid-owned rhythm, static
  rendering, whichever constraint it enforces). If the law cannot be written,
  the component is not ready. Kits keep a colocated GUIDE.md beside the code,
  and pattern-checkable laws also live in a design lint inside the standard
  lint command (WG-WEB-013): docs alone get broken politely.
- Tokens first, then primitives on the styleguide, then pages, then
  deletions, then docs. Do not skip the styleguide step: it is where drift
  becomes visible before it ships.
- Respect structural contracts when editing: anchor ids and scroll margins
  (on-page navigators), width-agnostic components (no `max-w-*`), grid-owned
  rhythm (no margins on article blocks), stable class names any tooling
  depends on.
- Copy you write (colophons, ledger rows, microcopy) follows the voice law;
  read it aloud.
- Update the design-system doc, the token mirror and the styleguide in the
  same commit as the change they describe.

## Verifying

Run the QC gates (implementation/QC_GATES.md) per phase, not once at the end.
Screenshot with the project's own tooling (headless scripts are more reliable
than embedded previews, which can stall on canvas-heavy pages). Report what
you measured, not what you believe.

## Feeding back

If the project taught you something reusable, append a worked ruling to the
relevant wargame in this repo, or file a new wargame. That is how the
framework grows.
