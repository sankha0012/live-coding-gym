import re

_PATTERN = re.compile(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?")


def parse_duration(text):
    m = _PATTERN.fullmatch(text)
    if not text or m is None:
        raise ValueError(f"invalid duration: {text!r}")
    h, mi, s = (int(g) if g else 0 for g in m.groups())
    return float(h * 3600 + mi * 60 + s)
