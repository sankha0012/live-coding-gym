# Senior talking points


<p class="lede">The second half of the hour is conversation. Your angle: you own the what and the why, and you work closely with engineers on the how.</p>
<div class="tablewrap"><table><thead><tr><th>They ask</th><th>Hit these points</th><th>Your story</th></tr></thead><tbody>
<tr><td>How would this run in production at 80M orders a month?</td><td>Batch vs online; latency budget; vectorise or precompute; caching; what breaks first; cost per request</td><td>Panini8 platform choices</td></tr>
<tr><td>How do you monitor a model?</td><td>Input drift (PSI), prediction drift, performance by cohort once labels arrive, alert thresholds, retraining triggers, owners</td><td>MoneyLion: drift, feature stability and degradation monitoring on Metaflow, AWS, Snowflake</td></tr>
<tr><td>How do you evaluate an LLM feature?</td><td>Golden set by category, task metrics, LLM-as-judge calibrated on human labels, online metrics (resolution rate, CSAT), regression suite on every prompt change</td><td>Panini8 customer-service tool: response time, usage with and without AI, ratings</td></tr>
<tr><td>Agents that use tools and handle errors?</td><td>Schema-validated tool calls, timeouts, retries with backoff for transient errors only, idempotency, fallbacks, guardrails, human handoff, tracing</td><td>AI-assisted exam: hint-only assistant, guardrails on what it may reveal</td></tr>
<tr><td>How do you control cost?</td><td>Route easy requests to small models, caching, batching, prompt length, self-hosted open models vs API, GPU spot for batch jobs</td><td>Migration from third-party LLM APIs to open-source models</td></tr>
<tr><td>How do you validate a model before launch?</td><td>Out-of-time validation for non-stationary data, leakage checks, business metrics, champion/challenger, staged rollout</td><td>MoneyLion audit pipeline and productionisation template for tree models</td></tr>
<tr><td>How do you lead without authority?</td><td>Demos, weekly reports, a viable path, small wins, clear owners</td><td>Panini8 adoption; training other teams at MoneyLion</td></tr>
</tbody></table></div>
<div class="say">I'm strongest at deciding what to build and how to measure it, and I'm hands-on enough to prototype and to review what engineers build.</div>
