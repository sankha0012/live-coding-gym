def compose(*fns):
    def run(x):
        for f in fns:
            x = f(x)
        return x
    return run
