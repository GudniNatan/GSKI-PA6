from functools import total_ordering


class NotFoundException(Exception):
    pass


class ItemExistsException(Exception):
    pass


@total_ordering
class BSTNode(object):
    def __init__(self, key, value, left=None, right=None):
        self.key = key
        self.value = value
        self.left = left
        self.right = right

    def __str__(self):
        return f"{{{self.key}:{self.value}}}"

    def __eq__(self, other):
        if isinstance(other, BSTNode):
            return self.key == other.key
        return self.key == other

    def __lt__(self, other):
        if isinstance(other, BSTNode):
            return self.key < other.key
        return self.key < other


class Map(object):
    def __init__(self, *args, **kwargs):
        self.root = None
        self.size = 0

    # Public functions
    def insert(self, key, value):
        if self.root is None:
            self.root = BSTNode(key, value)
        else:
            self.__add_recur(key, self.root, value)
        self.size += 1

    def update(self, key, data):
        self.__findNode(self.root, key).value = data

    def find(self, key):
        return self.__findNode(self.root, key).value

    def contains(self, key):
        try:
            self.__findNode(self.root, key)
            return True
        except NotFoundException:
            return False

    def remove(self, value):
        self.root = self.__rem(value, self.root)
        self.size -= 1

    def __setitem__(self, key, data):
        try:
            self.insert(key, data)
        except ItemExistsException:
            self.update(key, data)

    def __getitem__(self, key):
        return self.find(key)

    def __len__(self):
        return self.size

    def __str__(self):
        return " ".join(map(str, self.__inorder()))

    # Internal functions
    def __add_recur(self, key, node, value):
        if node < key:
            if node.right is None:
                node.right = BSTNode(key, value)
            else:
                self.__add_recur(key, node.right, value)
        elif key < node:
            if node.left is None:
                node.left = BSTNode(key, value)
            else:
                self.__add_recur(key, node.left, value)
        else:
            raise ItemExistsException

    def __rem(self, key, node):
        if node is None:
            raise NotFoundException()
        elif key < node:
            node.left = self.__rem(key, node.left)
        elif node < key:
            node.right = self.__rem(key, node.right)
        else:
            node = self.__remove_node(node)
        return node

    def __remove_node(self, node):
        if node.left is None or node.right is None:
            return node.left or node.right
        leftmost = self.__leftmost(node.right)
        node.key = leftmost.key
        node.value = leftmost.value
        node.right = self.__rem(leftmost.key, node.right)
        return node

    def __leftmost(self, node):
        """Find leftmost node in subtree of given node."""
        if node.left:
            return self.__leftmost(node.left)
        return node

    def __findNode(self, node, key):
        if node is None:
            raise NotFoundException()
        elif key < node:
            return self.__findNode(node.left, key)
        elif node < key:
            return self.__findNode(node.right, key)
        return node

    def __inorder(self):
        """Create an inorder iterator for this BST map."""
        return self.__inorder_recur(self.root)

    def __inorder_recur(self, node):
        if node is not None:
            yield from self.__inorder_recur(node.left)
            yield node
            yield from self.__inorder_recur(node.right)

    # Extra
    def __contains__(self, key):
        return self.contains(key)

    def search(self, lo, hi=None):
        if hi is None:
            hi = lo
        yield from self._search_recur(lo, hi, self.root)

    def _search_recur(self, lo, hi, node):
        """Search for matching data within the specified range."""
        if node is None:
            return
        if lo <= node.key <= hi:
            yield from self._search_recur(lo, hi, node.left)
            yield node.data
            yield from self._search_recur(lo, hi, node.right)
        elif lo > node:
            yield from self._search_recur(lo, hi, node.right)
        else:
            yield from self._search_recur(lo, hi, node.left)


if __name__ == "__main__":
    m = Map()
    m.insert(17, "fimma")
    m.insert(22, "fjarri")
    m.insert(13, "tvistur")
    m.insert(14, "fimmarimma")
    m.insert(24, "fjarkalki")
    m.insert(11, "fjarlarki")
    m.insert(16, "fkalarki")
    m.insert(18, "fjarkalarki")
    m.insert(9, "fjalarki")
    m.insert(3, "fjarkalarki")
    m.insert(1, "fjaalari")
    m[17] = "sexa"
    print(m)
