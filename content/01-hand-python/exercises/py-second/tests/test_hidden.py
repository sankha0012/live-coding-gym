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
    got = eval('second_highest([5, 1, 5, 3])', ns)
    assert _close(got, eval('3', ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('second_highest([7, 7])', ns)
    assert _close(got, eval('None', ns)), repr(got)

def test_check_3():
    ns = _ns()
    got = eval('second_highest([])', ns)
    assert _close(got, eval('None', ns)), repr(got)

def test_second_highest_not_second_lowest():
    ns = _ns()
    assert ns['second_highest']([1, 2, 3, 10]) == 3

def test_negative_values():
    ns = _ns()
    assert ns['second_highest']([-5, -3, -9]) == -5

def test_zero_is_a_valid_answer():
    ns = _ns()
    assert ns['second_highest']([0, 5]) == 0
    assert ns['second_highest']([5, 0, 0]) == 0

def test_input_not_mutated():
    ns = _ns()
    vals = [1, 9, 3]
    ns['second_highest'](vals)
    assert vals == [1, 9, 3]
