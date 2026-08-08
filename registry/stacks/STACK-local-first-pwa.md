---
summary: Profile 04, local-first PWA with a WASM compute core, shape, constraints and the sharp edges Guth paid for
type: stack
tags: [web, infra, perf, testing]
status: active
review_by: 2027-02
---

# Stack profile 04: local-first PWA with a WASM core

For a browser-delivered product whose data never leaves the operator's
machines, with real-time or otherwise latency-sensitive local
processing, and optionally a LAN companion for heavier compute.
Reference implementation: Project_Guth, S1.

Harvested 2026-08-08 from Guth's `docs/EOS_FEEDBACK.md`, where it was
filed as the venture's fifth draft wargame at Session 0 and matured
through S1. That id is Guth's own and is not an EOS wargame id. It
carries worked evidence rather than intent: every sharp edge below cost
the venture time before it was written down.

## Shape

- **Client**: SvelteKit with TypeScript, `adapter-static`, prerendered,
  SSR off. Cross-origin isolation (COOP and COEP) is stamped by a Vite
  middleware plugin, not by static header config. `worker.format = "es"`.
- **Compute core**: C++20 as one CMake project with two targets,
  Emscripten and native. The wasm side splits into an audio-thread
  worklet (`-sAUDIO_WORKLET`, built with `-matomics -mbulk-memory`,
  linked with `-Wl,--wrap=malloc` for the allocation proof) and a
  MODULARIZE ES6 worker module. Determinism flags `-ffp-contract=off
  -fno-fast-math`, no libm transcendentals on analysis paths, constant
  tables committed as hexfloat headers.
- **Thread topology**: the worklet writes a lock-free ring in shared
  wasm memory; a worker polls with wrap-aware uint32 arithmetic and
  producer headroom; results publish through an odd-even seqlock; the
  main thread reads inside `requestAnimationFrame`.
- **Storage**: OPFS for blobs, IndexedDB through Dexie for records,
  with the boundary in the schema layer. JSON Schemas are the
  cross-language contract, with a generated-types drift gate.
- **Serving**: any static server that sets the isolation pair. Guth's
  reference implementation is loopback-bound.

## Constraints to design around

- **Cross-origin isolation is not optional** and it is not free. Shared
  memory and precise timers need it, and the dev server needs the
  middleware plugin because the framework serves the document response
  outside the static header configuration.
- **Browsers cannot run sanitisers.** That is the whole argument for the
  native twin: a solo maintainer gets memory safety from the native
  target under AddressSanitizer and UBSan, and the wasm target inherits
  it because both come from one source tree.
- **Worker failures arrive as bare error Events with no message.** Ship
  worker error plumbing, meaning `onerror` plus an error postMessage
  protocol, from the first commit. The silent form costs real diagnosis
  time; this is the sharp edge Guth reported most strongly.
- **Vite refuses a literal dynamic import of a module inside `static/`.**
  The Emscripten MODULARIZE output lives there, so the worker builds
  the specifier at runtime.
- **PowerShell 5.1 default-encoding reads corrupt UTF-8.** Guth lost an
  operator-verbatim document to mojibake this way. Read with an explicit
  encoding on Windows hosts.

## Quality floor

Code is the only thing that crosses the wire, so the gate sits in CI:

- Native clang under AddressSanitizer and UBSan.
- Cross-target golden byte-identity: goldens generated on one target and
  compared on the other, with the analyser version embedded in the
  format. This is the change-proof pattern of
  `packs/architecture/guides/WG-ARCH-006-change-proof.md` applied to a
  dual-target core.
- libFuzzer smoke on every parser and kernel entry point.
- App typecheck and static build, plus the schema drift gate.
- A repo-root addition guard.

## When not to reach for it

If the data may leave the machine, this profile buys constraint for
nothing: take `STACK-fullstack-app.md` instead. If there is no
latency-sensitive compute, the wasm core and its whole toolchain are
weight, and a static client over an API is lighter. The profile earns
its cost only where local processing and local data are both
requirements rather than preferences.
