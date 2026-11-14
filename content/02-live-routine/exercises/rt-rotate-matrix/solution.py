def rotate(m: list[list[int]]) -> list[list[int]]:
    return [list(row) for row in zip(*m[::-1])]
