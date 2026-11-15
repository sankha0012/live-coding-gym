import pytest

ns = {"__name__": "__main__"}
exec(open("solution.py").read(), ns)
f = ns["average_delivery_minutes"]


def D(m, status="delivered"):
    return {"status": status, "actual_minutes": m}


def test_large_values_dropped():
    assert f([D(20), D(30), D(400)], max_minutes=60) == pytest.approx(25.0)


def test_value_equal_to_cap_stays():
    assert f([D(20), D(30), D(400)], max_minutes=30) == pytest.approx(25.0)


def test_nothing_left_is_none():
    assert f([D(20), D(30), D(400)], max_minutes=10) is None


def test_cap_with_cancelled_and_missing():
    got = f([D(10), D(None), D(500, "cancelled"), D(40), D(90)], max_minutes=50)
    assert got == pytest.approx(25.0)


def test_default_keeps_everything():
    assert f([D(20), D(30), D(400)]) == pytest.approx(150.0)
    assert f([D(20), D(30), D(400)], max_minutes=None) == pytest.approx(150.0)
