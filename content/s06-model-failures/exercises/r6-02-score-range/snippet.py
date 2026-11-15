scores = [0.92, 1.30, 0.48, -0.20, 0.51]
THRESHOLD = 0.5

flagged = [s for s in scores if s >= THRESHOLD]
print("flagged:", flagged)
print("rate:", len(flagged) / len(scores))
print("mean:", round(sum(scores) / len(scores), 3))

clean = [s for s in scores if 0.0 <= s <= 1.0]
print("kept:", len(clean), "dropped:", len(scores) - len(clean))
print("clean mean:", round(sum(clean) / len(clean), 3))
