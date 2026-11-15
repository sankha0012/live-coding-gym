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
    got = eval('check_batch([10, 11, 9, 10], 10, 2)', ns)
    assert _close(got, eval('[]', ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('check_batch([10, None, 11, None], 10, 2)', ns)
    assert _close(got, eval("['null_rate']", ns)), repr(got)

def test_check_3():
    ns = _ns()
    got = eval('check_batch([20] * 25, 10, 2)', ns)
    assert _close(got, eval("['mean_shift']", ns)), repr(got)

def test_check_4():
    ns = _ns()
    got = eval('check_batch([], 10, 2)', ns)
    assert _close(got, eval("['empty']", ns)), repr(got)

def test_check_5():
    ns = _ns()
    got = eval("check_batch([None, float('nan')], 10, 2)", ns)
    assert _close(got, eval("['null_rate']", ns)), repr(got)

def test_check_6():
    ns = _ns()
    got = eval('check_batch([20] * 10 + [None] * 5, 10, 2)', ns)
    assert _close(got, eval("['mean_shift', 'null_rate']", ns)), repr(got)

def test_nan_counts_as_missing_for_null_rate():
    ns = _ns()
    got = eval("check_batch([10, 10, 10, 10, float('nan')], 10, 2)", ns)
    assert _close(got, ['null_rate']), repr(got)

def test_nan_does_not_poison_the_mean():
    ns = _ns()
    got = eval("check_batch([20] * 10 + [float('nan')], 10, 2)", ns)
    assert _close(got, ['mean_shift', 'null_rate']), repr(got)

def test_threshold_uses_standard_error_of_valid_values():
    ns = _ns()
    assert _close(eval('check_batch([12] * 25, 10, 2)', ns), ['mean_shift'])
    # 4 valid values among 100: allowed gap is 3*2/sqrt(4)=3, so a gap of 2 is fine
    assert _close(eval('check_batch([12] * 4 + [None] * 96, 10, 2)', ns), ['null_rate'])

def test_shift_below_reference():
    ns = _ns()
    assert _close(eval('check_batch([0] * 25, 10, 2)', ns), ['mean_shift'])

def test_missing_values_not_treated_as_zero_in_mean():
    ns = _ns()
    got = eval('check_batch([10] * 8 + [None] * 2, 10, 1)', ns)
    assert _close(got, ['null_rate']), repr(got)

def test_null_rate_equal_to_limit_is_ok():
    ns = _ns()
    assert _close(eval('check_batch([10, 10, 10, None], 10, 2, max_null_rate=0.25)', ns), [])

def test_max_null_rate_parameter_is_used():
    ns = _ns()
    assert _close(eval('check_batch([10, None, 10, 10], 10, 2, max_null_rate=0.5)', ns), [])
    assert _close(eval('check_batch([10, None, 10, 10], 10, 2, max_null_rate=0.1)', ns), ['null_rate'])

def test_z_parameter_is_used():
    ns = _ns()
    assert _close(eval('check_batch([11] * 25, 10, 2)', ns), [])
    assert _close(eval('check_batch([11] * 25, 10, 2, z=0.5)', ns), ['mean_shift'])

def test_gap_equal_to_limit_is_ok():
    ns = _ns()
    assert _close(eval('check_batch([13] * 4, 10, 2)', ns), [])
