---
title: Atomic file writes
summary: Write to a temp file in the same folder, then os.replace it over the target, so readers never see half a file.
tags: [production, files]
---
```python
import os, tempfile

def atomic_write(path, text):
    folder = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=folder)      # same folder = same filesystem
    try:
        with os.fdopen(fd, "w") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())                # bytes are on disk before the rename
        os.replace(tmp, path)                   # readers see old or new, never half
    except BaseException:
        os.unlink(tmp)
        raise
```

- Use it for state files, checkpoints, model artifacts and config that another process reads.
- Key rule: build the full content in a temp file, then swap it in with one `os.replace`.
- Say: "The rename is atomic, so a crash leaves the old file or the new one, never a mix."

<!-- more -->

## Details

`open(path, "w")` truncates the file first. A crash, or a serialisation error in the middle, leaves it empty or cut off. The temp-and-replace pattern never touches the target until the new content is complete.

```python
import pathlib

d = pathlib.Path(tempfile.mkdtemp())
atomic_write(d / "state.txt", "v1")
try:
    atomic_write(d / "state.txt", None)     # f.write(None) raises TypeError
except TypeError:
    pass
(d / "state.txt").read_text()               # 'v1'  the old content is untouched
[p.name for p in d.iterdir()]               # ['state.txt']  no temp file left behind
```

Why each step is there:

- **Same directory.** A rename is atomic only inside one filesystem. A temp file in `/tmp` may be on another disk.
- **`os.replace`, not `os.rename`.** `replace` overwrites an existing target on every platform.
- **`fsync`.** Without it the rename can reach the disk before the data, and a power loss leaves an empty new file.
- **Cleanup.** On any failure the temp file is removed and the original error is re-raised.

For JSON, serialise to a string first with `json.dumps`. Then a value that cannot be serialised fails before any file is opened.

Atomic does not mean safe for two writers. The last `replace` wins. Use a lock if writers can overlap.

## Common mistakes

- Creating the temp file in the system temp folder, on a different filesystem from the target.
- Using a fixed temp name such as `path + ".tmp"` when two writers can run at once.
- Leaving the temp file behind when the write fails.
- Catching the error during cleanup and not re-raising it.
- Calling `os.replace` while the temp file is still open and not flushed.

## See also

- [tempfile and os: temp files, os.replace, paths](#/kb/py-tempfile-os)
- [Files and pathlib](#/kb/py-files-pathlib)
- [Checkpointing and resuming a batch](#/kb/prod-checkpointing)
