---
summary: Plural categories, text expansion figures, the pseudo-locale gate and what each of them does not catch
kind: fact
scope: estate
sources: [EV-0442, EV-0443, EV-0444, EV-0445, EV-0446]
volatility: slow
review: on-change-of:CLDR-plural-categories
type: implementation
tags: [content, forms, tooling]
---

# i18n mechanics

Detail behind B1, B2 and B3 in `packs/writing-content/PACK.md`. The
format decision itself is
`packs/writing-content/wargames/WG-WRIT-002-message-structure.md`.

## Plural categories

Six category tags exist: zero, one, two, few, many and other. Only
`other` is mandatory. Which of the rest a locale uses is a property of
that locale and of the CLDR release, not of the message
(EV-0443).

The trap the specification names explicitly: `one` does not mean the
number one. It means any number that behaves like one in that language,
and which numbers those are differs per locale. English happens to make
those two sets identical, which is why the mistake survives so long in
an English-only codebase.

Consequences:

- Categories are looked up per locale. Never derive a locale's forms
  from the English singular and plural pair, and never translate the
  English pair.
- A hardcoded switch over six tags is already wrong for some locales
  and will drift as CLDR releases land. Ask the library.
- The rules cover grammatical number only. Gender, grammatical case and
  clause ordering are separate problems, which is part of why the
  selection belongs inside the message (EV-0442,
  EV-0444).

## Text expansion

Expansion is inversely related to source length
(EV-0445). English strings up to about ten characters
average two to three times longer once translated into European
languages. Strings over about seventy characters average around thirty
per cent longer.

The design consequence is counter-intuitive and worth stating plainly:
the shortest strings need the most layout slack. Buttons, tabs, chips
and field labels are exactly the strings a designer is most tempted to
put in a fixed-width box.

Limits of these figures: English into European languages only. They say
nothing about CJK, which usually contracts, and nothing about
right-to-left scripts, vertical text or line-breaking. They are
averages attributed to a third party with no distribution or worst
case given, so they size a risk and do not set a limit.

## The pseudo-locale gate

A pseudo-locale renders every externalised string in a transformed form
that is still readable but longer, accented and bracketed. Running the
product under it converts a class of defect from a post-translation
surprise into a pre-translation build failure, at no translation cost
(EV-0446).

What it catches:

- Truncation and overflow, seen as clipped text or a container that
  scrolls when it should not.
- Strings never externalised, seen as untransformed text on screen.
- Hardcoded text in templates and code, the same signal.
- Sentences assembled from parts, seen as a line with transformed and
  untransformed fragments side by side.

What it does not catch, and this boundary is the honest part of the
source: anything that only emerges during translation. Source
ambiguity, terminology inconsistency, register and whether the copy is
understandable at all. Passing a pseudo-locale run proves the machinery
works, never that the writing does.

Its usefulness depends entirely on the i18n library already supporting
a pseudo-locale. Where the library does not, the gate is a build step
someone has to write, and the cost of writing it is part of the format
decision in WG-WRIT-002.
