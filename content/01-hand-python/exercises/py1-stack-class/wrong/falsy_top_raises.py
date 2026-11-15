class Stack:
    def __init__(self):
        self._items = []
    def push(self, x):
        self._items.append(x)
    def pop(self):
        if not self._items or not self._items[-1]:
            raise IndexError("empty")
        return self._items.pop()
    def peek(self):
        if not self._items or not self._items[-1]:
            raise IndexError("empty")
        return self._items[-1]
    def __len__(self):
        return len(self._items)
