PRE = 'SCHEMA = {"distance_km": ("float", 0.0, 50.0, 3.0), "items": ("int", 1, 30, 1), "hour": ("int", 0, 23, 12)}'


def _ns():
    ns = {'__name__': '__main__'}
    exec(open('solution.py').read() + '\n\n' + PRE, ns)
    return ns


def test_keep_extra_copies_unknown_fields():
    ns = _ns()
    row = {'distance_km': 2.5, 'items': 3, 'hour': 20, 'promo': 'x', 'zone': 7}
    clean, issues = ns['validate'](row, ns['SCHEMA'], keep_extra=True)
    assert clean == {'distance_km': 2.5, 'items': 3, 'hour': 20, 'promo': 'x', 'zone': 7}
    assert issues == ['extra:promo', 'extra:zone']


def test_keep_extra_still_cleans_schema_fields():
    ns = _ns()
    clean, issues = ns['validate']({'distance_km': 'abc', 'items': 100, 'promo': 1}, ns['SCHEMA'], keep_extra=True)
    assert clean == {'distance_km': 3.0, 'items': 30, 'hour': 12, 'promo': 1}
    assert issues == ['bad_type:distance_km', 'clipped:items', 'extra:promo', 'missing:hour']


def test_default_and_false_drop_extra():
    ns = _ns()
    row = {'distance_km': 1.0, 'items': 2, 'hour': 3, 'promo': 1}
    want = ({'distance_km': 1.0, 'items': 2, 'hour': 3}, ['extra:promo'])
    assert ns['validate'](row, ns['SCHEMA']) == want
    assert ns['validate'](row, ns['SCHEMA'], keep_extra=False) == want


def test_keep_extra_does_not_modify_input():
    ns = _ns()
    row = {'distance_km': 'abc', 'promo': 1, 'hour': None}
    before = dict(row)
    ns['validate'](row, ns['SCHEMA'], keep_extra=True)
    assert row == before
