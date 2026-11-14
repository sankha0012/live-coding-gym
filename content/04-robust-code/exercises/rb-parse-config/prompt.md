A service gets its settings as raw strings (environment variables). Write the class `ConfigError(Exception)` and the function `parse_config(raw: dict[str, str]) -> dict`.

Keys and rules:

- `name`: required, text. Leading and trailing spaces are removed. It must not be empty after that. Missing means the problem `name: missing`.
- `port`: int from 1 to 65535, spaces around the number allowed. Default `8080`.
- `debug`: bool. Accepts `true`, `false`, `1`, `0`, in any letter case, with spaces around. Default `False`.
- `timeout_s`: float, finite and greater than 0, spaces around the number allowed. Default `5.0`.
- `tags`: comma separated text, each item stripped, empty items dropped. Default `[]`.

A key that is absent gets its default. A key that is present but cannot be converted, or is out of range (an empty string counts as present), is a problem `<key>: invalid`. Keys not listed above are ignored.

If there is any problem, raise `ConfigError` once, after checking every key. It has an attribute `problems`: the list of problem strings sorted alphabetically. `str(error)` joins them with `"; "`. Do not change the input dict.

Example: `parse_config({"name": " api ", "port": "99999", "debug": "maybe"})` raises `ConfigError` with `problems == ["debug: invalid", "port: invalid"]`.
