---
summary: Everything in containers, platform-native builds, or a mixed fleet?
type: wargame
tags: [ops, infra, hosting]
status: active
review_by: 2027-07
---

# WG-OPS-002: Everything containers, platform builds, or mixed?

## The question

The deploy artefact decides local parity, portability between hosts
and how many deployment models one operator maintains. The fork is
whether every surface ships as a container, rides its platform's
native build, or mixes.

## It depends on

- Parity requirements: must local and production be the same bytes?
- Handover clauses: does a client receive something that must run
  anywhere?
- How many deployment models the operator can hold (each is its own
  failure vocabulary).
- Whether the fronts are static exports (which barely benefit from
  containers).

## Options

### A. Everything container
Every surface an OCI image from one Dockerfile family; one deployment
model, local parity by construction, image-portable between hosts.
Costs build time and the container tax on static fronts.

### B. Platform-native builds
Vercel builds the front, buildpacks build the API. Fastest DX; parity
is approximate and portability is the platform's goodwill.

### C. Mixed, API containerised
The API and workers as containers (the portable, stateful, riskiest
parts); static and edge fronts on their platform's native build. Two
models, each where it earns its keep.

## Decision rule

Handover or parity clauses in force, or a cloud estate ruled by
WG-OPS-001: A, one model, local harness running the same images.
PaaS-hosted with static-export fronts: C; the API is always a
container (it is the part that must move one day), the fronts follow
their host. B alone only for ventures with no API at all.

## Default

C. Containerise what holds state and logic; let static fronts be
static.

## Worked rulings

- **WiseWattage (2026, argued)**: C. Railway builds the API from its
  Dockerfile (multi-stage, dependency layer keyed on the manifest);
  the app and website ride Vercel's build. Two models, consciously.
- **AutoWatt (2026-07, argued)**: A. Its ADR-0002: three App Runner
  services from one image family, the same images standing up locally
  via the harness; parity and handover clauses made one model the
  cheaper of the two.
