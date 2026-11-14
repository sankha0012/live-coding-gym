# Classes and dataclasses

## The problem it solves

A class bundles data with the operations on it. Interview prompts like "write a Stack", "write a Counter", or "model a bank account" test whether you can define `__init__`, keep state on `self`, and raise the right error when a rule is broken. Dataclasses remove the boilerplate for plain records.

## The smallest runnable example

```python
class Stack:
    def __init__(self):
        self._items = []

    def push(self, x):
        self._items.append(x)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def __len__(self):
        return len(self._items)

s = Stack()
s.push(1)
s.push(2)
print(s.pop(), len(s))          # 2 1
try:
    Stack().pop()
except IndexError as e:
    print("error:", e)
```

The parts to type from memory: `class Name:`, `def __init__(self, ...)`, attributes as `self.x = ...`, methods with `self` first, `raise SomeError("message")`. The single leading underscore in `_items` is a convention that says "internal".

## Dataclasses

```python
from dataclasses import dataclass, field

@dataclass(order=True)
class Job:
    priority: int
    name: str = ""
    tags: list = field(default_factory=list, compare=False)

jobs = [Job(3, "c"), Job(1, "a"), Job(2, "b")]
print([j.name for j in sorted(jobs)])    # ['a', 'b', 'c']
print(Job(1, "a") == Job(1, "a"))        # True
print(Job(1, "a"))                       # Job(priority=1, name='a', tags=[])
```

`@dataclass` writes `__init__`, `__repr__` and `__eq__` for you from the annotated fields. `order=True` adds comparison, field by field in the order you declared them, so `sorted` works. That is why `priority` comes first. Use `frozen=True` to make instances read-only, which also makes them hashable.

## A class with a rule: the bank account

```python
class Account:
    def __init__(self, balance=0):
        if balance < 0:
            raise ValueError("balance cannot be negative")
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("insufficient funds")
        self.balance -= amount

a = Account(10)
a.withdraw(4)
print(a.balance)         # 6
try:
    a.withdraw(100)
except ValueError as e:
    print(e)
print(a.balance)         # 6, unchanged after the failure
```

Check the rule before you change the state. If you subtract first and raise after, the object is left in a bad state. The last line of the example shows the good behaviour: a failed call changes nothing.

## Trap 1: forgetting `self`

```python
class Bad:
    def __init__(self):
        count = 0          # local variable, lost when __init__ ends
    def inc(self):
        self.count += 1    # AttributeError

try:
    Bad().inc()
except AttributeError as e:
    print(e)
```

State must be stored as `self.count`. A method must list `self` as the first parameter, or you get a `TypeError` about too many arguments.

## Trap 2: class attributes shared by all instances

```python
class Shared:
    items = []             # one list for every instance
    def add(self, x):
        self.items.append(x)

a, b = Shared(), Shared()
a.add(1)
print(b.items)             # [1]  -- surprise
```

Create mutable state inside `__init__`. In a dataclass, a list field needs `field(default_factory=list)`. Writing `tags: list = []` raises a `ValueError` right away, which protects you from the previous trap.

## Trap 3: comparing and printing objects

Without `__eq__`, two objects with the same data are not equal. Without `__repr__`, printing shows `<Foo object at 0x...>`, which is useless in a failing test. Dataclasses fix both. For a plain class, add `__repr__` that returns something like `f"Account({self.balance})"`.

## When to use which

Use a plain class when behaviour and rules matter (Stack, Account). Use a dataclass for a record of fields (a job, a point, a row). Use a plain dict when the shape is tiny and short-lived. A named, typed record reads better to an interviewer than a tuple with magic indexes.

## Say it like this

"I keep the state on self, and every method checks the rule before it changes anything, so a failed call leaves the object as it was. I raise ValueError for a bad amount and IndexError for popping an empty stack, because those are the standard errors. For a plain record I use a dataclass, and with order true I can sort the objects directly. Each method is constant time."
