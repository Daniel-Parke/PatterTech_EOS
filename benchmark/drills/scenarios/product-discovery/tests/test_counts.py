import pytest

from app.counts import Count, CountClosed
from app.items import Catalogue, Item


def a_count():
    return Count(count_id="c-1", site="deli", area="dry store",
                 opened_by="priya")


def test_entering_the_same_item_twice_replaces_the_line():
    count = a_count()
    count.enter("i-1", 6, "each", "priya")
    count.enter("i-1", 2.5, "kg", "ellie")
    assert count.total_lines() == 1
    assert count.lines["i-1"].entered_by == "ellie"


def test_a_closed_count_refuses_writes():
    count = a_count()
    count.close()
    with pytest.raises(CountClosed):
        count.enter("i-1", 6, "each", "priya")


def test_missing_lists_items_nobody_entered():
    count = a_count()
    count.enter("i-1", 6, "each", "priya")
    assert count.missing(["i-1", "i-2"]) == ["i-2"]


def test_search_ignores_archived_items():
    catalogue = Catalogue([
        Item("i-1", "chopped tomatoes", "tin"),
        Item("i-2", "chopped parsley", "bunch", archived=True),
    ])
    assert [i.item_id for i in catalogue.search("chopped")] == ["i-1"]
