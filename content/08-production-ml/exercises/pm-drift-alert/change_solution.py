class DriftAlert:
    def __init__(self, high: float, low: float):
        if low > high:
            raise ValueError("low must not be greater than high")
        self.high = high
        self.low = low
        self.active = False
        self.raised_count = 0

    def update(self, score: float):
        if not self.active and score > self.high:
            self.active = True
            self.raised_count += 1
            return "raised"
        if self.active and score < self.low:
            self.active = False
            return "cleared"
        return None
