# What the interviewer sees

## The problem it solves

When AI is allowed, the interviewer cannot judge you by typing speed. They judge three things instead: your prompt, your edits, and whether you understand the result. Candidates who paste a task into the assistant and paste the answer back look the same as everyone else, and they fail the explanation. This lesson shows what each judgement looks like and what to say while you work.

## What they judge

**Your prompt.** Is it a clear spec? Does it name inputs, outputs, edge cases and limits? Did you ask for tests? A short, precise prompt shows you know the problem.

**Your edits.** Did you accept the first answer, or did you read it and change something? Even one small, justified change, such as adding a guard for an empty input, shows you are in control.

**Your understanding.** Afterwards you explain the code. They may ask: what is the complexity, what happens with an empty list, why this data structure, what would break in production. You must answer without looking at the assistant.

## The smallest runnable example

Imagine the assistant returned this for "keep only the latest event per user":

```python
def latest_per_user(events):
    best = {}
    for e in events:
        u = e["user"]
        if u not in best or e["ts"] > best[u]["ts"]:
            best[u] = e
    return sorted(best.values(), key=lambda e: e["user"])


events = [
    {"user": "b", "ts": 1},
    {"user": "a", "ts": 5},
    {"user": "a", "ts": 2},
]
print(latest_per_user(events))
```

A good spoken walk-through of this is short. "One pass over the events. A dict keeps the newest event for each user. I compare timestamps, so input order does not matter. Then I sort by user so the output is deterministic. It is O(n) for the loop and O(u log u) for the sort, where u is the number of users. One edge case: two events with the same timestamp keep the first one, because I use a strict greater-than. If the business wants the last one, I would change it to greater-or-equal."

That answer names the idea, the complexity, an edge case and a trade-off. It took about twenty seconds.

## Things to say aloud while you work

- Before prompting: "I will ask for one function, with these edge cases, and ask for tests."
- Reading the answer: "This loop handles the normal case. I want to check the empty input."
- Finding a problem: "This misses ties. I will tell the assistant the rule, or fix it by hand."
- Running tests: "Passing. Let me add one more edge input to be sure."
- Finishing: "The time is O(n). The main risk is memory if the input is very large."

Narration makes your thinking visible. Silence makes the interviewer guess.

## The three traps

**1. Copying without reading.** If you cannot explain a line, they will ask about that line. Read before you move on. Ask the assistant to explain a line if you need to, then say it back in your own words.

**2. Over-prompting.** A very long prompt full of rules you do not need looks like a script you memorised. Give the rules that matter for this task. Short and exact wins.

**3. Hiding the assistant.** Do not pretend you wrote it by hand. The rules allow the assistant, and honesty is part of what they judge. Say what you delegated and what you checked yourself.

## Say it like this

"I used the assistant for the first draft, and I wrote a prompt with the signature, the edge cases and a request for tests. Then I read the answer and checked it with an empty input, one item and a bad value. I changed one thing, the tie rule, and I can explain why. The code is one pass with a dict, so O(n), and sorting adds a log factor. My main concern for production would be very large inputs, so I would stream or batch them."
