from itertools import islice


def process_stream(records, handle_batch, chunk_size, max_errors=None):
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")
    results, errors = [], []
    it = iter(records)
    index = 0
    while True:
        batch = list(islice(it, chunk_size))
        if not batch:
            break
        try:
            results.extend(handle_batch(batch))
        except Exception:
            for offset, record in enumerate(batch):
                try:
                    results.extend(handle_batch([record]))
                except Exception as exc:
                    errors.append(
                        {"index": index + offset, "error": f"{type(exc).__name__}: {exc}"}
                    )
        index += len(batch)
        if max_errors is not None and len(errors) >= max_errors:
            break
    return results, errors
