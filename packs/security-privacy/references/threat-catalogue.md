---
summary: STRIDE for the system, the agentic catalogue for the agent, and how both map onto the ten guarded classes
type: guide
tags: [security, arch]
kind: fact
scope: estate
volatility: fast
review: on-change-of:EV-0213
sources: [EV-0011, EV-0212, EV-0213, EV-0218, EV-0223, EV-0224]
---

# Reference: threat catalogues and the guard mapping

Level 3 detail behind the default that says run one STRIDE pass per
data-flow boundary plus one agentic pass. Read this when doing either
pass.

## Two catalogues, both kept

STRIDE gives six prompts against a data-flow boundary: spoofing,
tampering, repudiation, information disclosure, denial of service and
privilege escalation (EV-0224). It is teachable, repeatable and
cheap. It has no vocabulary at all for a model that follows
instructions found in the data it reads, so it covers the system around
the agent and stops there.

The agentic catalogue covers the agent: instructions arriving through
data, tool misuse, excessive agency, memory and context poisoning,
identity and delegation failures across tool boundaries (EV-0213,
EV-0212). It is new, and its categories have not been tested by much
adversarial use, so treat it as a prompt list rather than a taxonomy.

Keeping both is a judgement, not a finding. Choosing one would leave a
named gap either way.

## Running the passes

The manifesto position is that a threat model answers four questions,
and the fourth is whether you did a good enough job (EV-0223). In
practice, for a solo venture:

- Timebox it. Thirty minutes per boundary, once, at design time.
- Draw the boundary first. If you cannot say what crosses it, the model
  will be about feelings.
- Write findings as work, not as observations. Admiring the problem is
  the failure mode this material is most prone to.
- One person does not own it. The hero threat modeller is an
  anti-pattern because the model dies when they are busy.

## Agent-specific risks worth naming

**Tool misuse.** The agent has a tool that does more than the task
needs. The control is narrowing the tool, not instructing the agent to
be careful.

**Exfiltration through instructions in data.** Covered by B1 and B2.
The catalogue entry matters because it names the variants: a URL the
agent is asked to fetch with data in the query string, a commit message
carrying content, a base64 blob in a log line, an image request whose
path encodes the payload.

**Confused deputy across a tool boundary.** The agent holds credentials
for two systems and untrusted content in one argues for an action in
the other. The MCP specification's MUSTs address this directly: no
token passthrough, no session identifier used as authentication,
per-client consent before proxying, exact command shown before local
installation (EV-0011, EV-0218).

**Memory and context poisoning.** Planted text that survives into a
later run through notes, caches or long-lived context. This is why the
escalation artefact records the source rather than the instruction.

## Mapping onto the guarded classes

The threat model produces findings; the guard produces verdicts. The
seam between them is this mapping, and `kernel/GUARD_SPEC.md` is the
authority for the classes themselves.

| Agent risk | Guarded class it lands in |
| --- | --- |
| Exfiltration through instructions in data | external-write, pii-egress, secrets |
| Tool misuse with a broad tool | dependency-install, deletion, destructive-git |
| Confused deputy across tool boundaries | external-write, production-data |
| Excessive agency on an irreversible step | irreversible, deployment, money-movement |
| Memory or context poisoning | none directly, which is the point |

The last row is the useful one. Context poisoning has no action-time
signature, so the guard cannot catch it and the control has to sit
earlier: the instruction-source boundary, and the escalation artefact
that makes the planted text visible to the next run.

## Licence note

The OWASP material here is CC BY-SA 4.0 and the Microsoft and
manifesto material CC BY 4.0, so all of it is paraphrase-with-
attribution rather than copy. The exact rows are in
`registry/evidence.json`.
