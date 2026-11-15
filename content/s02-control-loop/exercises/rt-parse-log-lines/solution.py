def parse_logs(lines: list[str]) -> tuple[dict, list]:
    counts = {}
    errors = []
    for line in lines:
        parts = line.split(" ", 2)
        if len(parts) < 3:
            continue
        _, level, message = parts
        counts[level] = counts.get(level, 0) + 1
        if level == "ERROR":
            errors.append(message)
    return counts, errors
