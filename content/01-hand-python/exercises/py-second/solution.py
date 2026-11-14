def second_highest(values):
    distinct = sorted(set(values), reverse=True)
    return distinct[1] if len(distinct) >= 2 else None
