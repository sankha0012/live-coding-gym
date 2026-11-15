# Talking about tools and AI assistance honestly

## The problem it solves

Interviewers ask about the tools on your CV and about how you work. The way to be convincing is to say specific, true things: what the tool does, what you used it for, and what went wrong or was hard. Overclaiming is easy to detect with one follow-up question. This page gives talking points and a way to answer about AI assistance.

## The rule for every tool

Prepare four sentences:

1. **What it is** in one line.
2. **What I used it for** in this project.
3. **A concrete detail**: a setting, a number, a problem.
4. **A limit or a trade-off.**

Only claim what you did. "I read the dashboard" and "I set up the pipeline" are different statements.

## Talking points

**MLflow** tracks experiments: for each run you log parameters, metrics and artifacts such as the model file, then compare runs in a UI. It also has a model registry that versions models. For reproducibility, log the seed, the data version and the code commit as well. Limit: it records what you tell it to; it does not capture the data by itself.

**Prometheus** scrapes numeric metrics over HTTP from a `/metrics` endpoint and stores them as time series. Use a Counter for things that only increase (requests, errors), a Gauge for values that go up and down, and a Histogram for latency so you can estimate percentiles. Alerts are written as queries (PromQL). Limit: label values with many distinct values (such as user ids) make the number of series explode.

**SQLAlchemy** is a Python toolkit for databases. Its Core builds SQL expressions with bound parameters, which also protects against SQL injection, and its ORM maps tables to classes with sessions managing transactions. **Alembic** is the migration tool for it: versioned scripts with upgrade and downgrade steps, and the database records its current revision. For a live table, change the schema in backward-compatible steps (add a nullable column, backfill, switch the code, drop later).

**pandas** gives labelled tables (DataFrames) with vectorised operations. Traps to know: `merge` on a non-unique key multiplies rows, so check the row count after; chained indexing may write to a copy; row-by-row `apply` is slow compared with vectorised code; and time-ordered data must be split by time, not randomly.

**scikit-learn** gives models and preprocessing behind one `fit`/`predict` interface. A `Pipeline` keeps preprocessing and the model together so that `fit` sees only the training part of each cross-validation fold and the same steps run at serving time. Know precision, recall and how a threshold trades them off.

**FastAPI** is a web framework built on type hints. Pydantic models validate request and response bodies, it generates OpenAPI documentation, and handlers can be async. For a model service, load the model once at startup, validate inputs, expose a health endpoint and log latency and errors.

## Likely follow-ups

- MLflow: "How do you know two runs are comparable?" (same data split, same metric, seeds logged.)
- Prometheus: "Why a histogram rather than an average?" (averages hide the slow tail; percentiles show it.)
- Alembic: "How do you roll back?" (the downgrade step, but destructive changes such as dropping a column cannot restore data, which is why you avoid them in one step.)
- pandas: "Why did the row count change after the join?" (duplicate keys, or an inner join dropping rows.)
- sklearn: "Where could leakage come from?" (fitting transformers before the split, features that include the target's future.)
- FastAPI: "How do you handle a slow model call?" (timeout, fallback, and keeping the model loaded.)

## Answering about AI assistance

Be direct and specific. A good answer has three parts:

1. **Yes, and what for.** "I used an assistant for boilerplate and for first drafts of small functions."
2. **How I stayed in control.** "I planned the steps first, asked for one piece at a time, read every line, ran my own tests and changed things by hand."
3. **Proof.** Offer to explain any line, or explain one now.

Examples of what to avoid: claiming you wrote everything by hand if you did not, or saying "the AI did it" without being able to explain what it did. If the interviewer asks what the assistant got wrong, have one real example, such as a mutable default or a leaked scaler, and say how you found it.

If you were told AI is not allowed for a task, do not use it. If you are allowed, you can say so openly.

## Common mistakes

- Listing tools without any detail.
- Claiming experience with a feature you only read about.
- Defensive answers about AI use. A calm account of your process is stronger.
- Not knowing the limits of the tool you named.

## Related

- [Experiment tracking](#/kb/tool-experiment-tracking)
- [Monitoring tools](#/kb/tool-monitoring)
- [Model serving](#/kb/tool-model-serving)
- [Sklearn pipelines](#/kb/ml-sklearn-pipeline)
- [Merging in pandas](#/kb/pd-merge)
- [Verifying AI-written code](#/kb/ai-verifying-ai-code)
