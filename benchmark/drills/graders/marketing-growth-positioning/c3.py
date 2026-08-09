#!/usr/bin/env python3
"""Criterion 3: a segment the product is explicitly not for.

The criterion the drill exists for, and the one an agent trained to be
helpful softens. Three things are checked, in this order:

- an exclusion has to be stated outright, not hedged. "May not be ideal
  for" is a hedge and is reported as one.
- the excluded thing cannot be a universal. "Not for everyone" excludes
  nobody and the frozen spec says so in as many words.
- the excluded thing has to be bounded enough that a reader could hold
  a lead against it: a number, a named kind of buyer, or a noun with a
  clause attached that says which ones.

What no script settles is whether a salesperson would actually walk
away on the strength of the sentence. This grader checks the floor the
spec states and reports what it matched, so a human reading the run can
see the sentence rather than trust the verdict.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import (FAIL, PASS, emit, one_line, scratch_dir,  # noqa: E402
                     sentences, the_doc)

CID = "c3"

HARD = re.compile(
    r"\b(?:is |are |it is |we are )?not (?:for|built for|aimed at|meant for|"
    r"designed for|sold to|the right (?:tool|fit|choice|product) for)\b|"
    r"\bwe do not (?:serve|sell to|build for|target|want)\b|"
    r"\bdo not (?:buy|choose|use) (?:this|us|it)\b|"
    r"\bwrong (?:tool|fit|choice|product) for\b|"
    r"\bwill not work for\b|\bwe turn (?:away|down)\b|\bwe say no to\b|"
    r"\bwe walk away from\b|\bdisqualif\w*\b|\bnot who (?:this|it) is for\b|"
    r"\bout of scope\b|\bwe should not sell to\b", re.I)

SOFT = re.compile(
    r"\b(?:may|might|can|could) not be\b|\bless (?:suited|well suited|of a "
    r"fit|relevant)\b|\bnot ideal for\b|\bnot always\b|\bprimarily (?:for|"
    r"aimed)\b|\bbest suited\b|\bless of a fit\b|\bmay be a poor fit\b",
    re.I)

# A document that talks about its own exclusion ("the paragraph about
# who this is not for") is quoting itself, not excluding anybody. The
# cue there belongs to the sentence it refers to.
ABOUT_ITSELF = re.compile(
    r"\b(?:about|paragraph|sentence|section|statement|line|heading|"
    r"claim that|says?) [^.]{0,30}$", re.I)

VAGUE = re.compile(
    r"^\W*(?:everyone|everybody|anyone|anybody|all|every ?one|"
    r"all practices|every practice|every clinic|every business|"
    r"some practices|others|other people|any practice)\b", re.I)

NUMBER = re.compile(
    r"\d|\b(?:one|two|three|four|five|six|seven|eight|nine|ten|twelve|"
    r"fifteen|twenty|thirty|fifty|hundred)\b", re.I)

# Kinds of buyer this market actually contains, plus the shapes of
# demand the tickets show us refusing.
SEGMENT = re.compile(
    r"\bmulti[- ]?site\b|\bmultiple sites\b|\bgroup\b|\bgroups\b|\bchain\b|"
    r"\bchains\b|\bfranchise\b|\bhospital\b|\bnhs\b|\btrust\b|\binpatient\b|"
    r"\boutpatient\b|\bclinical notes?\b|\bsoap notes?\b|\bmedical records?\b|"
    r"\binvoic\w*\b|\bclaims?\b|\bbilling\b|\bpractice management\b|"
    r"\ball[- ]in[- ]one\b|\ball in one\b|\beverything in one\b|"
    r"\bchiropract\w*\b|\bosteopath\w*\b|\bpodiatr\w*\b|\bdental\b|\bvet\w*\b|"
    r"\bgym\b|\bsports clubs?\b|\bstudent\b|\buniversity\b|"
    r"\boccupational health\b|\bmsk triage\b|\btriage service\b|"
    r"\bper[- ]practitioner\b|\bper[- ]seat\b|\benterprise\b|"
    r"\bsole trader\b|\bagency\b|\bagencies\b", re.I)

NOUN = re.compile(
    r"\b(?:practices?|clinics?|groups?|sites?|chains?|departments?|"
    r"services?|teams?|trusts?|providers?|businesses|business|buyers?|"
    r"organisations?|owners?|franchises?|schools?|gyms?|studios?|"
    r"hospitals?|surgeries|partnerships?)\b", re.I)

QUALIFIER = re.compile(
    r"\b(?:that|which|who|whose|with|without|needing|wanting|running|"
    r"looking for|expecting|requiring|over|under|more than|fewer than|"
    r"larger than|bigger than|above|below)\b", re.I)

# Words that carry no information about which buyer is meant. A clause
# built only of these is "not for the sort of buyer who would not get on
# with it", which reads like a disqualifier and disqualifies nobody.
EMPTY = {
    "fit", "fits", "good", "bad", "right", "wrong", "sort", "sorts",
    "kind", "kinds", "type", "types", "buyer", "buyers", "customer",
    "customers", "get", "getting", "along", "well", "suit", "suited",
    "suits", "want", "wants", "wanted", "need", "needs", "needed",
    "like", "likes", "use", "uses", "using", "would", "could", "should",
    "them", "they", "product", "tool", "tools", "software", "thing",
    "things", "work", "works", "really", "properly", "much", "very",
    "just", "simply", "everyone", "anyone", "everybody", "anybody",
}


def informative(span):
    """Does this clause say anything about which buyer is meant?"""
    from _common import content_words
    return sum(1 for w in content_words(span) if w not in EMPTY) >= 2


def verdict_for(span):
    """(ok, why) for the text following an exclusion cue."""
    span = span.strip(" ,:;-")
    if not span:
        return None, "the exclusion names nothing at all"
    if VAGUE.match(span):
        return False, ("the excluded segment is a universal: %r excludes "
                       "nobody" % one_line(span, 90))
    hit = SEGMENT.search(span)
    if hit:
        return True, "names %r" % hit.group(0)
    if NUMBER.search(span):
        return True, "bounded by a number"
    qualifier = QUALIFIER.search(span)
    if NOUN.search(span) and qualifier:
        if informative(span[qualifier.start():]):
            return True, "names a kind of buyer with a clause narrowing it"
        return False, ("the clause meant to narrow the segment says nothing "
                       "about which buyer is meant: %r" % one_line(span, 90))
    return False, ("the excluded segment is not bounded: %r names no "
                   "number, no kind of buyer and no clause a reader could "
                   "hold a lead against" % one_line(span, 90))


def main():
    scratch = scratch_dir()
    docs = the_doc(CID, scratch)

    best, hedges = None, []
    for where, text in docs:
        found_hard = False
        for sentence in sentences(text):
            cue = next((m for m in HARD.finditer(sentence)
                        if not ABOUT_ITSELF.search(
                            sentence[max(0, m.start() - 40):m.start()])), None)
            if cue is None:
                if SOFT.search(sentence):
                    hedges.append((where, sentence))
                continue
            ok, why = verdict_for(sentence[cue.end():])
            if ok is None:
                # A bare heading, "Not for", carries the cue and no
                # object. It is furniture, not a claim about anybody.
                continue
            found_hard = True
            if ok:
                emit(CID, PASS,
                     "%s excludes a segment outright (%s): %r"
                     % (where, why, one_line(sentence, 150)))
            best = best or (where, "%s. Sentence: %r"
                            % (why, one_line(sentence, 150)))
        if not found_hard and hedges:
            best = best or (
                where,
                "no outright exclusion, only a hedge: %r. A segment that is "
                "merely a worse fit has not been excluded"
                % one_line(hedges[0][1], 150))

    if best is None:
        where = docs[0][0]
        emit(CID, FAIL,
             "%s names no segment the product is not for: no sentence says "
             "who it is not built for, who is the wrong fit, or who the "
             "answer is no to" % where)
    where, why = best
    emit(CID, FAIL, "%s: %s" % (where, why))


if __name__ == "__main__":
    main()
