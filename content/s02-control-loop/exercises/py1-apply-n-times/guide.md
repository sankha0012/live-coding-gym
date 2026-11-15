**Why this matters.** Applying a function repeatedly is the shape behind retries, simulations and iterative updates. The idea to get right is that each call must receive the previous result, not the original input.

**How we get there.**
1. We need exactly `n` rounds, so we loop with `for _ in range(n)`. The underscore says we do not use the counter.
2. Inside the loop, replace the value with the result of the call: `x = f(x)`. Reassigning `x` is what chains the calls together.
3. After the loop, return `x`.

That is the whole function: a loop, one assignment and a return.

**Check it.** When `n` is 0, `range(0)` is empty, so `f` is never called and `x` comes back untouched, with no special case. We make n calls of `f` and use constant extra space.

**Watch out.** Running the loop `n + 1` or `n - 1` times is the classic off-by-one, and it also changes how many times `f` is called.
