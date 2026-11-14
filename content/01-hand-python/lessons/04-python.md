# Python core


<p class="lede">Twelve moves cover almost every “write a function” task. Practise them in the Python drills.</p>
<pre class="code">xs = [3, 1, 2]; xs.append(5); xs[-1]; xs[1:3]; len(xs)
d = {"a": 1}; d["b"] = 2; d.get("z", 0); "a" in d
for k, v in d.items(): ...
s = set(xs); 3 in s                         # O(1) membership

evens = [x for x in xs if x % 2 == 0]       # filter + map
sorted(pairs, key=lambda p: (-p[1], p[0]))  # count desc, then name

from collections import Counter, defaultdict
Counter(["a", "b", "a"]).most_common(2)     # [('a', 2), ('b', 1)]
groups = defaultdict(list); groups[key].append(item)

for i, x in enumerate(xs): ...
for a, b in zip(xs, xs[1:]): ...            # consecutive pairs
best = min(couriers, key=lambda c: dist(c, order))

def f(x, tags=None):                        # never tags=[]
    if not x: return None                   # guard the edge case
assert f([1, 2]) == 3                       # quick test</pre>
