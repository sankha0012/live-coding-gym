class TTLCache:
    def __init__(self, ttl_s, max_size, clock):
        if max_size < 1:
            raise ValueError("max_size must be at least 1")
        self.ttl_s = ttl_s
        self.max_size = max_size
        self.clock = clock
        self._data = {}  # key -> (value, stored_at, ttl), oldest set first

    def _purge(self):
        now = self.clock()
        dead = [k for k, (_, t, ttl) in self._data.items() if now - t >= ttl]
        for k in dead:
            del self._data[k]

    def set(self, key, value, ttl_s=None):
        self._purge()
        self._data.pop(key, None)
        if len(self._data) >= self.max_size:
            del self._data[next(iter(self._data))]
        self._data[key] = (value, self.clock(), self.ttl_s if ttl_s is None else ttl_s)

    def get(self, key, default=None):
        self._purge()
        item = self._data.get(key)
        return default if item is None else item[0]

    def __len__(self):
        self._purge()
        return len(self._data)
