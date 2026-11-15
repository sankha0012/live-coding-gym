def _close(a, b):
    if isinstance(a, bool) or isinstance(b, bool):
        return a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= 1e-6 + 1e-9 * abs(b)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_close(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return set(a) == set(b) and all(_close(a[k], b[k]) for k in a)
    return a == b

PRE = 'ORDERS = [\n    {"city": "SP", "status": "delivered", "subtotal": 50.0, "fee": 5.0},\n    {"city": "SP", "status": "cancelled", "subtotal": 30.0, "fee": 5.0},\n    {"city": "RJ", "status": "delivered", "subtotal": None, "fee": 7.5},\n    {"city": "RJ", "status": "delivered", "subtotal": 20.0, "fee": 0.0},\n]\n'

def _ns():
    ns = {'__name__': '__main__'}
    exec(open('solution.py').read() + '\n\n' + PRE, ns)
    return ns

def test_check_1():
    ns = _ns()
    got = eval('gmv_by_city(ORDERS)', ns)
    assert _close(got, eval("{'SP': 55.0, 'RJ': 27.5}", ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('gmv_by_city([])', ns)
    assert _close(got, eval('{}', ns)), repr(got)

def test_rounded_to_two_decimals_exactly():
    ns = _ns()
    orders = [{"city": "SP", "status": "delivered", "subtotal": 0.1, "fee": 0.0} for _ in range(3)]
    got = ns['gmv_by_city'](orders)
    assert got == {'SP': 0.3}, repr(got)

def test_city_with_only_cancelled_orders_is_absent():
    ns = _ns()
    orders = [
        {"city": "SP", "status": "cancelled", "subtotal": 9.0, "fee": 1.0},
        {"city": "RJ", "status": "delivered", "subtotal": 4.0, "fee": 1.0},
    ]
    got = ns['gmv_by_city'](orders)
    assert got == {'RJ': 5.0}, repr(got)

def test_sums_several_orders_per_city():
    ns = _ns()
    orders = [{"city": "SP", "status": "delivered", "subtotal": s, "fee": 1.0} for s in (10.0, None, 5.0)]
    got = ns['gmv_by_city'](orders)
    assert got == {'SP': 18.0}, repr(got)
