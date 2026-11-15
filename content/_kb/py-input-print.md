---
title: input() and print() (Coderbyte-style stdin and stdout)
summary: Read text from stdin with input(), convert it yourself, and write results with print() and its sep and end options.
tags: [python, io, stdin]
---
```python
line = input()                       # one line as a str, without the newline
n = int(input())                     # input() never returns a number: convert
a, b = map(int, input().split())     # line "3 4" gives a = 3, b = 4
nums = [int(x) for x in input().split()]   # line "5 6 7" gives [5, 6, 7]
print("a", "b", 3)                   # a b 3     items joined by one space
print("a", "b", sep="-")             # a-b
print("no newline", end="")          # stays on the same line
print(*[1, 2, 3])                    # 1 2 3     star unpacks the list
```

- `input()` always returns a string. Wrap it in `int()` or `float()` when you need a number.
- `print()` converts every argument with `str()`, puts `sep` between them and `end` after them.
- `print()` returns `None`. A function that must give back a value needs `return`.

<!-- more -->

## Details

`input(prompt)` writes the prompt, then waits for one line. When there is no more input it raises `EOFError`. In an online judge do not pass a prompt: the prompt text would become part of your output.

To read every line until the end, use `sys.stdin`:

```python
import sys
for line in sys.stdin:               # each line still ends with "\n"
    line = line.strip()
tokens = sys.stdin.read().split()    # or: all remaining tokens as one flat list
```

`print` has four useful keyword options: `sep` (default one space), `end` (default newline), `file` and `flush`.

```python
import sys
print("x", 1, sep="")                # x1
print("warn", file=sys.stderr)       # goes to stderr, not to the checked output
print(", ".join(["a", "b"]))         # a, b
print()                              # an empty line
```

On Coderbyte the starter code usually ends with a line like `print(FunctionName(input()))`. Keep that line. Your function receives the input as a parameter and must `return` the answer.

## Common mistakes

- Doing maths on the raw string: `input() + 1` raises `TypeError`, and `"2" * 3` gives `'222'`.
- Printing inside the function and returning nothing, so the caller prints `None`.
- Leaving debug prints in the code: a judge compares the whole output.
- Printing a list directly: `print([1, 2])` shows `[1, 2]` with brackets. Use `print(*xs)` or `join`.
- Calling `int()` on a line with several numbers. Split first.

## See also

- [str.split and str.join](#/kb/py-str-split-join)
- [f-strings and number formatting](#/kb/py-f-strings)
- [The Coderbyte format](#/kb/iv-coderbyte-format)
- Official docs: https://docs.python.org/3/library/functions.html
