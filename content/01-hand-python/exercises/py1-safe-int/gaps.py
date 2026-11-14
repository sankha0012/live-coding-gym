def safe_int(value, default=0):
    ____:
        if isinstance(value, float):
            return int(value) if value.____() else default
        return int(value)
    except (____, TypeError):
        return default
