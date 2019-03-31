import shelve
from dataclasses import asdict, fields
from sortedcontainers import SortedDict, SortedSet
from collections import deque
from math import inf


class RelationError(Exception):
    """Should be raised when unable to link relational attributes."""
    pass


class RepoFullError(Exception):
    """Should be raised when repo is full."""
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

    There is an additional feature of a max amount of items the repo can hold.
    If the repo itself is full, the items can be added to the instance queue,
    where they will be added to the repo as soon as space is available (such as
    on a deletion). If a queued item is added to the repo the message, remove
    function for the item and item will be returned alongside the presumed
    deleted item message, add function and item. Additionally a function
    adding the item back onto the front of the front of the queue will be
    provided.
    """

    def __init__(self, dataclass, max_items=-1):
        self.max_items = inf if max_items < 0 else max_items
        self.size = 0
        self.instance_queue = deque()
        self.dataclass = dataclass
        self.dicts = {field.name: SortedDict() for field in fields(dataclass)}
        try:
            self.load()
        except KeyError:
            pass

    def save(self):
        with shelve.open('data/data') as db:
            db[self.dataclass.__name__] = {
                "dicts": self.dicts,
                "max_items": self.max_items,
                "size": self.size,
                "instance_queue": self.instance_queue
            }

    def load(self):
        try:
            with shelve.open('data/data') as db:
                class_rep = db[self.dataclass.__name__]
                self.dicts = class_rep["dicts"]
                self.max_items = class_rep["max_items"]
                self.size = class_rep["size"]
                self.instance_queue = class_rep["instance_queue"]
        except (KeyError, TypeError):
            pass

    def add(self, instance, *args):
        """Add an instance of the dataclass to the Repo."""
        if instance not in self:
            if self.size > self.max_items:
                raise RepoFullError()
            self.size += 1
            message = f"Added {instance} succesfully to the repo\n"
        else:
            message = f"{instance} already in the repo."
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
        self.size -= 1
        message = f"Removed {instance} successfully from the repo\n"
        if args:
            self._rem(*args)
        return [(message, self.add, instance)]

    def remove(self, instance, *args):
        """Remove an instance of the dataclass from the Repo."""
        message = self._rem(instance, *args)
        if self.instance_queue:  # add from queue if not empty
            message += self.queue_add()
        return message

    def update(self, old_instance, new_instance):
        """Update an old instance of the dataclass with a new one."""
        return self._rem(old_instance) + self.add(new_instance)

    def contains(self, instance):
        """Get if the instance of the dataclass is in this Repo."""
        return instance in self

    def search(self, field, key):
        """Get a SortedSet of all results matching key in given field."""
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

    def enqueue(self, instance):
        """Add an instance to the repo queue.

        The instance will be added to the repo itself as soon as space is
        available.
        """
        self.instance_queue.append(instance)

    def queue_add(self):
        """Add from the queue to the repo."""
        if self.size < self.max_items:
            raise RepoFullError
        instance = self.instance_queue.get()
        reponame = type(self).__name__
        message = f"Added {instance} from the queue to the {reponame}"
        return self.add(instance) + [
            (message, self.instance_queue.append_left, instance)
        ]

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
            return instance in self.search(field, field_val)

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
