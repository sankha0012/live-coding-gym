# Counting with a dict

The most common hand-coded pattern: walk a sequence and count.

    counts = {}
    for item in items:
        counts[item] = counts.get(item, 0) + 1

`dict.get(key, 0)` returns 0 when the key is missing, so no `if` is needed.
