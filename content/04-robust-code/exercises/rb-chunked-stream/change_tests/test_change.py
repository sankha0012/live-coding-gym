from solution import process_stream


def double(batch):
    return [x * 2 for x in batch]


def bad_odd_mod4(batch):
    if any(x % 4 == 1 for x in batch):
        raise KeyError("bad")
    return double(batch)


def test_stops_after_budget_reached():
    res, errs = process_stream(range(10), bad_odd_mod4, 2, max_errors=2)
    assert [e["index"] for e in errs] == [1, 5]
    assert res == [0, 4, 6, 8]


def test_does_not_read_further_chunks():
    pulled = []

    def gen():
        for i in range(10):
            pulled.append(i)
            yield i

    process_stream(gen(), bad_odd_mod4, 2, max_errors=2)
    assert len(pulled) == 6


def test_reaching_chunk_is_fully_handled():
    def h(batch):
        if any(x % 2 == 1 for x in batch):
            raise ValueError("odd")
        return double(batch)

    res, errs = process_stream(range(8), h, 4, max_errors=1)
    assert [e["index"] for e in errs] == [1, 3]
    assert res == [0, 4]


def test_budget_not_reached_runs_everything():
    res, errs = process_stream(range(10), bad_odd_mod4, 2, max_errors=4)
    assert [e["index"] for e in errs] == [1, 5, 9]
    assert res == [0, 4, 6, 8, 12, 14, 16]


def test_default_never_stops():
    res, errs = process_stream(range(10), bad_odd_mod4, 2)
    assert [e["index"] for e in errs] == [1, 5, 9]
    res2, errs2 = process_stream(range(10), bad_odd_mod4, 2, max_errors=None)
    assert (res, errs) == (res2, errs2)
