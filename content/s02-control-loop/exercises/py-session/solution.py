def sessionize(timestamps, gap=30):
    if not timestamps:
        return []
    ts = sorted(timestamps)
    sessions = [[ts[0]]]
    for t in ts[1:]:
        if t - sessions[-1][-1] > gap:
            sessions.append([t])
        else:
            sessions[-1].append(t)
    return sessions
