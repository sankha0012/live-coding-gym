import time

class CircuitBreaker:
    def __init__(self, max_failures=3, cooldown=30, clock=None):
        self.max_failures = max_failures
        self.cooldown = cooldown
        self.clock = clock or time.time
        self.failures = 0
        self.opened_at = None      # None means closed

    def call(self, fn, fallback):
        pass
