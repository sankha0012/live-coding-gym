class IdempotentRunner:
    def __init__(self, func):
        self._func = func
        self._done = {}

    def run(self, key, payload):
        if payload not in self._done:
            try:
                self._done[payload] = (self._func(payload), None)
            except Exception as e:
                self._done[payload] = (None, e)
        result, error = self._done[payload]
        if error is not None:
            raise error
        return result
