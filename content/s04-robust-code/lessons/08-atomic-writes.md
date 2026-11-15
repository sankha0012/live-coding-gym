# Atomic writes

## What it is

An atomic write changes a file so that any reader, and any crash, sees either the complete old content or the complete new content, never a mixture. The standard recipe is to write the new content to a temporary file in the same folder, flush it to disk, then swap it into place with `os.replace`, which is atomic on the same filesystem. See [Atomic file writes](#/kb/prod-atomic-write), [Checkpointing](#/kb/prod-checkpointing) and [Temporary files](#/kb/py-tempfile-os).

## How it breaks in production

`open(path, "w")` truncates the file immediately. If the process is killed, the disk fills, or the serialisation raises halfway, you are left with an empty or half-written file, and that file is often the model artifact, the checkpoint or the config that the next job loads. A reader that opens the file while it is being written sees partial JSON and crashes. The failure is rare, so it passes every test and shows up once in production. Temporary files on a different filesystem break the guarantee, because `os.replace` across filesystems fails. And skipping the flush means a power loss can leave the renamed file empty.

## The defence in code

```python
import os
import tempfile


def atomic_write(path, text):
    folder = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=folder)      # same folder, same filesystem
    try:
        with os.fdopen(fd, "w") as f:
            f.write(text)
            f.flush()
            os.fsync(f.fileno())                # bytes on disk before the swap
        os.replace(tmp, path)                   # old or new, never half
    except BaseException:
        os.unlink(tmp)                          # no stray temp file
        raise


with tempfile.TemporaryDirectory() as d:
    target = os.path.join(d, "state.json")
    atomic_write(target, '{"v": 1}')
    try:
        atomic_write(target, None)              # fails inside f.write
    except TypeError:
        pass
    assert open(target).read() == '{"v": 1}'    # the old content survived
    assert os.listdir(d) == ["state.json"]      # and no temp file is left
    print(open(target).read())
```

The test forces a failure in the middle of the write and checks two things: the previous content is intact and the folder holds no leftovers. That is the whole contract. Use the same pattern for checkpoints, so a restart resumes from a complete file.

## What to say in the interview

"I never write important files in place. I write to a temporary file in the same folder, flush and fsync, then use os.replace, so a crash leaves the old file or the new one but never half of it. On any error I delete the temporary file and re-raise. I test it by making the write fail halfway and checking that the old content is still there."
