class DriftAlert:
    def __init__(self, high, low):
        if low > high:
            raise ValueError("bad")
        self.high, self.low, self.active = high, low, False

    def update(self, score):
        if score > self.high:
            self.active = True
            return "raised"
        if score < self.low:
            self.active = False
            return "cleared"
        return None
