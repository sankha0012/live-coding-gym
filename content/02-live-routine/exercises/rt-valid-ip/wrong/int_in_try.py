def is_valid_ip(s):
    parts = s.split('.')
    if len(parts) != 4:
        return False
    for p in parts:
        try:
            n = int(p)
        except ValueError:
            return False
        if not 0 <= n <= 255 or (len(p) > 1 and p[0] == '0'):
            return False
    return True
