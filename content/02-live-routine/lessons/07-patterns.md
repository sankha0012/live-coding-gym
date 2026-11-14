# Algorithm patterns


<p class="lede">No dynamic programming needed for a data round. These six cover the “algorithm live coding” type.</p>
<div class="tablewrap"><table><thead><tr><th>Pattern</th><th>You'll recognise it when you hear</th><th>Core idea</th></tr></thead><tbody>
<tr><td>Hash map counting</td><td>most frequent, duplicates, group by</td><td>Counter / dict in one pass, O(n)</td></tr>
<tr><td>Sort then scan</td><td>intervals, sessions, consecutive</td><td>sort by time, loop with the previous value</td></tr>
<tr><td>Greedy</td><td>assign, nearest, schedule</td><td>best local choice, then say if it's optimal</td></tr>
<tr><td>Two pointers / window</td><td>within k minutes</td><td>move left and right indexes</td></tr>
<tr><td>Set membership</td><td>seen before, in A not B</td><td>set, O(1) lookup</td></tr>
<tr><td>Accumulate per key</td><td>average per customer</td><td>two dicts: total and count</td></tr></tbody></table></div>
<p>Say the complexity every time: one loop O(n), sort O(n log n), nested loops O(n²), dict or set lookup O(1).</p>
