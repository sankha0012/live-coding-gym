---
title: str.split and str.join
summary: Split a string into a list of pieces, and join a list of strings back into one string.
tags: [python, strings]
---
```python
"the  sky is blue".split()        # ['the', 'sky', 'is', 'blue']  any whitespace, no empty pieces
"a,b,,c".split(",")               # ['a', 'b', '', 'c']           exact separator, keeps empty pieces
" ".join(["blue", "is", "sky"])   # 'blue is sky'
"-".join(str(n) for n in [1, 2])  # '1-2'  join needs strings
```

- `split()` with no argument splits on any run of whitespace and drops leading and trailing space.
- `split(" ")` splits on every single space, so double spaces give empty strings.
- `join` is called on the separator, not on the list.

<!-- more -->

## Details

`str.split(sep=None, maxsplit=-1)` returns a list. With `maxsplit=1` you get at most two pieces:

```python
"key=value=x".split("=", 1)   # ['key', 'value=x']
```

`str.splitlines()` splits on line endings and does not leave a trailing empty string. `str.partition(sep)` always returns three parts `(before, sep, after)`, which is handy when the separator may be missing.

`sep.join(iterable)` raises `TypeError` if any item is not a string. Convert first: `", ".join(map(str, numbers))`.

Joining is the right way to build a string from many parts. Repeated `+=` in a loop creates a new string each time.

## Common mistakes

- Using `split(" ")` when the input may contain double spaces or tabs.
- Calling `list.join(" ")` (it is `" ".join(list)`).
- Forgetting that an empty string gives `[]` for `"".split()` but `['']` for `"".split(",")`.

## See also

- [Slicing](#/kb/py-slicing)
- Official docs: https://docs.python.org/3/library/stdtypes.html
