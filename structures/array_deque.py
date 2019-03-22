class ArrayDeque(object):
    def __init__(self):
        self.capacity = 4
        self.back = self.front = 0
        self.arr = [None] * self.capacity
        self.size = 0

    def push_front(self, value):
        if self.capacity == self.size:
            self._resize(1)
        # Update location of front before array
        self.front = (self.front - 1) % self.capacity
        self.arr[self.front] = value
        self.size += 1

    def push_back(self, value):
        if self.capacity == self.size:
            self._resize(0)
        # Update array before location of back
        self.arr[self.back] = value
        self.back = (self.back + 1) % self.capacity
        self.size += 1

    def pop_front(self):
        if not self.is_empty():
            element = self.arr[self.front]
            self.front = (self.front + 1) % self.capacity
            self.size -= 1
            return element

    def pop_back(self):
        if not self.is_empty():
            self.back = (self.back - 1) % self.capacity
            self.size -= 1
            return self.arr[self.back]

    def get_size(self):
        return self.size

    def is_empty(self):
        return self.size <= 0

    def __str__(self):
        string = ""
        if self.is_empty():
            return string
        if self.back > self.front or self.back == 0:
            for i in range(self.front, self.front + self.size - 1):
                string += str(self.arr[i]) + " "
        else:
            for i in range(self.front, self.capacity):
                string += str(self.arr[i]) + " "
            for i in range(self.back - 1):
                string += str(self.arr[i]) + " "
        return string + str(self.arr[self.back - 1])

    def _resize(self, offset=0):
        """Resize with optional offset.

        Doubles the size of the underlying array. Offset should not be more
        than self.size - 1. Additionally it rearranges the elements so they do
        not wrap circularly.
        """
        new_arr = [None] * (self.capacity * 2)
        if self.back > self.front:
            for i in range(self.front, self.back):
                new_arr[i - self.front + offset] = self.arr[i]
        if self.back <= self.front:
            for i in range(self.front, self.capacity):
                new_arr[i - self.front + offset] = self.arr[i]
            # new_arr should now have self.capacity - self.front elements
            new_offset = self.capacity - self.front + offset
            # Reorder all the elements from 0 to self.back in the new array
            for i in range(self.back):
                new_arr[i + new_offset] = self.arr[i]
        # Update properties
        self.capacity *= 2
        self.arr = new_arr
        self.front = offset
        self.back = self.size + offset
