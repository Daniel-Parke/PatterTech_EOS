"""Pack activation measured across venture archetypes.

The 1.0 gate asks for activation precision and recall per pack, with at
least one negative case each. This is that measurement, and it is worth
being honest about what it is worth: the expected pack lists in
`fixtures/activation/profiles.json` were authored by hand from each
archetype, but in the same commit as the code that satisfies them. That
is the weaker guarantee `benchmark/drills/MANIFEST.json` records for its
Wave B specs, and a perfect score here measures internal consistency
rather than independent correctness.

The parts that do not depend on my expectations are the ones to read:
which packs no venture profile can activate at all, and which activate
in every profile. Those are properties of the vocabulary, not of the
corpus author.
"""

import json
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from tools.eos import contextgen  # noqa: E402

CORPUS = json.loads(
    (Path(__file__).parent / "fixtures" / "activation" / "profiles.json")
    .read_text(encoding="utf-8"))
PROFILES = CORPUS["profiles"]

# Every predicate these packs declare is a task fact, so no venture's
# Session 0 answers can reach them. They activate when the work arrives,
# which is `eos context` reading a task record and a diff.
TASK_ONLY_PACKS = {"agentic-swarm", "coding", "product-discovery"}


def _activated(facts):
    return {r["pack"]
            for r in contextgen.activation_from_facts(REPO, facts)["activated"]}


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p["id"])
def test_profile_activates_exactly_what_the_archetype_expects(profile):
    got = _activated(profile["facts"])
    expected = set(profile["expected_packs"])
    assert sorted(got - expected) == [], "activated a pack the archetype does not need"
    assert sorted(expected - got) == [], "missed a pack the archetype needs"


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p["id"])
def test_every_declared_fact_is_in_the_vocabulary(profile):
    """A profile carrying a typo would silently under-activate."""
    result = contextgen.activation_from_facts(REPO, profile["facts"])
    assert result["unknown_predicates"] == []


@pytest.mark.parametrize("profile", PROFILES, ids=lambda p: p["id"])
def test_every_profile_leaves_most_of_the_estate_out(profile):
    """Narrowing is the whole job.

    A system that never misses a pack because it activates everything has
    not solved activation, so the widest archetype in the corpus still
    has to leave a clear majority of packs alone.
    """
    activated = _activated(profile["facts"])
    total = len(contextgen.pack_triggers(REPO))
    assert len(activated) <= total / 2, (
        f"{profile['id']} activated {len(activated)} of {total} packs")


def test_the_disposable_script_pulls_in_nothing_but_the_always_walk():
    """The negative case that matters most.

    A one-off local script must not inherit deployment, pricing or API
    guidance. security-privacy is the exception by construction: its
    predicate runs_agents holds for every governed venture, because the
    seed exists so agents can work in the repository.
    """
    profile = next(p for p in PROFILES if p["id"] == "disposable-script")
    assert _activated(profile["facts"]) == {"security-privacy"}


def test_no_venture_profile_can_activate_a_task_only_pack():
    """Holds the finding the corpus surfaced.

    Three packs declare nothing but task facts, so a Session 0 interview
    cannot reach them however it is answered. That is correct rather than
    broken, and it is worth a test because the alternative reading, that
    the corpus is short of profiles, is the one somebody will reach for.
    """
    for pack in TASK_ONLY_PACKS:
        trigger = next(t for t in contextgen.pack_triggers(REPO)
                       if t["pack"] == pack)
        settled = _venture_settled(trigger["predicates"])
        assert settled == [], (
            f"{pack} now has a venture-settled predicate {settled}, so it "
            f"belongs in the corpus rather than in TASK_ONLY_PACKS")


def _venture_settled(predicates):
    """Those the vocabulary settles with an interview question."""
    import re
    text = (REPO / "kernel" / "PREDICATES.md").read_text(encoding="utf-8")
    head = text.split("## Retired")[0]
    rows = re.findall(r"^\|\s*`([a-z0-9_]+)`\s*\|[^|]*\|([^|]*)\|", head, re.M)
    settler = {name: cell.strip() for name, cell in rows}
    return sorted(p for p in predicates if settler.get(p, "").isdigit())


def test_every_pack_that_can_activate_does_somewhere_in_the_corpus():
    """A pack no profile reaches is either niche or wrongly predicated.

    The corpus has to say which. Silence would let a pack sit
    unactivatable behind a plausible-looking trigger list.
    """
    fires = set()
    for profile in PROFILES:
        fires |= _activated(profile["facts"])
    reachable = {t["pack"] for t in contextgen.pack_triggers(REPO)} - TASK_ONLY_PACKS
    assert sorted(reachable - fires) == []


def test_precision_and_recall_are_reported_not_assumed():
    """The gate asks for the numbers, so compute them rather than imply them."""
    tp = fp = fn = 0
    for profile in PROFILES:
        got = _activated(profile["facts"])
        expected = set(profile["expected_packs"])
        tp += len(got & expected)
        fp += len(got - expected)
        fn += len(expected - got)
    assert tp > 0
    precision = tp / (tp + fp)
    recall = tp / (tp + fn)
    assert precision == 1.0 and recall == 1.0, (
        f"precision {precision:.3f}, recall {recall:.3f}")


# --- reading the facts off a brief --------------------------------------


BRIEF = Path(__file__).parent / "fixtures" / "activation" / "BRIEF-example.md"


def test_facts_are_read_from_a_brief_rather_than_asserted_by_hand():
    """The link that makes the Session 0 walk computed rather than eyeballed."""
    facts = contextgen.facts_from_brief(BRIEF.read_text(encoding="utf-8"))
    assert facts == ["runs_agents", "has_user_interface", "hosts_service",
                     "publishes_public_content", "collects_contact_details"]
    assert _activated(facts) == {"legal-licensing", "marketing-growth",
                                 "security-privacy", "ui-ux"}


def test_a_brief_with_no_block_yields_nothing_rather_than_raising():
    """A brief compiled before the block existed is old, not malformed."""
    assert contextgen.facts_from_brief("# A brief\n\nNo block here.\n") == []


def test_an_unfilled_slot_is_not_a_fact():
    """E008 catches an unfilled slot in a seed; this must not read one as
    a predicate and then report it as unknown, which would send the
    reader hunting for a typo instead of an uncompiled template."""
    text = "## Venture facts\n\n```facts\n{{VENTURE_FACTS}}\n```\n"
    assert contextgen.facts_from_brief(text) == []
