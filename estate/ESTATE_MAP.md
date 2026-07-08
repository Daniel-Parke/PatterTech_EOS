---
summary: The estate map, which repo owns which responsibility and how they interact
type: registry
tags: [eos]
status: active
review_by: 2026-10
---

# ESTATE MAP

The human narrative of who owns what across the PatterTech estate. The
machine-readable version, with the per-repo `owns` and `does_not_own` fields, is
`estate/repos.yaml`. The governance and harvest ledger (venture status, EOS
pins) stays in `registry/PROJECTS.md`. When any of these disagree, this map and
`repos.yaml` describe ownership and interaction; `PROJECTS.md` describes
governance.

## The shape

PatterTech is a multi-repo estate by deliberate decision (a repo per venture with
the EOS as the shared brain, ADR-0001). The adopted north star lives in
`PatterStudio/docs/PatterTech_Platform_Vision_Design.md`: a local-first venture
factory, with a base (PatterOS), a shared service fabric (PatterStack, inside
PatterStudio today), products as clients, and ventures as tenants. The domain
model everywhere is Organisation, then Venture, then Project.

## Who owns what

| Repo | Owns | Does not own |
| --- | --- | --- |
| **PatterTech_EOS** | Doctrine, wargames, kernel templates, governance, this estate manifest | Any runnable product code; runtime services; the design-system code |
| **PatterTech_Website** | Public marketing and publishing; the V2 document model, field kit, dev-only editor and visual media capability (until WebKit extracts them) | Print documents; the design doctrine; accounts, mailing list, analytics, SaaS |
| **PatterStudio** (remote `PatterTech_Business`) | Print and investor documents; PatterStack (the runtime fabric); the canonical patter-doc document model | Web article rendering; the public marketing story |
| **PatterOS** | The local-first base and provisioner; the sovereignty charter and the reserved Patter brand | Products; the fabric |
| **PatterStage** | The agent control plane, its scheduler and Composer graph semantics | The shared run engine (it will consume PatterStack's) |
| **WiseWattage** | A live energy SaaS with its own auth (Clerk), billing and hosting | The factory that produces it |
| **PatterTech_WebKit** (planned) | The shared web design system, kit, document model and editor, reusable across sites | (extracted from the Website in Phase 3) |
| **PatterTech_App** (planned) | The out-of-band business platform and the estate data spine | The static marketing site |

## How they interact

- The **document model** is meant to be one typed tree across print and web:
  PatterStudio's `patter-doc` asset pack is canonical, and the Website's block
  tree (`src/lib/doc`) is its web profile. They are not yet unified; that is the
  convergence work.
- The **design system** is triple-implemented today (EOS `TOKENS.md` doctrine,
  the Website's `globals.css`, and PatterStudio's hand-ported print CSS). The
  intent is one shared source, extracted into `PatterTech_WebKit`.
- The **visual media** (branded MP4 and GIF recordings, and the new `/embed`
  routes) are rendered by the Website and referenced by PatterStudio's content
  bank.

## The two shared brains

The estate carries two complementary shared brains, split by lifecycle:

- **PatterTech_EOS** holds the git-pinned knowledge: doctrine, this manifest, and
  (in time) the shared document-model schema as a compiled seed pack.
- **PatterStack** (inside PatterStudio) holds the live, queryable capability:
  the MCP tool gateway, the corpus, the run engine, and the document engine.

The Platform Vision predates the EOS v1.0.0 tag and does not yet mention it;
reconciling the two by this plane (git for knowledge, MCP for capability) is a
standing piece of estate work.

## Agent files

Every repo carries `AGENTS.md` as its canonical entry point, with `CLAUDE.md` a
byte-identical copy (the EOS standard, enforced here by `eos_check` E003 and in
PatterTech_Website by `scripts/check-agent-files.mjs`).
