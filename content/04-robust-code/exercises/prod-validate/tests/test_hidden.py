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

PRE = 'SCHEMA = {"distance_km": ("float", 0.0, 50.0, 3.0), "items": ("int", 1, 30, 1), "hour": ("int", 0, 23, 12)}'

def _ns():
    ns = {'__name__': '__main__'}
    exec(open('solution.py').read() + '\n\n' + PRE, ns)
    return ns

def test_check_1():
    ns = _ns()
    got = eval("validate({'distance_km': 2.5, 'items': 3, 'hour': 20}, SCHEMA)", ns)
    assert _close(got, eval("({'distance_km': 2.5, 'items': 3, 'hour': 20}, [])", ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval("validate({'distance_km': 'abc', 'items': 100, 'promo': 1}, SCHEMA)", ns)
    assert _close(got, eval("({'distance_km': 3.0, 'items': 30, 'hour': 12}, ['bad_type:distance_km', 'clipped:items', 'extra:promo', 'missing:hour'])", ns)), repr(got)

def test_check_3():
    ns = _ns()
    got = eval("validate({'distance_km': float('nan'), 'items': '4', 'hour': -1}, SCHEMA)", ns)
    assert _close(got, eval("({'distance_km': 3.0, 'items': 4, 'hour': 0}, ['clipped:hour', 'missing:distance_km'])", ns)), repr(got)
