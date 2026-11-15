def _ns():
    ns = {"__name__": "__main__"}
    exec(open("solution.py").read(), ns)
    return ns


def test_drops_short_last_chunk():
    f = _ns()["chunk_words"]
    assert f("a b c d e", 2, 0, drop_short=True) == ["a b", "c d"]
    assert f("a b c d e f", 4, 1, drop_short=True) == ["a b c d"]


def test_nothing_full_gives_empty():
    f = _ns()["chunk_words"]
    assert f("a b", 5, 2, drop_short=True) == []
    assert f("", 3, 1, drop_short=True) == []


def test_full_chunks_and_default_unchanged():
    f = _ns()["chunk_words"]
    assert f("a b c d e", 2, 1, drop_short=True) == ["a b", "b c", "c d", "d e"]
    assert f("a b c d e", 2, 0) == ["a b", "c d", "e"]
