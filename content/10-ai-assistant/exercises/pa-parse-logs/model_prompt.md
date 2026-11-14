Write a Python function `summarise_logs(lines: Iterable[str]) -> dict` for inference logs.

Line format: `<ISO timestamp> <LEVEL> model=<name> latency_ms=<int> status=<int>`, for example `2026-11-02T10:15:03Z INFO model=ranker-v2 latency_ms=41 status=200`. Fields after the level are `key=value` pairs and may appear in any order.

Output: a dict with `models` and `bad_lines`. `models` maps each model name to `{"count": int, "errors": int, "p50_latency_ms": float, "max_latency_ms": int}`. A request is an error when status is 500 or more. Use the median for p50, computed with the standard library. `bad_lines` is the number of lines skipped.

Edge cases: blank lines are ignored and not counted as bad. A line with a missing model, latency or status, a non-numeric latency or status, or a negative latency is bad: count it and skip it, never raise. Extra unknown fields are ignored. Models with only bad lines do not appear. The input can be a generator, so read it once and do not load it all into a list unless needed for the median. Output must be deterministic: sort model names.

Write pytest tests for: a normal set, shuffled field order, a malformed line, an empty input, a generator input and a model with an even number of requests. Standard library only. Then explain the time and memory cost and what changes if the log is 50 GB.
