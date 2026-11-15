Add an optional keyword argument `level` (default `"ERROR"`) to `parse_logs`. It chooses whose messages go into the second returned list. The counts dict still counts every level, and malformed lines are still skipped.

Example: `parse_logs(["2026-08-01T10:00:00 ERROR disk full", "2026-08-01T10:00:01 WARN slow"], level="WARN")` returns `({"ERROR": 1, "WARN": 1}, ["slow"])`. Called without `level`, the function behaves as before.
