from itertools import islice


def process_stream(records, handle_batch, chunk_size):
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
        except Exception as exc:
            errors.append({"index": index, "error": f"{type(exc).__name__}: {exc}"})
        index += len(batch)
    return results, errors
