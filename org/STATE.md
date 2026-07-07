---
summary: Live state of the EOS itself, the active session claim and the Resume Packet
type: org
tags: [eos]
---

# STATE

The live state of the EOS. Touched at session start (claim) and session
close (Resume Packet). Reality wins over this file; fix it and note the
correction in the session log.

active_session: none

## Now

Phase B under way: B1 (the kernel org templates) landed in session
S-0002, 2026-07-07. Building v1.0 per ADR-0001; the queue holds B2 to
F. Venture A waits on phases B to D before its reseed and Genesis; treat
B2 to D2 as the critical path.

## Flags for Daniel

- The Venture A sprint clock is running (day 2 of 42). B2 to D2 are
  sized at roughly six to eight sessions; launch build sessions as
  often as slots allow.

## Resume Packet

- venture: the EOS itself (PatterTech_Framework, rename lands at REL)
- eos_version: pre-1.0.0, main at B1 close
- phase: B in flight; B1 done, next item B2 (kernel extraction:
  operating model, templates, state, cadence, questions)
- last_verified: eos_check --repo 0 errors, 6 expected warnings;
  indexes fresh
- next_action: entry mode 2, take B2 from org/QUEUE.md, playbook PB-E03,
  source Venture A@d2e3250
- blockers: none
- constraints: voice law; wargame first; protected set needs an ADR and
  now includes the B1 templates (constitution Parts II and III, the
  three charters)
- files_in_flight: none
