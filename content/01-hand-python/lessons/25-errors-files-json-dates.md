# Errors, files, JSON and dates

## The problem it solves

Real input is messy. A number is missing, a file is absent, a date has the wrong format. Robust code expects this. This lesson covers the four standard-library tools that appear in nearly every data task: `try` and `except`, `with open`, `json` and `csv`, and `datetime`.

## The smallest runnable example

```python
import csv
import io
import json
from datetime import date, datetime

def safe_int(text, default=0):
    try:
        return int(text)
    except (ValueError, TypeError):
        return default

print(safe_int("42"), safe_int("x"), safe_int(None, -1))   # 42 0 -1

record = {"id": 7, "tags": ["a", "b"], "ok": True}
text = json.dumps(record, sort_keys=True)
print(text)                            # {"id": 7, "ok": true, "tags": ["a", "b"]}
print(json.loads(text) == record)      # True

row = next(csv.reader(io.StringIO('a,"b,c",d')))
print(row)                             # ['a', 'b,c', 'd']

d1 = date.fromisoformat("2026-11-01")
d2 = date.fromisoformat("2026-11-14")
print((d2 - d1).days)                  # 13
stamp = datetime.strptime("14/11/2026 08:30", "%d/%m/%Y %H:%M")
print(stamp.isoformat(), stamp.strftime("%Y-%m-%d"))
```

Run it and keep the file open while you retype it.

## try and except

Catch the specific error you expect. The shape is:

```python
try:
    risky()
except ValueError:
    handle()
else:
    only_if_no_error()
finally:
    always_runs()
```

`int("x")` raises `ValueError`. `d["k"]` raises `KeyError`. `xs[9]` raises `IndexError`. `1 / 0` raises `ZeroDivisionError`. A missing file raises `FileNotFoundError`. Catch the narrowest one that fits.

To signal your own failure, `raise ValueError("clear message")`. To pass an error up after logging it, use a bare `raise`.

## Files

```python
import json
import tempfile
from pathlib import Path

with tempfile.TemporaryDirectory() as tmp:
    path = Path(tmp) / "data.json"
    path.write_text(json.dumps({"n": 1}))
    with open(path) as f:
        data = json.load(f)
    print(data)                       # {'n': 1}
    with open(path, "w") as f:
        json.dump({"n": 2}, f)
    print(path.read_text())           # {"n": 2}
```

`with open(...) as f` closes the file even if an error happens. Use `json.load(f)` and `json.dump(obj, f)` for file objects, and `json.loads(text)` and `json.dumps(obj)` for strings. The letter `s` means string. Mode `"r"` reads, `"w"` replaces the file, `"a"` appends.

## Dates

`date.fromisoformat("2026-11-14")` parses an ISO date. `strptime(text, format)` parses any format, and `strftime(format)` prints one. Subtracting two dates gives a `timedelta`, and `.days` is the whole number of days. Add days with `d + timedelta(days=3)`.

## Trap 1: the bare except

```python
def bad(text):
    try:
        return int(text)
    except:
        return 0
```

A bare `except:` also catches `KeyboardInterrupt` and hides typos such as a misspelled variable. Name the exception. Use `except Exception` only at the outer edge of a program, and log what happened.

## Trap 2: JSON does not round-trip everything

```python
import json
print(json.loads(json.dumps({1: "a"})))     # {'1': 'a'}  keys become strings
print(json.loads(json.dumps((1, 2))))       # [1, 2]      tuple becomes list
try:
    json.dumps({"d": {1, 2}})
except TypeError as e:
    print("TypeError:", e)                   # sets are not serialisable
```

Keys become strings, tuples become lists, and sets, dates and custom objects raise `TypeError`. Convert them yourself before you dump, for example `sorted(my_set)` or `d.isoformat()`.

## Trap 3: parsing CSV with split, and date formats

```python
line = 'a,"b,c",d'
print(line.split(","))                       # ['a', '"b', 'c"', 'd']  wrong
print(next(csv.reader([line])))              # ['a', 'b,c', 'd']      right
```

Quoted fields can contain commas, so use the `csv` module. For dates, an invalid one such as `"2026-13-01"` raises `ValueError`. If the prompt says "invalid input", decide what to return and say it. Also note that `"%d/%m/%Y"` and `"%m/%d/%Y"` swap day and month, a real source of silent bugs.

## Say it like this

"I catch only the errors I expect, like ValueError for a bad number, and I return a default the prompt names. I open files with a with block so they always close. I use the csv module for quoted fields and json for structured data, and I remember that JSON turns keys into strings. For dates I parse ISO strings and subtract them, so the day count is exact. Each step is linear in the input."
