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


def test_fractional_scores_are_not_rounded():
    rs = [{"id": "a", "score": 2.2}, {"id": "z", "score": 2.9}, {"id": "m", "score": 2.5}, {"id": "b", "score": 3}]
    assert ids(rank(rs)) == [("b", 3), ("z", 2.9), ("m", 2.5), ("a", 2.2)]
    rs = [{"id": "b", "score": 2.0}, {"id": "a", "score": 2}]
    assert ids(rank(rs)) == [("a", 2), ("b", 2.0)]
    rs = [{"id": "x", "score": -0.5}, {"id": "y", "score": -0.2}, {"id": "w", "score": -3}]
    assert ids(rank(rs)) == [("y", -0.2), ("x", -0.5), ("w", -3)]


def test_records_themselves_are_not_modified():
    import copy
    rs = [{"id": "b", "score": 1}, {"id": "a", "score": None}, {"id": "c", "score": 7}]
    before = copy.deepcopy(rs)
    out = rank(rs)
    assert rs == before
    assert all(set(r) == {"id", "score"} for r in out)
    assert all(set(r) == {"id", "score"} for r in rs)


def test_repeated_ids_are_all_kept():
    rs = [{"id": "a", "score": 1, "n": 0}, {"id": "a", "score": 5, "n": 1}, {"id": "a", "score": 1, "n": 2},
          {"id": "a", "score": None, "n": 3}, {"id": "a", "score": None, "n": 4}]
    assert [r["n"] for r in rank(rs)] == [1, 0, 2, 3, 4]


def test_mixed_ties_everything_at_once():
    rs = [
        {"id": "b", "score": 3, "n": 0}, {"id": "a", "score": None, "n": 1}, {"id": "a", "score": 3, "n": 2},
        {"id": "b", "score": 3, "n": 3}, {"id": "c", "score": 0, "n": 4}, {"id": "a", "score": None, "n": 5},
        {"id": "a", "score": 3, "n": 6},
    ]
    assert [r["n"] for r in rank(rs)] == [2, 6, 0, 3, 4, 1, 5]
