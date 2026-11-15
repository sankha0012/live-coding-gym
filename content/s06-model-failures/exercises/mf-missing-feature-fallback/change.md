Add an optional third parameter `empty_is_missing: bool = False`: `fill_features(row, defaults, empty_is_missing=False)`. When it is `True`, a value that is the empty string `""` also counts as missing and is filled from `defaults`. `0`, `0.0` and `False` are still real values. With it `False` or not given, nothing changes.

For example `fill_features({"city": "", "items": 0}, {"city": "unknown", "items": 1}, empty_is_missing=True)` returns `({"city": "unknown", "items": 0}, ["city"])`.
