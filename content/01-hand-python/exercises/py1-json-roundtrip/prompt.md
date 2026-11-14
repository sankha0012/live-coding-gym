Write two functions.

`to_json(data: dict) -> str` returns JSON text with keys sorted at every level and compact separators (no spaces): `{"b": 1, "a": 2}` gives `'{"a":2,"b":1}'`.

`from_json(text: str)` parses JSON text and returns the Python value. If the text is not valid JSON (including an empty string), return `None`.
