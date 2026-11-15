Add an optional second parameter `key: str = "id"`: `dedupe_events(events, key="id")`. It names the field that identifies an event, instead of `"id"`. Two events are duplicates when their `key` values are equal. With `key` not given, nothing changes.

For example `dedupe_events([{"uid": 7, "v": 1}, {"uid": 7, "v": 2}, {"uid": 8, "v": 3}], key="uid")` returns `([{"uid": 7, "v": 1}, {"uid": 8, "v": 3}], 1)`.
