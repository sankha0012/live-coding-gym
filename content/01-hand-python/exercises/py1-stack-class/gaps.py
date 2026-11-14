class Stack:
    def __init__(self):
        self._items = ____

    def push(self, x):
        self._items.____(x)

    def pop(self):
        if not self._items:
            raise ____("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if not self._items:
            raise IndexError("peek from empty stack")
        return self._items[____]

    def __len__(self):
        return ____(self._items)
