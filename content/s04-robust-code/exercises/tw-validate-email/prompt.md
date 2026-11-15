# Test `validate_email`

`validate_email(s)` returns `True` or `False` using this simple rule set. An address is valid only if all of these hold:

- It contains exactly one `@`.
- The part before the `@` (local part) is not empty.
- The part after the `@` (domain) contains at least one `.`, and does not start or end with `.`.
- It contains no spaces.

Example: `"ana@ifood.com"` is `True`; `"ana@ifood"` is `False`. It never raises for string input.

Write pytest tests in the editor. They must pass on the correct implementation and fail on every buggy one. The function is imported with: from solution import validate_email
