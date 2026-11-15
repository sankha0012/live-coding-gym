batch = [{"id": 1, "x": 4}, {"id": 2, "x": 0}, {"id": 3, "x": 5}, {"id": 4}, {"id": 5, "x": 2}]

def score(row):
    return round(10 / row["x"], 2)

results = {}
for row in batch:
    try:
        results[row["id"]] = score(row)
    except:
        pass

print(results)
print("status:", "ok" if results else "failed")

failed = []
done = {}
for row in batch:
    try:
        done[row["id"]] = score(row)
    except (KeyError, ZeroDivisionError) as exc:
        failed.append((row["id"], type(exc).__name__))
print("done:", len(done), "failed:", failed)
