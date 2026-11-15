def safe_int(value, default=0):
    try:
        if isinstance(value, float):
            return round(value) if abs(value - round(value)) < 1e-9 else default
        return int(value)
    except (ValueError, TypeError, OverflowError):
        return default
