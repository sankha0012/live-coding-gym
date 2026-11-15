class IdempotentRunner:
    def __init__(self, func):
        self._func = func
        self._done = {}
        self._err = {}

    def run(self, key, payload):
        if self._done.get(key) is None and key not in self._err:
            try:
                self._done[key] = self._func(payload)
            except Exception as e:
                self._err[key] = e
        if key in self._err:
            raise self._err[key]
        return self._done[key]
