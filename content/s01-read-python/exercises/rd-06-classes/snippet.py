class RunningMean:
    def __init__(self, name):
        self.name = name
        self.total = 0.0
        self.count = 0

    def add(self, value):
        self.total += value
        self.count += 1
        return self

    def mean(self):
        if self.count == 0:
            return 0.0
        return self.total / self.count

    def __repr__(self):
        return f"RunningMean({self.name!r}, n={self.count}, mean={self.mean():.2f})"


latency = RunningMean("latency")
latency.add(120).add(80)
print(latency)
other = RunningMean("empty")
print(other)
alias = latency
alias.add(100)
print(latency.count, latency.mean())
