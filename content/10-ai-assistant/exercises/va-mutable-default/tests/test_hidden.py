from solution import record_event


def test_fresh_list_each_call():
    assert record_event("a") == ["a"]
    assert record_event("b") == ["b"]


def test_results_not_shared():
    first = record_event("a")
    second = record_event("b")
    assert first is not second
    assert first == ["a"]


def test_appends_in_place():
    log = ["x"]
    out = record_event("y", log)
    assert out is log
    assert log == ["x", "y"]


def test_empty_passed_list_is_used():
    log = []
    out = record_event("a", log)
    assert out is log
    assert log == ["a"]
