def _ns():
    ns = {"__name__": "__main__"}
    exec(open("solution.py").read(), ns)
    return ns


DOCS = {"a": [1, 0], "b": [0, 1], "c": [1, 1]}


def test_min_score_filters():
    f = _ns()["top_k"]
    assert f([1, 0], DOCS, 3, min_score=0.5) == ["a", "c"]
    assert f([1, 0], DOCS, 3, min_score=0.9) == ["a"]
    assert f([1, 0], DOCS, 3, min_score=1.1) == []


def test_k_still_applies_after_filter():
    f = _ns()["top_k"]
    assert f([1, 0], DOCS, 1, min_score=0.5) == ["a"]


def test_equal_to_threshold_is_kept():
    f = _ns()["top_k"]
    assert f([1, 0], {"x": [1, 0], "y": [0, 1]}, 2, min_score=0.0) == ["x", "y"]
    assert f([1, 0], {"x": [1, 0], "y": [0, 1]}, 2, min_score=1.0) == ["x"]


def test_default_unchanged():
    f = _ns()["top_k"]
    assert f([1, 0], DOCS, 3) == ["a", "c", "b"]
