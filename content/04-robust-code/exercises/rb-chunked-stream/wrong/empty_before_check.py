from itertools import islice


def process_stream(records, handle_batch, chunk_size):
    results, errors = [], []
    it = iter(records)
    first = list(islice(it, 1))
    if not first:
        return results, errors
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")
    from itertools import chain
    it = chain(first, it)
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
    return results, errors
