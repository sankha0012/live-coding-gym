# When you are stuck

Everyone gets stuck in a live round. The interviewer does not score the moment, they score what you do next. A calm, spoken recovery is a skill you can practise.

## What to do, in order

1. **Say it.** "I am stuck on how to handle ties. Let me think aloud." Silence is the worst option.
2. **Go back to the tiny example.** Solve three items by hand and write each step as a comment. The comments often turn into the code.
3. **Solve a simpler version.** Drop one rule (duplicates, empty input, negatives), get it working, then add the rule back.
4. **Write the slow version.** Correct and slow beats clever and unfinished. Say: "This is O(n squared). When it works I will look for a faster way."
5. **Ask the assistant a narrow question**, not "solve it". For example: "What data structure gives me constant-time lookup of the value I need?" Then read and decide whether it fits.
6. **Ask the interviewer for a hint** after about three minutes. Taking a hint well is a good signal.

## Slow first, then faster

You cannot see how to find two numbers that sum to a target quickly, so write the slow version and say so:

```python
def two_sum_slow(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

assert two_sum_slow([2, 7, 11, 15], 9) == [0, 1]
assert two_sum_slow([], 5) == []
```

Now ask what the inner loop is searching for: the value `target - nums[i]`. A dictionary answers that in one step:

```python
def two_sum(nums, target):
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []

assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 3], 6) == [0, 1]
assert two_sum([], 5) == []
print("ok")
```

You reached the fast version by improving a working one.

## What to say

| Moment | Say |
|---|---|
| No idea | "Let me work a small example by hand." |
| A bug you cannot see | "I will print the values at each step and compare with my hand example." |
| Out of time | "Here is the working slow version. With more time I would use a dictionary." |

## Traps

- Deleting everything instead of finding the one wrong line with a print.
- Refusing a hint, or asking the assistant to write the whole solution, which leaves you unable to explain it.

Related: [The six-step routine](#/kb/iv-routine-six-steps), [Complexity in Python](#/kb/py-complexity).
