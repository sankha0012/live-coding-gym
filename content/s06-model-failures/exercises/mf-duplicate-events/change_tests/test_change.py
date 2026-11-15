from solution import dedupe_events


def test_custom_key_example():
    ev = [{"uid": 7, "v": 1}, {"uid": 7, "v": 2}, {"uid": 8, "v": 3}]
    assert dedupe_events(ev, key="uid") == ([{"uid": 7, "v": 1}, {"uid": 8, "v": 3}], 1)


def test_id_field_ignored_when_key_given():
    ev = [{"id": 1, "k": "a"}, {"id": 2, "k": "a"}, {"id": 1, "k": "b"}]
    unique, dups = dedupe_events(ev, key="k")
    assert unique == [{"id": 1, "k": "a"}, {"id": 1, "k": "b"}]
    assert dups == 1


def test_falsy_key_values_deduped():
    ev = [{"n": 0}, {"n": ""}, {"n": 0}]
    assert dedupe_events(ev, key="n") == ([{"n": 0}, {"n": ""}], 1)


def test_empty_and_input_untouched():
    assert dedupe_events([], key="uid") == ([], 0)
    ev = [{"uid": 1}, {"uid": 1}]
    dedupe_events(ev, key="uid")
    assert ev == [{"uid": 1}, {"uid": 1}]
