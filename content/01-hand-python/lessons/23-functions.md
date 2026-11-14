# Functions

## The problem it solves

In a live round you write many small functions. The signature, the defaults, the return value and the edge case are all things the interviewer reads. A clean function with a clear return and no hidden state reads as senior. This lesson covers the parts that go wrong under pressure.

## The smallest runnable example

```python
def total(prices, tax=0.0, *, round_to=2):
    """Return the sum of prices plus tax."""
    return round(sum(prices) * (1 + tax), round_to)

print(total([10, 20]))                 # 30.0
print(total([10, 20], 0.1))            # 33.0
print(total([10, 20], tax=0.1, round_to=0))

def stats(xs):
    return min(xs), max(xs)            # returns a tuple

lo, hi = stats([3, 1, 2])
print(lo, hi)

def show(*args, **kwargs):
    return args, kwargs

print(show(1, 2, a=3))                 # ((1, 2), {'a': 3})

double = lambda x: x * 2
print(list(map(double, [1, 2])))
rows = [("bo", 5), ("al", 5), ("cy", 9)]
print(sorted(rows, key=lambda r: (-r[1], r[0])))
```

The parts: positional parameters, a default (`tax=0.0`), a keyword-only parameter after `*`, a docstring, a tuple return that unpacks into two names, `*args` for extra positional values, `**kwargs` for extra named values, and `lambda` for a one-line function.

## Return values

A function with no `return` gives back `None`. A bare `return` gives `None` too. If the prompt says "return an empty list for empty input", then `return []` and do not fall off the end. Return the same type on every path: either always a list, or always a number. A function that sometimes returns a list and sometimes `None` forces the caller to check.

## Sorting with a key

`sorted(items, key=f)` calls `f` once per item and sorts by the result. A tuple key sorts by the first part, then the second. To reverse one part, negate a number. To reverse a string part, sort twice or use `reverse=True` when all parts go the same way.

## Trap 1: the mutable default argument

```python
def add(x, bucket=[]):
    bucket.append(x)
    return bucket

print(add(1))   # [1]
print(add(2))   # [1, 2]  -- the same list is reused

def add_safe(x, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(x)
    return bucket

print(add_safe(1), add_safe(2))   # [1] [2]
```

The default is created once, when the function is defined. Use `None` and make a new list inside. This is the most famous Python interview trap, so say it out loud when you see it.

## Trap 2: changing the caller's data

```python
def add_one_bad(xs):
    for i in range(len(xs)):
        xs[i] += 1
    return xs

def add_one(xs):
    return [x + 1 for x in xs]

data = [1, 2]
add_one(data)
print(data)            # [1, 2], unchanged
add_one_bad(data)
print(data)            # [2, 3], the caller's list changed
```

Lists are passed by reference. If the prompt does not say "in place", return a new value. A hidden test often calls your function twice with the same input.

## Trap 3: a lambda in a loop and late binding

```python
fs = [lambda: i for i in range(3)]
print([f() for f in fs])          # [2, 2, 2]
gs = [lambda i=i: i for i in range(3)]
print([g() for g in gs])          # [0, 1, 2]
```

A closure looks up the variable when it is called, not when it is created. Bind the value with a default argument, as in `i=i`. This also appears when you write a decorator or a compose function.

## Small useful patterns

Composition and memoisation, both short:

```python
def compose(f, g):
    return lambda x: f(g(x))

def fib(n, cache=None):
    cache = {} if cache is None else cache
    if n < 2:
        return n
    if n not in cache:
        cache[n] = fib(n - 1, cache) + fib(n - 2, cache)
    return cache[n]

print(compose(str, abs)(-3), fib(30))   # 3 832040
```

Without the cache, `fib(30)` makes over a million calls. With it, about sixty. Say the complexity: linear time and linear space.

## Say it like this

"The function takes the input and returns a new value, so it does not change the caller's data. I avoid a mutable default and use None instead. I return the same type on every path, including the empty case. For sorting I use a key that returns a tuple, so the tie rule is explicit. The cost is one pass plus the sort, so n log n."
