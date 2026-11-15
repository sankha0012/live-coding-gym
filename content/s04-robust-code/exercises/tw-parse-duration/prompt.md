`parse_duration(text)` converts a duration string to a whole number of seconds (an `int`).

- The text is one or more parts written as digits followed by a unit: `h` (3600 s), `m` (60 s) or `s` (1 s). Example: `"1h30m"` is 5400, `"45s"` is 45, `"2h"` is 7200.
- Parts must be in the order hours, minutes, seconds, and each unit appears at most once. Any subset is fine: `"1h5s"` is 3605. Each number can have any size, with no limit of 59: `"90m"` is 5400.
- Units are lowercase only. No spaces, no signs, no decimals.
- Anything else raises `ValueError`: the empty string, text with no digits (`"abc"`), a number with no unit (`"90"`), unknown units (`"5x"`), junk around valid parts (`"1h30mxyz"`), wrong order (`"30m1h"`) and repeated units (`"1h1h"`).

Write pytest tests in the editor. They must pass on the correct implementation and fail on every buggy one. The function is imported with: from solution import parse_duration
