---
summary: Copy-exact template for a new wargame in any module
type: template
tags: [eos, wargame]
---

# WG-<MOD>-NNN: <the question, as a question>

The ID is module-prefixed and globally unique: WEB, ARCH, DEL, OPS, VOX,
EOS. Numbers run per module (`WG-WEB-015`, `WG-ARCH-001`). One fork per
wargame; if a second independent question grows inside one, split it into
a new wargame and cross-link (see doctrine/MODULE_SHAPE.md).

Start the file with this front-matter:

```yaml
---
summary: <the question in one line>
type: wargame
tags: [<module tag>, <trigger tags such as auth, state, money, motion>]
status: draft | active | contested | superseded
review_by: <YYYY-MM, usually a year out>
supersedes: <WG id, if any>
superseded_by: <WG id, if any>
---
```

## The question

One paragraph stating the fork precisely.

## It depends on

The triggers that actually decide it, as a short list. If you cannot name
what it depends on, you are not ready to rule.

## Options

### A. <name>
What it is, what it buys, what it costs.

### B. <name>
...

## Decision rule

If <trigger>, choose <option>. If <trigger>, choose <option>. Otherwise the
default.

## Default

The option to take when the triggers are silent, and why.

## Worked rulings

Rulings are marked argued (engaged the triggers afresh) or inherited (took
the default without new argument). Only argued rulings count towards
promotion (see GOVERNANCE.md).

- **<Project> (<date>, argued|inherited)**: chose <option> because <reason
  in one or two sentences>. <Link or path to where it landed.>
