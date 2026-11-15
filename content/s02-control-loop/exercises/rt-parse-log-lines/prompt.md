Each log line looks like `"2026-08-01T10:00:00 ERROR message text"`: a timestamp, a level, then the message, separated by spaces. The message may contain spaces.

Write `parse_logs(lines: list[str]) -> tuple[dict, list]` that returns two things:
1. a dict mapping each level to how many lines had that level,
2. the list of messages from `ERROR` lines, in input order.

A line is malformed if it has fewer than three space-separated parts. Skip malformed lines completely. An empty list returns `({}, [])`.

Example: `parse_logs(["2026-08-01T10:00:00 ERROR disk full", "bad line", "2026-08-01T10:00:01 INFO ok"])` returns `({"ERROR": 1, "INFO": 1}, ["disk full"])`.
