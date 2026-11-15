---
title: Regular expressions with re
summary: Find, extract, replace and split text by pattern with re.search, findall, sub and split.
tags: [python, regex, strings]
---
```python
import re
re.findall(r"\d+", "a1 b22 c333")          # ['1', '22', '333']   all matches
m = re.search(r"(\w+)@(\w+)\.com", "mail ana@site.com now")   # first match or None
m.group(0), m.group(1), m.groups()         # ('ana@site.com', 'ana', ('ana', 'site'))
re.sub(r"\s+", " ", "a   b \n c")          # 'a b c'              replace
re.split(r"[,;]\s*", "a, b;c")             # ['a', 'b', 'c']      split on a pattern
re.fullmatch(r"\d{4}-\d{2}", "2024-03") is not None   # True      whole string must match
```

- Always write patterns as raw strings: `r"\d+"`.
- `search` looks anywhere, `match` only at the start, `fullmatch` needs the whole string.
- `search`, `match` and `fullmatch` return `None` when nothing matches. Check before calling `.group()`.

<!-- more -->

## Details

Pattern pieces:

```
\d digit        \w letter, digit or _     \s whitespace     . any character except newline
\D \W \S        the opposites
[abc] one of    [a-z] range               [^abc] none of
^ start         $ end                     \b word boundary
* 0 or more     + 1 or more               ? 0 or 1          {3} exactly 3    {2,4} 2 to 4
(...) group     (?:...) group, not captured                 a|b either
```

To match a special character literally, put a backslash before it: `\.` or `\(`. `re.escape(text)` does it for a whole string.

Quantifiers are greedy and take as much as possible. Add `?` to take as little as possible:

```python
re.findall(r"<.+>", "<a><b>")     # ['<a><b>']
re.findall(r"<.+?>", "<a><b>")    # ['<a>', '<b>']
```

`findall` changes shape when the pattern has groups. It returns the groups, not the whole match:

```python
re.findall(r"(\w)=(\d)", "a=1 b=2")    # [('a', '1'), ('b', '2')]
```

Named groups make the result readable:

```python
m = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})", "on 2024-03-15")
m.group("year")       # '2024'
m.groupdict()         # {'year': '2024', 'month': '03'}
```

In `sub`, refer to groups with `\1`, `\2`:

```python
re.sub(r"(\w+) (\w+)", r"\2 \1", "hello world")    # 'world hello'
```

Flags: `re.IGNORECASE` ignores case, `re.MULTILINE` makes `^` and `$` match at each line. Pass them as `flags=`.

If you use a pattern many times, compile it once: `pat = re.compile(r"^\w+$")`, then `pat.match(s)`.

A common cleaning step keeps only letters and digits:

```python
re.sub(r"[^a-z0-9]", "", "A man, a plan!".lower())   # 'amanaplan'
```

For simple cases prefer string methods: `in`, `startswith`, `split`, `replace`.

## Common mistakes

- Calling `.group()` on `None` after a failed search: `AttributeError`.
- Using `match` when you meant `search`. `re.match(r"\d+", "ab12")` is `None`.
- Forgetting to escape the dot. `a.c` also matches `abc`.
- Expecting numbers from `findall`. Matches are strings. Convert with `int()`.
- Forgetting the `r` prefix, so `"\b"` becomes a backspace character.

## See also

- [String methods: lower, strip, replace, startswith, isalpha and friends](#/kb/py-str-methods)
- [str.split and str.join](#/kb/py-str-split-join)
- [Input validation and data contracts](#/kb/prod-input-validation)
- Official docs: https://docs.python.org/3/library/re.html
