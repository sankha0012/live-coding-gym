# Explaining code line by line and defending trade-offs

## The problem it solves

After you finish a task, the interviewer asks "walk me through it" and "why did you do it this way?" With assistant-written code, the danger is that you cannot answer. The answer is a habit: explain in a fixed order, in plain words, and be ready to name the alternatives.

## Explaining line by line

Use this order:

1. **One sentence of purpose.** "This groups events per user and returns the count of distinct days."
2. **The shape of the data.** What comes in, what goes out, with an example.
3. **The lines, in order.** For each: what it does, and why it is needed. Group trivial lines.
4. **The edge cases.** What happens on empty input, a duplicate, a bad value.
5. **The cost.** Time and memory in terms of the input size.

Example for a short function:

```python
def distinct_days(events):
    days = {}
    for user, ts in events:
        days.setdefault(user, set()).add(ts[:10])
    return {u: len(d) for u, d in days.items()}
```

"It takes `(user, timestamp)` pairs, where the timestamp is a string like `2024-01-05T10:00`, and returns how many different dates each user was active. `days` maps each user to a set of dates. For every event, `setdefault` creates the set the first time we see the user, and `ts[:10]` keeps just the date part, so a second event on the same day does nothing, because sets keep one copy. Finally the dict comprehension replaces each set by its size. Empty input gives an empty dict. It is one pass, so O(n) time, and memory is up to one date per user per day. The assumption is that timestamps start with an ISO date."

Say the assumption out loud. Interviewers value a stated assumption more than a hidden one.

## Pointing at lines

Often you will be asked about one specific line: "what does this do?" Answer with the local meaning first (the line in isolation), then its role (why the function needs it). If you do not know, trace it with a tiny input aloud. That is acceptable. Guessing is not.

## Defending trade-offs

For each design choice, prepare three sentences: **what I chose**, **what I gave up**, **when I would choose differently**.

| Choice | A good defence |
|---|---|
| Dict of sets instead of sorting events | "O(n) and simple, but it holds everything in memory; for data that does not fit I would process in chunks or sort externally." |
| Fixed window counter for a rate limit | "Simple and cheap, but a burst at a window edge can pass twice the limit; a token bucket smooths that, at the cost of a little more state." |
| Retry with exponential backoff | "Reduces load on a failing service, but adds latency and needs a cap and a max attempts, and the operation must be idempotent." |
| Median instead of mean | "Robust to outliers, but ignores the magnitude of extreme values, which might matter here." |

## Handling follow-up questions

- **Why not X?** Name X's benefit and the reason it did not apply here.
- **What if the input is 100x larger?** Say where it breaks (memory, time) and the first change you would make.
- **How would you test it?** Name three cases: normal, empty, edge.
- **What would you change with more time?** One or two concrete items, not a list of everything.
- **I do not know.** Say it, and reason from what you do know. A calm, honest answer beats an invented one.

## Practice

Take any exercise you have finished, close the editor, and explain the solution aloud for two minutes in the order above. Then ask yourself the five follow-ups. If you cannot answer one, go back and read that part of the code again.

## Common mistakes

- Reading the code aloud word by word instead of saying what it means.
- Describing the assistant's intent rather than what the code does.
- Defending a choice by saying "it is the standard way", with no reason.
- Not mentioning the limits of your solution.

## Related

- [Explaining code](#/kb/iv-explaining-code)
- [The six-step routine](#/kb/iv-routine-six-steps)
- [Complexity](#/kb/py-complexity)
