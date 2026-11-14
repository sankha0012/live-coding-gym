# When you are stuck

## The problem it solves

Everyone gets stuck in a live round. The interviewer does not score whether you got stuck. They score what you do next. Silence for two minutes, a frozen face, or random edits to the code all look bad. A calm, spoken recovery looks good, and it is a skill you can practise.

## What to do, in order

1. **Say it.** "I am stuck on how to handle the ties. Let me think out loud." Silence is the worst option. Speaking keeps the interviewer on your side and lets them help.
2. **Go back to the tiny example.** Take three items and solve them by hand. Write each step you do as a comment. Most of the time, your hands already know the algorithm and the comments become the code.
3. **Solve a simpler version.** Drop one rule. No duplicates, no empty input, only positive numbers. Get that working, then add the rule back.
4. **Write the slow version.** Two nested loops that are correct beat a clever idea that is not finished. Say: "This is O(n squared). Once it works, I will look for a faster way."
5. **Ask for a hint, after about three minutes.** Be specific: "Would a dictionary help me here?" Taking a hint well is scored. Say thanks, use it, and keep going.

## The smallest runnable example

You must find two numbers that add up to a target and you cannot see the fast way. Write the slow version first and say so:

```python
def two_sum_slow(nums: list[int], target: int) -> list[int]:
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []


assert two_sum_slow([2, 7, 11, 15], 9) == [0, 1]
assert two_sum_slow([], 5) == []
print("slow works")
```

Now ask "what am I looking up in the inner loop?" The answer is "the number `target - nums[i]`". A lookup is what a dictionary does well:

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, n in enumerate(nums):
        if target - n in seen:
            return [seen[target - n], i]
        seen[n] = i
    return []


assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 3], 6) == [0, 1]
assert two_sum([], 5) == []
print("fast works")
```

You reached the fast version by improving a working one, not by waiting for an idea. That is the pattern: working first, faster second.

## What to say in common stuck moments

| Moment | What to say |
|---|---|
| No idea at all | "Let me work through a small example by hand first." |
| Idea, but not sure it is right | "My plan is X. Let me check it on this example." |
| Forgot a method name | "I do not remember the exact name. The idea is to count items, so I will use Counter and check the docs name after." |
| Bug you cannot find | "I will print the values at each step and compare with my hand example." |
| Out of time | "Here is the working slow version. With more time I would use a dictionary to make it O(n)." |

## Three traps people hit

**Trap 1: going silent.** You think hard for four minutes without a word. The interviewer cannot tell if you are close or lost. Narrate, even if you only say "I am comparing two options".

**Trap 2: rewriting everything.** Panic makes you delete the code and start again. Instead, find the one line that is wrong with a print statement or a hand trace. A small fix is faster than a rewrite.

**Trap 3: refusing help.** Some learners think a hint means failure. It does not. A hint taken well, with a short "that makes sense, so I can use a dictionary", is a positive signal. Refusing it and staying stuck is a negative one.

## Say it like this

"I am stuck on the fast approach, so I will write the simple version with two loops first. It is O(n squared) but it is correct, and I can test it. Once it passes my example, I will ask myself what the inner loop is searching for, and see if a dictionary can answer that in one step. If I am still stuck after that, I will ask you for a hint."
