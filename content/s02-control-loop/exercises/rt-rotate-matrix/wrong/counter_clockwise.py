def rotate(m):
    return [list(row) for row in zip(*m)][::-1]
