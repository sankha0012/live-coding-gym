def compose(*fns):
    fns = list(fns)
    def run(x):
        while fns:
            x = fns.pop()(x)
        return x
    return run
