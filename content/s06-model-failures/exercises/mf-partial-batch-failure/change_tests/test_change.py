from solution import score_batch


def fn(row):
    if row["price"] < 0:
        raise ValueError("price is negative")
    return row["price"] * 2


def test_fill_example():
    got = score_batch([{"price": 1}, {"price": -5}], fn, fill=0.0)
    assert got == {"scores": [2, 0.0], "errors": [{"index": 1, "reason": "ValueError: price is negative"}]}


def test_fill_zero_is_used_not_ignored():
    got = score_batch([{"price": -1}, {"price": 2}, {}], fn, fill=0)
    assert got["scores"] == [0, 4, 0]
    assert [e["index"] for e in got["errors"]] == [0, 2]


def test_good_scores_never_replaced_by_fill():
    got = score_batch([{"price": 0}, {"price": 3}], fn, fill=-1)
    assert got == {"scores": [0, 6], "errors": []}


def test_string_fill():
    assert score_batch([{"price": -1}], fn, fill="n/a")["scores"] == ["n/a"]


def test_default_fill_still_none():
    assert score_batch([{"price": -1}], fn)["scores"] == [None]
