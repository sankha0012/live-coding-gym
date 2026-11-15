**Why this matters.** A parser has two jobs: read good input correctly and refuse bad input. A lenient parser passes every happy-path test, so most of the tests should be about refusal.

**How we get there.**
1. Test each unit alone, `"45s"`, `"2h"`, `"10m"`. A wrong multiplier shows up immediately.
2. Test combinations, `"1h30m"`, `"1h5s"`, `"1h2m3s"`, plus big numbers like `"90m"`. This proves skipped units and values above 59 work.
3. Check the result is an `int`, since the spec says whole seconds. A version returning `float` still equals the number, so only `isinstance` catches it.
4. Test the empty string by itself. The pattern with every part optional matches `""`, so the correct code needs an explicit check for it.
5. Parametrize the bad inputs: no digits, a number with no unit, unknown unit, junk at the end, wrong order, repeated unit. A parser that scans with `findall` and ignores what it cannot read accepts the junk and the wrong order.

**Check it.** Each bad input is its own test case, so a failure names the case.

**Watch out.** Happy-path tests alone would pass the lenient parser.
