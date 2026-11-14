from solution import rank


def test_score_desc():
    recs = [{"name": "a", "score": 1}, {"name": "b", "score": 3}, {"name": "c", "score": 2}]
    assert [r["name"] for r in rank(recs)] == ["b", "c", "a"]


def test_ties_by_name():
    recs = [{"name": "zed", "score": 5}, {"name": "amy", "score": 5}, {"name": "bob", "score": 5}]
    assert [r["name"] for r in rank(recs)] == ["amy", "bob", "zed"]


def test_mixed():
    recs = [{"name": "b", "score": 2}, {"name": "a", "score": 2}, {"name": "c", "score": 9}]
    assert [r["name"] for r in rank(recs)] == ["c", "a", "b"]


def test_empty_and_no_mutation():
    assert rank([]) == []
    recs = [{"name": "b", "score": 1}, {"name": "a", "score": 2}]
    copy = list(recs)
    rank(recs)
    assert recs == copy


def test_negative_scores_and_returns_new_list():
    recs = [{"name": "b", "score": -1}, {"name": "a", "score": -1}, {"name": "c", "score": -5}, {"name": "d", "score": 0}]
    out = rank(recs)
    assert [r["name"] for r in out] == ["d", "a", "b", "c"]
    assert out is not recs
