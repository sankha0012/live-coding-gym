# Robust ML systems


<p class="lede">What the iFood round tests: code around a model that stays correct when data is messy and dependencies fail. Before saying "done", walk this list out loud.</p>
<div class="tablewrap"><table><thead><tr><th>Concern</th><th>What to do in code</th><th>Drill</th></tr></thead><tbody>
<tr><td>Bad input</td><td>Validate schema, types, ranges; treat None and NaN as missing; repair with defaults and record every repair</td><td>Validate a feature row</td></tr>
<tr><td>Model errors</td><td>try/except per row, check outputs with math.isfinite, fallback values, track the fallback rate</td><td>Batch predictions</td></tr>
<tr><td>Dependency down</td><td>Timeouts, retries with backoff for transient errors only, circuit breaker, safe default</td><td>Circuit breaker · Retry with backoff</td></tr>
<tr><td>Determinism</td><td>No random without a seed, no reliance on set order, full sort keys with tie-breaks, md5 not hash(), inject the clock</td><td>Deterministic split · Bug hunt</td></tr>
<tr><td>Duplicates and order</td><td>Idempotent processing: dedupe by id, last-write-wins by (timestamp, id)</td><td>Idempotent events</td></tr>
<tr><td>Silent failure</td><td>Count and alert: null rate, fallback rate, mean shift, PSI</td><td>Alert on a broken feed · PSI</td></tr>
<tr><td>Side effects</td><td>Don't mutate inputs; return new objects; pure functions are easy to test</td><td>Bug hunt</td></tr>
<tr><td>Proof</td><td>Small asserts for the happy path and each edge case, written before you say done</td><td>Every drill</td></tr>
</tbody></table></div>
<div class="say">Before I call this done, let me check: what happens with a missing value, a NaN, an empty batch, the model throwing, the same event twice, and two runs in a row?</div>
