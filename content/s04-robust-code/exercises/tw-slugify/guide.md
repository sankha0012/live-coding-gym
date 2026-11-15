**Why this matters.** Slugs go into URLs, so wrong ones become broken links or duplicates. The function is one line, which makes it easy to forget how many different inputs it must handle.

**How we get there.**
1. Test the main promise: `"Hello World"` becomes `"hello-world"`. A version that forgets `lower()` fails here.
2. Test repeated spaces, `"a  b"`. Replacing each single space with a dash gives `a--b`, and splitting on `" "` leaves empty pieces.
3. Test leading and trailing whitespace, `"  a b  "`, which must not create dashes at the ends.
4. Test tabs and newlines, `"a\tb\nc"`. `split()` with no argument treats all whitespace alike.
5. Test the empty string and a blank string. Both give `""`, and a version that special-cases empty input by returning a dash fails.

**Check it.** One behaviour per test means a failure names the bug. The correct version, `"-".join(s.lower().split())`, is linear in the length of the string.

**Watch out.** `split(" ")` looks almost the same as `split()`, yet it breaks on repeated spaces and on tabs.
