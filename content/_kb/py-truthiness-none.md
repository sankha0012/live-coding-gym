---
title: 'Truthiness, None and "is" versus "=="'
summary: Which values count as false in an if, how to test for None, and when to use is instead of ==.
tags: [python, booleans, none]
---
```python
bool(0), bool(""), bool([]), bool({}), bool(None)   # all False: the falsy values
bool("0"), bool(" "), bool([0]), bool(-1)           # all True: everything else
a = [1, 2]; b = [1, 2]
a == b            # True    same contents
a is b            # False   two different objects
x = None
x is None         # True    the right way to test for None
0 or "default"    # 'default'   careful: 0 is falsy too
```

- Falsy: `None`, `False`, `0`, `0.0`, `""` and every empty container. Everything else is truthy.
- `==` compares values. `is` compares identity (the same object in memory).
- Use `is None` and `is not None`. Use `==` for everything else.

<!-- more -->

## Details

`if xs:` is the normal way to say "if the list is not empty". `if not s:` is true for an empty string and also for `None`.

The trap is that `0`, `0.0` and `""` are valid values that are also falsy. When zero or empty is a real answer, test for `None` explicitly:

```python
def get(d, key, default):
    value = d.get(key)
    return default if value is None else value

get({"n": 0}, "n", 5)       # 0    correct
{"n": 0}.get("n") or 5      # 5    wrong: 0 was replaced
```

`and` and `or` return one of their operands, not always a bool:

```python
None or "default"   # 'default'   first truthy value, or the last one
[] or "x"           # 'x'
1 and 2             # 2           first falsy value, or the last one
0 and 2             # 0
```

Both stop as soon as the answer is known (short circuit). That makes `if xs and xs[0] > 3:` safe for an empty list.

`is` on numbers and strings gives results that depend on interpreter details:

```python
x = 1000
y = int("1000")
x == y    # True
x is y    # False
```

`None`, `True` and `False` are single objects, so `is` is reliable for them.

More facts: `True == 1` and `False == 0`, so `True + True` is `2`. `None == False` is `False`. `[] == False` is `False` even though `[]` is falsy. NaN is truthy.

## Common mistakes

- Writing `if x == None`. It works but `is None` is the correct and safe form.
- Using `value or default` when `0` or `""` is a legal value.
- Using `is` to compare strings or numbers.
- Writing `if x:` to mean "x is not None" when x can be `0`.
- Returning `None` by accident from a branch with no `return`, then treating it as "empty".

## See also

- [Mutability, aliasing and copying](#/kb/py-copy-mutability)
- [Dictionaries: get, setdefault, items, membership](#/kb/py-dicts)
- [lambda, map, filter, any, all](#/kb/py-lambda-map-filter)
- Official docs: https://docs.python.org/3/library/stdtypes.html
