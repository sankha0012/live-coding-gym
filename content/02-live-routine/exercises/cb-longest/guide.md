**Why this matters.** Real text comes with commas, full stops and quotes glued to words. If you measure `"hello,"` you count the comma and may pick the wrong winner.
**How we get there.**
1. Split the sentence into words with `sen.split()`.
2. Clean each word by keeping only letters and digits: `"".join(ch for ch in word if ch.isalnum())`. Cleaning must happen before measuring, otherwise punctuation inflates the length.
3. Keep a running `best`, starting as the empty string. This is the "running best" pattern: remember the champion so far and replace it when something beats it.
4. Replace only when `len(clean) > len(best)`. Strictly greater means that on a tie the earlier word stays, which is exactly the rule we were given.
5. Return `best` after the loop.
**Check it.** A sentence of only punctuation cleans down to empty strings and returns `""`. We touch each character once, so the time is linear in the length of the sentence.
**Watch out.** Using `>=` instead of `>` silently returns the last of the tied words, and it is easy to do without noticing.
