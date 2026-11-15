## Contract

`class ConfigError(Exception)` and `parse_config(raw: dict[str, str]) -> dict`.

`raw` maps setting names to strings (environment variables). The result has exactly these keys:

- `name`: str, stripped, not empty. Required.
- `port`: int, 1 to 65535. Default `8080`.
- `debug`: bool from `true`, `false`, `1`, `0` in any letter case. Default `False`.
- `timeout_s`: float, finite and greater than 0. Default `5.0`.
- `tags`: list of str, split on commas, items stripped, empty items dropped, order and duplicates kept. Default `[]`.

Spaces around every value are allowed. A key that is absent gets its default; a key that is present but unconvertible or out of range is invalid, and an empty or blank string counts as present. A missing `name` is `name: missing`; a blank `name` is `name: invalid`. Unlisted keys are ignored and the input dict is never changed.

All keys are checked, then one `ConfigError` is raised. `error.problems` is the alphabetically sorted list of strings like `port: invalid`; `str(error)` joins them with `"; "`.

Example: `{"name": " api ", "port": "99999", "debug": "maybe"}` raises with `problems == ["debug: invalid", "port: invalid"]`.

## Library notes

- `int(s)` returns an int and raises `ValueError` on bad text. It accepts spaces, a sign and underscores (`int("1_0") == 10`), not `"80.5"`.
- `float(s)` returns a float. It happily parses `"nan"` and `"inf"`, so a successful parse is not enough.
- `math.isfinite(x)` returns False for nan and both infinities.
- `str.split(",")` returns a list and keeps empty pieces (`"a,,b"` gives `['a', '', 'b']`), and the pieces keep their spaces.

## Gotchas

- Stopping at the first bad key hides the other problems.
- One default list object reused across calls leaks changes between callers.
- Comparing nan with `<` or `>` is always False, so a range check alone never rejects it.
