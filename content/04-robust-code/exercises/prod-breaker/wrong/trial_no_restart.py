import time

class CircuitBreaker:
    def __init__(self, max_failures=3, cooldown=30, clock=None):
        self.max_failures = max_failures
        self.cooldown = cooldown
        self.clock = clock or time.time
        self.failures = 0
        self.opened_at = None

    def call(self, fn, fallback):
        if self.opened_at is not None and self.clock() - self.opened_at < self.cooldown:
            return fallback
        try:
            result = fn()
        except Exception:
            self.failures += 1
            if self.opened_at is None and self.failures >= self.max_failures:
                self.opened_at = self.clock()
            return fallback
        self.failures, self.opened_at = 0, None
        return result
