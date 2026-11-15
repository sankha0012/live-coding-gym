class Stack:
    def __init__(self):
        self._items = []
    def push(self, x):
        self._items.append(x)
    def pop(self):
        v = self._items.pop() if self._items else None
        if v is None:
            raise IndexError("empty")
        return v
    def peek(self):
        if not self._items or self._items[-1] is None:
            raise IndexError("empty")
        return self._items[-1]
    def __len__(self):
        return len(self._items)
