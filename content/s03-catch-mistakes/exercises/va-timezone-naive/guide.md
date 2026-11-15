**Why this matters.** Expiry compares two moments in time. If one is mislabelled by a few hours, a token expires early or lives too long.

**How we get there.**
1. Reproduce with an aware value in another zone: `2024-01-01 12:00-03:00` is 15:00 UTC. The buggy code calls `replace(tzinfo=timezone.utc)` and reads it as 12:00 UTC, three hours off.
2. Locate it. `replace` keeps the clock numbers and only swaps the label. That is right for a naive value, which we define as UTC, but wrong for an aware one, which already names a zone.
3. Write a helper `_utc(dt)`. If `dt.tzinfo is None`, attach UTC with `replace`. Otherwise use `dt.astimezone(timezone.utc)`, which moves the instant correctly.
4. Compare `_utc(now) >= _utc(expires_at)`. Both sides are aware and in UTC, so mixing naive and aware values no longer raises.

**Check it.** Equal instants count as expired because of `>=`. Neither input is modified, since both operations return new objects.

**Next time.** Compare in UTC, and test with an aware value in a non-UTC zone.

**Watch out.** `astimezone` on a naive value makes Python assume the machine's local zone, so results change between servers.
