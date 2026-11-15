from solution import check_health


def ok():
    return "ok"


def degraded():
    return "degraded"


def down():
    return "down"


def boom():
    raise OSError("x")


def test_strict_turns_degraded_into_down():
    out = check_health([("cache", degraded)], strict=True)
    assert out == {"status": "down", "reasons": ["cache: degraded"]}


def test_strict_mixed_checks_keep_reasons():
    out = check_health([("a", ok), ("b", degraded), ("c", ok), ("d", degraded)], strict=True)
    assert out == {"status": "down", "reasons": ["b: degraded", "d: degraded"]}


def test_strict_with_only_ok_stays_ok():
    assert check_health([("a", ok), ("b", ok)], strict=True) == {"status": "ok", "reasons": []}
    assert check_health([], strict=True) == {"status": "ok", "reasons": []}


def test_strict_with_real_failures_is_unchanged():
    out = check_health([("a", down), ("b", boom), ("c", degraded)], strict=True)
    assert out == {
        "status": "down",
        "reasons": ["a: down", "b: down (raised OSError)", "c: degraded"],
    }


def test_not_strict_is_still_degraded():
    assert check_health([("cache", degraded)], strict=False)["status"] == "degraded"
    assert check_health([("cache", degraded)])["status"] == "degraded"
