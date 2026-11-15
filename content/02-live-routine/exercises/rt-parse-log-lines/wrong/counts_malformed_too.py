def parse_logs(lines):
    counts = {}
    errors = []
    for line in lines:
        parts = line.split(" ", 2)
        if len(parts) >= 2:
            counts[parts[1]] = counts.get(parts[1], 0) + 1
        if len(parts) == 3 and parts[1] == "ERROR":
            errors.append(parts[2])
    return counts, errors
