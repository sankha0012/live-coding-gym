from functools import reduce
def compose(*fns):
    return lambda x: reduce(lambda acc, f: f(acc), fns, x)
