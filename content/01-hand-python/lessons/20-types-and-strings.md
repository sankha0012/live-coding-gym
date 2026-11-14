# Types and strings

## The problem it solves

Most interview tasks start with text: a log line, a CSV row, a user id, a sentence. If you cannot slice, split, join and format a string without looking it up, you lose minutes on every task. This lesson gives you the small set of moves that cover nearly all of it.

Strings are immutable. Every method returns a new string. It never changes the old one. Remember this, because it explains the first trap below.

## The smallest runnable example

```python
line = "  2026-11-14,order-17,  42.5 "
clean = line.strip()                 # remove outer spaces
date, order, amount = [p.strip() for p in clean.split(",")]
year = date[:4]                      # slice: first four chars
last = order[-2:]                    # slice: last two chars
words = "the sky is blue".split()    # split on any whitespace
back = " ".join(reversed(words))     # join a list into one string
msg = f"{order} cost {float(amount):.2f} in {year}"
print(date, order, amount)
print(year, last, back)
print(msg)
print(int("42") + 1, str(7) + "x", "ab" * 3)
print("Hello".lower(), "hello".upper(), "a-b".replace("-", "_"))
print("abc".startswith("ab"), "abc".find("z"), "b" in "abc")
```

Run it. The output shows each move in action. The moves to memorise:

- `strip()`, `lower()`, `upper()`, `replace(old, new)`
- `split(sep)` gives a list. `sep.join(list)` gives a string.
- `s[a:b]` slices. `s[-1]` is the last char. `s[::-1]` reverses.
- `f"{x:.2f}"` formats a float with two decimals.
- `isalpha()`, `isdigit()`, `isalnum()` test a character.

Slices never raise an error when out of range. `"abc"[5:]` is `""`. Indexing does: `"abc"[5]` raises `IndexError`.

## Types you must know

`int`, `float`, `str`, `bool`, `None`. Convert with `int(x)`, `float(x)`, `str(x)`. Converting text that is not a number raises `ValueError`. That is a real edge case: a task may say "ignore bad rows". See the errors lesson.

Truthiness: empty string, `0`, `None` and empty containers are false. So `if not s:` is the short guard for an empty string.

## Trap 1: thinking a method changes the string

```python
s = "  hi  "
s.strip()
print(repr(s))       # still '  hi  '
s = s.strip()
print(repr(s))       # 'hi'
```

You must assign the result. This is the most common beginner bug in a live round.

## Trap 2: `split(" ")` versus `split()`

```python
text = "a  b"
print(text.split(" "))   # ['a', '', 'b']
print(text.split())      # ['a', 'b']
```

`split()` with no argument splits on runs of whitespace and drops empty pieces. `split(" ")` keeps empty strings when there are double spaces. If the prompt says "extra spaces are ignored", use `split()`.

## Trap 3: building strings in a loop with `+=` and using `str` as a name

Two small habits. First, collect pieces in a list and call `"".join(parts)` at the end. It is cleaner, and it is linear time. Second, never name a variable `str`, `list`, `dict` or `input`. After `str = "x"` the call `str(5)` fails with `TypeError`, and the error message confuses people.

```python
parts = []
for ch in "hello":
    parts.append(ch.upper() if ch in "aeiou" else ch)
print("".join(parts))   # hEllO
```

## Characters and numbers

`ord("a")` gives 97. `chr(97)` gives `"a"`. A letter shift, like a Caesar cipher, uses both: `chr((ord(ch) - 97 + k) % 26 + 97)`. Test it on small input, for example shifting `"z"` by 1 should give `"a"`.

```python
k = 1
print(chr((ord("z") - 97 + k) % 26 + 97))   # a
```

## Checks to run in the live round

After you write a string function, test three inputs out loud: an empty string, a single character, and one with odd spacing or capitals. This takes ten seconds and shows the interviewer you think about edge cases.

```python
def first_word(s):
    parts = s.split()
    return parts[0] if parts else ""

assert first_word("") == ""
assert first_word("  go now ") == "go"
print("ok")
```

## Say it like this

"I clean the input with strip and split, so extra spaces do not matter. I keep the pieces in a list and join them at the end, which is linear time. Strings are immutable, so I assign the result of each method. I checked the empty string and a string with double spaces, and both return what the prompt asks."
