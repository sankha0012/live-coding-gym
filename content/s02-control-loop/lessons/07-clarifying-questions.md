# Clarifying questions

Interview prompts are short on purpose. "Return the top three words" hides decisions: what counts as a word, what happens on ties, what if there are fewer than three, and in what format the answer comes back. Guessing may solve the wrong problem quickly. Two minutes of questions is cheap, and it is the easiest part of the round to score well on.

## The five questions

1. **Input.** Type, size, odd values (None, negatives, mixed case, extra spaces)?
2. **Empty or tiny.** Return an empty result, a default, or raise?
3. **Ties and duplicates.** Which wins? Does order of equal items matter?
4. **Output.** Type and order? A list or a dict? Sorted? Indices or values?
5. **Limits.** Is O(n log n) fine? Can I change the input in place?

Ask specific questions. "Any edge cases?" makes the interviewer do your work; "If two words tie, should I sort them alphabetically?" gets a one-word answer. If the answer is "your choice", pick the simple option and say it aloud.

## Write the answers down

Put each answer into the file as a comment. They become part of the spec, and part of the prompt for the assistant:

```python
# words: split on whitespace, lowercase
# ties: alphabetical
# fewer than k words: return all of them
# empty text: return []
```

Now the assistant gets a prompt with decisions in it, and you can check its answer against the comments. Here is the code those answers lead to:

```python
from collections import Counter

def top_words(text: str, k: int) -> list[tuple[str, int]]:
    counts = Counter(text.lower().split())
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ordered[:k]

assert top_words("b a b A c", 2) == [("a", 2), ("b", 2)]
assert top_words("", 3) == []
assert top_words("x", 3) == [("x", 1)]
print("ok")
```

The sort key is the tie rule, the slice handles "fewer than k", and the empty string gives an empty counter. A trap here: `Counter.most_common(k)` on equal counts keeps first-seen order, not alphabetical order, so it would not match the rule you were given.

## Traps

- **Vague questions** that cost you time and give you nothing.
- **Asking, then ignoring the answers.** Check the code against your comments before you say you are done.
- **Asking for ten minutes.** Five questions is the limit; if the interviewer is happy with your assumptions, move on.

## What you say

"Before I code: can the input contain None? If two words tie, should I break the tie alphabetically? If there are fewer than k words, do I return what I have? I will write those rules as comments."

Related: [The six-step routine](#/kb/iv-routine-six-steps), [Counter and defaultdict](#/kb/py-counter-defaultdict).
