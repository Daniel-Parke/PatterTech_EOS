---
summary: The repository refers to the operator by role rather than by name, with attribution and the record of who ruled as the two exceptions
type: decision
tags: [eos]
status: accepted
decided_by: Daniel Parke
date: 2026-08-15
---

# ADR-0011: a role, not a name

The owner asked on 2026-08-15 that this repository stop referring to him
by name, in the third person throughout, and that it be done wherever it
can be done. This record is that change, and it needs an ADR because
`GOVERNANCE.md` is in the protected set and carried five of the
occurrences.

## Context

The repository is public. It named one person 166 times across 72 files,
in prose that was written conversationally and read as a private
document made public rather than a document written to be read.

There is a second reason beyond preference. The estate's own model says
the operator is a role: `TOUR.md` defines it as the person who has
adopted a repository and holds its human gates, and says plainly that in
a venture it is whoever launches sessions there. Prose that names one
person contradicts that. A venture seeded from these templates inherits
sentences about somebody who has nothing to do with it.

## Decision

**One.** Narrative prose refers to `the operator`. That covers 67 files,
including the protected `GOVERNANCE.md` and the ten decision records'
bodies.

**Two.** Two categories keep the name, because a role would be a worse
answer in both.

`LICENSE` and `NOTICE` keep the copyright holder. Apache-2.0 attribution
identifies a legal person, and an organisation name in place of one
would weaken it.

The `decided_by` field on every decision record keeps the name, and so
does `authorised_by` in `org/capability-profile.json`. Those fields are
the record of who ruled. A decision record whose author is "the
operator" cannot answer the question it exists to answer, which is who
decided and therefore who may unmake it. The bodies of those same
records are rewritten, so only the field carries a name.

**Three.** `benchmark/PROTOCOL.md` is frozen and said the sealed suite's
private key is held by a named person. It now says the operator. That
went through the sanctioned freeze amendment rather than around it, and
the amendment records that no threshold, gate, session count or scoring
rule changed.

**Four.** Two references to Daniele Procida, who wrote Diátaxis, stay
exactly as they are. They are a different person and a source
attribution, and an automated pass that removed them would have been a
bug, not a tidy-up.

## Counter-evidence and what argues against this

**It loses information.** "The operator ruled" is weaker than a name
where the reader wants to know whose judgement they are reading. That is
what the `decided_by` field is preserved for, and the bodies now point
at it rather than repeating it.

**A mechanical pass over 67 files can produce nonsense.** It did.
`TOUR.md` briefly read "in this repository the operator is the
operator", which is true and useless. Two such degenerate sentences were
found and rewritten by hand. There may be others that read stiffly
rather than wrongly, and those are worth fixing when the file is next
touched rather than in a second sweep.

**The git history still carries the name**, in author fields and in
commit messages, and this record does not change that. Author identity
is inherent to the commits and removing it would be a different and much
larger operation than this one.

## Migration

No venture is affected. The templates a seed compiles from are among the
67 files, so a venture seeded after this carries role language and one
seeded before carries the old wording, which is a difference in prose
and not in behaviour. Check E003 still holds the two routers byte
identical, and the suite is green.
