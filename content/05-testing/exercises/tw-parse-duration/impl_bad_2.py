import re

_UNITS = {"h": 3600, "m": 60, "s": 1}


def parse_duration(text):
    if not text:
        raise ValueError("empty duration")
    parts = re.findall(r"(\d+)([hms])", text)
    if not parts:
        raise ValueError(f"invalid duration: {text!r}")
    return sum(int(n) * _UNITS[u] for n, u in parts)
