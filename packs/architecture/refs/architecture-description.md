---
summary: The MADR heading set, the C4 levels worth authoring, the arc42 sections worth borrowing, and the ISO 42010 vocabulary behind them
kind: fact
scope: estate
sources: [EV-0097, EV-0101, EV-0102, EV-0149, EV-0158]
volatility: slow
review: 2027-05
type: example
tags: [arch, content]
---

# Architecture description reference

Level 3 material for defaults D11 and D4 of
`packs/architecture/PACK.md`. The
one idea that ties all four sources together, and it is ISO 42010's
(EV-0158): a view exists to answer a named concern of a named
stakeholder, so any diagram with no stated concern is undefended and
can be cut.

## Decision records: MADR (EV-0097, MIT or CC0)

MADR scales with the decision. Full, minimal and bare variants mean a
record can be three lines or three pages, which keeps ceremony opt-in
per decision rather than mandatory per change.

The headings a record carries under D11:

```markdown
# ADR-0007: Enforce module boundaries with import-linter

## Context and Problem Statement
What forced the decision, and what breaks if nothing is decided.

## Considered Options
- Option A
- Option B
- Option C

## Decision Outcome
Chosen option: "B", because ...

### Consequences
- Good, because ...
- Bad, because ...

## Pros and Cons of the Options
Why each losing option lost.
```

`Considered Options` with two or more entries and `Decision Outcome`
are the two headings a checker can verify mechanically. A record with
one considered option teaches the template and hides the argument.

Rules that matter more than the template:

- Immutable once accepted. A reversal is a new record that supersedes
  the old one, and supersession is named in both directions.
- Name the anti-pattern the decision guards against, or the next agent
  will reintroduce it.
- Cite the tool or standard by name and state the direction of any
  dependency the decision allows. Direction is the part people leave
  implicit and later argue about.
- Records live somewhere predictable, one file each, named
  ADR-NNNN-short-slug.md. `docs/decisions/` is the directory this
  estate uses, and both the directory and the filename prefix are what
  make a record findable by a tool rather than by memory.

**Honest limit.** EV-0097 records that there is no measured evidence
decision records improve outcomes, and that mandating a template for
every choice becomes ceremony. That is why the ADR-0008 authority
audit moved the rule to a default, and why D11 asks for a record on
door-closing decisions only.

## Views: C4 (EV-0101, CC BY 4.0)

Four levels with deliberately diminishing obligation:

| Level | Answers | Worth authoring? |
| --- | --- | --- |
| Context | who and what the system talks to | yes, once |
| Container | the deployable and storage units | yes, keep current |
| Component | the modules inside a container | only if it adds value, ideally generated |
| Code | classes and functions | almost never by hand |

Context and container are the workhorses. The author's own position is
that lower levels are rarely worth manual upkeep, so a component view
should come from the same source as the boundary contract or not at
all.

## Models as code: Structurizr DSL (EV-0102)

One text model, version controlled, generating many views that cannot
drift from each other. Derived diagrams are regenerated, never
hand-edited.

```
workspace {
  model {
    user = person "Operator"
    sys = softwareSystem "Shop" {
      billing = container "billing"
      catalogue = container "catalogue"
    }
    user -> billing "prices an order"
    billing -> catalogue "reads product data"
  }
  views {
    container sys { include *; autolayout lr }
  }
}
```

The discipline collapses the moment someone edits a rendered output,
so treat rendered diagrams the way you treat generated clients: build
outputs, never sources.

## Sections: arc42 (EV-0149)

Twelve fixed sections, of which only three are diagrams: building
block view, runtime view, deployment view. The other nine carry goals,
constraints, scope, solution strategy, crosscutting concepts,
decisions, quality requirements, risks and glossary.

The transferable lesson is that diagrams are a minority of an
architecture record. Borrow the headings that answer a real question
and leave the rest out. arc42's own authors ship a lighter canvas,
which is evidence that section-complete templates invite box-filling.

A `Building Block View` heading in a Markdown file naming every module
is the minimum arc42-shaped artefact. Its C4 equivalent is a
`Container diagram` heading over the same list. Either satisfies the
same obligation as a Structurizr container view, and either is
mechanically detectable, which a hand-drawn image is not.

## Vocabulary: ISO/IEC/IEEE 42010:2022 (EV-0158)

Stakeholders, concerns, viewpoints, views, model kinds, correspondence
rules. Reach for this vocabulary when a stakeholder demands that
rigour, and not otherwise: the standard is paywalled, it was read here
as a public abstract only, and it prescribes the structure of a
description rather than the architecture itself.

## What to produce by default

For a venture at inception: one decision record per door closed, a
Structurizr container view, and a component view only when the
boundary contract can generate it. That is the whole obligation. Add
arc42 sections when a specific question keeps getting asked and has
nowhere to live.
