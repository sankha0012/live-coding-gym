from solution import Order


def msg(**kw):
    base = dict(order_id="o1", items=2, total=10.5, status="new")
    base.update(kw)
    try:
        Order(**base)
    except ValueError as e:
        return str(e)
    return None


def test_valid_order():
    o = Order("o1", 2, 10.5, "paid")
    assert (o.order_id, o.items, o.total, o.status) == ("o1", 2, 10.5, "paid")
    assert Order("o2", 50, 0, "shipped").total == 0


def test_all_problems_reported_in_order():
    assert msg(order_id="", items=0, total=-1, status="x") == (
        "order_id invalid; items invalid; total invalid; status invalid"
    )


def test_single_problems():
    assert msg(order_id="") == "order_id invalid"
    assert msg(items=51) == "items invalid"
    assert msg(items=1.5) == "items invalid"
    assert msg(status="done") == "status invalid"


def test_nan_and_bool_rejected():
    assert msg(total=float("nan")) == "total invalid"
    assert msg(items=True) == "items invalid"
    assert msg(total=True) == "total invalid"
    assert msg(order_id=None) == "order_id invalid"


def test_boundaries_valid():
    assert msg(items=1) is None
    assert msg(items=50) is None
    assert msg(total=0.0) is None
