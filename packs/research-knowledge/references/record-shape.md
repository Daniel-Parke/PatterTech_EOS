---
summary: The fields a source record and a claim record carry, what each one prevents, and where the shape comes from
type: guide
tags: [data, content, tooling]
kind: fact
scope: estate
authority: default
review: 2029-09
sources: [EV-0538, EV-0539, EV-0540, EV-0541, EV-0542, EV-0543, EV-0124]
---

# The record shape

Two record types, kept apart. A **source record** is one row per source
and says what was read. A **claim record** says what the venture now
believes and which source records support it. One source supports many
claims, and a claim rests on many sources, so merging the two into one
row is how a venture ends up with four slightly different versions of
one source and no way to see the divergence.

This is the field list B1 and B5 of `packs/research-knowledge/PACK.md`
ask for. A venture may name the fields whatever it likes and store them
in whatever it likes. What it may not do is drop one and keep the claim.

## The source record

| Field | What it holds | What its absence costs |
| --- | --- | --- |
| id | A stable identifier for this source inside the venture | Claims cite by URL, and the URL changes |
| source | What the thing is, in words a reader recognises | The record is only findable by whoever wrote it |
| url or locator | Where it was got from | Nobody can go back to it |
| class | primary, secondary or tertiary, by distance from the thing | A blog post and a specification carry equal weight |
| version_or_commit | The exact tag, commit, edition or dated revision read; the string `unknown` where none exists | The claim floats over every version the source ever had |
| access_date | The day it was read | The claim cannot be aged, so it can never be retired |
| licence | Read off the source, never inferred from its class | A reuse decision made on a guess |
| maintenance | active, stable, stale, or the citation no longer resolving | A dead source reads exactly like a live one |
| frozen_copy | Where the copy taken at first read lives, or the recorded reason there is none | Content drift is undetectable, because there is nothing to compare against |
| finding | The principle taken from it, in our own words | The record is a bookmark |
| applicability_limits | The conditions under which the finding holds | The finding gets applied where it was never true |
| counter_evidence | What disagrees, or a record that disagreement was searched for | The base is confident in the direction the record is biased |
| review | A date, or `on-change-of:<the thing that moves>` | Nothing ever prompts a re-read |

The estate's own instance of this shape is
`kernel/schemas/evidence.schema.json`, which fixes eighteen keys and is
enforced by check S017. A venture copying it gets the mechanical rows of
`packs/research-knowledge/CHECKS.md` for free, because those rows are
schema validation and nothing more.

Where the source is software, a machine-readable citation file carries
several of these fields in a form the hosting platform, archives and
reference managers already read, so the metadata travels attached to the
artefact rather than living in a note (EV-0540). It has no field for a
finding, a limit or counter-evidence, so it complements this shape and
does not replace it.

## The claim record

| Field | What it holds |
| --- | --- |
| id | A stable identifier for the claim |
| claim | What the venture believes, stated so it could be wrong |
| sources | The source record ids it rests on, at least one |
| grade | The certainty band, on the four values `kernel/METADATA_SPEC.md` already carries, attached to this claim rather than to any source |
| basis | Whether the claim is definitional, empirical, or our interpretation of a primary source |
| decided | When the claim was accepted |
| supersedes and superseded_by | The bidirectional link when a claim replaces an earlier one |

The grade sits here and not on the source record on purpose. The same
source supports one claim strongly and another weakly, and a band pasted
onto a source is inherited by everything cited from it, including the
things it barely mentions.

`basis` carries the distinction B5 asks for: an interpretation of a
primary source is a finding of ours and is recorded as ours, never
attributed to the source that did not say it.

## Why these fields and not others

Three published shapes converge on the same small set, which is the
argument for it being the right small set.

Provenance is modelled as an entity, an activity that used or generated
it, and an agent responsible for the activity (EV-0538). Read against
the table above: the source is the entity, the read is the activity, the
person or run is the agent, and the claim `wasDerivedFrom` the source.
The stated reason for recording any of it is so a reader can form their
own assessment of quality and reliability, which is why the record
carries limits and counter-evidence rather than only a conclusion.

The reusability principles ask for a persistent identifier, a stated
usage licence and detailed provenance, and for the metadata to stay
reachable when the thing it describes no longer is (EV-0539). That last
one is the whole argument for `access_date` and `frozen_copy`: the
record is the durable artefact.

The two failure modes the record has to survive are separately named and
separately handled. A source that stops resolving is caught by a link
check; a source that resolves to something changed is caught only by
comparison against a frozen copy (EV-0541). Where an archive holds a
prior state and runs a time gate, the frozen state is addressable rather
than merely kept (EV-0542).

`version_or_commit` earns its place on a case rather than a principle. A
maintained official standard published an erratum on a numbered page
three months after release (EV-0543). A record that pins the edition can
be re-checked against the correction. A citation that names only the
publisher cannot. The same argument runs through in-band deprecation
signalling, where the date something became deprecated and the date it
stops answering are deliberately separate fields (EV-0124).

## The one field ventures skip

`counter_evidence`, and it is skipped because it is the only field that
costs a second search. A record with the field left null on an empirical
claim fails C5 of `packs/research-knowledge/CHECKS.md`, and the two
legal values are a statement of what disagrees or an explicit note that
disagreement was searched for, where, and not found. Both are honest. An
empty field is neither.
