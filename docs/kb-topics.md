# Knowledge-base topics

One article per id at `content/_kb/<id>.md`. Exercises name the topics they use with `kb: [id, id]` in `exercise.yaml`.

## Python core
- py-input-print: input() and print() (Coderbyte-style stdin and stdout)
- py-strings-basics: Strings: indexing, immutability, common checks
- py-str-split-join: str.split and str.join
- py-str-methods: String methods: lower, strip, replace, startswith, isalpha and friends
- py-f-strings: f-strings and number formatting
- py-slicing: Slicing
- py-lists: Lists: append, extend, insert, pop, in, copy
- py-list-comprehensions: List comprehensions
- py-loops-enumerate-zip: Loops with enumerate, zip and range
- py-sorting: Sorting: sorted, key functions, ties and stability
- py-dicts: Dictionaries: get, setdefault, items, membership
- py-dict-comprehensions: Dict and set comprehensions
- py-counter-defaultdict: Counter and defaultdict
- py-sets: Sets and set operations
- py-tuples-unpacking: Tuples and unpacking
- py-functions-args: Functions: defaults, *args, **kwargs, the mutable default trap
- py-lambda-map-filter: lambda, map, filter, any, all
- py-closures-decorators: Closures and decorators
- py-classes: Classes: __init__, methods, properties, dunder methods
- py-dataclasses: Dataclasses
- py-exceptions: Exceptions: try, except, raise, custom errors
- py-files-pathlib: Files and pathlib
- py-json: JSON: dumps, loads, sort_keys
- py-csv: The csv module
- py-datetime: Dates and times: datetime, timedelta, zoneinfo
- py-math-nan: Floats, NaN, infinity and rounding
- py-random-seeds: Random numbers and seeds
- py-hashlib: Stable hashing with hashlib (and why not hash())
- py-itertools: itertools: chain, islice, accumulate, groupby, pairwise
- py-collections-deque: deque and OrderedDict
- py-heapq: heapq: top-k and priority queues
- py-bisect: bisect: binary search in a sorted list
- py-typing-hints: Type hints
- py-truthiness-none: Truthiness, None and "is" versus "=="
- py-copy-mutability: Mutability, aliasing and copying
- py-iterators-generators: Iterators and generators
- py-regex-basics: Regular expressions with re
- py-time-clock-injection: Clocks: time.monotonic and injecting a clock or sleep
- py-tempfile-os: tempfile and os: temp files, os.replace, paths
- py-complexity: Big-O of common Python operations

## Algorithm patterns
- algo-two-pointers: Two pointers
- algo-sliding-window: Sliding window
- algo-hash-map-counting: Hash map counting and lookup
- algo-stack: Stack patterns (brackets, undo)
- algo-binary-search: Binary search
- algo-intervals: Merging intervals
- algo-lru-cache: LRU cache
- algo-prefix-sums: Prefix sums and running totals
- algo-matrix: Grids and matrices

## Interview technique
- iv-routine-six-steps: The six-step live-coding routine
- iv-explaining-code: Explaining code: structure and phrases
- iv-coderbyte-format: The Coderbyte format

## SQL
- sql-select-where: SELECT, WHERE and operators
- sql-order-limit: ORDER BY and LIMIT
- sql-distinct: DISTINCT and COUNT(DISTINCT)
- sql-joins: INNER JOIN
- sql-left-join-anti-join: LEFT JOIN and anti-joins (rows with no match)
- sql-self-join: Self joins
- sql-group-by: GROUP BY and aggregate functions
- sql-having: HAVING
- sql-conditional-aggregation: Conditional aggregation (CASE inside SUM, AVG, COUNT)
- sql-case: CASE expressions
- sql-subqueries: Subqueries: scalar, IN, EXISTS, correlated
- sql-cte: Common table expressions (WITH)
- sql-window-functions: Window functions: OVER, PARTITION BY, ORDER BY
- sql-row-number-rank: ROW_NUMBER, RANK and DENSE_RANK
- sql-lag-lead: LAG and LEAD
- sql-running-totals-frames: Running totals, moving averages and window frames
- sql-ntile-first-value: NTILE, FIRST_VALUE and LAST_VALUE
- sql-nulls: NULL: IS NULL, COALESCE, COUNT(col) versus COUNT(*)
- sql-dates-sqlite: Dates in SQLite: strftime, date, julianday
- sql-dedupe: De-duplicating rows
- sql-data-quality-checks: Data-quality queries: nulls, duplicates, orphans, ranges
- sql-dialects: Dialect differences: SQLite, Postgres, BigQuery, MySQL

## Testing
- test-pytest-basics: pytest basics
- test-parametrize: pytest.mark.parametrize
- test-fixtures: Fixtures and tmp_path
- test-raises: Testing exceptions with pytest.raises
- test-fakes-monkeypatch: Fakes, fake clocks and monkeypatch
- test-what-to-test: What to test: behaviours, edges, failure paths

## pandas
- pd-read-inspect: Reading and inspecting a DataFrame
- pd-select-filter: Selecting and filtering rows and columns
- pd-groupby-agg: groupby and aggregation
- pd-merge: merge: joins, row counts and validate
- pd-missing-values: Missing values: isna, fillna, dropna
- pd-dtypes-datetime: dtypes, astype and datetimes
- pd-sort-dedupe: sort_values and drop_duplicates
- pd-pivot: pivot_table and crosstab
- pd-rolling: rolling and resample
- pd-time-split-leakage: Time-based splits and leakage
- pd-outliers: Outliers with the IQR rule

## Machine learning and statistics
- ml-sklearn-pipeline: scikit-learn Pipeline
- ml-column-transformer: ColumnTransformer and encoders
- ml-cross-validation: Cross-validation
- ml-joblib-persistence: Saving and loading models with joblib
- ml-train-test-split-leakage: Train/test splits and data leakage
- ml-metrics-precision-recall-f1: Precision, recall, F1 and accuracy
- ml-auc-ks: AUC and KS
- ml-calibration: Calibration
- ml-psi-drift: Drift and the population stability index (PSI)
- ml-ab-test-z: A/B tests and the two-proportion z-test
- ml-bootstrap: The bootstrap

## Robust and production code
- prod-input-validation: Input validation and data contracts
- prod-determinism: Determinism: seeds, ordering, time
- prod-idempotency: Idempotency and idempotency keys
- prod-retry-backoff: Retries with backoff
- prod-timeouts-deadlines: Timeouts and deadlines
- prod-circuit-breaker: Circuit breaker
- prod-rate-limiter-token-bucket: Rate limiting with a token bucket
- prod-ttl-cache: Caches with a TTL
- prod-atomic-write: Atomic file writes
- prod-chunked-batch-processing: Chunked batch processing and isolating bad records
- prod-structured-logging: Structured logging
- prod-fallbacks: Fallbacks and fallback chains
- prod-canary-shadow-ab: Canary, shadow and A/B assignment with stable hashing
- prod-monitoring-percentiles: Monitoring and latency percentiles
- prod-drift-alerts-hysteresis: Alerts, thresholds and hysteresis
- prod-checkpointing: Checkpointing and resuming a batch
- prod-schema-evolution: Schema versions and evolution
- prod-train-serve-skew: Training-serving skew
- prod-event-dedup-ordering: Duplicate and out-of-order events
- prod-health-checks: Health checks

## AI assistants and LLM engineering
- ai-prompt-anatomy: Anatomy of a good prompt
- ai-verifying-ai-code: Verifying AI-written code
- ai-embeddings-topk: Embeddings, cosine similarity and top-k retrieval
- ai-chunking: Chunking text with overlap
- ai-llm-json-parsing: Parsing JSON from an LLM reply
- ai-eval-harness: A tiny evaluation harness
- ai-context-budget: Fitting chat history into a token budget
