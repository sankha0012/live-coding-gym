---
title: Grids and matrices
summary: A grid is a list of rows; index it as grid[row][col] and check bounds before visiting neighbours.
tags: [algorithms, lists, grids]
---
```python
grid = [[1, 2, 3],
        [4, 5, 6]]
rows, cols = len(grid), len(grid[0])      # 2 rows, 3 columns
grid[1][2]                                # 6    grid[row][col]
for r in range(rows):
    for c in range(cols):
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:   # up, down, left, right
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                pass                      # grid[nr][nc] is a valid neighbour
[list(col) for col in zip(*grid)]         # [[1, 4], [2, 5], [3, 6]]   transpose
```

- Row first, then column: `grid[r][c]`. The row is the vertical position.
- Visiting every cell is O(rows * cols).
- Check bounds before you index. A negative index does not fail, it wraps to the other side.

<!-- more -->

## Details

Create a grid with a comprehension, so each row is its own list:

```python
good = [[0] * 3 for _ in range(2)]
bad = [[0] * 3] * 2                       # the same row object twice
bad[0][0] = 9
bad                                       # [[9, 0, 0], [9, 0, 0]]
```

Useful one-liners:

```python
[sum(row) for row in grid]                # [6, 15]         row sums
[sum(col) for col in zip(*grid)]          # [5, 7, 9]       column sums
[list(r) for r in zip(*grid[::-1])]       # [[4, 1], [5, 2], [6, 3]]   rotate clockwise
[x for row in grid for x in row]          # [1, 2, 3, 4, 5, 6]         flatten
```

`zip(*grid)` gives tuples, so wrap them in `list` when you need to change cells.

**Connected regions** (islands, flood fill). Loop over every cell. When you find an unvisited cell of interest, start a search from it: put it on a stack, then pop a cell, mark it, and push its valid unvisited neighbours. Keep a `seen` set of `(r, c)` tuples, or overwrite the cell if you may change the input. Each cell is handled once, so the cost stays O(rows * cols). For shortest paths in steps, use a `deque` and `popleft()` (breadth-first).

For eight neighbours, add the four diagonals to the direction list.

Copy a grid with `[row[:] for row in grid]`. `grid[:]` copies only the outer list.

## Common mistakes

- Swapping the axes: `grid[x][y]` with x as the column. Name the variables `r` and `c`.
- Building the grid with `[[0] * cols] * rows`, so one write changes every row.
- Checking `grid[nr][nc]` before the bounds test. Index `-1` reads the last row with no error.
- Calling `len(grid[0])` on an empty grid. Guard with `if not grid or not grid[0]`.
- Marking a cell as seen only when it is popped, so it is pushed many times. Mark it when you push.

## See also

- [Stack patterns (brackets, undo)](#/kb/algo-stack)
- [List comprehensions](#/kb/py-list-comprehensions)
- [Mutability, aliasing and copying](#/kb/py-copy-mutability)
- [deque and OrderedDict](#/kb/py-collections-deque)
