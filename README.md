# PatterTech Framework

A documentation-based framework for taking a project from idea to shipped work
without re-learning the same lessons every time. It codifies doctrine (what we
never compromise), foundations (how to derive the specifics per project),
patterns (the reusable shapes), wargames (the "it depends" decisions, argued
out once so future agents can rule quickly), and templates (how a new project
locks its choices in).

The framework is written for agents as much as for people. A capable agent
dropped into a new project should be able to read this repo, lock in a
project's choices, and produce work that holds the standard without anyone
repeating the reasoning that got us here.

## Module map

| Module | Status | Covers |
| --- | --- | --- |
| `modules/web-design/` | Populated (module 01) | Web design, UI/UX, front-end implementation, QC |
| `modules/architecture/` | Mount point | System architecture, ADR practice |
| `modules/devops-deployment/` | Mount point | CI/CD, hosting, environments, release |
| `modules/cost/` | Mount point | Cost efficiency, budget wargames |
| `modules/hardware/` | Mount point | Hardware selection and sizing |

Module 01 (web-design) is the worked pattern for the rest: doctrine ->
foundations -> patterns -> wargames -> templates -> worked example. Future
modules follow the same shape. See `VISION.md` for the plan that grows this
into a kernel that can framework any project.

## How to consume this repo

1. Read `START.md` (the bootstrap: read order and ground rules).
2. Starting a new project: copy `modules/web-design/templates/PROJECT_LOCKIN.md`
   into the project repo, walk the wargames it cites, and fill it in. The
   lock-in file is the project's contract with the framework.
3. Working in an existing project: read that project's lock-in first, then the
   module docs it cites. The project file wins on specifics; the framework wins
   on doctrine.
4. Learned something new: append a worked ruling to the relevant wargame, or
   file a new wargame from `templates/WG_TEMPLATE.md`. Doctrine changes come
   last and require a wargame first.

## Worked examples

- `modules/web-design/examples/pattertech-website.md`: the PatterTech website
  redesign (the "instrument and the journal" language), including the diagnosis
  of why the earlier site read as AI-generated and the moves that fixed it.

## Related repos

- `PatterTech_Website`: the first conforming project (its
  `docs/DESIGN_SYSTEM.md` is the lock-in).
- `PatterTech_Business`: brand, voice and chart standards
  (`platform/docs/VOICE.md`, `CHART_STYLE.md`); the Studio print pipeline.
- `Venture A`: the org kernel (`org/`) whose file-based operating model this
  framework borrows; the seed-pack work there is the extraction source for the
  future modules (see `VISION.md`).
