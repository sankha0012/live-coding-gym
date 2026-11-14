Write a Python function `score_file(in_path, out_path, model, chunk_size=10_000)` that scores a large CSV in chunks.

Inputs: a CSV with a header and an `id` column, and a `model` object with `predict(rows: list[dict]) -> list[float]` that returns one score per row, in order. `predict` may raise an exception on some batches.

Output: a CSV with columns `id,score,status`. Every input row appears exactly once, in the original order. `status` is `ok` or `failed`. A failed row has an empty score.

Behaviour:
- Read the input as a stream and process `chunk_size` rows at a time. Never load the whole file.
- If `predict` raises, retry that chunk once. If it fails again, split the chunk in halves and score each half, down to single rows. A row that still fails is written as `failed`. The job never aborts because of one bad batch.
- If `predict` returns the wrong number of scores, treat it as a failure of that chunk.
- Return a summary dict `{"rows": n, "ok": n, "failed": n}`.
- Deterministic: no randomness, no sleeping.

Edge cases: an empty file with only a header (write only the header, return zeros), a last chunk smaller than `chunk_size`, and `chunk_size` below 1 (raise ValueError).

Write pytest tests using a fake model that fails on chosen rows: all ok, one poison row in the middle, a wrong-length result, empty file and order preserved. Then explain the memory use and why splitting a failed chunk finds the bad row.
