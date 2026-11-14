def compose(*fns):
    def run(x):
        for f in reversed(fns):
            x = f(x)
        return x
    return run
