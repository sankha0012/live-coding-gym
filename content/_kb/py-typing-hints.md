---
title: Type hints
summary: Annotate parameters and return values so readers and tools know what a function expects and gives back.
tags: [python, typing, readability]
---
```python
from typing import Callable

def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs)

def find(users: dict[str, int], name: str) -> int | None:   # may return None
    return users.get(name)

def apply(f: Callable[[int], int], x: int = 0) -> int:      # f takes an int, returns an int
    return f(x)
```

- Syntax is `name: type` for parameters, `-> type` for the return value, `name: type = default` for defaults.
- Python does not check hints at run time. They are for people, editors and tools such as mypy.
- `X | None` means the value can be missing. The caller must handle `None`.

<!-- more -->

## Details

Built-in containers take their item types in square brackets:

```python
names: list[str] = []
counts: dict[str, int] = {}
seen: set[int] = set()
pair: tuple[str, int] = ("a", 1)       # exactly two items
values: tuple[int, ...] = (1, 2, 3)    # any number of ints
```

A function that returns nothing is annotated `-> None`.

Hints are not enforced. This runs without error:

```python
x: int = "not an int"
x            # 'not an int'
```

Accept the widest type you need, return a precise one. `Iterable[int]` accepts lists, tuples, sets and generators:

```python
from collections.abc import Iterable

def total(xs: Iterable[int]) -> int:
    return sum(xs)

total((1, 2))    # 3
```

Other names you will see:

- `Any`: anything, turns checking off for that value.
- `Callable[[int, str], bool]`: a function taking an int and a str, returning a bool. Useful when you inject a clock or a sleep function.
- `Literal["r", "w"]`: only these exact values.
- `TypedDict`: a dict with fixed keys and a type per key.
- `Optional[int]`: the older spelling of `int | None`.

You can name a long type and reuse it: `Row = dict[str, str | int]`.

A default of `None` needs the `| None` in the hint:

```python
def tags(xs: list[str] | None = None) -> list[str]:
    if xs is None:
        xs = []
    return xs
```

In a live interview, hints on the signature are a cheap way to show the reader your contract before any code is written.

## Common mistakes

- Expecting a wrong type to raise an error. It will not unless you validate yourself.
- Writing `def f(x: int = None)`. The hint should be `int | None`.
- Writing `tuple[int]` for a tuple of many ints. That means exactly one. Use `tuple[int, ...]`.
- Annotating with a value instead of a type, such as `xs: []`.
- Forgetting `-> None` versus `-> int | None` when some paths return nothing.

## See also

- [Functions: defaults, *args, **kwargs, the mutable default trap](#/kb/py-functions-args)
- [Dataclasses](#/kb/py-dataclasses)
- [Input validation and data contracts](#/kb/prod-input-validation)
- Official docs: https://docs.python.org/3/library/typing.html
