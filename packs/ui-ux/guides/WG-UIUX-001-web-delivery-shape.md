---
id: WG-UIUX-001
summary: Should a user journey arrive as static HTML, server rendering, client rendering, islands, a progressive web application or an installed native client?
kind: wargame
type: wargame
tags: [arch, delivery, eos, perf, web, wargame]
scenario_modes: [selection, gap]
applicable_doctrines: [DOC-UIUX-011, DOC-UIUX-015, DOC-NAT-008, DOC-NAT-009]
gap_domain: web-delivery-shape
applies_when: [has_user_interface]
engages_when: [requires_rendering_mode_choice]
consequence: routine
relations: []
scope: estate
authority: advisory
basis: standard
evidence_grade: observational
sources: [EV-0027, EV-0241, EV-0563, EV-0564, EV-0575]
review: 2027-08
lifecycle: active
---

# WG-UIUX-001: How should the interface be delivered?

## Decision question and stakes

Choose how one representative user journey reaches the device and becomes
usable: static HTML, server rendering, client rendering, progressively enhanced
islands or PWA behaviour, or an installed native client. The decision controls
first useful content, interaction latency, navigation, caching, offline
behaviour, accessibility, deployment and how many runtimes the team must own.

The product may use more than one shape, but every additional shape must own a
distinct journey rather than reflect framework preference.

## Doctrines or coverage gap under pressure

- `DOC-UIUX-011` treats field performance on public surfaces as design input.
- `DOC-UIUX-015` keeps content visible without client execution.
- `DOC-NAT-008` separates shared domain logic from native interface code.
- `DOC-NAT-009` starts online-first with a read cache until offline writes are
  a named requirement.
- The uncovered domain is `web-delivery-shape`: retired web procedures do not
  govern this choice and no current rule makes one rendering mode universal.

## Preconditions and engagement triggers

Name the journey, target users, supported devices, connection conditions,
search or linkability needs, install tolerance, offline read and write needs,
interaction density and failure cost. Distinguish content becoming visible
from the journey becoming interactive. State which team can operate the build,
server and client runtimes.

Applicability is `has_user_interface`. Engage when
`requires_rendering_mode_choice` is true.

## Options

### A. Static semantic HTML

Generate or serve complete HTML with ordinary links and forms, adding little
or no client execution. This has the smallest runtime and strong cache,
resilience and indexing properties. It is insufficient for interactions that
need sustained local state, immediate graphical feedback or offline writes.

### B. Server-rendered application with progressive enhancement

Render each route on the server and add client behaviour where it shortens the
task. Content and primary actions have an HTML path while enhanced controls can
hydrate. This adds a live server and risks duplicate server-client state or
hydration cost.

### C. Islands or route-scoped client application

Keep the document and navigation server or statically delivered, but give
bounded interactive regions their own client state. This limits script and
failure blast radius while supporting richer work. Boundaries can become
awkward when state and focus must cross several islands.

### D. Client-rendered application or PWA

Load an application shell, hold substantial state on the device and optionally
add service-worker caching or installability. It supports highly interactive
flows and can retain useful state through network loss. It makes the client
bundle, cache invalidation, recovery and no-script behaviour part of the
product.

### E. Installed native client

Use a platform toolkit and distribution route where deep device integration,
background work, sustained offline use or platform interaction is central.
This can best fit the device but adds platform builds, store or installer
operations and a separate interface implementation.

## Failure premises

### Premortem for A. Static semantic HTML

Assume A failed. A task that needed continuous local state became a chain of
slow round trips, or the team rebuilt browser behaviour poorly with ad hoc
scripts while still claiming the surface was static.

### Premortem for B. Server-rendered application with progressive enhancement

Assume B failed. The server became a latency and availability dependency,
hydration duplicated work, or enhanced and basic paths diverged so only one
was tested.

### Premortem for C. Islands or route-scoped client application

Assume C failed. Shared state leaked across islands, keyboard focus was lost on
handoff, or several small bundles and runtimes cost more than one coherent
client.

### Premortem for D. Client-rendered application or PWA

Assume D failed. First useful content waited for script, a stale cache served a
broken mixed version, or install and offline claims exceeded what the tested
journey actually supported.

### Premortem for E. Installed native client

Assume E failed. Platform-specific interfaces drifted, distribution delayed
urgent fixes, or device capability was invoked as a reason after a web route
had already met the representative need.

## Decision rule

Use A for reading, discovery and bounded submissions when it meets the
journey. Use B when per-request server knowledge is required and progressive
enhancement can preserve the primary path. Use C when only bounded regions
need sustained interaction. Use D when substantial client state or offline
reads materially improve the named journey and cache recovery is tested. Use E
only for a named platform capability, sustained offline write model or device
interaction that the tested web route cannot meet.

If two options meet the user outcome, choose the one with fewer runtimes and
less client execution. A framework already present is a cost input, not the
decision rule.

## Safe default

Deliver meaningful semantic HTML for content, navigation and primary actions,
then add the smallest progressively enhanced client boundary needed by the
representative task. This is A or B for most public routes, not a ban on richer
application surfaces.

## Cheapest discriminating test

Implement the hardest representative route in the simplest two credible
shapes. On target devices and constrained network, record first useful
content, usable interaction, navigation, transferred and executed script,
accessibility tree, cache recovery, offline requirement and operational
components. Complete the route with keyboard only and with client script
unavailable where the Doctrine claims content should remain visible.

## Fallback, exit and revisit

**Fallback `semantic-server-route`:** retain a server or static HTML route for
content and primary actions while richer client behaviour is disabled or
repaired.

**Exit condition:** leave the chosen shape when it cannot meet field
performance, accessibility, cache recovery or the named offline behaviour on
supported devices, or when its extra runtime has no remaining user journey.

**Revisit trigger:** repeat when a material journey, device class, offline
write requirement, install requirement, search need or operating boundary
changes.

## Counter-evidence and transfer limits

The W3C design principles support user needs, compatibility and simplicity,
but are a Group Note rather than a conformance standard (EV-0575). WCAG
conformance is a floor, not proof of usability for the target audience
(EV-0027). Lab rendering numbers do not transfer without the supported devices
and connection conditions. A result for one route does not force the same
shape on an editor, dashboard, marketing page and background native workflow.
