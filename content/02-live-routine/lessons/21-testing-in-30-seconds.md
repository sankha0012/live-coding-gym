# Testing in 30 seconds

## The problem it solves

You finish the code and say "I think it works". That sentence is worth nothing. Interviewers want to see you prove it, and they want to see it fast. The habit is simple: run one tiny example, then one edge case, and say out loud what you expect before you run them.

It takes about thirty seconds. It catches the off-by-one error that would otherwise show up when the interviewer types their own input.

## The method

1. **Write the expected answer first.** Say it: "For `[1, 2, 3]` I expect `6`." If you write the expected value after you see the output, you will agree with whatever the code printed.
2. **Run the tiny example.** Use an input small enough to check by hand, about three to five items.
3. **Run one edge case.** Pick the one that is most likely to break your code: empty input, one item, all items equal, or a tie.
4. **Say what you saw.** "Matches" or "Not what I expected, let me trace it."

Use plain `print` or `assert` lines in the same file. You do not need a test framework in a live round.

## The smallest runnable example

Take a function that returns the index of the first even number, or -1.

```python
def first_even(nums: list[int]) -> int:
    for i, n in enumerate(nums):
        if n % 2 == 0:
            return i
    return -1


# tiny example: I expect 2, because 4 is the first even number
assert first_even([1, 3, 4, 6]) == 2

# edge case: empty list, I expect -1
assert first_even([]) == -1

print("ok")
```

If an `assert` fails, Python stops and shows the line. That is the right behaviour in an interview: you see the failure, you say "my plan was wrong here", and you trace the example by hand.

Now a slightly bigger case. A moving sum over a window of size `k`:

```python
def window_sums(nums: list[int], k: int) -> list[int]:
    if k <= 0 or k > len(nums):
        return []
    total = sum(nums[:k])
    out = [total]
    for i in range(k, len(nums)):
        total += nums[i] - nums[i - k]
        out.append(total)
    return out


assert window_sums([1, 2, 3, 4], 2) == [3, 5, 7]   # tiny example
assert window_sums([1, 2], 3) == []                # edge: k too big
print("ok")
```

The edge case here is the one the code explicitly guards against. Test the guard, because guards are where bugs hide.

## Which edge case should I pick?

| Problem shape | Good edge case |
|---|---|
| Lists and loops | Empty list, one item |
| Counting or ranking | A tie |
| Search | Not found, and the first or last item |
| Strings | Empty string, extra spaces, mixed case |
| Intervals | Touching intervals, one interval inside another |
| Numbers | Zero, negative, very large |

## Three traps people hit

**Trap 1: testing only the happy path.** Your tiny example works and you stop. The bug lives in the empty input. Always run one edge case, even when you feel sure.

**Trap 2: checking by eye.** Printing a long list and saying "looks right" is not a test. Use `assert` with the expected value you said out loud, so that the computer compares and not you.

**Trap 3: changing the test to fit the code.** When an assert fails, the first suspect is your code, not your expected value. But do check the expected value once by hand. If the test is wrong, say so and fix it. If you silently edit the number until it passes, the interviewer will notice.

## Say it like this

"Let me test this. For the input one, two, three, four with window two, I expect three, five, seven. Running it. That matches. Now an edge case: the window is larger than the list, so I expect an empty list. Running. Good. I did not test negative numbers, but the code only adds and subtracts, so the sign does not change the logic."
