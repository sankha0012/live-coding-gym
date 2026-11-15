from solution import check_health


def ok():
    return "ok"


def degraded():
    return "degraded"


def down():
    return "down"


def boom():
    raise ConnectionError("db unreachable")


def test_all_ok():
    assert check_health([("model", ok), ("db", ok)]) == {"status": "ok", "reasons": []}


def test_empty_is_ok():
    assert check_health([]) == {"status": "ok", "reasons": []}


def test_degraded():
    out = check_health([("model", ok), ("cache", degraded)])
    assert out == {"status": "degraded", "reasons": ["cache: degraded"]}


def test_worst_wins_regardless_of_order():
    out = check_health([("a", down), ("b", degraded), ("c", ok)])
    assert out["status"] == "down"
    assert out["reasons"] == ["a: down", "b: degraded"]
    out = check_health([("b", degraded), ("a", down)])
    assert out["status"] == "down"


def test_raising_check_is_down_and_others_still_run():
    calls = []

    def last():
        calls.append("last")
        return "degraded"

    out = check_health([("db", boom), ("cache", last)])
    assert out["status"] == "down"
    assert out["reasons"] == ["db: down (raised ConnectionError)", "cache: degraded"]
    assert calls == ["last"]


def test_invalid_result_is_down():
    out = check_health([("x", lambda: True), ("y", lambda: None)])
    assert out["status"] == "down"
    assert out["reasons"] == ["x: down (invalid result)", "y: down (invalid result)"]


def test_unhashable_and_wrong_case_results_are_invalid():
    out = check_health([("x", lambda: []), ("y", lambda: "OK")])
    assert out["status"] == "down"
    assert out["reasons"] == ["x: down (invalid result)", "y: down (invalid result)"]


def test_any_exception_type_is_down_with_its_class_name():
    def bad_key():
        return {}["k"]

    def bad_math():
        return 1 / 0

    def bad_value():
        raise ValueError("nope")

    out = check_health([("a", bad_key), ("b", bad_math), ("c", bad_value), ("d", ok)])
    assert out == {
        "status": "down",
        "reasons": [
            "a: down (raised KeyError)",
            "b: down (raised ZeroDivisionError)",
            "c: down (raised ValueError)",
        ],
    }


def test_each_check_runs_exactly_once():
    calls = []

    def make(name, result):
        def fn():
            calls.append(name)
            return result
        return fn

    check_health([("a", make("a", "degraded")), ("b", make("b", "ok")), ("c", make("c", "down"))])
    assert calls == ["a", "b", "c"]
