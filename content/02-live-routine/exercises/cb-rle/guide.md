**Why this matters.** Run-length encoding is the simplest compression idea: say how many, then what. The real difficulty is the loop, because we only know a run ended when the next character differs, and the last run has no next character.
**How we get there.**
1. Keep one piece of state: `count`, how long the current run is, starting at 1. We write into a list `out`.
2. Loop `i` from 1 up to and including `len(s)`. At each step we compare `s[i]` with the previous character `s[i - 1]`.
3. If `i < len(s)` and they match, the run grows: `count += 1`.
4. Otherwise the run is over. Append `str(count) + s[i - 1]` and reset `count = 1`.
5. Going one step past the end (`len(s) + 1`) forces that same "run over" branch for the final run, so no extra code is needed after the loop. Finish with `"".join(out)`.
**Check it.** An empty string never enters the loop and returns `""`. A single character gives `1a`. We build a list and join once, so the time is O(n).
**Watch out.** Forgetting to write out the last run is the classic bug; the extra loop step is the cure.
