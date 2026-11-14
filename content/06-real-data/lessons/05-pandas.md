# pandas


<p class="lede">About 25 moves. The pandas drills here are self-check (the browser can't run pandas), so type them from memory, then compare.</p>
<pre class="code">df = pd.read_csv("orders.csv", parse_dates=["created_at"])
df.shape; df.head(); df.dtypes; df.isna().sum(); df["status"].value_counts()   # LOOK FIRST

df[df["status"] == "delivered"]
df[(df["x"] > 10) &amp; (df["city"].isin(["SP", "RJ"]))]       # parentheses!
df["gmv"] = df["subtotal"].fillna(0) + df["delivery_fee"]
df["late"] = df["actual_minutes"] &gt; df["promised_minutes"]  # bool.mean() = rate

df.groupby("city")["gmv"].sum().sort_values(ascending=False)
df.groupby("city").agg(orders=("order_id", "count"), late_rate=("late", "mean"))
df.merge(rest, on="restaurant_id", how="left")             # check len before/after

g.sort_values("gmv", ascending=False).groupby("city").head(3)   # top N per group
df.set_index("created_at")["gmv"].resample("W").sum().pct_change()
df.groupby("customer_id")["created_at"].shift(1)                 # = LAG
df.groupby("customer_id").cumcount() + 1                          # = ROW_NUMBER
pd.pivot_table(df, index="city", columns="cuisine", values="gmv", aggfunc="sum")
pd.qcut(df["score"], 10, labels=False)                            # deciles</pre>
<div class="tablewrap"><table><thead><tr><th>SQL</th><th>pandas</th></tr></thead><tbody>
<tr><td>WHERE</td><td><code>df[cond]</code></td></tr><tr><td>GROUP BY + agg</td><td><code>groupby().agg()</code></td></tr>
<tr><td>HAVING</td><td>filter after groupby</td></tr><tr><td>JOIN</td><td><code>merge</code></td></tr>
<tr><td>ROW_NUMBER</td><td><code>groupby().cumcount() + 1</code> or <code>rank</code></td></tr><tr><td>LAG</td><td><code>groupby().shift(1)</code></td></tr>
<tr><td>CASE WHEN</td><td><code>np.where</code></td></tr></tbody></table></div>
