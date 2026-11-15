Let the caller choose which percentiles to report. Change the signature to `percentiles(latencies, ps=(50, 95, 99))`.

- `ps` is a sequence of whole numbers from 1 to 100. The result has one key `"p<number>"` per entry, in the order given, each computed with the same nearest-rank method.
- Called without `ps` it behaves exactly as before.
- An empty `latencies` list gives `None` for every requested key.

Example: `percentiles(list(range(1, 101)), ps=(10, 90))` returns `{"p10": 10, "p90": 90}` and `percentiles([], ps=[75])` returns `{"p75": None}`.
