from structures.array_deque import ArrayDeque
from structures.sll import LinkedList


class Queue:
    def __init__(self, type: str):
        if type == 'array':
            self.container = ArrayDeque()
        else:
            self.container = LinkedList()

    def add(self, element):
        self.container.push_back(element)

    def remove(self):
        return self.container.pop_front()

    def get_size(self):
        return self.container.get_size()
