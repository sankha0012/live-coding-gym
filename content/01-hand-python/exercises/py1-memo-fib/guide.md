**Why this matters.** The naive Fibonacci recursion recomputes the same values again and again and takes exponential time. Remembering results fixes that, and here the memory is a dict that lives across calls.

**How we get there.**
1. The base cases come first: for `n < 2`, the answer is `n` itself, and we never store it.
2. For larger `n`, look in `cache` before doing any work: `if n not in cache`.
3. Only on a miss, compute `fib(n - 1, cache) + fib(n - 2, cache)` and store it in `cache[n]`. We pass the same `cache` down, so every level shares one memory.
4. Return `cache[n]`.

**Check it.** Each `n` from 2 up is computed once, so time and memory are linear, and a second call with the same dict stores nothing new. Recursion goes `n` deep, which is fine for 90.

**Watch out.** Resetting `cache = {}` inside the function, or leaving `cache` out of the recursive calls while doing so, throws the memory away, and the run goes back to exponential time: `fib(90)` never finishes. A mutable default like `{}` is a trap in most code; here it is deliberate.
