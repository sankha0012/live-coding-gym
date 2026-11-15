# Prompting while the interviewer watches

In this round the assistant is allowed, the interviewer sees how you use it, and the prompts you write are evaluated. That changes how you behave, not just what you type. A good session sounds and looks like an engineer working with a fast typist.

## Narrate before you switch

If the assistant is in another window, a recording may show tab switches. Say what you are about to do each time: "I will ask the assistant for the parsing function only." Then type the prompt where the interviewer can see it, and say the result aloud when you come back: "It gave me a loop over the lines. I am reading it now."

## Type prompts you would be happy to have read

Write a prompt that names the function, the input, the output and one edge case. Do not paste the whole task statement and hope. Do not write "fix it". A prompt such as "On input `[]` this raises `IndexError` in `top3`; return `[]` instead" shows that you ran the code, understood the failure and chose the fix.

## Read before you accept

Do not paste and run in one motion. Pause and read, and say what you see: "This builds a dict of counts, then sorts the items. The sort key is `(-count, word)`, so ties are alphabetical." If you spot a problem, say so and fix it by hand or ask for the one change.

A short example of reading with a critical eye. You asked for a function returning the average of a list, and got:

```python
def average(nums):
    return sum(nums) / len(nums)

print(average([2, 4, 6]))   # 4.0
try:
    average([])
except ZeroDivisionError as e:
    print("empty list:", e)
```

The normal case is correct, but an empty list raises `ZeroDivisionError`. Your clarifying answer said empty input returns `0.0`. Say it, then make the edit yourself: `return sum(nums) / len(nums) if nums else 0.0`.

## What a good session looks like

- A plan in comments is visible before the first prompt.
- Prompts are small, specific and one at a time.
- After each answer there is a pause, a run, and a sentence of explanation.
- At least one change is typed by hand.
- You never present code you cannot explain. If a line is unclear, ask the assistant to explain that line, or rewrite it more simply.

## What to avoid

- Pasting a large answer without reading it.
- Silence while the assistant works. Use the time to write the next test.

Related: [Verifying AI-written code](#/kb/ai-verifying-ai-code), [Explaining code](#/kb/iv-explaining-code).
