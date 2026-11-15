def MovingAverage(s):
    parts = s.split()
    k = int(parts[0])
    xs = [float(x) for x in parts[1:]]
    if len(xs) <= k:
        return "none"
    out = [sum(xs[i:i + k]) / k for i in range(len(xs) - k + 1)]
    return ",".join(f"{v:.2f}" for v in out)

print(MovingAverage(input()))
