from collections import deque


class BoundedQueue:
    def __init__(self, capacity, policy="drop_oldest"):
        if capacity < 1 or policy not in ("drop_oldest", "reject"):
            raise ValueError("bad")
        self.capacity, self.policy, self.dropped = capacity, policy, 0
        self._items = deque()

    def put(self, item):
        if len(self._items) >= self.capacity:
            self.dropped += 1
            return False
        self._items.append(item)
        return True

    def get(self):
        if not self._items:
            raise IndexError("empty")
        return self._items.popleft()

    def __len__(self):
        return len(self._items)
