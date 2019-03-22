class Item(object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.key == other.key
        return self.key == other

    def __gt__(self, other):
        if isinstance(other, type(self)):
            return self.key > other.key
        return self.key > other

    def __lt__(self, other):
        if isinstance(other, type(self)):
            return self.key < other.key
        return self.key < other

    def __str__(self):
        return "{" + str(self.key) + ": " + str(self.value) + "}"

    def __repr__(self):
        str(self)


class Map(object):
    def __init__(self):
        self.list = list()

    def insert(self, key, value):
        self.ordered_insert(Item(key, value))

    def ordered_insert(self, item):
        for i, list_item in enumerate(self.list):
            if list_item == item:
                raise ValueError()
            elif list_item > item:
                self.list.insert(i, item)
                return
        self.list.append(item)

    def _get_item(self, key):
        index = self.binary_search(self.list, key, 0, len(self.list))
        try:
            return self.list[index]
        except IndexError:
            pass

    def __contains__(self, key):
        return self._get_item(key) is not None

    def binary_search(self, a_list, item, lo, hi):
        mid = (hi + lo) // 2
        if hi - lo <= 1:
            if a_list[mid] < item and lo != hi:
                return mid + 1
            return mid
        elif a_list[mid] == item:
            return mid
        elif a_list[mid] < item:
            return self.binary_search(a_list, item, mid, hi)
        return self.binary_search(a_list, item, lo, mid)

    def find(self, key):
        item = self._get_item(key)
        return None if item is None else item.value

    def update(self, key, value):
        item = self._get_item(key)
        if item is not None:
            item.value = value

    def remove(self, key):
        index = self.binary_search(self.list, key, 0, len(self.list))
        if self.list[index] == key:
            self.list.pop(index)

    def __str__(self):
        return str(self.list)

    def __len__(self):
        return len(self.list)


if __name__ == "__main__":
    a = Map()
    a.insert(5, 1)
    a.insert(3, 123)
    a.update(3, 34)
    a.insert(1, 123)
    a.insert(80, 123)
    print(a)
    print(80 in a)

    a.remove(5)
    print(a.find(3))
    print(a)
    a.find(81)
