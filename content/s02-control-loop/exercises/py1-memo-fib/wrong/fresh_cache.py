def fib(n, cache={}):
    cache = {}
    if n < 2:
        return n
    if n not in cache:
        cache[n] = fib(n - 1) + fib(n - 2)
    return cache[n]
