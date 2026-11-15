---
title: "Classes: __init__, methods, properties, dunder methods"
summary: Define a class with state in __init__, behaviour in methods, computed attributes and special methods.
tags: [python, classes, oop]
---
```python
class Account:
    def __init__(self, owner, balance=0):    # runs when you call Account(...)
        self.owner = owner
        self.balance = balance
    def deposit(self, amount):               # self is the object itself
        self.balance += amount
    def __repr__(self):
        return f"Account({self.owner!r}, {self.balance})"
acc = Account("ana"); acc.deposit(50)
acc                                          # Account('ana', 50)
```

- Every method takes `self` first. Python passes it for you: `acc.deposit(50)`.
- Create attributes in `__init__` with `self.name = value`.
- Dunder methods such as `__repr__`, `__eq__` and `__len__` let built-in syntax work on your objects.

<!-- more -->

## Details

A property is a method read like an attribute. Use it for values computed from other attributes. Without a setter it is read-only.

```python
class Temp:
    def __init__(self, c):
        self.c = c
    @property
    def f(self):                             # read as t.f, no parentheses
        return self.c * 9 / 5 + 32
    def __eq__(self, other):
        return isinstance(other, Temp) and self.c == other.c
    def __lt__(self, other):
        return self.c < other.c

t = Temp(100)
t.f                                          # 212.0
t == Temp(100)                               # True   False without __eq__
sorted([Temp(30), Temp(5)])[0].c             # 5      sorting uses __lt__
```

Common dunder methods: `__repr__` (text for debugging), `__str__` (text for `print`, falls back to `__repr__`), `__eq__` (`==`), `__lt__` (`<` and sorting), `__len__` (`len(obj)`), `__contains__` (`in`), `__getitem__` (`obj[key]`).

A class that defines `__eq__` without `__hash__` cannot be used in a set or as a dict key.

A variable written in the class body is shared by all instances. That is fine for constants and wrong for a list each object should own:

```python
class Bag:
    items = []                               # one list for every Bag
a, b = Bag(), Bag()
a.items.append(1)
b.items                                      # [1]
```

Inheritance: `class Savings(Account):` reuses the parent's methods. Call `super().__init__(owner, balance)` in the child's `__init__` to run the parent's setup. A leading underscore, as in `self._cache`, marks an attribute as internal by convention.

## Common mistakes

- Forgetting `self` in the method definition or before an attribute name.
- Misspelling `__init__`, so the object is created with no attributes.
- Calling a property with parentheses: `t.f()` raises `TypeError`.
- Keeping per-object state in a class attribute.
- Comparing objects with `==` without defining `__eq__`: it compares identity.

## See also

- [Dataclasses](#/kb/py-dataclasses)
- [Functions: defaults, *args, **kwargs, the mutable default trap](#/kb/py-functions-args)
- [Exceptions: try, except, raise, custom errors](#/kb/py-exceptions)
- Official docs: https://docs.python.org/3/tutorial/classes.html
