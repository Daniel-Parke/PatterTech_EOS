"""Frozen source-inventory tests for T-0026.

These tests cover the inventory-only freeze.  Reviewed dispositions live in
the separate Doctrine migration ledger.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

import pytest

from tools.eos.knowledge_migration import (
    BASELINE_COMMIT,
    EXPECTED_INVENTORY_SHA256,
    EXPECTED_STANDARD_SHA256,
    inventory_document,
    inventory_sha256,
    preliminary_authority,
    read_baseline,
)


REPO = Path(__file__).resolve().parents[1]
INVENTORY = REPO / "org" / "migration" / "DOCTRINE_SOURCE_INVENTORY.json"


@pytest.fixture(scope="module")
def blocks():
    return read_baseline(REPO)


def _find(blocks, *, pack, family, startswith):
    matches = [
        block
        for block in blocks
        if block.path == f"packs/{pack}/PACK.md"
        and block.family == family
        and block.text.startswith(startswith)
    ]
    assert len(matches) == 1
    return matches[0]


def test_frozen_count_families_and_hashes(blocks):
    assert len(blocks) == 501
    assert Counter(block.family for block in blocks) == {
        "requirements": 121,
        "defaults": 257,
        "preferences": 120,
        "voice-scope": 3,
    }
    assert inventory_sha256(blocks) == EXPECTED_INVENTORY_SHA256
    standard = [block for block in blocks if block.family != "voice-scope"]
    assert len(standard) == 498
    assert inventory_sha256(standard) == EXPECTED_STANDARD_SHA256


def test_canonical_row_encoding_is_frozen(blocks):
    block = _find(
        blocks,
        pack="agentic-development",
        family="defaults",
        startswith="**B2.",
    )
    assert block.canonical_row == (
        "packs/agentic-development/PACK.md\tdefaults\t001\t0145-0153\t"
        "9e3aa2e7005c81a4eaaab25dbc33ed18f4c9a2f5cb0b76f1bb3b6e7f34bd9ec0"
    )


def test_reconstruction_is_deterministic(blocks):
    again = read_baseline(REPO)
    assert [block.canonical_row for block in again] == [
        block.canonical_row for block in blocks
    ]
    assert [block.text for block in again] == [block.text for block in blocks]


def test_format_exceptions_are_in_the_inventory(blocks):
    api = [
        block
        for block in blocks
        if block.path == "packs/api-integration/PACK.md"
        and block.family == "requirements"
        and block.text.startswith("**BR-")
    ]
    assert len(api) == 4

    delivery = [
        block
        for block in blocks
        if block.path == "packs/delivery-testing/PACK.md"
        and block.family == "requirements"
        and block.text[0].isdigit()
    ]
    devops = [
        block
        for block in blocks
        if block.path == "packs/devops-reliability/PACK.md"
        and block.family == "requirements"
        and block.text[0].isdigit()
    ]
    assert len(delivery) == 6
    assert len(devops) == 7

    house = [
        block
        for block in blocks
        if block.path == "packs/pattertech-house/PACK.md"
        and block.family == "requirements"
        and block.text.startswith("**H")
    ]
    assert len(house) == 8

    table_default = _find(
        blocks,
        pack="identity-access",
        family="defaults",
        startswith="| Start with record ownership",
    )
    assert table_default.start == table_default.end

    taste = _find(
        blocks,
        pack="native-client",
        family="preferences",
        startswith="Taste. Depart freely",
    )
    assert taste.start == 252
    assert taste.end == 257

    voice = [block for block in blocks if block.family == "voice-scope"]
    assert [(block.ordinal, block.start, block.end) for block in voice] == [
        (1, 102, 102),
        (2, 103, 103),
        (3, 104, 104),
    ]


def test_preliminary_authority_applies_documented_overrides(blocks):
    assert preliminary_authority(_find(
        blocks,
        pack="docs-dx",
        family="requirements",
        startswith="**B1.",
    )) == "default"
    assert preliminary_authority(_find(
        blocks,
        pack="docs-dx",
        family="requirements",
        startswith="**B4.",
    )) == "binding"
    assert preliminary_authority(_find(
        blocks,
        pack="native-client",
        family="requirements",
        startswith="**B1.",
    )) == "default"
    assert preliminary_authority(_find(
        blocks,
        pack="legal-licensing",
        family="requirements",
        startswith="**B7.",
    )) == "binding"
    assert preliminary_authority(_find(
        blocks,
        pack="pattertech-house",
        family="requirements",
        startswith="**H1.",
    )) == "preference"


def test_checked_in_inventory_is_a_prose_free_fixpoint(blocks):
    checked_in = json.loads(INVENTORY.read_text(encoding="utf-8"))
    assert checked_in == inventory_document(blocks)
    assert checked_in["kind"] == "doctrine-source-inventory"
    assert checked_in["baseline_commit"] == BASELINE_COMMIT
    assert len(checked_in["rows"]) == 501
    assert all("disposition" not in row and "reason" not in row
               for row in checked_in["rows"])
    assert all("text" not in row and "source_text" not in row
               for row in checked_in["rows"])
