# Prompt anatomy

The interviewer reads your prompts, and they are graded. A good prompt is a small specification with five parts. If you can write the five parts, you understand the problem, which is exactly what is being checked.

## The five parts

1. **Task.** Which function, which language, one sentence of purpose.
2. **Inputs and outputs.** The signature, the types and the exact return shape.
3. **Constraints.** Libraries allowed, deterministic, do not mutate the input.
4. **Edge cases.** Empty input, None or NaN, ties, invalid arguments.
5. **Example.** One real input and its real output. Optionally: ask for asserts.

## Weak and strong

```text
Weak:   write a function to remove duplicates

Strong: Write unique_in_order(items: list[str]) -> list[str] in Python 3.12,
        standard library only. Return a new list with the first occurrence of
        each item, in the original order. Case-sensitive. Do not change the
        input. An empty list returns [].
        Example: unique_in_order(["b", "a", "b", "A"]) -> ["b", "a", "A"]
        Then write asserts for the example, an empty list and all-equal items.
```

The weak prompt leaves four decisions to the assistant: order, case, whether to mutate, and the return type. The strong one decides them, so you can check each sentence against one line of the answer. A plausible answer, and the checks you asked for:

```python
def unique_in_order(items: list[str]) -> list[str]:
    seen = set()
    out = []
    for item in items:
        if item not in seen:
            seen.add(item)
            out.append(item)
    return out

assert unique_in_order(["b", "a", "b", "A"]) == ["b", "a", "A"]
assert unique_in_order([]) == []
assert unique_in_order(["x", "x", "x"]) == ["x"]
print("ok")
```

Map the prompt to the code: "first occurrence" is the `not in seen` test, "original order" is the list `out`, "do not change the input" holds because nothing writes to `items`.

## Things to remember

- Eight clear lines beat a long paragraph.
- Include one edge case in your example. Assistants handle the happy path by themselves; edge cases are where your prompt adds value.
- For ML code, always say what happens with missing values, empty batches and ties.
- If the first answer misses a rule, quote the rule and ask for that single change. Do not start over.

## What you say

"I write the spec first so the assistant does not guess, and so that I can check the answer against it." That sentence is true, and it shows the interviewer a method.

Related: [Anatomy of a good prompt](#/kb/ai-prompt-anatomy), [Verifying AI-written code](#/kb/ai-verifying-ai-code).
