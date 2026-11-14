class DriftAlert:
    def __init__(self, high, low):
        if low > high:
            raise ValueError("bad")
        self.high, self.low, self.active = high, low, False

    def update(self, score):
        new = score > self.high
        event = None
        if new and not self.active:
            event = "raised"
        elif not new and self.active:
            event = "cleared"
        self.active = new
        return event
