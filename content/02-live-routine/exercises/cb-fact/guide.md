**Why this matters.** The math is easy; the surprise is the input. On this kind of platform `input()` hands you the text `"4"`, not the number 4, and multiplying text gives nonsense or an error.
**How we get there.**
1. Convert first: `n = int(num)`. Everything after this works on a real number.
2. Start a running product at `result = 1`. One is the neutral value for multiplication, and it also makes `1!` correct without special code.
3. Loop `for i in range(2, n + 1)` and multiply `result *= i`. We start at 2 because multiplying by 1 changes nothing, and we stop at `n + 1` because `range` excludes its end.
4. Return `result`. For `4` that is 1 times 2 times 3 times 4, which is 24.
**Check it.** For `1` the range is empty, so we return 1, which is right. With num up to 18 the answer fits comfortably, and Python integers would not overflow anyway. The loop runs n times, so it is O(n) time and O(1) space.
**Watch out.** Skipping `int()` is the classic slip: `range(2, num + 1)` fails on a string, and that is exactly the habit this warm-up trains.
