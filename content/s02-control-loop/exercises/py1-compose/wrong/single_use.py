def compose(*fns):
    order = reversed(fns)

    def run(x):
        for f in order:
            x = f(x)
        return x
    return run
