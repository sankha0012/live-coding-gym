def is_valid_ip(s):
    parts = s.split(".")
    if len(parts) != 4:
        return False
    for i, p in enumerate(parts):
        if not (p.isdigit() and p.isascii()):
            return False
        if len(p) > 1 and p[0] == "0":
            return False
        if i < 3 and int(p) > 255:
            return False
    return True
