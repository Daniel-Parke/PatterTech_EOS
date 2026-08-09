"""The item list a site counts against."""

from dataclasses import dataclass


@dataclass
class Item:
    item_id: str
    name: str
    unit: str
    unit_cost: float = None
    supplier: str = ""
    archived: bool = False


class Catalogue:
    def __init__(self, items=()):
        self._items = {item.item_id: item for item in items}

    def add(self, item):
        self._items[item.item_id] = item
        return item

    def get(self, item_id):
        return self._items.get(item_id)

    def live(self):
        return [i for i in self._items.values() if not i.archived]

    def search(self, term):
        term = term.strip().lower()
        if not term:
            return []
        return [i for i in self.live() if term in i.name.lower()]

    def __len__(self):
        return len(self._items)
