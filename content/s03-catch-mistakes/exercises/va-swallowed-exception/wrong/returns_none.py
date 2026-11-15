def parse_quantity(raw):
    try:
        return int(raw.strip())
    except Exception:
        return None
