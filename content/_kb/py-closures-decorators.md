---
title: Closures and decorators
summary: A closure is a function that remembers outer variables; a decorator wraps a function to add behaviour.
tags: [python, functions, decorators]
---
```python
from functools import wraps
def log_calls(func):
    @wraps(func)                       # keeps func.__name__ and its docstring
    def wrapper(*args, **kwargs):
        print("calling", func.__name__)
        return func(*args, **kwargs)   # pass the result back
    return wrapper
@log_calls                             # same as: add = log_calls(add)
def add(a, b): return a + b
add(1, 2)                              # prints 'calling add', returns 3
```

- A decorator is a function that takes a function and returns a replacement.
- The wrapper takes `*args, **kwargs` so it works with any signature.
- An inner function can read outer variables. To rebind one it needs `nonlocal`.

<!-- more -->

## Details

A closure keeps the variables of the function that created it, even after that function has returned. Each call to the outer function makes a separate set of variables.

```python
def make_counter():
    count = 0
    def inc():
        nonlocal count                 # rebind the outer variable
        count += 1
        return count
    return inc

c = make_counter()
c(), c()                               # (1, 2)
make_counter()()                       # 1    a new counter starts again
```

A decorator that takes its own arguments needs one more level: a function that returns the decorator.

```python
def repeat(times):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return [func(*args, **kwargs) for _ in range(times)]
        return wrapper
    return decorator

@repeat(3)
def hi(): return "hi"
hi()                                   # ['hi', 'hi', 'hi']
hi.__name__                            # 'hi'   thanks to wraps
```

The standard library has ready-made decorators. `functools.lru_cache` remembers results for arguments it has already seen.

Closures look up the variable when they run, not when they are created:

```python
fs = [lambda: i for i in range(3)]
[f() for f in fs]                      # [2, 2, 2]   all see the final i
fs = [lambda i=i: i for i in range(3)]
[f() for f in fs]                      # [0, 1, 2]   a default captures the value
```

## Common mistakes

- Forgetting `return wrapper`, so the decorated name becomes `None`.
- Forgetting `return func(*args, **kwargs)` in the wrapper, so every call returns `None`.
- Assigning to an outer variable without `nonlocal`: `UnboundLocalError`.
- Writing `@log_calls()` for a decorator that takes no arguments, or `@repeat` without them.
- Leaving out `wraps`, so the function's name shows as `wrapper`.

## See also

- [Functions: defaults, *args, **kwargs, the mutable default trap](#/kb/py-functions-args)
- [lambda, map, filter, any, all](#/kb/py-lambda-map-filter)
- [Retries with backoff](#/kb/prod-retry-backoff)
- Official docs: https://docs.python.org/3/library/functools.html
