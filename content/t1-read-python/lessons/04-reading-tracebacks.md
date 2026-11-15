# Reading tracebacks

## The problem it solves

A traceback looks long and alarming, but it has a fixed structure. Read it correctly and it tells you the error type, the line, and the chain of calls that led there, usually in under ten seconds.

## Read it from the bottom

```python
def parse(line):
    name, amount = line.split(",")
    return name, int(amount)

def total(lines):
    return sum(parse(line)[1] for line in lines)

print(total(["ann,5", "bo,x"]))
```

Running this prints a traceback similar to this (line numbers and memory addresses vary):

```text
Traceback (most recent call last):
  File "demo.py", line 8, in <module>
    print(total(["ann,5", "bo,x"]))
  File "demo.py", line 6, in total
    return sum(parse(line)[1] for line in lines)
  File "demo.py", line 6, in <genexpr>
    return sum(parse(line)[1] for line in lines)
  File "demo.py", line 3, in parse
    return name, int(amount)
ValueError: invalid literal for int() with base 10: 'x'
```

1. **Last line first.** `ValueError: invalid literal for int() with base 10: 'x'` says: an `int()` call got the text `'x'`.
2. **The line above it** is where it happened: `return name, int(amount)` in `parse`.
3. **Work upward** to see who called it. The generator expression inside `total` called `parse`, and `total` was called from the main script. The top entry is the outermost call.
4. **Decide where the fix belongs.** The bug may be in the data (`"bo,x"` is bad input), in the function that did not expect it, or in the caller.

## The common error types

| Error | Typical meaning |
|---|---|
| `KeyError: 'x'` | dict has no key `'x'`; use `.get` or check first |
| `IndexError: list index out of range` | index past the end; check the length or the loop bounds |
| `TypeError: unsupported operand type(s) for +: 'int' and 'str'` | mixed types, often a number that is still a string |
| `ValueError: ...` | right type, unacceptable value (for example `int("x")`) |
| `AttributeError: 'NoneType' object has no attribute 'x'` | a value is `None`; a function probably returned nothing |
| `ZeroDivisionError` | dividing by zero, often an empty list's length |
| `UnboundLocalError` | a local variable was used before it got a value |
| `NameError` | a name is misspelled or never defined |
| `RecursionError` | a function calls itself without reaching a base case |

`AttributeError: 'NoneType' ...` is very frequent. It usually means a function that forgot `return`, or a method like `list.sort()` that returns `None` while you used its result.

## Errors that are not tracebacks

Many bugs raise nothing. The result is wrong but no error appears: an off-by-one, a swallowed exception, a shared mutable default. For those the only way is to predict the output yourself and compare.

## Using the traceback with the assistant

When you ask for help, give it what you read: the last line, the line number, the input that caused it, and what you expected. "`int()` fails on `'x'` at line 3 for input `bo,x`; I expect that row to be skipped" is a good prompt. "It crashes, fix it" is not, because you will get a change you cannot judge.

## Common mistakes

- Reading from the top and stopping at the first long path.
- Catching the exception to make it disappear, which hides the real problem.
- Fixing the line where it crashed when the real cause is in the data or the caller.

## Related

- [Exceptions](#/kb/py-exceptions)
- [Truthiness and None](#/kb/py-truthiness-none)
