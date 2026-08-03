---
summary: The estate narrative, how the repos relate, which are governed and what the seams between them are
type: registry
tags: [eos]
status: active
review_by: 2026-11
---

# ESTATE MAP

The human narrative of the PatterTech estate. Membership, roles and
per-repo ownership are in `estate/repos.json`, which is canonical, and
this file does not restate them. Read that file for who owns what; read
this one for how the pieces relate and where the seams are.
`registry/PROJECTS.md` carries governance and harvest state for the
seeded ventures. When these disagree, `estate/repos.json` describes
ownership and `registry/PROJECTS.md` describes governance.

## The shape

PatterTech is a multi-repo estate by deliberate decision: one repo per
venture, with the EOS as the shared brain (ADR-0001, unchanged by
ADR-0002). The north star is a local-first venture factory with a base,
a shared service fabric, products as clients and ventures as tenants.
The domain model everywhere is organisation, then venture, then project.

## Governed and not

Three repos are governed by the EOS: Venture A, Guth and
PatterTech_Website. Governed means the EOS seeded it or has adopted it,
it carries a pin, and it feeds rulings back through the harvest.

Every other repo in the manifest is an inventory row, `governed: false`
and `status: candidate`. That is not a judgement about the repo. It is
an honest statement that the EOS neither seeded it nor currently
governs it, and it exists so the quarterly estate review has to answer
adopt or defer for each one rather than quietly leaving them out.

Two rows carry a different status for a reason. PatterTech_EOS is
`self`: it is the manifest's own home, not a venture. PatterTech_WebKit
is `planned`: it has no directory and no commits, and it stays listed
because the extraction it names is a live intention inside
PatterTech_Website.

Exclusions are recorded too, in the `excluded` block of the manifest,
each with the ruling that excluded it. A repo left out silently would be
indistinguishable from one nobody remembered.

## The seams that matter

- **The document model** is meant to be one typed tree across print and
  web. PatterStudio's asset-pack model is canonical and the Website's
  block tree is its web profile. They are not unified yet, and that
  convergence is the largest piece of unscheduled estate work.
- **The design system** is implemented three times: the EOS token
  doctrine, the Website's stylesheet, and PatterStudio's hand-ported
  print CSS. The intended fix is one shared source extracted into
  PatterTech_WebKit, which has not started.
- **Visual media**, the branded recordings and the embed routes, is
  rendered by the Website and referenced by PatterStudio's content bank.
- **The agent control plane** in PatterStage intends to consume
  PatterStack's run engine rather than keep its own. Today it keeps its
  own.
- **State the static site cannot hold** goes to PatterTech_App. The
  Website stays a pure static client on purpose, so anything that must
  remember a person or prove a consent belongs in the App. The App is
  dormant, so today that seam has nothing behind it.

## The two shared brains

The estate carries two complementary shared brains, split by lifecycle.
**PatterTech_EOS** holds the git-pinned knowledge: the packs, this
manifest, the registries, and in time the shared document-model schema
as a compiled seed. **PatterStack**, inside PatterStudio, holds the
live queryable capability: the tool gateway, the corpus, the run engine
and the document engine. Git for knowledge, a service for capability.

The platform vision document inside PatterStudio predates the EOS and
does not mention it. Reconciling the two along that split is standing
estate work, and it is nobody's task yet.

## What the 2026-08-03 pass established

Every row in the manifest was checked read-only against the repository
on disk: its role, its branch tip, whether a remote is configured, and
whether the repo's own README still describes it correctly. Nothing was
written into any sibling repository, which the build's approval
explicitly reserves.

Three findings worth carrying: Venture A, PatterHome and PatterPower have
no git remote configured locally, so nothing in them is pushed anywhere.
PatterTech_App's README says it has no remote, and it does have one.
PatterHome had a commit on the day of the pass, which makes it the most
active repo the EOS does not govern.

## Agent files

Every repo that agents work in carries `AGENTS.md` as its entry point
with `CLAUDE.md` a byte-identical copy: the EOS standard, enforced here
by check E003 and in PatterTech_Website by its own lint script. The
three document-and-guide repos (PatterOS, PatterHome, PatterPower) carry
none, which is one of the things the adopt-or-defer review should settle.
