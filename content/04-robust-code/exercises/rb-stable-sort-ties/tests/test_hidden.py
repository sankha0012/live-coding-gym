from solution import rank


def ids(rs):
    return [(r["id"], r["score"]) for r in rs]


def test_example():
    rs = [
        {"id": "b", "score": 2},
        {"id": "a", "score": None},
        {"id": "c", "score": 5},
        {"id": "a", "score": 2},
    ]
    assert ids(rank(rs)) == [("c", 5), ("a", 2), ("b", 2), ("a", None)]


def test_none_last_and_ties_by_id():
    rs = [{"id": "z", "score": None}, {"id": "m", "score": None}, {"id": "q", "score": 0}, {"id": "k", "score": -1.5}]
    assert ids(rank(rs)) == [("q", 0), ("k", -1.5), ("m", None), ("z", None)]


def test_full_ties_keep_input_order():
    rs = [{"id": "a", "score": 1, "n": i} for i in range(5)]
    assert [r["n"] for r in rank(rs)] == [0, 1, 2, 3, 4]
    rs = [{"id": "a", "score": None, "n": i} for i in range(4)]
    assert [r["n"] for r in rank(rs)] == [0, 1, 2, 3]


def test_input_not_modified():
    rs = [{"id": "b", "score": 1}, {"id": "a", "score": 2}]
    before = list(rs)
    out = rank(rs)
    assert rs == before and rs[0]["id"] == "b"
    assert out is not rs


def test_empty():
    assert rank([]) == []


def test_zero_score_is_not_none():
    rs = [{"id": "a", "score": None}, {"id": "b", "score": 0}]
    assert ids(rank(rs)) == [("b", 0), ("a", None)]
