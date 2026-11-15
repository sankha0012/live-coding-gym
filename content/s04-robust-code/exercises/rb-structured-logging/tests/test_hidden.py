import pytest

from solution import make_record


def test_basic():
    got = make_record("info", "order_paid", {"order_id": 7}, lambda: 100.0)
    assert got == {"level": "info", "event": "order_paid", "ts": 100.0, "order_id": 7}


def test_none_fields_and_clock_called_once():
    calls = []

    def clock():
        calls.append(1)
        return 5

    got = make_record("error", "boom", None, clock)
    assert got == {"level": "error", "event": "boom", "ts": 5}
    assert len(calls) == 1


def test_reserved_keys_rejected():
    for key in ("level", "event", "ts"):
        with pytest.raises(ValueError) as e:
            make_record("info", "x", {key: "hacked"}, lambda: 1)
        assert key in str(e.value)


def test_bad_level_and_event():
    for level in ("INFO", "fatal", "", None):
        with pytest.raises(ValueError):
            make_record(level, "x", {}, lambda: 1)
    for event in ("", None, 5):
        with pytest.raises(ValueError):
            make_record("info", event, {}, lambda: 1)


def test_fields_not_modified_and_new_dict():
    f = {"a": 1}
    out = make_record("debug", "x", f, lambda: 1)
    assert f == {"a": 1}
    out["a"] = 2
    assert f == {"a": 1}


def test_real_values_win_when_no_collision():
    out = make_record("warning", "slow", {"level_name": "x", "ms": 12}, lambda: 3)
    assert out["level"] == "warning" and out["level_name"] == "x" and out["ms"] == 12


def test_key_order_is_level_event_ts_then_fields():
    out = make_record("info", "x", {"b": 1, "a": 2}, lambda: 9)
    assert list(out) == ["level", "event", "ts", "b", "a"]
    assert list(make_record("info", "x", None, lambda: 9)) == ["level", "event", "ts"]


def test_falsy_values_and_zero_clock_are_kept():
    calls = []

    def clock():
        calls.append(1)
        return 0

    out = make_record("debug", "x", {"a": 0, "b": None, "c": "", "d": [], "e": False}, clock)
    assert out == {"level": "debug", "event": "x", "ts": 0, "a": 0, "b": None, "c": "", "d": [], "e": False}
    assert len(calls) == 1


def test_only_exact_reserved_names_are_rejected():
    out = make_record("info", "x", {"Level": 1, "EVENT": 2, "timestamp": 3, "ts_ms": 4}, lambda: 7)
    assert out == {"level": "info", "event": "x", "ts": 7, "Level": 1, "EVENT": 2, "timestamp": 3, "ts_ms": 4}


def test_reserved_key_never_overwrites_and_does_not_alter_fields():
    f = {"ts": 1, "a": 2}
    with pytest.raises(ValueError) as e:
        make_record("info", "x", f, lambda: 5)
    assert "ts" in str(e.value)
    assert f == {"ts": 1, "a": 2}
    f2 = {}
    make_record("info", "x", f2, lambda: 5)
    assert f2 == {}
