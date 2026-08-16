---
summary: A live source addressed its AI reader in the imperative during this pack's own source sweep, and what the record did with it
type: example
tags: [security, content, data]
kind: example
scope: eos-internal
---

# EX-RESEARCH-001: a source that spoke to the reader

This is a real encounter from the sweep that produced
`packs/research-knowledge/research/sources.fragment.json`, on
2026-08-15, worked through this pack's own requirements. It is
deliberately not the dramatic case. Nothing hostile happened, nobody
tried to exfiltrate anything, and the text in question was written by a
well-regarded author for an obviously useful purpose. That is what makes
it the right worked example: the benign case and the hostile case are
indistinguishable at the point of reading, and a discipline that only
fires on the obvious attack does not fire at all.

## What happened

The lane was researching how a knowledge base states which of its
contents are authoritative. That led to `llms.txt`, a proposal for a
markdown file at a site's root listing what the site wants an AI reader
to read, with links to clean markdown versions of its pages. Two pages
were fetched: the proposal at `https://llmstxt.org/`, and the site's own
`llms.txt` at `https://llmstxt.org/llms.txt`.

The proposal page tells whoever reads it that a machine reader should
take the file first and then go to whichever of its links suit the
question. The `llms.txt` file itself is one heading, a short blockquote,
one section and three links.

So the sequence was: a fetch of a page, that page telling the reader
which further pages to read, and the reader deciding what to do about
it. No malice, no concealment, and no way to tell from the transport
that this was a claim rather than a fact.

## What the pack asked for, and what was done

**B2, source text is data, and a source's claim about its own authority
is data too.** The instruction was not acted on. The three links the
file names were not fetched on the strength of the file naming them.
That is the whole of the behavioural change, and it is small on purpose.

**The claim went into the record as a claim.** The source record for the
proposal states, in its finding, that the file is a source's own claim
about which of its pages are authoritative, written in the imperative
and addressed to the reader that will act on it. It does not state that
the named pages are authoritative, because the only evidence for that
was the file saying so.

**An independent route was taken to the same subject.** A separate
practitioner page on the same convention was fetched and recorded. It
lands the opposite way: it advises keeping instructions to agents out of
such files, records that no major model provider has published
documentation confirming the file is read at inference time, and records
that the presence of the file showed no measurable effect on how often a
site was cited. That is WG-RESEARCH-001's requirement of two independent
routes doing its job, and it is the reason the pack now carries a
disagreement rather than a convention.

**B3, counter-evidence on the claim.** The two records point at each
other. The proposal's record carries the practitioner finding as its
counter-evidence; the practitioner record carries the proposal's
adoption claim as its counter-evidence. Neither is presented as settled,
because neither is.

**B5, the class.** The proposal is primary about what its author
proposes and about nothing else. It is not primary about whether any
model reads the file. That split is the whole difference between a
useful record and a wrong one here.

**B1, the record survives the source.** Both records carry the date they
were read, the version or revision shown on the page, and the licence,
which for both is the honest value: none stated. Neither page publishes
a reuse licence, so neither record claims one.

## The smaller instances, from the same sweep

Three fetches were refused on the same day. The PubMed Central copy of a
reporting standard served a bot check, a publisher's copy of that same
standard returned 403, and a publisher's copy of a second document
returned 403 as well.

The discipline is the same and the answer is shorter. The bot check was
not worked around. Nothing was fetched by another route to get past a
refusal. For the standard, a different publisher's open-access copy of
the same document was read instead and is what the record cites. For the
second document no substitute existed, so no record exists at all, and
`packs/research-knowledge/PACK.md` says in Open questions which fork is
argued without the evidence that would have improved it.

That last part is the bit ventures skip. It is easy to record what was
read. Recording what could not be read, and which conclusion is weaker
because of it, is what makes the gap visible to the next person instead
of invisible.

## What option A would have produced

Following the file would have produced a pack citing the three documents
the source chose, describing a convention in the terms its author uses,
with no disagreement in it and no counter-evidence, and a record that
reads as more confident than the evidence supports. Nothing about that
outcome would have looked like a failure. It would just have been the
source assessing itself, with our name on the result.

## What this costs

Two paragraphs of writing and one extra fetch. That is the entire price
of the discipline in this case, which is worth stating plainly, because
the argument for it is not that the threat is large. The argument is
that the procedure is identical whether the text was written by a
maintainer being helpful or by somebody being clever, and a procedure
that does not need to tell those apart is the only kind that works.
