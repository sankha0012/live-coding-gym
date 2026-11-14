def fib(n, cache={}):
    if n < 2:
        return n
    if n not in cache:
        cache[n] = fib(n - 1, cache) + fib(n - 2, cache)
    return cache[n]
