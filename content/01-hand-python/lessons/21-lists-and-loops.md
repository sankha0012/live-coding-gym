# Lists and loops

## The problem it solves

Almost every task is "walk over a sequence and build a result". You need to index, slice, loop with the position, loop over two lists together, and build a new list in one line. These five moves are the whole toolkit.

## The smallest runnable example

```python
xs = [4, 8, 15, 16, 23, 42]
print(xs[0], xs[-1], xs[1:3], xs[::2])     # 4 42 [8, 15] [4, 15, 23]
print(len(xs), sum(xs), min(xs), max(xs))

for i, x in enumerate(xs):                 # position and value
    if i == 2:
        print("third:", x)

names = ["ana", "bo"]
ages = [31, 25]
for name, age in zip(names, ages):         # two lists together
    print(name, age)

evens = [x for x in xs if x % 2 == 0]      # filter
squares = [x * x for x in xs]              # map
print(evens, squares)

ys = []
ys.append(3)                               # add one
ys.extend([1, 2])                          # add many
ys.sort()                                  # in place, returns None
print(ys, sorted(ys, reverse=True))        # sorted makes a new list
```

Run it and read each line of output next to the code. Then close the file and retype it from memory. That is the exercise.

## Slicing rules

`xs[a:b]` includes `a` and excludes `b`. Negative numbers count from the end. `xs[::-1]` is a reversed copy. `xs.reverse()` reverses in place and returns `None`. A slice makes a new list, so `xs[:]` is a shallow copy.

Adjacent pairs is a classic task:

```python
xs = [1, 4, 9, 16]
pairs = list(zip(xs, xs[1:]))
diffs = [b - a for a, b in pairs]
print(pairs, diffs)   # [(1, 4), (4, 9), (9, 16)] [3, 5, 7]
```

`zip` stops at the shortest input, so the last element has no partner and nothing breaks on a short list. An empty list gives an empty result.

## Trap 1: `sort()` returns `None`

```python
xs = [3, 1, 2]
ys = xs.sort()
print(ys)            # None
print(sorted(xs))    # [1, 2, 3]
```

If you write `return xs.sort()` your function returns `None`. Use `return sorted(xs)` or sort first and return `xs` on the next line. Also remember that `.sort()` changes the caller's list, which can surprise a test that reuses the input.

## Trap 2: changing a list while you loop over it

```python
ys = [2, 4, 6, 8]
for y in ys:
    if y % 2 == 0:
        ys.remove(y)
print(ys)            # [4, 8]  -- every even number should be gone
```

Python moves an internal index while you remove items, so it skips elements. Build a new list instead: `[x for x in xs if keep(x)]`.

## Trap 3: copies that are not copies

```python
a = [[0] * 2] * 2
a[0][0] = 9
print(a)             # [[9, 0], [9, 0]]  -- both rows are the same list
b = [[0] * 2 for _ in range(2)]
b[0][0] = 9
print(b)             # [[9, 0], [0, 0]]
```

Multiplying a list of lists repeats the same inner list. Use a comprehension to build independent rows. For the same reason `b = a` does not copy: it gives a second name to the same list. Use `a[:]` or `list(a)`.

## Rotating and chunking

Two common prompts, both solved with slices and the modulo operator:

```python
def rotate(xs, k):
    if not xs:
        return []
    k %= len(xs)
    return xs[-k:] + xs[:-k] if k else xs[:]

def chunks(xs, n):
    return [xs[i:i + n] for i in range(0, len(xs), n)]

print(rotate([1, 2, 3, 4, 5], 2))   # [4, 5, 1, 2, 3]
print(rotate([1, 2, 3], 7))         # [3, 1, 2]
print(chunks([1, 2, 3, 4, 5], 2))   # [[1, 2], [3, 4], [5]]
```

Notice `k %= len(xs)` handles a `k` larger than the length. Notice the `if k` guard: `xs[-0:]` is the whole list, which would be wrong without it. The empty list is guarded first because modulo by zero raises `ZeroDivisionError`.

## Say it like this

"I loop once over the input and build a new list, so it is linear time and I do not change the caller's data. I use enumerate when I need the position and zip when I need two lists together. I avoid removing items while looping. For the edge cases I checked an empty list and a single item, and for rotate I take k modulo the length."
