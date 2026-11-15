A service saves its state as JSON. A crash or a bad value in the middle of a save must never leave a half-written file.

Write `atomic_write_json(path: str, obj) -> None`:

- Write the JSON to a temporary file in the same directory as `path`, then move it over `path` with `os.replace`.
- If anything fails (for example `obj` holds a value `json` cannot serialise), re-raise the original exception, leave the old file at `path` exactly as it was, and leave no temporary file behind.
- If `path` does not exist yet, it is created on success.
- On failure with no existing file, `path` must still not exist.
