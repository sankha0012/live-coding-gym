def parse_logs(lines):
    counts = {}
    errors = []
    for line in lines:
        parts = line.split(" ", 2)
        if len(parts) < 3:
            continue
        _, level, message = parts
        counts[level] = counts.get(level, 0) + 1
        if "ERROR" in line:
            errors.append(message)
    return counts, errors
