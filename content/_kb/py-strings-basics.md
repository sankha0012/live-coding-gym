---
title: "Strings: indexing, immutability, common checks"
summary: Index, measure, search and compare strings, and remember that a string can never be changed in place.
tags: [python, strings]
---
```python
s = "hello"
len(s)            # 5
s[0], s[-1]       # ('h', 'o')    first and last character
"ell" in s        # True          substring test
s + "!" * 2       # 'hello!!'     + joins, * repeats
s.find("l")       # 2             first position, -1 when missing
s.count("l")      # 2
s == "Hello"      # False         comparison is case-sensitive
```

- Strings are immutable: `s[0] = "H"` raises `TypeError`. Build a new string instead.
- Indexes start at 0. `s[len(s)]` raises `IndexError`; negative indexes count from the end.
- A character is just a string of length 1.

<!-- more -->

## Details

Loop over a string to get its characters one by one: `for ch in s:`. `list(s)` gives a list of characters, and `"".join(chars)` turns the list back into a string. That is the usual way to "edit" a string:

```python
chars = list("hello")
chars[0] = "H"
"".join(chars)        # 'Hello'
"hello"[::-1]         # 'olleh'   reversed copy
```

`s.index(sub)` works like `s.find(sub)` but raises `ValueError` when the substring is missing.

Convert with `str(42)` and `int("42")`. `"3" + 4` raises `TypeError`: Python never converts for you.

Characters have numeric codes. `<` and `>` compare strings code by code, so all uppercase letters come before all lowercase letters:

```python
ord("a"), chr(98)     # (97, 'b')
"abc" < "abd"         # True
"Z" < "a"             # True    uppercase sorts first
"10" < "9"            # True    text order, not numeric order
```

Single and double quotes mean the same thing. `"\n"` is a newline and `"\t"` a tab. A raw string `r"\d"` keeps the backslash. Triple quotes allow a string over several lines.

An empty string is falsy, so `if not s:` tests for `""`.

## Common mistakes

- Trying to assign to `s[i]`, or expecting `s.upper()` to change `s`.
- Comparing without normalising case: `"Ana" == "ana"` is `False`.
- Building a long string with `+=` in a loop instead of collecting parts and using `join`.
- Comparing numbers stored as text: `"10" < "9"` is `True`.

## See also

- [Slicing](#/kb/py-slicing)
- [String methods: lower, strip, replace, startswith, isalpha and friends](#/kb/py-str-methods)
- [str.split and str.join](#/kb/py-str-split-join)
- Official docs: https://docs.python.org/3/library/stdtypes.html
