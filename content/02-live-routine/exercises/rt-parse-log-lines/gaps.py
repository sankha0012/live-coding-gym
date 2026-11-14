def parse_logs(lines: list[str]) -> tuple[dict, list]:
    counts = {}
    errors = []
    for line in lines:
        parts = line.split(" ", ____)
        if len(parts) < ____:
            continue
        _, level, message = parts
        counts[level] = counts.get(level, 0) + 1
        if level == "ERROR":
            errors.append(____)
    return counts, errors
