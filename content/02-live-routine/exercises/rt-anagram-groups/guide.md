**Why this matters.** Grouping things that are "the same under some rewriting" is a daily job: duplicate detection, normalizing names, bucketing records. The trick is to find a key that every member of a group shares.
**How we get there.**
1. Two words are anagrams exactly when their letters, sorted, give the same string. So `"".join(sorted(w))` turns `tea`, `eat` and `ate` all into `aet`.
2. Use that string as a dict key and the words as a list under it: `groups.setdefault(key, []).append(w)`. `setdefault` creates the empty list the first time a key appears.
3. We walk the input in order and append, so each group keeps input order and duplicates.
4. The dict values are the groups. The prompt wants them ordered by their first word, so `sorted(groups.values(), key=lambda g: g[0])`.
**Check it.** An empty list gives an empty dict and `[]`. Sorting each word of length k costs O(k log k), so n words cost O(n k log k), plus the final sort of the groups.
**Watch out.** Sorting the groups by their key, or sorting the words inside each group, changes the order the prompt specifies, and the first group is the one that gives it away.
