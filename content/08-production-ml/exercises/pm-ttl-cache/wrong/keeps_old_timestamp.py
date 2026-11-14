class TTLCache:
    def __init__(self, ttl_s, max_size, clock):
        if max_size < 1:
            raise ValueError("max_size must be at least 1")
        self.ttl_s, self.max_size, self.clock = ttl_s, max_size, clock
        self._data = {}

    def _purge(self):
        now = self.clock()
        for k in [k for k, (_, t) in self._data.items() if now - t >= self.ttl_s]:
            del self._data[k]

    def set(self, key, value):
        self._purge()
        if key in self._data:
            self._data[key] = (value, self._data[key][1])
            return
        if len(self._data) >= self.max_size:
            del self._data[next(iter(self._data))]
        self._data[key] = (value, self.clock())

    def get(self, key, default=None):
        self._purge()
        item = self._data.get(key)
        return default if item is None else item[0]

    def __len__(self):
        self._purge()
        return len(self._data)
