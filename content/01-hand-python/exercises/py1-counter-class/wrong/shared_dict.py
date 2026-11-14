class Counter:
    _counts = {}

    def __init__(self):
        pass

    def add(self, item, k=1):
        self._counts[item] = self._counts.get(item, 0) + k

    def count(self, item):
        return self._counts.get(item, 0)

    def total(self):
        return sum(self._counts.values())

    def most_common(self, n):
        ranked = sorted(self._counts.items(), key=lambda kv: (-kv[1], kv[0]))
        return ranked[:n]
