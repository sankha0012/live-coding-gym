def _ns():
    ns = {"__name__": "__main__"}
    exec(open("solution.py").read(), ns)
    return ns


MSGS = [("system", "be brief"), ("user", "hi there"),
        ("assistant", "hello how can I help"), ("user", "refund my order please")]


def test_reserve_shrinks_budget():
    f = _ns()["trim_history"]
    assert f(MSGS, 11, reserve=2) == [("system", "be brief"), ("user", "refund my order please")]
    assert f(MSGS, 11, reserve=0) == [("system", "be brief"), ("assistant", "hello how can I help"),
                                      ("user", "refund my order please")]


def test_reserve_exactly_fits():
    f = _ns()["trim_history"]
    assert f(MSGS, 8, reserve=2) == [("system", "be brief"), ("user", "refund my order please")]
    assert f(MSGS, 8, reserve=3) == [("system", "be brief")]


def test_system_kept_even_with_big_reserve():
    f = _ns()["trim_history"]
    assert f(MSGS, 5, reserve=10) == [("system", "be brief")]
