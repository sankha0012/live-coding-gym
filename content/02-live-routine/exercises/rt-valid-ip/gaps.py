def is_valid_ip(s: str) -> bool:
    parts = s.split(".")
    if len(parts) != ____:
        return False
    for p in parts:
        if not p.____() or not p.isascii():
            return False
        if len(p) > 1 and p[0] == "____":
            return False
        if int(p) > ____:
            return False
    return True
