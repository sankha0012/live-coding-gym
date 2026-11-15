def safe_int(value, default=0):
    try:
        if isinstance(value, float):
            return value if value.is_integer() else default
        return int(value)
    except (ValueError, TypeError):
        return default
