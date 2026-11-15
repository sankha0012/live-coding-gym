def process_stream(records, handle_batch, chunk_size):
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")
    records = list(records)
    results, errors = [], []
    for start in range(0, len(records), chunk_size):
        batch = records[start:start + chunk_size]
        try:
            results.extend(handle_batch(batch))
        except Exception:
            for offset, record in enumerate(batch):
                try:
                    results.extend(handle_batch([record]))
                except Exception as exc:
                    errors.append({"index": start + offset, "error": f"{type(exc).__name__}: {exc}"})
    return results, errors
