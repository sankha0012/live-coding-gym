def parse_logs(lines):
    counts = {}
    errors = []
    for line in lines:
        ts, level, message = line.split(' ', 2)
        counts[level] = counts.get(level, 0) + 1
        if level == 'ERROR':
            errors.append(message)
    return counts, errors
