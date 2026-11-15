---
title: Anatomy of a good prompt
summary: A good prompt is a small spec with five parts - task, inputs and outputs, constraints, examples, tests.
tags: [ai, prompting]
---
```text
Task:        Write <name>(<args with types>) -> <return type> in Python 3.12.
             It <one sentence: what it does and why>.
In / out:    <what each argument is>. Returns <exact shape, order, rounding>.
Constraints: Standard library only. Deterministic. Do not mutate the input.
Edge cases:  Empty input -> <result>. None or NaN -> <rule>. Ties -> <rule>.
             Invalid argument -> raise ValueError.
Example:     <name>(<real input>) -> <real output>
Tests:       Then write asserts for the example, the empty case and the error.
```

- Use it every time you ask the assistant for code. The interviewer reads your prompt.
- Key rule: one function per prompt, and every rule you care about is written down.
- Say: "I write the spec first, so the assistant does not guess and I can check the answer against it."

<!-- more -->

## Details

A vague prompt gets code that guesses. You then spend the session fixing guesses. The five parts remove the guessing:

- **Task.** One sentence: which function, which language, what for.
- **Inputs and outputs.** The signature, the types, and the exact return shape. "Return the result" could be a list, a dict or a tuple.
- **Constraints.** Libraries allowed, determinism, no mutation, a time or memory limit.
- **Examples.** Two or three input and output pairs with real values, one of them an edge case.
- **Tests.** Ask for asserts that cover the examples and the edges.

A weak and a strong version of the same request:

```text
Weak:   write a function to remove duplicates

Strong: Write unique_in_order(items: list[str]) -> list[str] in Python 3.12,
        standard library only. Return a new list with the first occurrence of
        each item, in the original order. Comparison is case-sensitive.
        Do not change the input. An empty list returns [].
        Example: unique_in_order(["b", "a", "b", "A"]) -> ["b", "a", "A"]
        Then write three asserts: the example, an empty list, all items equal.
```

Each sentence of the strong prompt should map to one line of the answer. That is how you check it afterwards.

For ML code, always state what happens with missing values, NaN, an empty batch, duplicates and ties.

Eight clear lines beat a long paragraph.

If the first answer misses a rule, do not accept it and do not start over. Point to the rule and ask for that one change.

## Common mistakes

- Leaving out the edge cases, so the assistant chooses for you and you do not know what it chose.
- Asking for a whole pipeline at once, and getting two hundred lines you cannot explain.
- Not saying what the output looks like, or how ties and order are handled.
- Forgetting to ask for tests.

## See also

- [Verifying AI-written code](#/kb/ai-verifying-ai-code)
- [The six-step live-coding routine](#/kb/iv-routine-six-steps)
- [What to test: behaviours, edges, failure paths](#/kb/test-what-to-test)
