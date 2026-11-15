def sessionize(timestamps, gap=30):
    if not timestamps: return []
    timestamps.sort(); s = [[timestamps[0]]]
    for t in timestamps[1:]:
        if t - s[-1][-1] > gap: s.append([t])
        else: s[-1].append(t)
    return s
