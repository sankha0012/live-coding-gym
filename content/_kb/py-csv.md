---
title: The csv module
summary: Read and write CSV rows as lists or dicts, with quoting and commas inside fields handled for you.
tags: [python, csv, files]
---
```python
import csv
with open("people.csv", newline="") as f:
    for row in csv.DictReader(f):       # first line is the header
        print(row["name"], int(row["age"]))   # every value is a str

with open("out.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["name", "age"])
    w.writeheader()
    w.writerow({"name": "Ana", "age": 30})
```

- Every value you read is a string. Convert numbers yourself with `int()` or `float()`.
- Open files with `newline=""` so the module controls line endings.
- `csv.reader` gives lists, `csv.DictReader` gives dicts keyed by the header.

<!-- more -->

## Details

The readers take any iterable of lines, so you can test without a file by using `io.StringIO`:

```python
import csv, io
text = "name,age\nAna,30\nBo,25\n"
list(csv.reader(io.StringIO(text)))
# [['name', 'age'], ['Ana', '30'], ['Bo', '25']]
list(csv.DictReader(io.StringIO(text)))
# [{'name': 'Ana', 'age': '30'}, {'name': 'Bo', 'age': '25'}]
```

With `csv.reader` the header is just the first row. Skip it with `header = next(reader)`.

The module exists because fields can contain commas and quotes. `str.split(",")` gets this wrong:

```python
next(csv.reader(['x,"a,b",z']))   # ['x', 'a,b', 'z']
'x,"a,b",z'.split(",")            # ['x', '"a', 'b"', 'z']
```

Writing quotes fields only when needed, and ends lines with `\r\n` by default:

```python
out = io.StringIO()
csv.writer(out).writerow(["a,b", 'say "hi"', 3])
out.getvalue()                    # '"a,b","say ""hi""",3\r\n'
```

Use `writerows(list_of_rows)` to write many rows at once. For other separators pass `delimiter=";"` or `delimiter="\t"`.

A short row in `DictReader` fills the missing columns with `None`. `DictWriter.writerow` raises `ValueError` if the dict has a key that is not in `fieldnames`.

## Common mistakes

- Comparing `row["age"] > 18` without converting: it is a string, so this raises `TypeError`.
- Forgetting `writeheader()`, so the output file has no header line.
- Splitting lines by hand with `split(",")` and breaking on quoted commas.
- Reading the reader twice. It is an iterator and is empty after the first pass.
- Leaving out `newline=""` and getting blank lines between rows on Windows.

## See also

- [Files and pathlib](#/kb/py-files-pathlib)
- [Iterators and generators](#/kb/py-iterators-generators)
- [Reading and inspecting a DataFrame](#/kb/pd-read-inspect)
- Official docs: https://docs.python.org/3/library/csv.html
