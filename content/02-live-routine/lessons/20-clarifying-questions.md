# Clarifying questions

## The problem it solves

Most live-coding prompts are short on purpose. "Return the top three words" hides at least four decisions: what is a word, what about ties, what if there are fewer than three, and in what order should the answer come back. If you guess, you may solve the wrong problem fast. If you ask, you show the interviewer that you think like an engineer who ships code to production.

Spend two minutes on questions. It is not wasted time. It is the part of the round that is easiest to score well on, and it makes the code part shorter.

## The five questions

Ask these five, in this order, for almost every problem.

1. **Input.** What type is it, how big can it get, and can it contain odd values (None, negatives, mixed case, extra spaces)?
2. **Empty or tiny.** What should happen for empty input or a single item? Return an empty result, a default, or raise?
3. **Ties and duplicates.** If two items are equal, which wins? Is order of equal items important?
4. **Output.** What type and order do you want back? A list or a dict? Sorted? Indices or values?
5. **Limits.** Is O(n log n) fine, or should it be O(n)? Can I use extra memory? Can I change the input in place?

Here is how the answers sound for three common problem types.

| Problem type | Question | A sample answer you can accept |
|---|---|---|
| Counting words | What is a word? | Split on whitespace, lowercase, keep punctuation as is |
| Counting words | Ties in top k? | Break ties alphabetically |
| Two sum | Duplicates in the list? | Yes, but use each index once |
| Two sum | No pair found? | Return an empty list |
| Intervals | Do touching intervals merge? | Yes, [1,2] and [2,3] become [1,3] |
| Intervals | Is the input sorted? | No, sort it first |
| Strings | Case matters? | No, ignore case |
| Search | First or any match? | The first index |

If the interviewer says "your choice", pick the simple option and say it: "I will assume ties go alphabetically. I will note it in a comment."

## The smallest runnable example

Here is "top k words" after the questions were answered: words are split on whitespace and lowercased, ties go alphabetically, fewer than k words returns all of them, and the result is a list of `(word, count)`.

```python
from collections import Counter


def top_words(text: str, k: int) -> list[tuple[str, int]]:
    counts = Counter(text.lower().split())
    ordered = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return ordered[:k]


print(top_words("b a b A c", 2))   # [('a', 2), ('b', 2)]
print(top_words("", 3))            # []
```

Every answer you got is visible in the code. The sort key encodes the tie rule. The slice handles "fewer than k". The empty string gives an empty counter. When the contract is clear, the code is small.

## Three traps people hit

**Trap 1: asking vague questions.** "Any edge cases?" makes the interviewer do your work. Ask a specific one instead: "If two words have the same count, should I sort them alphabetically?" A specific question can be answered in one word.

**Trap 2: asking and not using the answers.** You ask about ties, hear "alphabetical", and then write `most_common(k)`, which keeps insertion order for ties. Write the answers down as comments at the top of the file and check them against the code before you say you are done.

**Trap 3: asking for ten minutes.** Five questions is the limit. If the interviewer is happy with your assumptions, stop asking and start the tiny example. Interviewers are scoring the round, and silence while you wait for a perfect spec is also a signal.

## A short checklist for the first two minutes

- Restate the task in one sentence.
- Ask the five questions, skipping any that clearly do not apply.
- Write the answers as comments: `# ties: alphabetical`, `# empty: return []`.
- Move to the tiny example.

## Say it like this

"Before I code, let me check a few things. Is the input always a list of strings, or can it hold None? If two words tie, should I break the tie alphabetically? And if there are fewer than k words, do I return what I have? Good. I will write those three rules as comments so that I can check my code against them at the end."
