from collections import defaultdict
class Counter:
    def __init__(self): self._c = defaultdict(int)
    def add(self, item, k=1): self._c[item] += k
    def count(self, item): return self._c[item]
    def total(self): return sum(self._c.values())
    def most_common(self, n):
        return sorted(self._c.items(), key=lambda kv: (-kv[1], kv[0]))[:n]
