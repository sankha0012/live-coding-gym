def days_between(a: str, b: str) -> int:
    def ordinal(s):
        parts = s.split("-")
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            raise ValueError(s)
        y, m, d = map(int, parts)
        if not (1 <= m <= 12):
            raise ValueError(s)
        leap = y % 4 == 0
        md = [31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        if not (1 <= d <= md[m - 1]):
            raise ValueError(s)
        days = 365 * y + (y - 1) // 4 + 1
        return days + sum(md[: m - 1]) + d
    return abs(ordinal(b) - ordinal(a))
