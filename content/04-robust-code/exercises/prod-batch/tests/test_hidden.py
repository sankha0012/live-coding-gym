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

PRE = 'def MODEL(row):\n    if row["x"] is None:\n        raise ValueError("missing x")\n    if row["x"] < 0:\n        return float("nan")\n    return 2.0 * row["x"]\n\nROWS = [{"id": 1, "x": 1.5}, {"id": 2, "x": None}, {"id": 3, "x": -1}, {"id": 4, "x": 0}]'

def _ns():
    ns = {'__name__': '__main__'}
    exec(open('solution.py').read() + '\n\n' + PRE, ns)
    return ns

def test_check_1():
    ns = _ns()
    got = eval('predict_batch(ROWS, MODEL, 10.0)', ns)
    assert _close(got, eval("([{'id': 1, 'pred': 3.0, 'status': 'ok'}, {'id': 2, 'pred': 10.0, 'status': 'fallback'}, {'id': 3, 'pred': 10.0, 'status': 'fallback'}, {'id': 4, 'pred': 0.0, 'status': 'ok'}], 0.5)", ns)), repr(got)

def test_check_2():
    ns = _ns()
    got = eval('predict_batch([], MODEL, 10.0)', ns)
    assert _close(got, eval('([], 0.0)', ns)), repr(got)


def test_inf_none_and_other_exceptions():
    ns = _ns()
    f = ns['predict_batch']
    def model(row):
        k = row["k"]
        if k == "inf": return float("inf")
        if k == "ninf": return float("-inf")
        if k == "none": return None
        if k == "type": raise TypeError("bad")
        if k == "key": return row["missing"]
        if k == "neg": return -2.5
        return 7
    rows = [{"id": i, "k": k} for i, k in enumerate(["inf", "ninf", "none", "type", "key", "neg", "ok"])]
    res, rate = f(rows, model, -1)
    assert [r["status"] for r in res] == ["fallback"] * 5 + ["ok", "ok"]
    assert [r["pred"] for r in res] == [-1] * 5 + [-2.5, 7]
    assert [r["id"] for r in res] == list(range(7))
    assert abs(rate - 5 / 7) < 1e-9


def test_rate_all_good_all_bad_and_zero_fallback():
    ns = _ns()
    f = ns['predict_batch']
    rows = [{"id": i} for i in range(4)]
    res, rate = f(rows, lambda r: 1.0, 0.0)
    assert rate == 0.0 and all(r["status"] == "ok" for r in res)
    res, rate = f(rows, lambda r: float("nan"), 0.0)
    assert rate == 1.0 and [r["pred"] for r in res] == [0.0] * 4
    assert all(r["status"] == "fallback" for r in res)
    res, rate = f(rows, lambda r: None if r["id"] == 0 else 1.0, 0.0)
    assert abs(rate - 0.25) < 1e-9
