from solution import final_state


def ev(i, entity, ts, state):
    return {"id": i, "entity": entity, "ts": ts, "state": state}


def test_in_order():
    events = [ev("1", "a", 1, "new"), ev("2", "a", 2, "paid"), ev("3", "b", 1, "new")]
    assert final_state(events) == {"a": "paid", "b": "new"}


def test_out_of_order_uses_event_time():
    events = [ev("2", "a", 5, "shipped"), ev("1", "a", 2, "new"), ev("3", "a", 4, "paid")]
    assert final_state(events) == {"a": "shipped"}


def test_exact_duplicate_ignored():
    events = [ev("1", "a", 1, "new"), ev("2", "a", 2, "paid"), ev("1", "a", 1, "new")]
    assert final_state(events) == {"a": "paid"}


def test_tie_later_wins_after_dedupe():
    events = [ev("1", "a", 1, "x"), ev("2", "a", 1, "y"), ev("1", "a", 1, "x")]
    assert final_state(events) == {"a": "y"}


def test_tie_between_distinct_events():
    events = [ev("1", "a", 3, "x"), ev("2", "a", 3, "y")]
    assert final_state(events) == {"a": "y"}


def test_empty_and_input_not_modified():
    assert final_state([]) == {}
    events = [ev("2", "a", 2, "b"), ev("1", "a", 1, "a")]
    snapshot = [dict(e) for e in events]
    final_state(events)
    assert events == snapshot


def test_duplicate_id_keeps_first_even_if_different():
    events = [ev("1", "a", 1, "x"), ev("1", "a", 9, "z")]
    assert final_state(events) == {"a": "x"}
