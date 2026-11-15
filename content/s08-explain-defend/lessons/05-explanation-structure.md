# Explanation structure

## The problem it solves

In this interview you may use an AI assistant. That does not remove the hard part. The interviewer will ask you to explain the code, and they will also judge how you asked for it. Many people can write a good prompt and then freeze when they must say what the code does. A fixed structure fixes that. You do not need to find the words while you think. You walk through six short steps, in the same order, every time.

## The six steps

1. **What it does.** One sentence. Input, output, purpose.
2. **How it works.** The main idea in two or three sentences. Name the data structure or the algorithm.
3. **Complexity.** Time and space, in terms of the input size.
4. **Trade-offs.** What you chose and what you gave up.
5. **Risks.** Where it can break: empty input, missing values, duplicates, bad data, failures of other systems.
6. **Next step.** What you would add with more time: a test, a log, a metric, an alert.

The whole explanation takes about a minute. If the interviewer wants more, they will ask, and each step is a good place to be interrupted.

## The smallest runnable example

Here is a function that keeps the latest event for each user.

```python
def latest_per_user(events):
    best = {}
    for user, ts, value in events:
        if user not in best or ts > best[user][0]:
            best[user] = (ts, value)
    return {u: v for u, (ts, v) in best.items()}


events = [("a", 1, "x"), ("b", 5, "y"), ("a", 3, "z")]
print(latest_per_user(events))  # {'a': 'z', 'b': 'y'}
```

## A full worked example

"This function takes a list of (user, timestamp, value) events and returns, for each user, the value of the most recent event.

I walk through the list once and keep a dictionary from user to the best (timestamp, value) pair seen so far. If the user is new, or the timestamp is larger, I replace the pair. At the end I drop the timestamps.

It is O(n) time, because each event is handled once with a constant-time dictionary lookup, and O(u) space, where u is the number of distinct users.

The trade-off is that I chose a single pass with a dictionary instead of sorting the events first. Sorting would be O(n log n) and would need more memory, but it would be simpler to read.

The risks: if two events for one user have the same timestamp, I keep the first one, so the result depends on input order. If timestamps have mixed types, the comparison fails. An empty list returns an empty dictionary, which is correct.

With more time I would add a test for ties, decide the tie rule with the team, and write it in the docstring."

Count the steps in that answer: what, how, complexity, trade-off, risks, next step. That is the template.

## The three traps people hit

1. **Reading the code line by line.** "Here I define a dictionary, here I loop..." The interviewer can read. They want the idea, the cost and the danger. Start from the purpose, not from line one.
2. **Skipping the risks.** Saying only that it works sounds junior. A senior engineer always names one way it can fail. Say it before you are asked. Ties, nulls, duplicates, empty input and a slow or failing dependency are good defaults.
3. **Giving complexity without saying what n is.** "It is O(n)" is incomplete. Say "O(n) in the number of events". If two sizes matter, name both, for example O(n + m) for a join of two lists.

## When the code came from an assistant

Say so, and then show ownership. A good sentence: "I asked the assistant for a first version, then I checked it against these edge cases and simplified the loop." Do not claim you wrote it by hand if you did not. Do show that you read it, ran it and understood it. If you do not understand a line, say "I would simplify this part" and do it. It is better to rewrite a line than to explain it wrongly.

## Say it like this

"It takes [input] and returns [output]. The idea is [data structure or algorithm]. It runs in [time] and uses [space], where n is [what]. I chose [choice] over [alternative] because [reason]. The main risks are [two risks], and with more time I would add [test, log or alert]."

Practise this out loud on every exercise you finish, even the small ones. After ten repetitions the structure becomes automatic, and you can spend your attention on the code and the interviewer instead of on finding words.
