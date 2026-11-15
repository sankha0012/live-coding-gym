arrivals_a = [("m_b", 0.9), ("m_a", 0.9), ("m_c", 0.7), ("m_d", 0.9)]
arrivals_b = list(reversed(arrivals_a))


def top2(rows):
    ranked = sorted(rows, key=lambda r: r[1], reverse=True)
    return [name for name, _ in ranked[:2]]


def top2_fixed(rows):
    ranked = sorted(rows, key=lambda r: (-r[1], r[0]))
    return [name for name, _ in ranked[:2]]


print("naive a:", top2(arrivals_a))
print("naive b:", top2(arrivals_b))
print("fixed a:", top2_fixed(arrivals_a))
print("fixed b:", top2_fixed(arrivals_b))
print("naive stable across orders:", top2(arrivals_a) == top2(arrivals_b))
print("fixed stable across orders:", top2_fixed(arrivals_a) == top2_fixed(arrivals_b))
