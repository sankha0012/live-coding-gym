def compress_spaces(s: str) -> str:
    return " ".join(p for p in s.split(" ") if p)
