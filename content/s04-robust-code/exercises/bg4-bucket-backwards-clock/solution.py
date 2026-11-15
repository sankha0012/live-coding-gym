class TokenBucket:
    def __init__(self, capacity, refill_per_s, clock):
        if capacity <= 0 or refill_per_s <= 0:
            raise ValueError("capacity and refill_per_s must be > 0")
        self.capacity = capacity
        self.rate = refill_per_s
        self.clock = clock
        self.tokens = float(capacity)
        self.last = clock()

    def allow(self, cost=1):
        now = self.clock()
        elapsed = max(0.0, now - self.last)
        self.last = now
        self.tokens = min(self.capacity, self.tokens + elapsed * self.rate)
        if cost > self.tokens:
            return False
        self.tokens -= cost
        return True
