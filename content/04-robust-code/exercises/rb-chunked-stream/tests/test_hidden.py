from solution import process_stream


def double(batch):
    return [x * 2 for x in batch]


def bad_on_three(batch):
    if 3 in batch:
        raise ValueError("three")
    return [x * 2 for x in batch]


def test_happy_path_and_batch_sizes():
    sizes = []

    def h(batch):
        sizes.append(len(batch))
        return double(batch)

    res, errs = process_stream(range(7), h, 3)
    assert res == [0, 2, 4, 6, 8, 10, 12]
    assert errs == []
    assert sizes == [3, 3, 1]


def test_empty_input():
    assert process_stream([], double, 4) == ([], [])


def test_is_lazy():
    pulled = []

    def gen():
        for i in range(10):
            pulled.append(i)
            yield i

    seen = []

    def h(batch):
        seen.append(len(pulled))
        return double(batch)

    process_stream(gen(), h, 4)
    assert seen == [4, 8, 10]


def test_isolates_failing_record():
    res, errs = process_stream(range(6), bad_on_three, 3)
    assert res == [0, 2, 4, 8, 10]
    assert errs == [{"index": 3, "error": "ValueError: three"}]


def test_does_not_stop_and_keeps_global_index():
    def h(batch):
        if any(x % 4 == 1 for x in batch):
            raise KeyError("odd")
        return double(batch)

    res, errs = process_stream(range(10), h, 5)
    assert [e["index"] for e in errs] == [1, 5, 9]
    assert res == [0, 4, 6, 8, 12, 14, 16]
    assert all(e["error"].startswith("KeyError") for e in errs)


def test_bad_chunk_size():
    for n in (0, -1):
        try:
            process_stream([1], double, n)
            assert False
        except ValueError:
            pass


def test_retry_is_one_record_at_a_time():
    calls = []

    def h(batch):
        calls.append(list(batch))
        if 3 in batch and len(batch) > 1:
            raise ValueError("batch")
        return double(batch)

    res, errs = process_stream(range(4), h, 4)
    assert res == [0, 2, 4, 6] and errs == []
    assert calls == [[0, 1, 2, 3], [0], [1], [2], [3]]


def test_bad_chunk_size_even_for_empty_input():
    for n in (0, -1, -5):
        for recs in ([], iter([]), [1, 2]):
            try:
                process_stream(recs, double, n)
                assert False, (n, recs)
            except ValueError:
                pass


def test_single_record_batch_is_retried_alone():
    calls = []

    def flaky(batch):
        calls.append(list(batch))
        if len(calls) % 2 == 1:
            raise RuntimeError("first try fails")
        return double(batch)

    res, errs = process_stream([5, 6], flaky, 1)
    assert res == [10, 12] and errs == []
    assert calls == [[5], [5], [6], [6]]


def test_error_message_keeps_exception_text():
    def h(batch):
        if "bad" in batch:
            raise ValueError("bad: record, really")
        return batch

    res, errs = process_stream(["a", "bad", "b", "c"], h, 2)
    assert res == ["a", "b", "c"]
    assert errs == [{"index": 1, "error": "ValueError: bad: record, really"}]
