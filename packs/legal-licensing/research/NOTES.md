---
summary: Research synthesis for the legal, licensing and compliance routing pack, patterns, trade-offs and what should bind
type: example
tags: [eos, testing]
---

# Legal, licensing and compliance routing: what the evidence supports

Research cutoff 2026-08-03. Sixteen new sources are proposed in
`sources.fragment.json`. Three ledgered records already cover ground
this pack needs and are cited rather than re-recorded: EV-0041 (ICO,
ceremony scales with risk to people, DPIA mandatory only for high-risk
processing), EV-0225 (Data (Use and Access) Act 2025, statutory
complaints route, recognised legitimate interests, reworked automated
decision-making), and EV-0069 (OpenSSF Scorecard, read the repository's
actual state rather than its self-description). Two more are cited for
their licence flags rather than their content, because they are the
live examples of a no-derivatives constraint inside our own evidence
base: EV-0182 and EV-0096, both CC BY-NC-ND 4.0, paraphrase only.

One correction to the ledger falls out of this work. EV-0225 records
that the ICO's own pages refused automated access, so the reading of
the Act rested on the statute plus secondary reporting. The revised
Article 13 text on legislation.gov.uk is machine-readable and now shows
the amendments in force from 2026-02-05, which gives a primary route to
the same answer without the ICO site.

## Three philosophies, and when each fits

**One. The standing verdict.** The ASF policy is the mature form: a
small group decides once that licences fall into freely includable,
includable under stated conditions, and never, and everyone downstream
applies the verdict mechanically. Blue Oak does the same for the
permissive family with a four-step quality gradient published as JSON,
which is a verdict you can import rather than read. This fits anything
high volume and low stakes per item, which is exactly what a dependency
tree is.

Trade-off: the verdict encodes the decider's situation, not yours. The
ASF bans the GPL family outright because everything it releases must
stay permissively licensed; a venture that never distributes a combined
work has no such promise to keep, and copying the ban blocks safe
dependencies while saying nothing about the network trigger that does
apply. Anti-pattern: importing the categories without importing the
reason, then defending the rule when it misfires.

**Two. Declare, do not detect.** REUSE 3.3 makes licensing a property
of each file: SPDX tags in headers, a sibling `.license` for files that
cannot hold comments, full texts in `LICENSES/`, bulk cases in
`REUSE.toml` by glob with defined precedence, and a lint tool that
turns the whole question into a CI pass or fail. SPDX supplies the
vocabulary, both the identifier list and the expression grammar where
AND means all obligations bite at once and OR means a choice someone
must actually record having made. The DCO does the same trick for
inbound work: one sign-off line per commit, checkable by a hook, with
the evidence sitting in the history.

This fits everything we publish, and it is the only pattern here that a
cold agent can satisfy without judgement. Trade-off: it proves
declarations are present and consistent, never that they are correct. A
fully conformant repository can declare the wrong licence.
Anti-pattern: treating a green lint as a compliance result.

**Three. Certify the process.** OpenChain ISO/IEC 5230:2020 names where
in the lifecycle compliance decisions happen, who makes them, and
whether the arrangement survives the person who set it up. It is
deliberately minimal and self-certification counts as much as third
party attestation. This fits an organisation with roles to assign. For
a one or two person venture it is satisfiable in an afternoon and
teaches nothing, so its value here is the sustainability question
alone: what happens to this decision when nobody remembers making it.

**A fourth, weaker one. Scan and review.** ScanCode v32.5.0 compares
full licence texts against a curated database rather than matching
headers with regular expressions, and picks up copyrights, package
manifests and declared dependencies in the same pass. Treat it as the
inventory producer, never the verdict producer. The evidence here is
thin on purpose: the project claims the most accurate detection engine
and publishes no accuracy figure on the page read, and no disclaimer
about legal advice was found there. That is a vendor claim, recorded as
one.

## Where the sources disagree

**Same facts, opposite action.** The FSF and the ASF agree completely
on the mechanics: GPLv2 and GPLv3 do not combine, and the Apache 2.0
patent terms are incompatible with GPLv2 while GPLv3 was written to
accept them. The FSF reads this as a reason to release under GPLv3 or
later; the ASF reads it as a reason to exclude the GPL family. Neither
is wrong. The disagreement is about which promise you are keeping to
your own downstream, and a venture must answer that before it can
adopt either rule.

**Three axes that are not one axis.** OSI approval asks whether a
licence restricts the wrong things. FSF free asks a related but
separate question, which is why the SPDX list carries them as two
independent flag columns and declines to merge them. Blue Oak asks
whether the drafting is any good. A licence can clear the Open Source
Definition and still be rated lead. Any pack rule that says "use an
open source licence" and stops there has collapsed three axes into one.

**The load-bearing contradiction: where copyleft actually triggers.**
The ASF framework reasons entirely in terms of source releases and
binary distribution, and its categories fall apart on a hosted service
because nothing is ever distributed. The AGPL section 13 obligation
runs the other way: a modified version reached by users over a network
must offer them the corresponding source, with no distribution needed.
So the dominant industry policy and the licence term most likely to
bite a venture that sells a hosted product are aimed at different
events. Worse, the AGPL question turns on what counts as modification
and where the program boundary sits behind an internal service, and the
licence text does not resolve either. This is the one place in this
domain where a wrong default is expensive and no source read settles
it, so it belongs in the escalation list rather than in a rule.

## Binding, default, preference

**Binding.** Every repository carries a licence file at its root and a
declared SPDX expression. No dependency enters without a recorded SPDX
expression; an unlicensed dependency is a blocking finding, because
absence of a licence is exclusive copyright and platform terms that let
you fork grant no right to use. AGPL and any copyleft in a shipped
artefact require a written decision before merge, not at release.
Before any personal data is processed, the privacy notice covers the
Article 13 checklist including both complaint routes, and the ICO
registration self-assessment is run and its outcome recorded, because
the charge duty exists independently of how good the notice is.

**Default.** A three-bucket allowlist keyed on SPDX identifiers,
enforced in CI, with the reason for each bucket written next to it.
REUSE-style per-file tagging for anything published. DCO sign-off on
inbound contributions, hook-checked. A dependency licence scan whose
output is an inventory routed to a human, not a gate that passes
silently.

**Preference.** Blue Oak rating as a tiebreak when choosing an outbound
licence. MIT against Apache-2.0. Which scanner.

## Open questions, honestly

- **CLA against DCO.** We have the DCO as a primary source and nothing
  comparable on contributor licence agreements, and no source compares
  the two on outcomes. The choice currently rests on assertion.
- **Agent-written code.** The US Copyright Office is answering
  copyrightability and training data as staged, separate inquiries and
  has not finished. No equivalent UK determination was located at this
  cutoff, so this is unresolved rather than merely unread. Record
  provenance; do not assume authorship.
- **Scanner accuracy.** No measured figure was found for any detector,
  and accuracy is not portable between codebases anyway, since scanning
  a REUSE-conformant project is a far easier problem.
- **The commercial activity line.** The Cyber Resilience Act turns on
  whether software is made available in the course of a commercial
  activity, and the Commission summary asserts the line without
  resolving the cases that matter, such as a sponsored maintainer or a
  hosted version of one's own project. Reporting obligations start
  2026-09-11 and full application 2027-12-11, so this needs a refresh
  before either date.
- **The fee figures.** Only the structure of SI 2018/480 was retrieved,
  not the tier amounts, and the version read is the text as made. Never
  quote a number from that record.

## When to stop and get actual legal advice

Four triggers, all cheap to detect and all expensive to get wrong:
copyleft code entering something we distribute or host in modified
form; any relicensing, licence change or transfer of contributor
rights; any personal data leaving the UK or any regulator contact,
including a data subject complaint escalating; and any letter alleging
infringement. Everything else in this domain is routing, and routing is
what the pack automates.

## Refresh triggers

Re-run on any of: a new SPDX License List release; a change to the ASF
policy page; the Cyber Resilience Act dates of 2026-09-11 and
2027-12-11; further Data (Use and Access) Act 2025 commencement; the
final publication of Copyright Office Part 3; and the ICO's own pages
becoming machine-readable again, which would remove the workaround this
synthesis currently depends on.
