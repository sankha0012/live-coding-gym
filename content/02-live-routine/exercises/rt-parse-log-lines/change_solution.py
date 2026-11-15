def parse_logs(lines: list[str], level: str = "ERROR") -> tuple[dict, list]:
    counts = {}
    errors = []
    for line in lines:
        parts = line.split(" ", 2)
        if len(parts) < 3:
            continue
        _, lvl, message = parts
        counts[lvl] = counts.get(lvl, 0) + 1
        if lvl == level:
            errors.append(message)
    return counts, errors
