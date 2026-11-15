# The Coderbyte format and quick testing

Coderbyte tasks are small, but many points are lost on format rather than on the algorithm. Learn the shape once and it stops costing you time.

## The shape

```python
def AddNumbers(text):
    nums = [int(x) for x in text.split()]
    return sum(nums)

# keep this function call here
print(AddNumbers(input()))
```

- The input arrives through `input()` as **text**, even when it looks like numbers. Convert it first.
- The function **returns** the answer and the last line prints it. Do not print inside the function.
- Return the exact format the task asks for. If it wants the text `true`, return `"true"`, not `True`.
- Keep the final `print(...)` line as it is, and tell the assistant that the input is text.

Useful conversions:

```python
print([int(x) for x in "4 5 6".split()])   # [4, 5, 6]
print("1,,2".split(","))                   # ['1', '', '2']  (empty piece kept)
print("a  b".split())                      # ['a', 'b']      (whitespace runs dropped)
print(",".join(["a", "b"]))                # a,b
```

## Quick testing in 30 seconds

1. **Say the expected answer first.** "For `4 5 6` I expect `15`." If you decide after seeing the output, you will agree with the output.
2. **Run the tiny example** that you can check by hand.
3. **Run one edge case:** empty input, one item, ties, negatives.
4. **Compare the output character by character** with the format in the task.

In a scratch cell, two asserts make the checks repeatable:

```python
def AddNumbers(text):
    return sum(int(x) for x in text.split())

assert AddNumbers("4 5 6") == 15
assert AddNumbers("") == 0
print("ok")
```

`"".split()` is `[]`, and `sum([])` is `0`, so the empty case passes without a special branch. You only know that because you ran it.

## Run Code and Run Test Cases

"Run Code" uses the input box. "Run Test Cases" may include hidden cases, so a pass on your own example is not a pass on theirs. Always try your edge cases before pressing it.

## Locally

```text
echo "4 5 6" | python solution.py
```

pipes text into `input()`.

## Common mistakes

- `"5" + "6"` is `"56"`, with no error, because the value was never converted.
- Leaving debug `print` calls in, so the output no longer matches.
- Returning a list when a string is requested.

Related: [The Coderbyte format](#/kb/iv-coderbyte-format), [input() and print()](#/kb/py-input-print), [Splitting and joining](#/kb/py-str-split-join).
