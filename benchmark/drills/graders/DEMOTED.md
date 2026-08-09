---
summary: Graders removed because an adversarial recheck proved they returned the wrong answer, and the criteria they covered now report manual
type: example
tags: [eos, testing]
---

# Graders withdrawn

Each of these was built, run, and then proved wrong by an independent
verifier that constructed a tree containing the exact defect the
criterion exists to catch and watched the grader pass it. They are
deleted rather than patched, so the criterion reports `manual` and a
human has to look.

A criterion with no grader is honest about what it does not know. A
grader that returns the wrong answer confidently is worse than both,
because a green drill is then evidence of nothing and reads as
evidence of something.

- **agentic-development c2**: matches Topology clauses only against a vocabulary (/extract/, /merge|weekly report|roll-up|PR/), so a stage named anything else is never graded; a tree adding one differently-worded bullet scored 11/11 while containing the several-writers-on-one-file defect the brief is built around

- **agentic-development c3**: same vocabulary gate; changing a path to the words 'the weekly report' flipped the verdict, which proves the gate reads wording rather than meaning

- **agentic-development c4**: close to vacuous: four repetitions of 'X is a factor in the checkpoint' tie four pressures, because it only requires a pressure word and a decision word in one clause

- **agentic-development c5**: finds an affirmed single-writer clause and stops, so a document whose Topology section describes four concurrent writers on the same artefact still passes

- **api-integration c9**: accepts a tolerance that enforces nothing: a constant read only inside a log.debug() argument counts as 'read', so a tree that assigns a positive tolerance and never compares against it passes
