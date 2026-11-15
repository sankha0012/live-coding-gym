---
title: The Coderbyte format
summary: "How a Coderbyte task is shaped: a function fed by input() as text, a required return format, recorded playback."
tags: [interview, coderbyte, stdin]
---
1. The argument arrives as **text**. Convert it first: `int(s)`, `s.split(",")`.
2. Return exactly what is asked, in the format asked: `"true"` is not `True`.
3. Keep the last line `print(FunctionName(input()))` as it is.
4. Try your own edge cases before you run the test cases.
5. Say it out loud before you switch tabs. The session is recorded.

- Read the task statement twice. The output format is usually in its last sentence.
- Most of the lost time goes to input parsing, not to the algorithm.

<!-- more -->

## Details

The editor gives you a function and one line that calls it:

```python
def AddNumbers(text):                    # text arrives as a string: "4 5 6"
    nums = [int(x) for x in text.split()]
    return sum(nums)

# keep this function call here
print(AddNumbers("4 5 6"))               # 15   (the real line passes input())
```

**Input.** `input()` always returns a string. Common conversions:

```python
int("4")                                 # 4
float("2.5")                             # 2.5
"a,b,c".split(",")                       # ['a', 'b', 'c']
[int(x) for x in "4 5 6".split()]        # [4, 5, 6]
```

**Output.** The function returns a value and the last line prints it. Do not print inside the function. If the task wants the text `true`, return the string `"true"`. If it wants numbers joined by commas, build the string with `",".join(...)`.

**Running.** "Run Code" uses the input box. "Run Test Cases" may include hidden cases. Before you use it, try empty input, one item, ties and negative numbers yourself.

**Playback.** The interviewer can replay the session later. Tab switches and pastes are timestamped. Say "I will check the docs" or "switching to my assistant" each time, so the recording matches what you said.

**Assistants.** Follow the rules in your invite. A common setup: the built-in AI is off, another assistant in a separate window is allowed, you must explain the code afterwards, and the prompts you write are evaluated too.

**Environment.** Python 3 with the usual data libraries installed. Documentation is often provided inside the exercise.

Follow the six-step routine inside this format. The interviewer wants to hear your decisions while you code.

## Common mistakes

- Doing arithmetic on the raw input: `"4" * 2` is `'44'`, with no error.
- Returning `True` when the task asks for the text `"true"`.
- Deleting or changing the final `print(...)` line.
- Printing debug output and leaving it in, so the output no longer matches.
- Switching tabs in silence.

## See also

- [input() and print() (Coderbyte-style stdin and stdout)](#/kb/py-input-print)
- [The six-step live-coding routine](#/kb/iv-routine-six-steps)
- [str.split and str.join](#/kb/py-str-split-join)
- [Anatomy of a good prompt](#/kb/ai-prompt-anatomy)
