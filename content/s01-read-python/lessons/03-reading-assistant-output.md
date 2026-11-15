# Reading assistant output with a checklist

## The problem it solves

Code from an assistant arrives fast and looks confident. The risk is not that it fails loudly. The risk is that you accept lines you did not read. If you cannot say what a line does, you cannot defend it, and you cannot find the bug in it. A checklist turns reading into a repeatable habit.

## The three questions for every line

For each line or small block, answer out loud:

1. **What does this line do?** Say it in plain words, with the types: "splits the string on commas, gives a list of strings".
2. **What could break?** Empty input, a missing key, a value that is `None` or `NaN`, a string where a number is expected, a boundary at the end of a loop.
3. **Is it needed?** Does this line serve what you asked for? Extra validation, a class, a helper or a feature you did not request is code you now own.

## An example

You asked for: "return the average of a list of numbers given as text, like `'4 8 15'`".

```python
def average(text):
    numbers = [float(x) for x in text.split()]
    total = 0
    for n in numbers:
        total += n
    return round(total / len(numbers), 2)
```

Go through it:

| Line | What it does | What could break | Needed? |
|---|---|---|---|
| `text.split()` | splits on any whitespace | `""` gives `[]` | yes |
| `[float(x) ...]` | converts each piece to a float | `"abc"` raises `ValueError` | yes |
| the loop | adds up the numbers | nothing | no: `sum(numbers)` does it |
| `total / len(numbers)` | divides | empty list raises `ZeroDivisionError` | yes |
| `round(..., 2)` | rounds to two decimals | not asked for; changes the result | check the task |

The reading found one unnecessary loop, one crash on empty input and one change you did not ask for (rounding). You decide each: simplify to `sum(numbers)`, handle empty input as the task requires, drop `round` unless the task wants it.

## The checklist

- [ ] I can explain every line without looking at the assistant's explanation.
- [ ] I know the type of every variable at each step.
- [ ] I checked the first pass, the last pass and the empty case of each loop.
- [ ] I looked at every `except`: it names an error and does something visible.
- [ ] Nothing mutates an input that the caller still uses.
- [ ] There are no imports, helpers or parameters I did not ask for.
- [ ] I know what the code returns on the output format given in the task.
- [ ] I ran it on a normal input and an edge input, and the results match what I predicted.

## When you do not understand a line

Do not accept it and move on. Choose one:

- Trace it by hand with a tiny input.
- Ask the assistant to explain only that line, then check the explanation against what you see when you run it.
- Rewrite it in a form you do read easily. A longer, plainer version that you understand beats a clever one that you do not.

## Common mistakes

- Trusting the assistant's own explanation as proof that the code is right. An explanation describes the intent; running tests shows the behaviour.
- Checking only that the output looks plausible on the example from the task.
- Leaving unused code "just in case". Delete it.

## Related

- [Verifying AI-written code](#/kb/ai-verifying-ai-code)
- [Explaining code to an interviewer](#/kb/iv-explaining-code)
