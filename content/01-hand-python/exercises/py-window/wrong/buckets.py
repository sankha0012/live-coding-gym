from collections import Counter
def max_in_window(ts, w=60):
    c = Counter(t // w for t in ts)
    return max(c.values(), default=0)
