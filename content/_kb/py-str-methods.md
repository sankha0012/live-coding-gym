---
title: "String methods: lower, strip, replace, startswith, isalpha and friends"
summary: The everyday string methods for cleaning, changing case, replacing and testing text.
tags: [python, strings, cleaning]
---
```python
"  Hi There \n".strip()          # 'Hi There'   whitespace off both ends
"Hi There".lower()               # 'hi there'
"hi there".title()               # 'Hi There'
"a-b-a".replace("a", "x")        # 'x-b-x'      every occurrence
"report.csv".endswith(".csv")    # True
"abc".isalpha(), "42".isdigit(), "a1".isalnum()   # (True, True, True)
"7".zfill(3)                     # '007'
```

- Every method returns a new string. The original never changes, so keep the result: `s = s.strip()`.
- `strip` only touches the two ends, never the middle. `lstrip` and `rstrip` do one side.
- The `is...` tests are `False` for an empty string.

<!-- more -->

## Details

Case: `lower()`, `upper()`, `capitalize()` (first letter only), `title()`, `swapcase()`. Use `lower()` on both sides for a case-insensitive comparison.

`replace(old, new, count)` replaces all occurrences unless you pass a count. Replacing with `""` deletes.

```python
"a-b-a".replace("a", "x", 1)     # 'x-b-a'
"a b  c".replace(" ", "")        # 'abc'
```

`startswith` and `endswith` accept a tuple of options:

```python
"photo.PNG".lower().endswith((".png", ".jpg"))   # True
```

`strip(chars)` removes any of the given characters from the ends, as a set. It does not remove a prefix or suffix. For that use `removeprefix` and `removesuffix`:

```python
"xxhixx".strip("x")                  # 'hi'
"abcab".rstrip("ab")                 # 'abc'       strips a, b in any order
"data.csv.csv".removesuffix(".csv")  # 'data.csv'  exactly one suffix
```

Tests look at every character: `isalpha()` letters, `isdigit()` digits, `isalnum()` letters or digits, `isspace()` whitespace, `isupper()` and `islower()`.

```python
"-5".isdigit(), "4.2".isdigit()      # (False, False)   sign and dot are not digits
"".isalpha()                         # False
"".join(ch for ch in "A man, a plan!".lower() if ch.isalnum())   # 'amanaplan'
```

Padding: `zfill(width)`, `ljust(width)`, `rjust(width)`, `center(width)`.

## Common mistakes

- Calling `s.strip()` or `s.lower()` and not storing the result.
- Using `strip(".csv")` to remove an extension: it strips the characters `.`, `c`, `s`, `v` from both ends.
- Using `isdigit()` to detect negative or decimal numbers.
- Expecting `strip()` to remove spaces inside the text.

## See also

- [Strings: indexing, immutability, common checks](#/kb/py-strings-basics)
- [str.split and str.join](#/kb/py-str-split-join)
- [Regular expressions with re](#/kb/py-regex-basics)
- Official docs: https://docs.python.org/3/library/stdtypes.html
