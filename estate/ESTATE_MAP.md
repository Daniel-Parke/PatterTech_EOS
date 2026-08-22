---
summary: The estate narrative, how the repos relate, which are governed and what the seams between them are
type: registry
tags: [eos]
status: active
review: 2026-11
---

# ESTATE MAP

The human narrative of the PatterTech estate. Membership, roles and
per-repo ownership are in `estate/repos.json`, which is canonical, and
this file does not restate them. Read that file for who owns what; read
this one for how the pieces relate and where the seams are.
`registry/PROJECTS.md` carries governance and harvest state for the
seeded ventures. When these disagree, `estate/repos.json` describes
ownership and `registry/PROJECTS.md` describes governance.

**The venture names here are placeholders.** Every venture below is
real, and so are its seams and its dates. A venture's name is replaced
by a stable placeholder, Venture A and so on, and the mapping back to
the real name is held privately. One placeholder per venture, always
the same one and never shared with another. This repository and
PatterTech_Website keep their own names, because both are public.

## The shape

PatterTech is a multi-repo estate by deliberate decision: one repo per
venture, with the EOS as the shared brain (ADR-0001, unchanged by
ADR-0002). The north star is a local-first venture factory with a base,
a shared service fabric, products as clients and ventures as tenants.
The domain model everywhere is organisation, then venture, then project.

## Governed and not

Five repos carry `governed: true` in the manifest as of 2026-08-22:
Venture A, Venture C, PatterTech_Website, PatterStage and Venture D. This
sentence read "three" until that date, and it had been wrong since
PatterTech_Website was adopted; the two admissions of 2026-08-22 made it
wrong by two. It is a count on a date, not a rule, and the manifest is
the authority. Governed means the EOS seeded or adopted the repo and
holds its pin. It does not mean the EOS rules it. Under ADR-0006 the
EOS hands off at venture birth, so rulings come back when a venture
chooses to send them and not because the EOS asked.

Every other repo in the manifest is an inventory row, `governed: false`
and `status: candidate`. That is not a judgement about the repo. It is
an honest statement that the EOS neither seeded nor adopted it, and it
exists so the estate review has to answer adopt or defer for each one
rather than quietly leaving them out. Under ADR-0008 that review is
triggered by an event, a repository added or a seed compiled, rather
than by a quarterly clock.

Two rows carry a different status for a reason. PatterTech_EOS is
`self`: it is the manifest's own home, not a venture. Venture K is
`planned`: it has no directory and no commits, and it stays listed
because the extraction it names is a live intention inside
PatterTech_Website.

The manifest lists the estate's repositories, not every directory on
disk. Sibling directories that are not PatterTech ventures are out of
scope and carry no row.

## The seams that matter

- **The document model** is meant to be one typed tree across print and
  web. Venture D's asset-pack model is canonical and the Website's
  block tree is its web profile. They are not unified yet, and that
  convergence is the largest piece of unscheduled estate work.
- **The design system** is implemented three times: the EOS token
  doctrine, the Website's stylesheet, and Venture D's hand-ported
  print CSS. The intended fix is one shared source extracted into
  Venture K, which has not started.
- **Visual media**, the branded recordings and the embed routes, is
  rendered by the Website and referenced by Venture D's content bank.
- **The agent control plane** in PatterStage keeps its own run engine.
  It once intended to consume the one in Venture D's service fabric;
  PatterStage's accepted ADR-0002 rules otherwise, and the estate's
  shared asset is the contract rather than the implementation. Corrected
  here on 2026-08-22, at the venture's registration.
- **State the static site cannot hold** goes to Venture J. The Website
  stays a pure static client on purpose, so anything that must remember
  a person or prove a consent belongs there. Venture J is dormant, so
  today that seam has nothing behind it.

## The two shared brains

The estate carries two complementary shared brains, split by lifecycle.
**PatterTech_EOS** holds the git-pinned knowledge: the packs, this
manifest, the registries, and in time the shared document-model schema
as a compiled seed. **The service fabric**, inside Venture D, holds the
live queryable capability: the tool gateway, the corpus, the run engine
and the document engine. Git for knowledge, a service for capability.

The platform vision document inside Venture D predates the EOS and
does not mention it. Reconciling the two along that split is standing
estate work, and it is nobody's task yet.

## What the 2026-08-03 pass established

Every row in the manifest was checked read-only against the repository
on disk: its role, its branch tip, whether a remote is configured, and
whether the repo's own README still describes it correctly. Nothing was
written into any sibling repository, which the build's approval
explicitly reserves. What it found about each repo is in that repo's
`notes` and is not repeated here.

The one finding that is about the estate rather than about a repo:
Venture A, Venture G and Venture H have no git remote configured
locally, so nothing in them is pushed anywhere and a lost machine would
be a lost repository.

## Agent files

The EOS standard is `AGENTS.md` as the entry point with `CLAUDE.md` a
byte-identical copy, enforced here by check E003 and in
PatterTech_Website by its own lint script. The manifest's `agent_files`
records which repos carry it. The three that carry none are the
document-and-guide repos, which is one of the things the adopt-or-defer
review should settle.
