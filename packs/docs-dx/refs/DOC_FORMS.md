---
summary: The four documentation forms as a diagnostic, the README question set, and what an agent entry file owes a reader
type: foundation
tags: [content, voice, product]
kind: fact
scope: estate
sources: [EV-0044, EV-0095, EV-0322, EV-0323, EV-0326, EV-0329, EV-0334]
volatility: slow
review: 2028-05
review_by: 2028-05
---

# Documentation forms reference

Level 3 material behind defaults D1, D2 and requirement B6. Read this
when a page has become confusing, or when starting a repository from
nothing.

## The four forms, as a diagnostic

The framework this paraphrases is published under a share-alike licence
(EV-0322), so what follows is a description of the idea rather than its
text.

It separates documentation along two independent distinctions: whether
the reader is acting or thinking, and whether they are studying or
working. Crossing those gives four forms.

| Form | Reader is | Question it answers |
| --- | --- | --- |
| Tutorial | learning by doing | take me through something that works |
| How-to | working, acting | how do I achieve this specific result |
| Reference | working, consulting | what exactly does this do |
| Explanation | studying, thinking | why is it like this |

**Use it as a diagnostic.** When a page is confusing and nobody can say
why, the usual answer is that it is two forms at once. A reader trying
to get a job done cannot use a page that keeps stopping to teach, and a
learner cannot use a page that assumes the vocabulary. Splitting the
page along the form boundary is usually the fix.

**Do not use it as a folder layout.** There is no research base behind
the four-way split; it is one practitioner's model that turned out
useful, and its own admirers say so (EV-0323). Four empty directories
created on day one produce a tutorial nobody wrote and a how-to that is
really reference. Create the page, then ask which form it is.

**What it does not cover.** It was written for product documentation
read by outsiders. It says nothing about internal engineering
documentation whose main reader is the team that wrote it, and nothing
about a machine reader. Where a model rather than a navigation tree is
how people reach documentation, the architecture may matter less to the
reader than to whatever ingests the text, and that argument is
speculation on both sides (EV-0323).

## The README question set

Sampled READMEs cluster on what the thing is and how to use it, and
systematically omit why it exists and whether it is maintained
(EV-0329). Those omissions are the decision-relevant part, because a
reader cannot answer them any other way.

A README answers, in this order:

1. **What is this**, in one or two sentences, in the reader's
   vocabulary.
2. **Why does it exist**, meaning what it is for and what it is not
   for.
3. **How do I use it**, meaning install, run and the smallest example
   that works. This is the section most likely to have gone stale, so
   it is the section most in need of execution under B3.
4. **What state is it in**, meaning maintained, experimental, frozen or
   archived, and where support comes from.
5. **Where do I go next**, meaning the links a reader needs, all of
   which must resolve under B1.

Missing installation, deployment and release instructions are the
single most damaging documentation gap practitioners report, ahead of
anything about prose quality (EV-0326). Scope note: that is perception
data from 146 practitioners, and the README taxonomy is descriptive of
open-source repositories sampled before 2018. Neither links a section
to an outcome.

## The agent entry file

The convention fixes the location and deliberately fixes nothing else:
a Markdown file at the repository root, no schema, no required sections
(EV-0044). That minimalism is why it was adopted across vendors that
agree on very little.

What it should carry is the operational surface an agent cannot infer
from the source:

- The commands that build, test, lint and run the thing, exactly as
  typed. These are executable claims about code, so B3 covers them.
- The conventions a reader would otherwise have to derive from reading
  everything.
- The boundaries: what must not be touched, and what needs a person.
- Where the deeper material is, rather than the deeper material itself.

**The failure to avoid.** Adoption counts measure that the file exists,
not that it is accurate, and there is no conformance test (EV-0044). A
file that confidently names a command removed two releases ago is worse
than no file, because it is trusted. This is why B6 binds the file's
commands to the execution gate rather than binding only its presence.

## Where the forms meet the truth question

The form tells you what a page is for. It does not tell you where its
truth lives, which is the earlier and more consequential fork in
`packs/docs-dx/guides/GD-DOCS-001-truth-location.md`. Reference is
usually derived. Explanation is always written by a person. Tutorials
and how-tos are written by a person and must be executable, which is
the most common gap in practice. Internal knowledge of any form is best
served by fixing the page in the change that made it wrong rather than
by scheduling documentation work that never gets scheduled (EV-0095).

## Style, in one paragraph

A small mechanical subset is worth enforcing: second person, active
voice, present tense, sentence case headings, code font for code,
numbered lists for sequences, unambiguous date formats, alt text on
images (EV-0334). Everything beyond that is house preference. Note that
the source is American English written for a different house, and this
repository's own voice law contradicts parts of it, so take the
principle of a short enforceable subset rather than the guide itself.
