scores = {"u1": 0.71, "u2": float("nan"), "u3": 0.93, "u4": 0.40, "u5": 0.88}

ranked = sorted(scores, key=scores.get, reverse=True)
print("ranked:", ranked)
print("top2:", ranked[:2])

best = max(scores, key=scores.get)
print("max:", best)

valid = {k: v for k, v in scores.items() if v == v}
print("valid:", sorted(valid, key=valid.get, reverse=True))
