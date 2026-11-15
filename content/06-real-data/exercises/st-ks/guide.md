**Why this matters.** In credit scoring we want a score where defaulters and good customers sit far apart. The KS statistic measures that separation as the biggest gap between the two cumulative distributions: 0 means the groups look alike, 1 means they are fully separated.

**How we get there.**
1. Split the scores into `goods` (label 0) and `bads` (label 1).
2. The gap can only change at an actual score, so loop over `sorted(set(s))` as the thresholds `t`.
3. At each `t`, compute the share of goods at or below it, `sum(g <= t for g in goods) / len(goods)`. Do the same for the bads. Dividing by each group's own size makes these cumulative proportions.
4. Take the absolute difference of the two shares and keep the largest in `best`, starting from 0.0.

**Check it.** Fully separated groups give 1.0, and groups that interleave evenly give a small value such as 0.5 for alternating scores. Each threshold scans every score, so this is O(n^2). With sorted lists and `bisect` it becomes O(n log n).

**Watch out.** Using raw counts instead of shares compares groups of different sizes unfairly.
