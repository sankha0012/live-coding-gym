class IdempotentRunner:
    _done = {}  # key -> (result, error)

    def __init__(self, func):
        self._func = func

    def run(self, key, payload):
        if key not in self._done:
            try:
                self._done[key] = (self._func(payload), None)
            except Exception as e:
                self._done[key] = (None, e)
        result, error = self._done[key]
        if error is not None:
            raise error
        return result
