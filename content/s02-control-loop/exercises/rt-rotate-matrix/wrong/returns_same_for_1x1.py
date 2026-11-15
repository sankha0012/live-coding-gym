def rotate(m):
    if len(m) <= 1:
        return m
    return [list(row) for row in zip(*m[::-1])]
