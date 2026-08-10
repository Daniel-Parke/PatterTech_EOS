---
summary: How heavy may a page be before the build must push back?
type: wargame
tags: [web]
status: active
review_by: 2027-08
---

# WG-MINI-001: How heavy may a page be?

## The question

What page-weight budget do ventures hold, and what happens when a
change would break it?

## It depends on

- The audience's connections: rural and mobile visitors pay for every
  kilobyte in waiting time.
- The page's job: a gallery earns more weight than a contact page.
- The cost of policing: a budget nobody measures is decoration.

## Options

### A. No budget
Ship what looks right. Cheap today; the pages drift heavy within a
year and nobody can say when it happened.

### B. Hard budget with a measured gate
200 KB of critical-path weight before images, measured on every change
that touches layout or media. Breaches need an argued exception.

### C. Advisory budget
A number in the docs and no gate. History says this decays into A.

## Decision rule

Choose B unless the venture has no build step at all, in which case
hold the same number by hand at each release.

## Ruling

B. The budget is 200 KB of critical-path weight before images,
measured, with breaches argued in writing. Argued once at module
birth.
