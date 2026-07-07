# WG-013: Where does a design law live so it actually holds?

status: active
review_by: 2027-07

## The question

A law written in a project's root docs was broken politely, in reviewed code,
by the component's own author: a carousel hard-coded a full bleed and an
interlude band while the docs said media is a citation, and the component's
JSDoc described the violation as the intended behaviour. Where does a law have
to live before a person or an agent cannot miss it: in the docs, beside the
code, or in a machine check?

## It depends on

- Whether the codebase is touched by many hands and agents, each loading a
  different slice of context. A law that lives one directory away might as
  well live nowhere.
- Whether the law can be expressed as a pattern. Widths, class names and raw
  tags can be machine-checked; taste cannot.
- The cost of a violation reaching production. A broken layout law is visible
  to every reader on every visit.

## Options

### A. Docs only
Cheap to write and easy to drift from. The incident shows the failure mode
exactly: the doc said one thing, the component said another, and the component
was what got read.

### B. Docs plus colocated contracts
A GUIDE.md inside the component folder and a JSDoc law header on every
component stating what it is for and what it must never do. The rule sits in
the file that actually gets opened.

### C. Docs plus colocated contracts plus machine lint
B, plus a dependency-free design lint wired into the standard lint command,
with a pragma escape that forces a written reason for every deliberate
exception.

## Decision rule

Any law that can be expressed as a pattern gets all three layers. Laws of
taste stop at B. A pragma without a reason beside it is treated as a
violation, not an exception.

## Default

C for pattern-checkable laws, B for the rest.

## Worked rulings

- **PatterTech Website (2026-07)**: chose C after the carousel and video
  incidents (one component at three widths on one page; a video playing its
  audio behind a 2px shell). Landed as `src/components/article/GUIDE.md`,
  JSDoc law headers across the article kit, and `scripts/design-lint.mjs`
  inside `npm run lint` with five rules: no viewport widths, no hand-rolled
  `max-w-*` in the kit, no raw `<iframe>`/`<video>` outside the sanctioned
  component, no `bleed-full` on media, and every `<img>` sized.
