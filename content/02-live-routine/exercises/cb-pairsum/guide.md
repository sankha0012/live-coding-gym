**Why this matters.** "Do two numbers add to a target?" is the most common warm-up in interviews. Checking every pair works but costs O(n squared); the insight is to ask the question per number instead.
**How we get there.**
1. Parse the text. Split on `"|"` into the numbers and the target, then `split(",")` the numbers and convert each with `int`.
2. Think about one number `x`. A partner exists only if `target - x` is another number in the list.
3. Keep a `seen` set of numbers we have already walked past. Membership in a set is fast, so each check is cheap.
4. For each `x`, first test `target - x in seen`. If yes, return `"true"`.
5. Only then add `x` to `seen`. If nothing matched by the end, return `"false"`.
**Check it.** `4,4|8` is true because the second 4 finds the first one in `seen`. `4|8` is false because the lone 4 is not in `seen` when we ask. One pass gives O(n) time and O(n) space for the set.
**Watch out.** Adding `x` before checking lets a number pair with itself, which wrongly accepts `4|8`.
