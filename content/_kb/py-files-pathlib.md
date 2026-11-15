---
title: Files and pathlib
summary: Build paths with pathlib.Path and read or write text files safely with a with block.
tags: [python, files, pathlib]
---
```python
from pathlib import Path
p = Path("data") / "notes.txt"               # / joins path parts
p.parent.mkdir(parents=True, exist_ok=True)  # create the folder if needed
p.write_text("a\nb\n", encoding="utf-8")     # creates or overwrites the file
p.read_text(encoding="utf-8")                # 'a\nb\n'
p.exists(), p.name, p.suffix, p.stem         # (True, 'notes.txt', '.txt', 'notes')
with open(p, encoding="utf-8") as f:         # the file is closed when the block ends
    lines = [line.rstrip("\n") for line in f]   # ['a', 'b']
```

- Always open files in a `with` block. It closes the file even when an error happens.
- Mode `"r"` reads (default), `"w"` overwrites, `"a"` appends, `"x"` fails if the file exists.
- Pass `encoding="utf-8"`. The default depends on the machine.

<!-- more -->

## Details

Looping over a file object gives one line at a time, each still ending with `"\n"`. This reads large files without loading them whole. `f.read()` returns everything as one string, and `.splitlines()` removes the line endings.

`write` does not add a newline. Add it yourself:

```python
with open(p, "a", encoding="utf-8") as f:
    f.write("c\n")
p.read_text(encoding="utf-8").splitlines()   # ['a', 'b', 'c']
```

`Path` objects work anywhere a filename is accepted, and `p.open()` is the same as `open(p)`. Useful parts and tests:

```python
p.parent                                     # PosixPath('data')   WindowsPath on Windows
p.with_suffix(".bak").name                   # 'notes.bak'
p.is_file(), p.parent.is_dir()               # (True, True)
sorted(x.name for x in Path("data").glob("*.txt"))   # ['notes.txt']
```

`glob` returns paths in no fixed order, so sort them when the order matters. `p.unlink()` deletes a file and `p.iterdir()` lists a folder.

A relative path is resolved from the folder where the program was started, not from the folder of the script. `Path(__file__).parent / "data.csv"` points next to the script.

Opening a missing file for reading raises `FileNotFoundError`. Writing into a missing folder raises it too, which is why `mkdir` comes first.

For binary data use modes `"rb"` and `"wb"`, or `read_bytes` and `write_bytes`.

## Common mistakes

- Opening with `"w"` to add a line: the old content is erased. Use `"a"`.
- Forgetting to strip the newline from lines before comparing or converting them.
- Building paths with string `+` and a hard-coded slash.
- Calling `open` without `with` and never closing the file.
- Reading a file a second time from the same handle: it is already at the end.

## See also

- [The csv module](#/kb/py-csv)
- [JSON: dumps, loads, sort_keys](#/kb/py-json)
- [tempfile and os: temp files, os.replace, paths](#/kb/py-tempfile-os)
- [Atomic file writes](#/kb/prod-atomic-write)
- Official docs: https://docs.python.org/3/library/pathlib.html
