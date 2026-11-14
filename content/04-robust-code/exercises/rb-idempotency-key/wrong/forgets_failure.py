class IdempotentRunner:
    def __init__(self, func):
        self._func = func
        self._done = {}

    def run(self, key, payload):
        if key not in self._done:
            self._done[key] = self._func(payload)
        return self._done[key]
