# Stats by hand


<p class="lede">Your strongest area. The drills here make you type it.</p>
<pre class="code">pos, neg = s[y == 1], s[y == 0]                  # AUC, O(n_pos·n_neg)
auc = ((pos[:, None] &gt; neg).sum() + 0.5 * (pos[:, None] == neg).sum()) / (len(pos) * len(neg))

p = (x1 + x2) / (n1 + n2)                         # two-proportion z
se = (p * (1 - p) * (1/n1 + 1/n2)) ** 0.5; z = (p2 - p1) / se

means = [rng.choice(x, len(x)).mean() for _ in range(2000)]
np.percentile(means, [2.5, 97.5])                 # bootstrap CI

idx = rng.permutation(len(X)); cut = int(0.8 * len(X))  # split; for time data split by date</pre>
<p>Have these answers ready: why AUC ignores monotone transforms; precision and recall at a 12% default rate; monitoring in production (PSI, drift, stability by cohort); bagging vs boosting; leakage.</p>
