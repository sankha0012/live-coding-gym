def parse_logs(lines):
    counts = {}
    errors = []
    for line in lines:
        parts = line.split()
        if len(parts) < 3:
            continue
        level = parts[1]
        counts[level] = counts.get(level, 0) + 1
        if level == 'ERROR':
            errors.append(parts[2])
    return counts, errors
