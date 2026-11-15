**Why this matters.** Time is an input, and real clocks are not perfectly monotonic. A limiter has to behave sensibly when time jumps.

**How we get there.**
1. Run the tests. One fails: `test_clock_going_backwards`.
2. Reproduce with the fake clock: `capacity=2`, start at time 10, `allow(2)` is `True` and empties the bucket. Move the clock to 5 and print `b.tokens` after `allow()`. It is negative, about `-5`.
3. Read the refill line: `self.tokens + (now - self.last) * self.rate`. With `now=5` and `last=10` the elapsed time is `-5`.
4. At time 6 the elapsed time is `+1`, but the bucket starts from `-4`, so the call is still denied. The test expects `True`.
5. Fix: `elapsed = max(0.0, now - self.last)`, keep `self.last = now`. Run the tests again.

**Check it.** The next refill is measured from the lower time, so one second later the bucket has exactly one token.

**Next time.** Whenever the code subtracts two timestamps, ask what happens if the result is negative.

**Watch out.** Do not skip updating `self.last` when the clock goes back, or the bucket will keep ignoring real time that passes afterwards.
