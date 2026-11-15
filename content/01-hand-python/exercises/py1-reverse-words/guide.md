**Why this matters.** Reversing word order looks trivial, but it hides a classic trap: what counts as a word? If you split on a single space, extra spaces turn into empty pieces and your answer keeps them.

**How we get there.**
1. Turn the sentence into a list of words. `s.split()` with no argument splits on any run of whitespace, so the extra spaces vanish on their own.
2. Reverse that list. `reversed(words)` walks it backwards without making a copy.
3. Glue the words back together with exactly one space: `" ".join(...)`.

Put together, the whole solution is one line: `" ".join(reversed(s.split()))`.

**Check it.** An empty string splits into an empty list, and joining an empty list gives `""`. So the empty case needs no special code. The time cost is linear in the length of the string.

**Watch out.** `split(" ")` looks almost the same but keeps empty pieces. That single character is the difference between passing and failing here.
