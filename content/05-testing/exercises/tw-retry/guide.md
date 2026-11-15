**Why this matters.** Retry logic is about counting: how many calls, how many sleeps, and what happens at the end. The trap is that real sleeping makes tests slow, and wrong counts hide in silence.

**How we get there.**
1. Build a small flaky function that fails a set number of times, then succeeds, and counts its calls. Pass `sleeps.append` as `sleep`, so we record instead of waiting.
2. Test success on the first try: one call, no sleeps.
3. Test success after two failures with three tries: three calls and `sleeps == [1, 1]`.
4. Test that other exception types are retried too, not just one kind.
5. Test all attempts failing. The call count must equal `tries`, and the error from the last attempt must come out, which `pytest.raises(..., match="fail 3")` checks.
6. Check that no sleep happens after the last failure, and cover `tries=1`.

**Check it.** The correct version loops `tries` times, so it never makes more calls than allowed.

**Watch out.** Each buggy version breaks one count: an extra sleep after the end, one attempt too few, or the final error swallowed so the function returns `None`.
