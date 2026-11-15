# Consulting documentation fast

The exercise often provides documentation, and the invite says you may use it. Nobody expects you to remember every signature. They expect you to find the right fact in seconds and to check it by running code. Do not ask an assistant for a fact that is two lines away in the docs.

## Four things to find

When you open the docs for a function, look for exactly these:

1. **The signature.** Names, order and defaults.
2. **Argument order and meaning.** Which one is the data, which one is the key?
3. **The return shape.** A new object, or `None` because it works in place?
4. **Edge cases.** What happens on empty input, a missing key, ties?

Python can show you the signature without leaving the editor:

```python
import inspect
print(inspect.signature(sorted))   # (iterable, /, *, key=None, reverse=False)
```

The `/` means `iterable` is positional only, and the `*` means `key` and `reverse` must be named. `help(sorted)` prints the full text.

## Then confirm by running

Reading says what should happen, running says what does. Three typical findings:

```python
x = [3, 1, 2]
print(x.sort(), x)         # None [1, 2, 3]   sort() works in place and returns None
print("1,,2".split(","))   # ['1', '', '2']   split(",") keeps empty pieces
print(round(2.5))          # 2                round() on a tie goes to the even number
```

The first one is a classic bug: `y = x.sort()` leaves `y` as `None`. The last one surprises people who expect 3.

Edge cases are in the docs too. For example `max([])` raises `ValueError`, but `max([], default=0)` returns `0`, and `statistics.median([])` raises `StatisticsError`. If your clarifying answer said "empty returns 0", the docs tell you which function needs a guard.

## Work quickly

- Search the page for the function name or the argument you are unsure about, rather than reading the whole page.
- Read the example section first, then the parameter list.
- Check the return line before you write code that uses the result.
- Say what you are doing: "I am checking whether `heapq.nlargest` takes `n` first." It does: `nlargest(n, iterable, key=None)`.

## With the assistant

Use docs for facts and the assistant for drafts. If the assistant uses a function you do not know, look it up before you accept it. A confident answer can use an argument that does not exist.

## Say it like this

"I do not remember whether `n` comes first, so I will check the signature. It is `nlargest(n, iterable)`. I will test it on a small list."

Related: [Python lists](#/kb/py-lists), [Sorting in Python](#/kb/py-sorting), [Verifying AI-written code](#/kb/ai-verifying-ai-code).
