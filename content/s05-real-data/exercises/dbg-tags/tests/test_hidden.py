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
    got = eval("(lambda: (add_tag({}, 'x'), add_tag({}, 'y'))[1])()", ns)
    assert _close(got, eval("['y']", ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('top_restaurants({10: 2, 20: 2, 30: 1}, 2)', ns)
    assert _close(got, eval('[10, 20]', ns)), repr(got)

def test_each_order_keeps_its_own_tags():
    ns = _ns()
    a, b = {"id": 1}, {"id": 2}
    ns["add_tag"](a, "vip")
    ns["add_tag"](b, "new")
    assert a["tags"] == ["vip"] and b["tags"] == ["new"]

def test_ties_by_smaller_id_whatever_the_dict_order():
    ns = _ns()
    f = ns["top_restaurants"]
    assert f({30: 1, 20: 2, 10: 2}, 2) == [10, 20]
    assert f({5: 1, 9: 3, 2: 1, 7: 3}, 3) == [7, 9, 2]
    assert f({4: 1, 2: 1}) == [2, 4]
