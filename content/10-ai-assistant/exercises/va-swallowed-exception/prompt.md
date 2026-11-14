An AI assistant wrote this. The tests fail. Find the bug and fix it with the smallest safe change.

`parse_quantity(raw)` reads an item count from a string. `None` or a blank string means "not provided" and returns `0`. Otherwise the text, ignoring surrounding spaces, must be a whole number and the function returns it as an `int`. Any other text, such as `"abc"` or `"3.5"`, is bad data and must raise `ValueError`, not be hidden behind a default.
