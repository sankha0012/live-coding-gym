---
title: "Sorting: sorted, key functions, ties and stability"
summary: Sort any iterable with sorted(), choose the order with key and reverse, and control what happens on ties.
tags: [python, sorting, lists]
---
```python
xs = [3, 1, 2]
sorted(xs)                        # [1, 2, 3]    new list, xs unchanged
sorted(xs, reverse=True)          # [3, 2, 1]
words = ["pear", "fig", "apple", "kiwi"]
sorted(words, key=len)            # ['fig', 'pear', 'kiwi', 'apple']   ties keep input order
sorted(words, key=lambda w: (-len(w), w))   # ['apple', 'kiwi', 'pear', 'fig']
max(words, key=len)               # 'apple'
xs.sort()                         # sorts xs in place, returns None
```

- `sorted(iterable)` returns a new list. `list.sort()` changes the list and returns `None`.
- `key` is a function called once per item. Items are ordered by what it returns.
- The sort is stable: items with equal keys stay in their original order.

<!-- more -->

## Details

A tuple key sorts by several fields: first element, then the second on ties, and so on. Negate a number to sort that field in descending order.

```python
counts = {"b": 2, "a": 2, "c": 5}
sorted(counts)                                        # ['a', 'b', 'c']   a dict gives its keys
sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))  # [('c', 5), ('a', 2), ('b', 2)]
```

You cannot negate a string. To mix directions with text, sort twice, least important field first. Stability keeps the first order inside ties:

```python
rows = [("ana", 2), ("bo", 5), ("cy", 2)]
rows.sort(key=lambda r: r[0], reverse=True)   # name descending
rows.sort(key=lambda r: r[1])                 # then count ascending
rows                                          # [('cy', 2), ('ana', 2), ('bo', 5)]
```

`reverse=True` also keeps equal items in their original order. It is not the same as reversing the result.

Strings sort by character code, so uppercase comes first. Pass `key=str.lower` to ignore case:

```python
sorted(["b", "a", "C"])                   # ['C', 'a', 'b']
sorted(["b", "a", "C"], key=str.lower)    # ['a', 'b', 'C']
```

`min` and `max` accept `key` too and return the first item on a tie. Sorting costs O(n log n).

## Common mistakes

- Writing `xs = xs.sort()` or `return xs.sort()`: both give `None`.
- Leaving ties unspecified when the expected output needs one exact order. Add a tie-breaker to the key.
- Sorting numbers stored as strings: `sorted(["10", "9"])` gives `['10', '9']`. Use `key=int`.
- Sorting a list that mixes types or contains `None`: `TypeError`.

## See also

- [lambda, map, filter, any, all](#/kb/py-lambda-map-filter)
- [heapq: top-k and priority queues](#/kb/py-heapq)
- [Tuples and unpacking](#/kb/py-tuples-unpacking)
- Official docs: https://docs.python.org/3/howto/sorting.html
