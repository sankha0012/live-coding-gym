**Why this matters.** Checking every substring is O(n cubed) or worse. The sliding window idea, grow on the right and shrink on the left only when forced, shows up in many string problems.
**How we get there.**
1. Track a window that starts at `start` and ends at the current index `i`, and a dict `last` with the most recent index of each character.
2. Move `i` forward. A seen character is a problem only if its earlier position is inside the window.
3. In that case, jump the start just past the old copy: `start = last[ch] + 1`. We guard it with `last[ch] >= start`, so the start never moves backwards.
4. Record `last[ch] = i` and update `best = max(best, i - start + 1)`, the current window length.
**Check it.** An empty string never loops and returns 0. In `"abba"` the second `a` has an old index before the window, which the guard ignores. Each character is visited once, so it is O(n) time and O(k) space for k distinct characters.
**Watch out.** Moving `start` without the `>= start` guard lets a stale index pull the window back, which counts a repeated character as unique.
