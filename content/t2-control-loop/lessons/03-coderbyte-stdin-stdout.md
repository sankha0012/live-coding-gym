# Coderbyte format: stdin, stdout, run and test

## The problem it solves

Coderbyte-style tasks look like small puzzles, but many points are lost to format: reading the input, converting types, and returning exactly the requested output. The algorithm is often the smaller part. Know the format so that you can spend your time on the solution.

## The shape of a task

The editor gives you a function and a line that calls it:

```python
def AddNumbers(text):
    # your code
    return text

# keep this function call here
print(AddNumbers(input()))
```

- The function receives the input as **text**. It is a string even when it looks like a number or a list.
- Whatever you **return** is printed by the last line. Return exactly the type and format the task asks for.
- Keep the final `print(FunctionName(input()))` line as it is.

## Parsing input

```python
text = "4 5 6"
nums = [int(x) for x in text.split()]        # [4, 5, 6]

text = "1,5,3"
nums = [int(x) for x in text.split(",")]     # [1, 5, 3]

text = "hello world"
words = text.split()                         # ['hello', 'world']
```

`split()` with no argument splits on any run of whitespace and drops empty pieces. `split(",")` splits only on commas and keeps empty strings: `"1,,2".split(",")` gives `['1', '', '2']`.

When the input has several lines (in a stdin-based task), read all of it:

```python
import sys
lines = sys.stdin.read().splitlines()
n = int(lines[0])
values = [int(x) for x in lines[1].split()]
```

## Returning the right format

Read the last sentence of the task statement. Typical requirements:

- A string `"true"` or `"false"`, not the booleans `True` and `False`.
- A number as a string: `str(total)` when the function must return text.
- Items joined by a separator: `",".join(words)`.
- A sorted result, or a specific tie-break.

`print(True)` shows `True`; a task that expects `true` will fail even though your logic is right.

## Run and test

1. **Run on the example** from the statement, and compare it character by character.
2. **Write your own edge cases** before pressing the test button: an empty input, one item, repeated items, negative numbers, whitespace around values.
3. **Check what you print.** There should be nothing extra, such as debug prints or a trailing text.
4. When running locally, feed input from a file or pipe:

```text
echo "4 5 6" | python solution.py
```

Add a few asserts in a scratch file to make the checks repeatable:

```python
assert AddNumbers("4 5 6") == 15
assert AddNumbers("") == 0
```

## With the assistant

- Tell it the input arrives as text, give a sample string and the exact expected return.
- Ask for the parsing and the algorithm as two separate small pieces. Parsing is where you can check the output type quickest.
- Keep the call line yourself. Edit it by hand if the assistant changed it.
- Because the session may be recorded, say aloud what you are about to do before you do it.

## Common mistakes

- Forgetting to convert `"5"` to `5`, so `"5" + "6"` gives `"56"` instead of `11`.
- Returning a list when a string is requested.
- Printing inside the function and also returning, so the output appears twice.
- Testing only the statement's example.

## Related

- [The Coderbyte format](#/kb/iv-coderbyte-format)
- [input() and print()](#/kb/py-input-print)
- [Splitting and joining strings](#/kb/py-str-split-join)
