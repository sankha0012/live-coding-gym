def days_between(a: str, b: str) -> int:
    ya, ma, da = map(int, a.split("-"))
    yb, mb, db = map(int, b.split("-"))
    return abs((yb - ya) * 365 + (mb - ma) * 30 + (db - da))
