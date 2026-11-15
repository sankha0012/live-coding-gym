def _close(a, b):
    return abs(a - b) <= 1e-6 + 1e-9 * abs(b)

def _ns():
    ns = {'__name__': '__main__'}
    exec(open('solution.py').read(), ns)
    return ns

def test_larger_eps_for_zero_bin():
    psi = _ns()['psi']
    assert _close(round(psi([0.5, 0.5], [1.0, 0.0], eps=0.01), 4), 2.2635)

def test_eps_applies_to_expected_too():
    psi = _ns()['psi']
    assert _close(round(psi([0.0, 1.0], [0.5, 0.5], eps=0.01), 4), 2.2635)

def test_eps_leaves_nonzero_bins_alone():
    psi = _ns()['psi']
    assert _close(round(psi([0.25, 0.25, 0.5], [0.2, 0.3, 0.5], eps=0.01), 4), 0.0203)

def test_default_eps_unchanged():
    psi = _ns()['psi']
    assert _close(round(psi([0.5, 0.5], [1.0, 0.0]), 3), 4.604)
    assert _close(round(psi([0.5, 0.5], [1.0, 0.0], eps=0.0001), 3), 4.604)
