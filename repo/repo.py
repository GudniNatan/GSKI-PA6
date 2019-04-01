import shelve
from dataclasses import asdict, fields, replace
from sortedcontainers import SortedDict, SortedSet
from math import inf


class RelationError(Exception):
    """Should be raised when unable to link relational attributes."""

    pass


class Repo(object):
    """The Repo holds dataclass objects and allows ordering by any key.

    This is fast as data is stored via binary search trees created for every
    key. This means that space complexity goes up by n for every key in the
    dataclass, but operation speed should be as follows:
    - insert: O(log(n))
    - update: O(log(n))
    - delete: O(log(n))
    - get by any key: O(log(n))
    - get ordered by any key: O(n)

    The Repo expects the dataclasses it holds to be hashable.
    When a add, update, or delete are used the Repo will return an array with
    tuples of:
    - The result message / what was changed
    - The reverse function, if called has the opposite effect, e.g. add/remove
    - The instance affected
    This is done recursively as commands such as delete may affect more than
    just the object you're deleting, such as all related objects.
    """

    def __init__(self, dataclass, max_items=-1):
        self.max_items = inf if max_items < 0 else max_items
        self.dataclass = dataclass
        self.dicts = {field.name: SortedDict() for field in fields(dataclass)}
        # When items are updated/deleted reliant repos are too
        self.reliant_repos = list()
        try:
            self.load()
        except KeyError:
            pass

    def save(self):
        with shelve.open('data/data') as db:
            db[self.dataclass.__name__] = {
                "dicts": self.dicts,
                "max_items": self.max_items,
            }

    def load(self):
        try:
            with shelve.open('data/data') as db:
                class_rep = db[self.dataclass.__name__]
                self.dicts = class_rep["dicts"]
                self.max_items = class_rep["max_items"]
        except (KeyError, TypeError):
            pass

    def add(self, instance, *args):
        """Add an instance of the dataclass to the Repo."""
        name = self.dataclass.__name__
        print(instance in self)
        if instance not in self:
            message = f"Added {name} succesfully to the repo.\n"
        else:
            message = f"{name} already in the repo.\n"
        for field, sorted_dict in self.dicts.items():
            field_val = instance.__getattribute__(field)
            try:
                sorted_dict[field_val].add(instance)
            except KeyError:
                sorted_dict[field_val] = SortedSet((instance,))
        if args:
            return [(message, self.remove, instance)] + self.add(*args)
        return [(message, self.remove, instance)]

    def _rem(self, instance, *args):
        for field, sorted_dict in self.dicts.items():
            field_val = instance.__getattribute__(field)
            matching_set = sorted_dict[field_val]
            matching_set.remove(instance)
            if not matching_set:
                sorted_dict.pop(field_val)
        name = self.dataclass.__name__
        message = f"Removed {name} successfully from the repo\n"
        if args:
            self._rem(*args)
        return [(message, self.add, instance)]

    def remove(self, instance, *args):
        """Remove an instance of the dataclass from the Repo."""
        undos = list()
        for repo in self.reliant_repos:
            field_name = self.dataclass.__name__.lower()
            results = repo.full_item_search(field_name, instance)
            for item in list(results):
                undos.extend(repo.remove(item))
        message = self._rem(instance, *args)
        return message + undos

    def update(self, old_instance, new_instance):
        """Update an old instance of the dataclass with a new one."""
        undos = self._rem(old_instance)
        repo_results = list()
        field_name = self.dataclass.__name__.lower()
        for repo in self.reliant_repos:
            results = list(repo.full_item_search(field_name, old_instance))
            repo_results.append((repo, results))
            for old_item in results:
                undos.extend(repo._rem(old_item))
        re_add_result = self.add(new_instance)
        for repo, results in repo_results:
            for old_item in results:
                new_item = replace(old_item, **{field_name: new_instance})
                try:
                    undos.extend(repo.add(new_item))
                except RelationError as err:
                    msg, rev, item = undos[-1]
                    msg += str(err)
                    undos[-1] = (msg, rev, item)
        undos.extend(re_add_result)        
        return undos

    def contains(self, instance):
        """Get if the instance of the dataclass is in this Repo."""
        return instance in self

    def search(self, field, key):
        """Get a SortedSet of all results matching key in given field."""
        return self.full_item_search(field, key)

    def full_item_search(self, field, key):
        try:
            return self.dicts[field][key]
        except KeyError:
            return set()

    def get(self, field, key):
        """Get first result matching key in given field."""
        return self.dicts[field][key][0]

    def search_range(self, field, lo, hi):
        """Get an ordered list of all results with key within given range."""
        results = self.dicts[field].irange(lo, hi)
        result_list = [self.dicts[field][result] for result in results]
        return [item for sublist in result_list for item in sublist]  # flatten

    def order_by(self, field):
        """Get a list of all items in the datatree ordered by field."""
        ordered_dict = self.dicts[field]
        return [item for sublist in ordered_dict.values() for item in sublist]

    def get_all(self):
        """Get a set containing every element in the Repo."""
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

    def clear(self):
        class_fields = fields(self.dataclass)
        self.dicts = {field.name: SortedDict() for field in class_fields}

    def __iter__(self):
        for ordered_dict in self.dicts.values():
            for keyset in ordered_dict.values():
                yield from keyset
            return

    def __str__(self):
        return str(self.get_all())

    def __contains__(self, instance):
        for field in asdict(instance):
            field_val = instance.__getattribute__(field)
            return instance in self.full_item_search(field, field_val)

    def __del__(self):
        """Save the repo on deletion/quit."""
        self.save()

    def get_related(self, instance: "dataclass", relationRepo: "Repo"):
        """Get set of related instances of instance in relationRepo."""
        other = None
        for field in fields(relationRepo.dataclass):
            if field != self.dataclass.__name__:
                other = field
        results = relationRepo.search(self.dataclass.__name__, instance)
        return {result[other] for result in results}
