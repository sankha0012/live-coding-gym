---
title: "tempfile and os: temp files, os.replace, paths"
summary: Create temporary files and folders that clean themselves up, swap files atomically, and build paths safely.
tags: [python, files, os]
---
```python
import os, tempfile
with tempfile.TemporaryDirectory() as tmp:      # folder is deleted at the end of the block
    path = os.path.join(tmp, "data.txt")        # join parts with the right separator
    tmp_path = path + ".tmp"
    with open(tmp_path, "w") as f:
        f.write("hello")
    os.replace(tmp_path, path)                  # rename, overwriting any old file
    os.listdir(tmp)                             # ['data.txt']
os.path.exists(tmp)                             # False
```

- `os.replace(src, dst)` overwrites `dst` in one step. Readers see the old file or the new one, never half.
- `TemporaryDirectory()` and `NamedTemporaryFile()` clean up when the `with` block ends.
- Build paths with `os.path.join` or `pathlib`, never with `+ "/"`.

<!-- more -->

## Details

Path helpers:

```python
os.path.join("data", "out", "a.csv")   # 'data/out/a.csv'   (backslashes on Windows)
os.path.basename("/x/y/a.csv")         # 'a.csv'
os.path.dirname("/x/y/a.csv")          # '/x/y'
os.path.splitext("report.csv")         # ('report', '.csv')
os.path.splitext("a.tar.gz")           # ('a.tar', '.gz')   only the last extension
```

Checks: `os.path.exists(p)`, `os.path.isfile(p)`, `os.path.isdir(p)`, `os.path.getsize(p)`.

Folders and files:

- `os.makedirs(p, exist_ok=True)` creates a folder and its parents, with no error if it is already there.
- `os.listdir(p)` returns names only, in no fixed order. Sort them if order matters.
- `os.remove(p)` deletes a file and raises `FileNotFoundError` if it is missing.
- `os.environ.get("NAME", "default")` reads an environment variable.

A temporary file that must survive the `with` block (to be renamed later) needs `delete=False`. Create it in the same folder as the final file, because `os.replace` is only atomic within one filesystem:

```python
with tempfile.NamedTemporaryFile("w", dir=tmp, suffix=".tmp", delete=False) as f:
    f.write("x")
    name = f.name          # full path of the temp file
os.replace(name, path)
```

`tempfile.mkstemp(dir=...)` is the lower-level version. It returns `(fd, path)` and you must close and delete the file yourself.

In tests, pytest's `tmp_path` fixture gives you a fresh temporary folder as a `pathlib.Path`.

## Common mistakes

- Using a temporary file after its `with` block. It is already deleted unless `delete=False`.
- Writing the temp file in the system temp folder and moving it to another disk. The swap is no longer atomic.
- `os.path.join("data", "/abs")` returns `'/abs'`. A part that starts with a slash throws away everything before it.
- Using `os.rename` to overwrite. It fails on Windows when the target exists. `os.replace` works everywhere.
- Relying on the order of `os.listdir`.

## See also

- [Files and pathlib](#/kb/py-files-pathlib)
- [Atomic file writes](#/kb/prod-atomic-write)
- [Fixtures and tmp_path](#/kb/test-fixtures)
- [Checkpointing and resuming a batch](#/kb/prod-checkpointing)
- Official docs: https://docs.python.org/3/library/tempfile.html
