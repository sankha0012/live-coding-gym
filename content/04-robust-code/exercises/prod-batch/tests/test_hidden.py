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
