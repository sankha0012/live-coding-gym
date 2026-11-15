from collections import deque


class BoundedQueue:
    def __init__(self, capacity: int, policy: str = "drop_oldest"):
        if capacity < 1:
            raise ValueError("capacity must be at least 1")
        if policy not in ("drop_oldest", "reject"):
            raise ValueError(f"unknown policy {policy!r}")
        self.capacity = capacity
        self.policy = policy
        self.dropped = 0
        self._items = deque()

    def put(self, item) -> bool:
        if len(self._items) > self.capacity:
            self.dropped += 1
            if self.policy == "reject":
                return False
            self._items.popleft()
        self._items.append(item)
        return True

    def get(self):
        if not self._items:
            raise IndexError("queue is empty")
        return self._items.popleft()

    def __len__(self) -> int:
        return len(self._items)
