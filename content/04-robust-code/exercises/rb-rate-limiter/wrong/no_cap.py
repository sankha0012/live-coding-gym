class TokenBucket:
    def __init__(self, capacity, refill_per_s, clock):
        if capacity <= 0 or refill_per_s <= 0:
            raise ValueError
        self.capacity, self.rate, self.clock = capacity, refill_per_s, clock
        self.tokens = float(capacity)
        self.last = clock()

    def allow(self, cost=1):
        now = self.clock()
        self.tokens += max(0.0, now - self.last) * self.rate
        self.last = now
        if cost > self.tokens:
            return False
        self.tokens -= cost
        return True
