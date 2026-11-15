class IdempotentRunner:
    def __init__(self, func):
        self._func = func
        self._done = {}

    def run(self, key, payload):
        if key and key in self._done:
            result, error = self._done[key]
        else:
            try:
                result, error = self._func(payload), None
            except Exception as e:
                result, error = None, e
            self._done[key] = (result, error)
        if error is not None:
            raise error
        return result
