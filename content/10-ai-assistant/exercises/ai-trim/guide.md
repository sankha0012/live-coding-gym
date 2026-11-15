**Why this matters.** A chat model has a limited context window, so a long conversation must be cut. The usual rule: keep the instructions, then the most recent turns, because those matter most for the next reply.

**How we get there.**
1. Define a message's cost as its word count, `len(m[1].split())`.
2. Handle the system message first. If the first message has role `system`, set it aside as `head` and count its cost as used. It is kept even if it alone is large.
3. Walk the rest backwards with `reversed(rest)`, so the newest messages come first.
4. If `used + cost > budget`, `break`. We stop at the first message that does not fit instead of skipping it, so we never keep an older message while dropping a newer one. Otherwise keep it and update `used`.
5. The tail was collected newest-first, so reverse it with `tail[::-1]` and return `head + tail`.

**Check it.** A budget of 0 keeps only the system message, and empty input gives `[]`. Each message is visited once, so cost is linear.

**Watch out.** `continue` instead of `break` leaves holes in the conversation, and forgetting to reverse returns the messages backwards.
