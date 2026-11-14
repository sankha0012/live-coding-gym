from solution import dedupe_events


def test_no_duplicates():
    ev = [{"id": 1}, {"id": 2}]
    assert dedupe_events(ev) == ([{"id": 1}, {"id": 2}], 0)


def test_keeps_first_and_counts():
    ev = [{"id": "a", "v": 1}, {"id": "b", "v": 2}, {"id": "a", "v": 3}, {"id": "a", "v": 4}]
    unique, dups = dedupe_events(ev)
    assert unique == [{"id": "a", "v": 1}, {"id": "b", "v": 2}]
    assert dups == 2


def test_order_preserved():
    ev = [{"id": i} for i in (5, 3, 5, 9, 3, 1)]
    unique, dups = dedupe_events(ev)
    assert [e["id"] for e in unique] == [5, 3, 9, 1]
    assert dups == 2


def test_empty():
    assert dedupe_events([]) == ([], 0)


def test_input_not_modified():
    ev = [{"id": 1}, {"id": 1}]
    dedupe_events(ev)
    assert ev == [{"id": 1}, {"id": 1}]


def test_same_id_different_type_is_different():
    unique, dups = dedupe_events([{"id": 1}, {"id": "1"}])
    assert len(unique) == 2 and dups == 0
