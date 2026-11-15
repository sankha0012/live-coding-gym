# The Python reading cheat-sheet

## The problem it solves

Assistant code is dense. It uses short forms that save space but hide what happens. You do not need to write all of them yourself. You do need to read each one without hesitation, so this page lists every construct you must be able to decode, with its meaning and its result.

## Slicing

`seq[start:stop:step]` works on lists, strings and tuples. The start is included, the stop is excluded, and negative numbers count from the end.

```python
xs = [10, 20, 30, 40, 50]
print(xs[1:4])     # [20, 30, 40]
print(xs[-2:])     # [40, 50]
print(xs[::-1])    # [50, 40, 30, 20, 10]   reversed copy
print(xs[::2])     # [10, 30, 50]
```

A slice always makes a new list (a shallow copy). Slicing past the end does not raise an error; indexing past the end does.

## Comprehensions

A comprehension builds a collection in one expression: `[what for item in source if condition]`.

```python
print([x * x for x in range(5)])               # [0, 1, 4, 9, 16]
print([x for x in range(10) if x % 3 == 0])    # [0, 3, 6, 9]
print({w: len(w) for w in ["hi", "there"]})    # {'hi': 2, 'there': 5}
print({x % 3 for x in range(10)})              # {0, 1, 2}
```

Read it as: "for each item, if the condition holds, keep this expression". With a nested `for`, the leftmost loop is the outer one.

## Dict methods

```python
d = {"a": 1}
print(d.get("b", 0))                    # 0         no KeyError
d["x"] = d.get("x", 0) + 1              # counting idiom
d.setdefault("k", []).append(1)         # create the list once, then append
for key, value in d.items():            # pairs, in insertion order
    print(key, value)
print(list(d.keys()), list(d.values()))
```

`d[key]` raises `KeyError` when the key is missing; `d.get(key)` returns `None` (or your default). `defaultdict` and `Counter` do the same counting job with less typing.

## Unpacking

```python
a, b = 1, 2
a, b = b, a                       # swap
first, *rest = [1, 2, 3, 4]       # first=1, rest=[2, 3, 4]
for name, age in [("ana", 31), ("bo", 25)]:
    print(name, age)
for i, ch in enumerate("ab", start=1):
    print(i, ch)                  # 1 a, then 2 b
print(list(zip([1, 2, 3], "ab"))) # [(1, 'a'), (2, 'b')]   stops at the shortest
```

## f-strings

```python
name, n = "Ann", 3.14159
print(f"{name}: {n:.2f}")          # Ann: 3.14
print(f"{5:03d} {1234567:,}")      # 005 1,234,567
print(f"{n!r}")                    # 3.14159   (repr)
```

Anything inside `{}` is a Python expression. After the colon comes a format spec: `.2f` two decimals, `03d` zero-padded width 3, `,` thousands separator, `>8` right-align in 8 characters.

## *args and **kwargs

In a definition, `*args` collects extra positional arguments into a tuple and `**kwargs` collects keyword arguments into a dict. In a call, `*` and `**` do the reverse: they unpack a sequence or dict into arguments.

```python
def f(*args, **kwargs):
    return args, kwargs

print(f(1, 2, a=3))                 # ((1, 2), {'a': 3})
print(f(*[1, 2], **{"a": 3}))       # ((1, 2), {'a': 3})
```

## Lambdas and key functions

A `lambda` is a function with one expression and no name. You will mostly see it as a `key`.

```python
people = [("bo", 25), ("ana", 31)]
print(sorted(people, key=lambda p: p[1], reverse=True))   # [('ana', 31), ('bo', 25)]
print(max(["pear", "fig", "apple"], key=len))             # apple
```

`key` is called once per item and the results are compared. `sorted` is stable: items with equal keys keep their original order.

## with

`with` runs setup, your block, and then cleanup, even if an error happens. For files, the cleanup is closing the file.

```python
with open("data.txt") as f:      # f is closed at the end of the block
    lines = [ln.strip() for ln in f]
```

## yield and generators

A function that contains `yield` returns a generator. It produces values one at a time and pauses between them. A generator can be consumed only once.

```python
def gen():
    yield 1
    yield 2

g = gen()
print(next(g), next(g))      # 1 2
print(list(gen()))           # [1, 2]
total = (x * 2 for x in range(3))     # generator expression
print(sum(total), sum(total))         # 6 0   the second sum sees nothing
```

## Truthiness and short forms

- Falsy values: `None`, `0`, `0.0`, `""`, `[]`, `{}`, `set()`. Non-empty strings (even `"0"`) are truthy.
- `a or b` gives `a` if it is truthy, else `b`. `a and b` gives `a` if it is falsy, else `b`.
- `x if cond else y` is the conditional expression.
- `any(...)` and `all(...)` take an iterable, often a generator expression.
- `//` is floor division and `%` the matching remainder: `-10 // 3` is `-4` and `-10 % 3` is `2`.

## Common mistakes

- Reading `xs[1:4]` as including index 4.
- Forgetting that a generator is used up after one pass.
- Thinking `*args` is special syntax of the name; only the `*` matters.
- Reading `a or b` as a boolean when it returns one of the operands.

## Related

- [Slicing](#/kb/py-slicing)
- [List comprehensions](#/kb/py-list-comprehensions)
- [Dict comprehensions](#/kb/py-dict-comprehensions)
- [Tuples and unpacking](#/kb/py-tuples-unpacking)
- [f-strings](#/kb/py-f-strings)
- [Function arguments](#/kb/py-functions-args)
- [Lambda, map and filter](#/kb/py-lambda-map-filter)
- [Iterators and generators](#/kb/py-iterators-generators)
- [Truthiness and None](#/kb/py-truthiness-none)
