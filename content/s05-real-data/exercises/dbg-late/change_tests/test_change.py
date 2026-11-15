import pytest

ns = {"__name__": "__main__"}
exec(open("solution.py").read(), ns)
f = ns["late_rate"]


def D(promised, actual, status="delivered"):
    return {"status": status, "promised_minutes": promised, "actual_minutes": actual}


def test_grace_forgives_small_delays():
    assert f([D(30, 33)], grace=5) == 0.0
    assert f([D(30, 33)]) == 1.0


def test_grace_boundary_is_strict():
    assert f([D(30, 35)], grace=5) == 0.0
    assert f([D(30, 36)], grace=5) == 1.0


def test_mixed_with_grace_and_cancelled():
    orders = [D(30, 31), D(30, 36), D(40, 80), D(40, 44), D(30, 90, "cancelled")]
    assert f(orders, grace=5) == pytest.approx(0.5)


def test_grace_uses_each_orders_own_promise():
    assert f([D(20, 26), D(60, 66)], grace=5) == pytest.approx(1.0)


def test_no_delivered_still_zero():
    assert f([D(30, 90, "cancelled")], grace=5) == 0.0
