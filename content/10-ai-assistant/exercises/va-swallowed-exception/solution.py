def parse_quantity(raw):
    """Parse an item count.

    None or blank -> 0. Whole-number text -> int.
    Anything else raises ValueError.
    """
    if raw is None or raw.strip() == "":
        return 0
    return int(raw.strip())
