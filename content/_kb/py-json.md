---
title: "JSON: dumps, loads, sort_keys"
summary: Turn Python dicts and lists into JSON text and back, with stable key order when you need it.
tags: [python, json, serialization]
---
```python
import json
json.dumps({"b": 1, "a": [1, 2]})                  # '{"b": 1, "a": [1, 2]}'
json.dumps({"b": 1, "a": None}, sort_keys=True)    # '{"a": null, "b": 1}'
json.loads('{"ok": true, "n": null, "x": 1.5}')    # {'ok': True, 'n': None, 'x': 1.5}
json.dumps({"a": 1, "b": 2}, separators=(",", ":"))  # '{"a":1,"b":2}'  compact
```

- `dumps` and `loads` work with strings. `dump` and `load` (no `s`) work with an open file.
- JSON has `true`, `false`, `null`. Python has `True`, `False`, `None`. The module converts for you.
- `sort_keys=True` gives the same text for the same data, which matters for hashing and comparing.

<!-- more -->

## Details

Only a few types can be written: `dict`, `list`, `tuple`, `str`, `int`, `float`, `bool` and `None`. Anything else raises `TypeError`. Pass `default=` to convert unknown objects:

```python
from datetime import date
json.dumps({"d": date(2024, 1, 2)}, default=str)   # '{"d": "2024-01-02"}'
```

The round trip is not always exact. Dict keys always become strings and tuples become lists:

```python
json.loads(json.dumps({1: "x"}))   # {'1': 'x'}
json.dumps((1, 2))                 # '[1, 2]'
```

Useful options for `dumps`:

- `indent=2` pretty-prints over several lines.
- `ensure_ascii=False` keeps `é` as `é` instead of `é`.

Reading and writing a file:

```python
with open("data.json", "w") as f:
    json.dump({"a": 1}, f)
with open("data.json") as f:
    data = json.load(f)            # {'a': 1}
```

Bad input raises `json.JSONDecodeError`, which is a subclass of `ValueError`. Catch it when the text comes from outside your program.

## Common mistakes

- Mixing up `loads` (string) and `load` (file object).
- Parsing a Python-style string such as `"{'a': 1}"`. JSON needs double quotes.
- Expecting integer keys to come back as integers. They come back as strings.
- Calling `json.loads("")`. An empty string is not valid JSON and raises `JSONDecodeError`.
- Writing `float("nan")`: `dumps` outputs `NaN`, which is not standard JSON and other parsers may reject it.

## See also

- [Dictionaries: get, setdefault, items, membership](#/kb/py-dicts)
- [Files and pathlib](#/kb/py-files-pathlib)
- [Parsing JSON from an LLM reply](#/kb/ai-llm-json-parsing)
- Official docs: https://docs.python.org/3/library/json.html
