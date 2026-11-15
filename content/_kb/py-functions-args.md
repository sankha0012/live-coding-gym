---
title: "Functions: defaults, *args, **kwargs, the mutable default trap"
summary: Define functions with default values, accept any number of arguments, and avoid the shared mutable default.
tags: [python, functions]
---
```python
def greet(name, greeting="Hi", *args, **kwargs):
    return f"{greeting} {name}", args, kwargs

greet("Ana")                          # ('Hi Ana', (), {})
greet("Ana", greeting="Yo")           # ('Yo Ana', (), {})
greet("Ana", "Yo", 1, 2, x=3)         # ('Yo Ana', (1, 2), {'x': 3})
greet(*["Ana", "Yo"], **{"x": 3})     # ('Yo Ana', (), {'x': 3})
```

- A function without `return` returns `None`.
- `*args` collects extra positional arguments in a tuple. `**kwargs` collects extra keyword arguments in a dict.
- Default values are created once, when `def` runs. Never use `[]` or `{}` as a default.

<!-- more -->

## Details

Parameters with defaults must come after those without. In a call, positional arguments come before keyword arguments.

The mutable default trap: the same list is reused on every call.

```python
def add(x, acc=[]):
    acc.append(x)
    return acc

add(1)                                # [1]
add(2)                                # [1, 2]   the list from the first call
```

The fix is `None` as the default and a new object inside:

```python
def add(x, acc=None):
    if acc is None:
        acc = []
    acc.append(x)
    return acc

add(1)                                # [1]
add(2)                                # [2]
```

Parameters after a bare `*` can only be passed by name. This keeps calls readable:

```python
def load(path, *, strict=False):
    return path, strict

load("a.csv", strict=True)            # ('a.csv', True)
```

Arguments are not copied. If a function changes a list it received, the caller sees the change:

```python
def clear_first(xs):
    xs[0] = 0

data = [5, 6]
clear_first(data)                     # data is [0, 6]
```

A name assigned inside a function is local. Reading an outer variable works. Rebinding it needs `global` or `nonlocal`, and passing values in and returning results is nearly always cleaner.

## Common mistakes

- Printing the result instead of returning it.
- Writing `def f(x, items=[])` or `def f(x, cache={})`.
- Calling `f` without parentheses: `f` is the function object, `f()` runs it.
- Changing an input list in place when the caller still needs the original. Copy it first.
- Putting a positional argument after a keyword argument: `SyntaxError`.

## See also

- [Tuples and unpacking](#/kb/py-tuples-unpacking)
- [Mutability, aliasing and copying](#/kb/py-copy-mutability)
- [Closures and decorators](#/kb/py-closures-decorators)
- [Type hints](#/kb/py-typing-hints)
- Official docs: https://docs.python.org/3/tutorial/controlflow.html
