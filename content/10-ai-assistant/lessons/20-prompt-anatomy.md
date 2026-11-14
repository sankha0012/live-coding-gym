# Prompt anatomy

## The problem it solves

In the interview you may use an AI assistant, and the interviewer reads your prompt. A vague prompt gets code that guesses. You then spend the session fixing guesses, and the interviewer sees that you did not know what you wanted. A good prompt is a small spec. It shows you understood the problem before any code existed.

A strong prompt has five parts:

- **Task:** one sentence. What function, in what language, for what purpose.
- **Inputs and outputs:** the signature, the types, and one example of each.
- **Constraints:** standard library only, deterministic, do not mutate the input, a time or memory limit.
- **Examples:** two or three input and output pairs, including an edge case.
- **Asks for tests:** tell the assistant to write asserts that cover the examples and the edges.

Ask for one function at a time. A big request hides mistakes in a big answer.

## The smallest runnable example

Here is a weak prompt and a strong one for the same job.

```text
Weak:   write code to clean my data

Strong: Write clip_scores(scores: list[float], low: float, high: float) -> list[float]
        in Python 3.12, standard library only.
        It returns a new list where each value is limited to the range low..high.
        Do not change the input list. NaN stays NaN. Raise ValueError if low > high.
        Example: clip_scores([-1.0, 0.5, 2.0], 0.0, 1.0) -> [0.0, 0.5, 1.0]
        Then write three asserts: the example, an empty list, and the ValueError.
```

The strong prompt leaves little to guess. This is the kind of code it should produce:

```python
import math


def clip_scores(scores: list[float], low: float, high: float) -> list[float]:
    if low > high:
        raise ValueError("low must not be greater than high")
    return [x if math.isnan(x) else min(max(x, low), high) for x in scores]


assert clip_scores([-1.0, 0.5, 2.0], 0.0, 1.0) == [0.0, 0.5, 1.0]
assert clip_scores([], 0.0, 1.0) == []
try:
    clip_scores([1.0], 2.0, 1.0)
except ValueError:
    pass
else:
    raise AssertionError("expected ValueError")
print("ok")
```

Notice that every rule in the prompt maps to one line of code. That is how you check the answer afterwards: walk down your own prompt and find the line that handles each sentence.

## The three traps

**1. Leaving the edge cases out.** If you do not say what happens with an empty list, a missing value or a tie, the assistant picks for you. It may pick well, but you will not know why. Write the rule in the prompt: "an empty list returns an empty list". For ML code, always think about missing values, NaN, empty batches, and duplicates.

**2. Asking for everything at once.** "Build a pipeline that loads, cleans, trains and serves" returns two hundred lines you cannot explain. Ask for the cleaning function first, check it, then the next piece. Small steps are also easier for the interviewer to follow.

**3. Not saying what the output looks like.** "Return the result" can be a list, a dict, a tuple or a DataFrame. Give the exact return type and one example. If the output must be sorted or deterministic, say so. If you need stable order for ties, say "ties keep the original order".

## A small checklist before you press enter

1. Did I name the function and its signature?
2. Did I give one example with a real value?
3. Did I list the edge cases: empty, missing, NaN, duplicates, invalid?
4. Did I state the limits: libraries, determinism, no mutation?
5. Did I ask for tests?

If you can answer yes to all five in under a minute, the prompt is ready. You do not need long prompts. Eight clear lines beat a long paragraph.

## Say it like this

"Before I ask the assistant, I write down what I want. The function name and signature, one example, the edge cases I care about, and the constraints, like standard library only and no mutation of the input. I also ask it to write tests for those cases. I keep the request to one function so I can read the whole answer and explain every line. If the first answer misses a rule, I do not accept it. I fix the prompt or the code and run the tests again."
