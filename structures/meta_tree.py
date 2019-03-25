from dataclasses import asdict, fields
from structures.bst_map import Map


class MetaTree(object):
    """The MetaTree holds dataclass objects and allows ordering by any key.
    This is fast as data is stored via binary search trees created for every
    key. This means that space complexity goes up by n for every key in the
    dataclass, but operation speed should be as follows:
    - insert: O(log(n))
    - update: O(log(n))
    - delete: O(log(n))
    - get by any key: O(log(n))
    - get ordered by any key: O(n)

    The MetaTree expects the dataclasses it holds to be hashable.
    """

    def __init__(self, dataclass):
        self.trees = {field.name: Map() for field in fields(dataclass)}

    def add(self, instance):
        """Add an instance of the dataclass to the MetaTree."""
        instance_dict = asdict(instance)
        for field, tree in self.trees.items():
            try:
                tree[instance_dict[field]].add(instance)
            except KeyError:
                tree[instance_dict[field]] = {instance, }

    def remove(self, instance):
        """Remove an instance of the dataclass from the MetaTree."""
        instance_dict = asdict(instance)
        for field, tree in self.trees.items():
            tree[instance_dict[field]].remove(instance)

    def update(self, old_instance, new_instance):
        """Update an old instance of the dataclass with a new one."""
        self.remove(old_instance)
        self.add(new_instance)

    def contains(self, instance):
        """Get if the instance of the dataclass is in this MetaTree."""
        return instance in self

    def __contains__(self, instance):
        return instance in self.trees.values()[0]

    def search(self, field, key):
        """Get a set of all results matching key in given field."""
        try:
            return self.trees[field][key]
        except KeyError:
            return set()

    def search_range(self, field, lo, hi):
        """Get an ordered list of all results with key within given range."""
        results = self.trees[field].get_range(lo, hi)
        return [item for sublist in results for item in sublist]  # flatten

    def order_by(self, field):
        """Get a list of all items in the datatree ordered by field."""
        bst = self.trees[field]
        return [item for sublist in bst.ordered() for item in sublist]

    def get_all(self):
        """Get a set containing every element in the MetaTree."""
        return set(self)

    def multi_field_search(self, field_dict: dict):
        """Get set of all results matching values of given fields."""
        matching = None
        for field, key in field_dict.items():
            if not key:
                continue
            if matching is None:
                matching = self.search(field, key)
            else:
                matching &= self.search(field, key)
        if matching is None:
            return set()
        return matching

    def __iter__(self):
        for bst in self.trees.values():
            for keyset in bst.ordered():
                yield from keyset
            return
