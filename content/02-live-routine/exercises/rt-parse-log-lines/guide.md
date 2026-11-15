**Why this matters.** Log lines are semi-structured text: a fixed header and then free text. The message may contain spaces, so splitting on every space would shred it, and real logs always contain a few broken lines.
**How we get there.**
1. Go through the lines one at a time and split with a limit: `line.split(" ", 2)`. That cuts at most twice, giving timestamp, level and the whole rest as the message.
2. If `len(parts) < 3`, the line is malformed, so `continue`. We must check this before unpacking, because unpacking two parts into three names would raise an error.
3. Otherwise unpack `_, level, message = parts`. The underscore marks the timestamp as unused.
4. Count levels with `counts[level] = counts.get(level, 0) + 1`.
5. If the level is `"ERROR"`, append the message to `errors`. We append in loop order, so input order is kept.
6. Return `counts, errors`.
**Check it.** An empty list returns `({}, [])`. One pass gives O(n) time in the total length of the lines.
**Watch out.** Plain `line.split()` keeps only the first word of the message, and unpacking without the length check crashes on a bad line.
