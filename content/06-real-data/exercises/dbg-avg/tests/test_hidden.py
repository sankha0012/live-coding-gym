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

PRE = 'O = [\n    {"status": "delivered", "actual_minutes": 25},\n    {"status": "delivered", "actual_minutes": 35},\n    {"status": "cancelled", "actual_minutes": None},\n]'

def _ns():
    ns = {'__name__': '__main__'}
    exec(open('solution.py').read() + '\n\n' + PRE, ns)
    return ns

def test_check_1():
    ns = _ns()
    got = eval('average_delivery_minutes(O)', ns)
    assert _close(got, eval('30.0', ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('average_delivery_minutes([])', ns)
    assert _close(got, eval('None', ns)), repr(got)

def test_check_3():
    ns = _ns()
    got = eval('average_delivery_minutes([O[2]])', ns)
    assert _close(got, eval('None', ns)), repr(got)
