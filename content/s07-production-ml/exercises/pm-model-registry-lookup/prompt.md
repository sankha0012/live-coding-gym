A model registry is a list of dicts like `{"name": "eta", "version": "1.10.0", "stage": "production"}`. Write `latest_version(records: list[dict], name: str, stage: str) -> dict` that returns the record with the highest version for that model name in that stage.

- A version is dotted integers such as `"1.9.0"` or `"2.1"`. Compare them as numbers part by part, so `"1.10.0"` is higher than `"1.9.0"`. A shorter version is padded with zeros, so `"2.1"` equals `"2.1.0"`.
- Return the original record dict (not a copy).
- If no record matches the name and stage, or the list is empty, raise `LookupError`.
- If two matching records have the same version, return the first one in the list.
- A record whose version cannot be parsed (for example `"v1"` or `""`) is skipped, it is not an error. If nothing valid is left, raise `LookupError`.
