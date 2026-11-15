---
title: Fitting chat history into a token budget
summary: Keep the system message and the newest turns that fit in the budget, and drop the oldest ones.
tags: [ai, context]
---
```python
def fit_history(messages, budget, count_tokens):
    """messages[0] is the system message. Keep it, plus the newest turns that fit."""
    system, rest = messages[:1], messages[1:]
    used = sum(count_tokens(m["content"]) for m in system)
    kept = []
    for m in reversed(rest):                # newest first
        cost = count_tokens(m["content"])
        if used + cost > budget:
            break                           # stop here: never skip one and keep an older one
        kept.append(m)
        used += cost
    return system + kept[::-1]              # back in chronological order
```

- Use it before every model call in a chat, so the request never exceeds the context window.
- Key rule: walk from the newest message backwards, stop at the first that does not fit, then restore the order.
- Say: "The token counter is injected. In tests it counts words, in production it is the real tokenizer."

<!-- more -->

## Details

```python
msgs = [
    {"role": "system", "content": "be brief"},
    {"role": "user", "content": "one two three"},
    {"role": "assistant", "content": "four five"},
    {"role": "user", "content": "six"},
]

def words(s):
    return len(s.split())

[m["content"] for m in fit_history(msgs, 5, words)]   # ['be brief', 'four five', 'six']
[m["content"] for m in fit_history(msgs, 2, words)]   # ['be brief']
len(msgs)                                             # 4   the input list is not changed
```

With a budget of 5: the system message costs 2, `"six"` costs 1, `"four five"` costs 2. The oldest turn would bring the total to 8, so it is dropped.

**Why `break` and not `continue`.** Skipping a large message and keeping an older small one leaves a gap in the conversation. The model then reads an answer without its question.

**Leave room for the reply.** The window holds input and output together. Use `budget = window - max_output_tokens - safety_margin`.

**Budget overhead.** Real APIs add a few tokens per message for roles and separators. Count them or keep a margin.

**Beyond dropping.** When old turns matter, replace them with a short summary message, or store them and retrieve the relevant ones. Tool results and pasted documents are often the largest items and can be truncated first.

Decide what happens when the system message alone is over budget. This skeleton still returns it. Raising an error is the stricter choice.

## Common mistakes

- Trimming from the newest end and keeping the oldest messages.
- Dropping the system message together with the old turns.
- Returning the kept messages in reversed order.
- Using `len(text)` as the token count. Characters are not tokens.
- Forgetting the space needed for the model's answer.
- Mutating the caller's message list with `pop` or `del`.

## See also

- [Chunking text with overlap](#/kb/ai-chunking)
- [Slicing](#/kb/py-slicing)
- [Sliding window](#/kb/algo-sliding-window)
