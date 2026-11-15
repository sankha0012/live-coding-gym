---
title: f-strings and number formatting
summary: Put values inside a string with f"{value}" and control decimals, padding, percent and thousands separators.
tags: [python, strings, formatting]
---
```python
name, n, x = "Ana", 7, 3.14159
f"{name} has {n}"         # 'Ana has 7'
f"{x:.2f}"                # '3.14'        two decimals
f"{0.256:.1%}"            # '25.6%'       multiplies by 100
f"{1234567:,}"            # '1,234,567'   thousands separator
f"{n:03d}"                # '007'         zero-padded to width 3
f"{name:>6}|{name:<6}|"   # '   Ana|Ana   |'   right and left aligned
f"{n + 1 = }"             # 'n + 1 = 8'   handy for debugging
```

- Anything inside `{}` is a normal Python expression. The format goes after a colon.
- The result is always a string. Formatting does not change the number itself.
- Without the leading `f` the braces are printed literally.

<!-- more -->

## Details

The format spec is `{value:[fill][align][width][,][.precision][type]}`. Common types: `d` integer, `f` fixed decimals, `e` scientific, `%` percent. Align with `<` (left), `>` (right) or `^` (centre).

```python
f"{1234.5:,.2f}"          # '1,234.50'
f"{12345.678:.2e}"        # '1.23e+04'
f"{'hi':*^8}"             # '***hi***'
f"{name!r}"               # "'Ana'"      repr, shows the quotes
f"{{literal}}"            # '{literal}'  double the braces to print them
digits = 3
f"{x:.{digits}f}"         # '3.142'      the precision can be a variable
```

Formatting rounds the same way `round()` does. Floats are stored in binary, so a value that looks like an exact half may round down:

```python
f"{2.5:.0f}"              # '2'      ties go to the even digit
f"{2.675:.2f}"            # '2.67'   2.675 is stored slightly below
```

`format(x, ".2f")` gives the same string as `f"{x:.2f}"`. `round(x, 2)` returns a float, not a string, so `round(2.5, 1)` prints as `2.5`, not `2.50`.

Dates take `strftime` codes: `f"{d:%Y-%m-%d}"`.

Since Python 3.12 you may reuse the same quote type inside the braces. Using the other quote type still works everywhere.

## Common mistakes

- Forgetting the `f` prefix.
- Using `round()` when the output needs a fixed number of decimals: use `:.2f`.
- Writing `{x:2f}` (width 2) when you mean `{x:.2f}` (two decimals).
- Doing maths on the formatted result: it is a string.

## See also

- [Floats, NaN, infinity and rounding](#/kb/py-math-nan)
- [input() and print() (Coderbyte-style stdin and stdout)](#/kb/py-input-print)
- [Strings: indexing, immutability, common checks](#/kb/py-strings-basics)
- Official docs: https://docs.python.org/3/library/string.html
