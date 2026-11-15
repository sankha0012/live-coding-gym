raw_prices = ["10.5", "abc", "7", "", "3.2"]

def parse_prices(rows):
    out = []
    for row in rows:
        try:
            out.append(float(row))
        except ValueError:
            pass
    return out

def parse_prices_strict(rows, max_bad_ratio=0.2):
    out, bad = [], []
    for row in rows:
        try:
            out.append(float(row))
        except ValueError:
            bad.append(row)
    if len(bad) / len(rows) > max_bad_ratio:
        raise ValueError(f"{len(bad)} of {len(rows)} rows invalid: {bad}")
    return out

prices = parse_prices(raw_prices)
print("kept:", len(prices), "mean:", round(sum(prices) / len(prices), 2))
try:
    parse_prices_strict(raw_prices)
except ValueError as exc:
    print("strict:", exc)
print("strict, clean input:", parse_prices_strict(["1", "2", "3"]))
