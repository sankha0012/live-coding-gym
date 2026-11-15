from solution import final_state


def ev(i, entity, ts, state):
    return {"id": i, "entity": entity, "ts": ts, "state": state}


def test_deleted_last_removes_entity():
    events = [ev("1", "a", 1, "new"), ev("2", "a", 2, "deleted"), ev("3", "b", 1, "new")]
    assert final_state(events) == {"b": "new"}


def test_only_deleted_entities_gives_empty():
    assert final_state([ev("1", "a", 1, "deleted")]) == {}


def test_older_deleted_does_not_remove():
    events = [ev("1", "a", 5, "paid"), ev("2", "a", 2, "deleted")]
    assert final_state(events) == {"a": "paid"}


def test_recreated_after_delete_stays():
    events = [ev("1", "a", 1, "new"), ev("2", "a", 2, "deleted"), ev("3", "a", 3, "new")]
    assert final_state(events) == {"a": "new"}


def test_out_of_order_delete_arrives_late_still_wins_by_ts():
    events = [ev("3", "a", 3, "deleted"), ev("1", "a", 1, "new"), ev("2", "a", 2, "paid")]
    assert final_state(events) == {}


def test_tie_and_duplicates_with_delete():
    events = [ev("1", "a", 4, "paid"), ev("2", "a", 4, "deleted")]
    assert final_state(events) == {}
    events = [ev("2", "a", 4, "deleted"), ev("1", "a", 4, "paid")]
    assert final_state(events) == {"a": "paid"}
    events = [ev("1", "a", 4, "paid"), ev("2", "a", 5, "deleted"), ev("2", "a", 5, "new")]
    assert final_state(events) == {}
    events = [ev("2", "a", 5, "new"), ev("2", "a", 5, "deleted")]
    assert final_state(events) == {"a": "new"}
