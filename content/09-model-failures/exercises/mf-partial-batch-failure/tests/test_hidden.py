from solution import score_batch


def fn(row):
    if row["price"] < 0:
        raise ValueError("price is negative")
    return row["price"] * 2


def test_all_good():
    got = score_batch([{"price": 1}, {"price": 2}], fn)
    assert got == {"scores": [2, 4], "errors": []}


def test_bad_row_does_not_sink_batch():
    rows = [{"price": 1}, {"price": -5}, {"price": 3}]
    got = score_batch(rows, fn)
    assert got["scores"] == [2, None, 6]
    assert got["errors"] == [{"index": 1, "reason": "ValueError: price is negative"}]


def test_order_and_length_preserved():
    rows = [{"price": -1}, {"price": 5}, {"price": -2}, {"price": 7}]
    got = score_batch(rows, fn)
    assert got["scores"] == [None, 10, None, 14]
    assert [e["index"] for e in got["errors"]] == [0, 2]


def test_missing_key_is_reported_not_raised():
    got = score_batch([{"price": 1}, {}], fn)
    assert got["scores"] == [2, None]
    assert got["errors"][0]["index"] == 1
    assert got["errors"][0]["reason"].startswith("KeyError")


def test_empty():
    assert score_batch([], fn) == {"scores": [], "errors": []}


def test_zero_score_is_kept():
    assert score_batch([{"price": 0}], fn) == {"scores": [0], "errors": []}
