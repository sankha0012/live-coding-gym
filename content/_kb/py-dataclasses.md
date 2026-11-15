---
title: Dataclasses
summary: The @dataclass decorator writes __init__, __repr__ and __eq__ for a class that mainly holds data.
tags: [python, classes, dataclasses]
---
```python
from dataclasses import dataclass, field
@dataclass
class Order:
    id: int                                     # required
    city: str = "Lisbon"                        # default value
    items: list = field(default_factory=list)   # a new list per object
o = Order(1)
o                       # Order(id=1, city='Lisbon', items=[])
o == Order(1)           # True   compared field by field
```

- Each field is a name with a type hint. The generated `__init__` takes them in that order.
- Fields without a default must come before fields with one.
- For a list, dict or set default use `field(default_factory=...)`.

<!-- more -->

## Details

Type hints are required by the syntax but are not checked when the program runs. `Order("x")` is accepted.

Options go in the decorator. `frozen=True` makes objects immutable and hashable. `order=True` adds `<`, `>` and sorting, comparing fields in order like a tuple.

`__post_init__` runs right after the generated `__init__`. Use it to validate or to compute a derived field.

```python
from dataclasses import asdict, dataclass, replace

@dataclass(frozen=True, order=True)
class Point:
    x: int
    y: int = 0
    def __post_init__(self):
        if self.x < 0:
            raise ValueError("x must be >= 0")

p = Point(1, 2)
asdict(p)               # {'x': 1, 'y': 2}
replace(p, y=5)         # Point(x=1, y=5)   a changed copy
Point(1) < Point(2)     # True
{p: "home"}[Point(1, 2)]  # 'home'   frozen objects can be dict keys
```

Assigning to a field of a frozen object raises `FrozenInstanceError`. Use `replace` to get a modified copy.

A plain `@dataclass` defines `__eq__` and is mutable, so its objects are not hashable. Add `frozen=True` when you need them in a set or as dict keys.

You can still write normal methods and properties in a dataclass. `asdict` converts nested dataclasses too, which is handy before `json.dumps`.

Compared with a hand-written class you save the repetitive `self.x = x` lines and get a readable `repr` for free.

## Common mistakes

- Writing `items: list = []`. Python raises `ValueError` at class definition and tells you to use `default_factory`.
- Leaving out the type hint: `count = 0` is a class attribute, not a field.
- Putting a field without a default after one with a default: `TypeError`.
- Expecting the type hints to validate or convert input.
- Changing a field on a `frozen=True` object.

## See also

- [Classes: __init__, methods, properties, dunder methods](#/kb/py-classes)
- [Type hints](#/kb/py-typing-hints)
- [Input validation and data contracts](#/kb/prod-input-validation)
- Official docs: https://docs.python.org/3/library/dataclasses.html
