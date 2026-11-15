# How to read a script top-down

## The problem it solves

You will meet code you did not write: from the assistant, a colleague or an interviewer's task. Reading it line by line from the top, with no map, is slow and you lose the thread. A short routine gives you the map first and the details second.

## The three-part map

Almost every small script has the same shape: **inputs**, a **loop or transformation**, and an **output**. Find these three before you read any detail.

```python
import sys

def total_by_user(lines):
    totals = {}
    for line in lines:                      # the loop
        user, amount = line.split(",")
        totals[user] = totals.get(user, 0) + int(amount)
    return totals

lines = sys.stdin.read().split()            # the input
result = total_by_user(lines)
for user in sorted(result):                 # the output
    print(user, result[user])
```

1. **Input.** Where does data come in? Here `sys.stdin.read().split()` gives a list of strings such as `"ann,5"`. Everything from outside arrives as text.
2. **Loop or transformation.** What happens to each item? Each line is split at the comma, the amount is converted to `int`, and added to the user's running total.
3. **Output.** What is printed or returned, and in what order? One line per user, sorted by name.

With input `ann,5 bo,2 ann,3` (separated by whitespace) the script prints `ann 8` and `bo 2`.

## The routine

1. **Skim the whole file first.** Read function names, imports and the last lines. Do not stop on details.
2. **Name the three parts** in one sentence: "It reads `name,number` pairs, adds the numbers per name, prints the totals sorted by name."
3. **Pick a tiny input** and trace it by hand: one or two items. Write down what each variable holds after each loop pass.
4. **Look at the types.** For each variable ask: string, number, list, dict? Many surprises come from a value that is a string when you expected a number.
5. **Check the ends of the loop.** What happens on the first pass, the last pass and with no items at all?
6. **Predict, then run.** Write down the expected output before you run the code. If the result differs, your mental model is wrong, and that is the thing to fix.

## Reading functions

When a line calls a function, do not dive in immediately. Read its name and its arguments and guess what it returns. Only open the function if the guess is not enough. When you do open it, ask the same three questions again: what comes in, what is done, what goes out.

## Reading by hand: a trace table

For loops, a small table beats reading in your head:

| pass | line | user | amount | totals |
|---|---|---|---|---|
| 1 | `ann,5` | ann | 5 | `{'ann': 5}` |
| 2 | `bo,2` | bo | 2 | `{'ann': 5, 'bo': 2}` |
| 3 | `ann,3` | ann | 3 | `{'ann': 8, 'bo': 2}` |

## Common mistakes

- Reading every line with equal attention. Skim for shape first.
- Assuming a variable name tells you its type. `count` could be a string.
- Skipping the empty input. Ask what the loop does with no items.
- Running the code instead of predicting. If you only run it, you learn what it did, not whether you understood it.

## Related

- [Python input and print](#/kb/py-input-print)
- [Loops, enumerate and zip](#/kb/py-loops-enumerate-zip)
- [Dicts](#/kb/py-dicts)
