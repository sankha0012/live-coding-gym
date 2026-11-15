**Why this matters.** Validating input is where small details bite. `int()` is forgiving: it accepts spaces, signs and other digits, so using it as the checker lets bad addresses through.
**How we get there.**
1. Split on dots with `s.split(".")` and require exactly four parts. `"1.2.3"` and `"1.2.3.4.5"` fail here, and so does `"1..2.3"` because the empty piece is still a part to check.
2. Check each part is made only of digits: `p.isdigit()`. That rejects empty strings, spaces and a minus sign.
3. `isdigit` also accepts digits from other scripts, so we add `p.isascii()` to allow only 0 to 9.
4. Reject leading zeros: `len(p) > 1 and p[0] == "0"`. A single `"0"` is fine, `"01"` is not.
5. Only now is it safe to convert, and we require `int(p) <= 255`. If every part passes, return `True`.
**Check it.** A negative number cannot reach `int` because its minus sign fails `isdigit`. We look at each character a constant number of times, so time is O(n).
**Watch out.** Checking the range first, or relying on `int()` in a try block, accepts padded or signed parts, and a missing `isascii` accepts non-Latin digits.
