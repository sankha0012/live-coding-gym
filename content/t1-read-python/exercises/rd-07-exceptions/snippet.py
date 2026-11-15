def parse_score(raw):
    try:
        value = float(raw)
    except ValueError:
        print(f"skip {raw!r}")
        return None
    finally:
        print(f"checked {raw!r}")
    if not 0 <= value <= 1:
        raise ValueError(f"score out of range: {value}")
    return value


rows = ["0.8", "abc", "1.5", "0.25"]
scores = []
for raw in rows:
    try:
        score = parse_score(raw)
    except ValueError as err:
        print("rejected:", err)
        continue
    if score is not None:
        scores.append(score)
print(scores)
