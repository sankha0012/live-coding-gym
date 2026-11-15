**Why this matters.** Rotating a grid is a picture-in-your-head problem. The way to solve it is to stop thinking about individual cells and find a short sequence of simple moves that produces the turn.
**How we get there.**
1. Look at the example. After a clockwise turn, the first column read from bottom to top becomes the first row. So the old rows end up as the new columns, in reverse order.
2. Reverse the order of the rows: `m[::-1]`. This makes a reversed copy and does not touch the input.
3. Transpose, which means swapping rows and columns. `zip(*rows)` does that: it hands the rows to `zip`, which regroups them column by column.
4. `zip` gives tuples, so we turn each one into a list: `[list(row) for row in zip(*m[::-1])]`. That is the whole solution.
**Check it.** For `[]` the `zip` gives nothing, so we return `[]`. We build a new n by n matrix, so time and space are both O(n squared).
**Watch out.** Transpose alone is a mirror, not a rotation; transpose plus the wrong flip turns it counter-clockwise; and the swap-in-place approach changes the caller's matrix.
