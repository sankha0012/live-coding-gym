SERVER_LATENCY = 45.0  # seconds the stuck upstream takes to answer


def fake_get(url, timeout=None):
    """Simulates an HTTP GET without sleeping; returns (payload, seconds_waited)."""
    if timeout is not None and SERVER_LATENCY > timeout:
        raise TimeoutError(f"no answer from {url} within {timeout}s")
    return {"score": 0.9}, SERVER_LATENCY


def score_blocking(user_id):
    payload, waited = fake_get(f"https://ranker.internal/{user_id}")
    return payload["score"], waited


def score_with_timeout(user_id, timeout=1.0, default=0.5):
    try:
        payload, waited = fake_get(f"https://ranker.internal/{user_id}", timeout=timeout)
        return payload["score"], waited
    except TimeoutError:
        return default, timeout


score, waited = score_blocking("u1")
print(f"blocking: score={score} waited={waited}s")
score, waited = score_with_timeout("u1")
print(f"with timeout: score={score} waited={waited}s")
budget = 100 * 1.0  # a 100-user batch has a budget of 1 second per user
print("100 users, blocking:", 100 * SERVER_LATENCY, "s vs budget", budget, "s")
print("100 users, timeout:", 100 * 1.0, "s")
