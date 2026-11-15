**Why this matters.** If a service crashes halfway through writing its state file, the next start finds half a JSON document. The fix is to never write to the real file at all: build the new one on the side and swap it in.

**How we get there.**
1. Create a temporary file in the same directory as `path` with `tempfile.mkstemp(dir=...)`. Same directory means same filesystem, which the next step needs.
2. Write the JSON into it, then `flush()` and `os.fsync(...)` so the bytes are really on disk, not only in a buffer.
3. Call `os.replace(tmp, path)`. It is a single rename, so readers see the old file or the new one, never a mix. It also creates `path` if it did not exist.
4. Wrap steps 2 and 3 in `try`. On any failure, `os.unlink(tmp)` (ignoring "already gone") and then a bare `raise`, so the caller still sees the original error.

**Check it.** If `json.dump` fails on an unserialisable value, the target is untouched and no `.tmp` file remains. Cost is one write of the data.

**Watch out.** Opening `path` directly truncates it before the write even starts, and skipping the cleanup leaves stray temp files after every failure.
