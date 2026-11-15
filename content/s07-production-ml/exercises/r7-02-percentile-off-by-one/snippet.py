import math

latencies_ms = [12, 15, 11, 14, 13, 16, 18, 12, 15, 14,
                13, 17, 19, 14, 15, 13, 16, 12, 14, 400]


def p95_naive(values):
    ordered = sorted(values)
    return ordered[int(0.95 * len(ordered))]


def p95_nearest_rank(values):
    ordered = sorted(values)
    return ordered[math.ceil(0.95 * len(ordered)) - 1]


print(len(latencies_ms))
print(p95_naive(latencies_ms))
print(p95_nearest_rank(latencies_ms))
print(max(latencies_ms))
