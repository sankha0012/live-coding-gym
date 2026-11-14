# Exploring objects without autocomplete

The Coderbyte editor gives you no autocomplete, but the interview allows documentation. Python carries its own documentation, so you can answer most "what was that method called?" questions in a few seconds with the Run button.

## Three tools

- `type(x)` tells you what you are holding. Many bugs start with a wrong guess here: a `str` where you expected an `int`, a `numpy.float64` where you expected a `float`, a `Series` where you expected a list.
- `dir(x)` lists the attributes and methods. Filter out the dunder names to see the useful part:

```python
print([m for m in dir("") if not m.startswith("_")])
```

- `help(x)` prints the docstring of an object, a method or a module. Ask about the method, not the result of calling it:

```python
help(str.split)        # right
help("a,b".split)      # also fine: a bound method
help("a,b".split(",")) # wrong: this is help on a list
```

## Two more that save time

- `inspect.signature(f)` shows the parameters and their defaults in one line, which is often all you need:

```python
import inspect
print(inspect.signature(sorted))   # (iterable, /, *, key=None, reverse=False)
```

- `vars(obj)` shows the instance attributes of your own objects, which helps when a dataclass or class does not hold what you think.

## A routine for an unknown object

1. `print(type(x))`
2. `print([m for m in dir(x) if not m.startswith("_")])`
3. `help(type(x).the_method)` for the one that looks right.
4. Try it on a tiny input with Run before you use it in the real code.

## Saying it in the interview

"I don't remember whether `rsplit` takes `maxsplit` as a keyword, so I'll check `help(str.rsplit)` quickly" sounds like an engineer who checks facts. Guessing silently and getting it wrong sounds worse.
