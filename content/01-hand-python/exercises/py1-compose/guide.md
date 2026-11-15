**Why this matters.** Composition builds a pipeline out of small functions. The details are the order, which is right to left like the maths `f(g(x))`, and that the result must keep working after the first call.

**How we get there.**
1. `compose(*fns)` collects the functions into a tuple and returns an inner function `run(x)`. This is a closure: `run` remembers `fns`.
2. Inside `run`, walk the functions from last to first with `reversed(fns)`. The last function is applied first.
3. Feed each result into the next call: `x = f(x)`.
4. Return `x` at the end.

**Check it.** With no functions the loop never runs, so the input comes back unchanged, which is exactly the identity. The cost is k calls for k functions. Note that we call `reversed(fns)` inside `run`, so every call to the composed function gets a fresh walk.

**Watch out.** Calling `reversed(fns)` outside `run` stores a one-shot iterator, so the second call to the composed function silently does nothing. Looping left to right gets the order wrong.
