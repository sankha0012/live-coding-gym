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

PRE = 'EV = [\n    {"event_id": "e1", "order_id": 7, "ts": 10, "status": "created"},\n    {"event_id": "e3", "order_id": 7, "ts": 30, "status": "delivered"},\n    {"event_id": "e2", "order_id": 7, "ts": 20, "status": "picked_up"},\n    {"event_id": "e3", "order_id": 7, "ts": 30, "status": "delivered"},\n    {"event_id": "e5", "order_id": 8, "ts": 5, "status": "created"},\n    {"event_id": "e4", "order_id": 8, "ts": 5, "status": "cancelled"},\n]'

def _ns():
    ns = {'__name__': '__main__'}
    exec(open('solution.py').read() + '\n\n' + PRE, ns)
    return ns

def test_check_1():
    ns = _ns()
    got = eval('apply_events(EV)', ns)
    assert _close(got, eval("({7: 'delivered', 8: 'created'}, 1)", ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('apply_events([])', ns)
    assert _close(got, eval('({}, 0)', ns)), repr(got)

def test_check_3():
    ns = _ns()
    got = eval('apply_events(list(reversed(EV)))', ns)
    assert _close(got, eval("({7: 'delivered', 8: 'created'}, 1)", ns)), repr(got)


def test_tie_breaks_by_event_id_not_status_or_arrival():
    ns = _ns()
    f = ns['apply_events']
    a = {"event_id": "e9", "order_id": 1, "ts": 50, "status": "alpha"}
    b = {"event_id": "e2", "order_id": 1, "ts": 50, "status": "zulu"}
    c = {"event_id": "e5", "order_id": 1, "ts": 50, "status": "mid"}
    for evs in ([a, b, c], [b, c, a], [c, b, a], [a, c, b]):
        assert f(evs) == ({1: "alpha"}, 0), evs


def test_many_duplicates_counted_each_time():
    ns = _ns()
    f = ns['apply_events']
    e1 = {"event_id": "x1", "order_id": 1, "ts": 1, "status": "a"}
    e2 = {"event_id": "x2", "order_id": 2, "ts": 2, "status": "b"}
    res, dupes = f([e1, e1, e2, dict(e1), e2, e1])
    assert res == {1: "a", 2: "b"} and dupes == 4
    assert f([e1, e2]) == ({1: "a", 2: "b"}, 0)
