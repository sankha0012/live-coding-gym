# Complexity cheatsheet

## The problem it solves

Interviewers ask "what is the complexity?" after almost every answer. You need a fast, correct answer without a long calculation. This cheatsheet lists the common cases. Learn it by heart, then check yourself with the example below.

Always name what n is. "O(n)" alone is not an answer. Say "O(n) in the number of rows".

## Python structures

| Operation | Cost |
|---|---|
| `list[i]`, `list.append(x)` | O(1) (append is amortised) |
| `x in list`, `list.index(x)`, `list.remove(x)` | O(n) |
| `list.insert(0, x)`, `list.pop(0)` | O(n) |
| `sorted(list)`, `list.sort()` | O(n log n) |
| `x in set`, `x in dict`, `d[k]`, `d[k] = v` | O(1) on average |
| `set` union, intersection | O(n + m) |
| `collections.deque` append or pop at either end | O(1) |
| `heapq.heappush`, `heapq.heappop` | O(log n) |
| `heapq.nlargest(k, data)` | O(n log k) |
| `str` concatenation with `+=` in a loop | can be O(n squared), use `"".join` |
| Slicing `a[i:j]` | O(j - i), it copies |

## SQL

| Operation | Cost |
|---|---|
| Full scan with `WHERE` | O(n) |
| `ORDER BY` without an index | O(n log n) |
| `GROUP BY` | about O(n), with hashing, or O(n log n) with sorting |
| Hash join of tables of size n and m | about O(n + m) |
| Nested loop join without an index | O(n * m) |
| Join with an index on the lookup side | about O(n log m) |
| Window function with `PARTITION BY` and `ORDER BY` | O(n log n) for the sorting |
| `COUNT(DISTINCT x)` | about O(n), and needs memory |

The database planner chooses the join method. Do not say that a join "is" O(n * m). Say "worst case O(n * m), usually much less with an index or a hash join".

## The smallest runnable example

A classic: find the users that appear in two lists. Compare two versions.

```python
def common_slow(a, b):
    return [x for x in a if x in b]       # O(n * m): "in list" is O(m)


def common_fast(a, b):
    sb = set(b)                           # O(m)
    return [x for x in a if x in sb]      # O(n) lookups -> O(n + m) total


print(common_slow([1, 2, 3], [2, 3, 4]))  # [2, 3]
print(common_fast([1, 2, 3], [2, 3, 4]))  # [2, 3]
```

Both give the same answer. The second one pays O(m) extra memory to turn each lookup from O(m) into O(1). That is the most common trade-off: memory for time.

## The three traps people hit

1. **Hidden loops.** `x in some_list` inside a loop is a second loop. `str.replace` or `sorted` inside a loop is also a loop. Count every call that touches the whole input.
2. **Confusing average and worst case.** Dictionary lookups are O(1) on average. Many colliding keys can slow them down. Python's `sorted` uses Timsort, which is O(n log n) in the worst case. Say "on average" when it matters.
3. **Forgetting space.** Building a copy, a set or a dictionary costs memory. At 80 million rows a set of ids may not fit. Mention space, and say what you would do when it does not fit: process in chunks or stream.

## Useful rules of thumb

- Two nested loops over the same input: O(n squared). Do not use that at 100,000 items or more.
- Sorting first often turns a search problem into O(n log n).
- Streaming a file line by line is O(1) memory. Reading it all is O(n).
- Batch size trades memory against the number of round trips.

## Say it like this

"The loop is O(n) in the number of events, and each dictionary lookup is O(1) on average, so the total is O(n). It uses O(u) extra memory for u distinct users. If the data does not fit in memory, I would process it in chunks, or let the database do the group by."

If you are unsure, say what you know: "The sort dominates, so it is O(n log n). I believe the rest is linear." Honest and structured beats a confident wrong number.
