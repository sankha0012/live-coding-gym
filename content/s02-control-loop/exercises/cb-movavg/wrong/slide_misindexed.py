def MovingAverage(s):
    parts = s.split()
    k = int(parts[0])
    xs = [float(x) for x in parts[1:]]
    if len(xs) < k:
        return "none"
    window = sum(xs[:k])
    out = [window / k]
    for i in range(k, len(xs)):
        window += xs[i] - xs[i - k + 1]
        out.append(window / k)
    return ",".join(f"{v:.2f}" for v in out)

print(MovingAverage(input()))
