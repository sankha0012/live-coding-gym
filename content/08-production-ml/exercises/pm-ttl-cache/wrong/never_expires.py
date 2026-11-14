class TTLCache:
    def __init__(self, ttl_s, max_size, clock):
        if max_size < 1:
            raise ValueError("max_size must be at least 1")
        self.max_size = max_size
        self._data = {}

    def set(self, key, value):
        self._data.pop(key, None)
        if len(self._data) >= self.max_size:
            del self._data[next(iter(self._data))]
        self._data[key] = value

    def get(self, key, default=None):
        return self._data.get(key, default)

    def __len__(self):
        return len(self._data)
