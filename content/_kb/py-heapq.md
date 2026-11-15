---
title: "heapq: top-k and priority queues"
summary: Keep the smallest item ready at index 0, pop items in order, and get the k largest or smallest fast.
tags: [python, heap, top-k]
---
```python
import heapq
h = [5, 1, 4]
heapq.heapify(h)                    # in place, O(n). h[0] is now the smallest: 1
heapq.heappush(h, 0)                # add, O(log n)
heapq.heappop(h)                    # 0   remove and return the smallest
heapq.nlargest(2, [5, 1, 4, 9])     # [9, 5]
heapq.nsmallest(2, [5, 1, 4, 9])    # [1, 4]
heapq.nlargest(2, ["bb", "a", "cccc"], key=len)   # ['cccc', 'bb']
```

- A heap is a normal list. The `heapq` functions keep the smallest item at index 0.
- It is always a min-heap. For a max-heap, push negated numbers.
- Only `h[0]` is guaranteed. The rest of the list is not sorted.

<!-- more -->

## Details

`heappush` and `heappop` cost O(log n). Reading `h[0]` is O(1). That beats sorting again after each insert.

For a priority queue, push tuples. Tuples compare item by item, so the first item is the priority:

```python
pq = []
heapq.heappush(pq, (2, "write"))
heapq.heappush(pq, (1, "read"))
heapq.heappop(pq)                   # (1, 'read')
```

If two priorities tie, Python compares the next item. Add a counter as a tie-breaker when that item cannot be compared (a dict, for example): `(priority, count, item)`.

Max-heap by negating:

```python
m = []
for x in [5, 1, 4]:
    heapq.heappush(m, -x)
-heapq.heappop(m)                   # 5
```

Top-k on a stream with a heap of size k. The heap holds the k largest seen so far, with the smallest of them on top ready to be thrown out:

```python
top = []
for x in [5, 1, 9, 4, 7]:
    heapq.heappush(top, x)
    if len(top) > 3:
        heapq.heappop(top)
sorted(top, reverse=True)           # [9, 7, 5]
```

This is O(n log k) and uses O(k) memory. `nlargest(k, items)` does the same job in one call. When k is close to n, plain `sorted(items)[:k]` is just as good.

Popping everything gives sorted order:

```python
h = [5, 1, 4, 9, 2]
heapq.heapify(h)                    # h is [1, 2, 4, 9, 5]: a heap, not sorted
[heapq.heappop(h) for _ in range(len(h))]   # [1, 2, 4, 5, 9]
```

## Common mistakes

- Calling `h.heappush(x)`. The functions live in the module: `heapq.heappush(h, x)`.
- Using `heappop` on a list that was never heapified. You get an arbitrary item.
- Looping over the heap and expecting sorted order.
- Popping from an empty heap. It raises `IndexError`.
- Pushing `(priority, dict)` pairs with equal priorities. It raises `TypeError` on the tie.

## See also

- [Sorting: sorted, key functions, ties and stability](#/kb/py-sorting)
- [Tuples and unpacking](#/kb/py-tuples-unpacking)
- [Big-O of common Python operations](#/kb/py-complexity)
- [Embeddings, cosine similarity and top-k retrieval](#/kb/ai-embeddings-topk)
- Official docs: https://docs.python.org/3/library/heapq.html
