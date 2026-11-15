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

PRE = ''

def _ns():
    ns = {'__name__': '__main__'}
    exec(open('solution.py').read() + '\n\n' + PRE, ns)
    return ns

def test_check_1():
    ns = _ns()
    got = eval("assign([(1, 0, 0), (2, 0, 0)], {'A': (1, 1), 'B': (5, 5)})", ns)
    assert _close(got, eval("{1: 'A', 2: 'B'}", ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('assign([(1, 0, 0)], {})', ns)
    assert _close(got, eval('{1: None}', ns)), repr(got)

def test_check_3():
    ns = _ns()
    got = eval("assign([(1, 0, 0)], {'B': (1, 0), 'A': (0, 1)})", ns)
    assert _close(got, eval("{1: 'A'}", ns)), repr(got)

def test_distance_is_euclidean():
    ns = _ns()
    got = eval("assign([(1, 0, 0)], {'A': (3, 3), 'B': (5, 0)})", ns)
    assert got == {1: 'A'}, repr(got)

def test_orders_processed_in_given_order():
    ns = _ns()
    got = eval("assign([(9, 0, 0), (3, 0, 0)], {'A': (1, 0), 'B': (5, 0)})", ns)
    assert got == {9: 'A', 3: 'B'}, repr(got)

def test_greedy_not_global_matching():
    ns = _ns()
    got = eval("assign([(1, 4, 0), (2, 0, 0)], {'A': (0, 0), 'B': (10, 0)})", ns)
    assert got == {1: 'A', 2: 'B'}, repr(got)

def test_more_orders_than_couriers_and_input_untouched():
    ns = _ns()
    couriers = {'A': (0, 0), 'B': (9, 9)}
    orders = [(1, 0, 0), (2, 0, 0), (3, 0, 0)]
    got = ns['assign'](orders, couriers)
    assert got == {1: 'A', 2: 'B', 3: None}, repr(got)
    assert couriers == {'A': (0, 0), 'B': (9, 9)}
    assert orders == [(1, 0, 0), (2, 0, 0), (3, 0, 0)]
