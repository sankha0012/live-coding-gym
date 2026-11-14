def parse_quantity(raw):
    """Parse an item count.

    None or blank -> 0. Whole-number text -> int.
    Anything else raises ValueError.
    """
    try:
        return int(raw.strip())
    except:
        return 0
