**Why this matters.** Settings come in as raw strings, and a typo in production should stop the service at start-up. Quietly falling back to a default hides the mistake until it hurts.

**How we get there.**
1. Describe each key as a small parser plus a default, in one table. `None` as the default means required.
2. Parsers raise `ValueError` on bad input: `port` checks `1 <= v <= 65535`, `timeout_s` uses `math.isfinite` and `> 0`, and `name` must be non-empty after `strip()`.
3. Parse the flag from its text: `"true"` and `"1"` mean True, `"false"` and `"0"` mean False, case ignored. Never `bool(text)`, since `bool("false")` is True.
4. Loop over the table. An absent key gets its default; a missing required key is `name: missing`. A present key is parsed inside `try/except (ValueError, TypeError)`, and a failure appends `<key>: invalid`.
5. After the loop, if there are problems, raise `ConfigError(problems)` once, which sorts and joins them with `"; "`.

**Check it.** Every key is checked even after a failure, so the operator sees all problems together.

**Watch out.** Using a default when a present value is bad, or stopping at the first error, hides or drips out the problems.
