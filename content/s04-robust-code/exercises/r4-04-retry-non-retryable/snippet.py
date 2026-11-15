class BadRequest(Exception): pass  # the server says our payload is invalid (HTTP 400)
calls = {"n": 0}

def score_api(payload):
    calls["n"] += 1
    if "user_id" not in payload:
        raise BadRequest("missing field: user_id")
    return {"score": 0.8}

def call_with_retry(fn, payload, attempts=3, retry_on=(Exception,)):
    delays = []
    for attempt in range(attempts):
        try:
            return fn(payload), delays
        except retry_on as exc:
            if attempt == attempts - 1:
                return f"gave up: {exc}", delays
            delays.append(0.5 * 2 ** attempt)  # would be time.sleep(...)

result, delays = call_with_retry(score_api, {"item": 7})
print(result)
print("calls:", calls["n"], "delays:", delays)
calls["n"] = 0
try:
    call_with_retry(score_api, {"item": 7}, retry_on=(TimeoutError, ConnectionError))
except BadRequest as exc:
    print(f"raised at once: {exc}")
print("calls:", calls["n"])
