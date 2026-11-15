**Why this matters.** A ranking job has to give the same, correct order on every run. A quiet mistake in the sort key gives a wrong order that is still stable, so nothing crashes and nobody notices.

**How we get there.**
1. Run the tests. Three fail, and all three involve a score of `0` or a negative score.
2. Reproduce with a tiny input: ids `q`, `k`, `m` with scores `0`, `-1.5`, `None`. The expected order is `q`, `k`, `m`. The code returns `k`, `m`, `q`: the zero record falls behind the missing one.
3. Read the key. It is a tuple: first a flag that should mean "score is missing", then the negated score, then the id.
4. Test the flag by hand. `not None` is `True`, which is right. `not 0` is also `True`, which is wrong: zero is a real score.
5. Replace `not r["score"]` with `r["score"] is None`. Run the tests again; all pass.

**Check it.** Keep the zero-score case as a test. Also note the second key part, `-(r["score"] or 0)`: it is fine only because `None` is already pushed last by the first part.

**Next time.** When AI-written code uses `not x`, `if x` or `x or default` on a number, ask whether zero is a valid value.

**Watch out.** Do not fix it by changing the tests. The tests describe the rule from the prompt.
