from solution import rank


def ids(rs):
    return [(r["id"], r["score"]) for r in rs]


RS = [
    {"id": "b", "score": 2},
    {"id": "a", "score": None},
    {"id": "c", "score": 5},
    {"id": "a", "score": 2},
]


def test_top_two():
    assert ids(rank(RS, limit=2)) == [("c", 5), ("a", 2)]
    assert ids(rank(RS, 3)) == [("c", 5), ("a", 2), ("b", 2)]


def test_limit_zero_and_too_large():
    assert rank(RS, limit=0) == []
    assert ids(rank(RS, limit=10)) == [("c", 5), ("a", 2), ("b", 2), ("a", None)]


def test_limit_none_is_everything():
    assert len(rank(RS, limit=None)) == 4


def test_limit_applies_after_ranking_with_ties_and_none():
    rs = [{"id": "x", "score": None, "n": 0}, {"id": "a", "score": 1, "n": 1},
          {"id": "a", "score": 1, "n": 2}, {"id": "a", "score": 1, "n": 3}]
    assert [r["n"] for r in rank(rs, limit=2)] == [1, 2]
    assert [r["n"] for r in rank(rs, limit=4)] == [1, 2, 3, 0]


def test_input_not_modified_and_new_list():
    rs = list(RS)
    out = rank(rs, limit=2)
    assert rs == RS and out is not rs
    assert rank([], limit=3) == []
