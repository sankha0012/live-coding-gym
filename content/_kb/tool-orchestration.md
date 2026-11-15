---
title: "Orchestration: DAGs, schedules, retries (Airflow and friends)"
summary: An orchestrator runs dependent jobs as a graph, on a schedule, with retries, alerts, history and backfills.
tags: [ml tools, airflow, orchestration]
---
- An orchestrator describes the jobs and their dependencies as a graph (a DAG) and runs it for you.
- It handles the schedule, retries, alerts, run history and re-runs. Cron only starts a command at a time.
- It sits above the code: tasks do the real work, the orchestrator decides when and in what order.
- Key terms: DAG, schedule, retries, backfill, idempotent task.
- Make tasks idempotent and parameterised by the run date, so retries and backfills are safe.

<!-- more -->

## Details

A DAG is a directed acyclic graph: tasks are nodes, dependencies are arrows, and there are no loops. A backfill runs the DAG for past dates, for example after a bug fix.

Idempotency makes retries and backfills safe. The task takes the run date as input and replaces that day's output instead of appending to it:

```python
def build_daily_features(run_date, orders):
    day = orders[orders["date"] == run_date]
    result = day.groupby("city")["amount"].sum().reset_index()
    store[run_date] = result          # overwrite the partition, never append
```

The tools:

- **cron**: no dependencies, retries, history or UI. Fine for one small independent job.
- **Airflow**: the long-standing standard, many integrations, heavy to run.
- **Prefect**: Python-first, workflows are ordinary functions with decorators.
- **Dagster**: models data assets, not only tasks.

Traps:

- Tasks that append without a key. A retry doubles the data.
- Tasks that read "now" instead of the run date. A backfill then gives wrong data.
- Passing large data between tasks. Pass a path or a table name.

## What to say and what not to claim

Say: "I use an orchestrator when there are dependencies, retries, alerting and history to manage. I make tasks idempotent and parameterised by the run date."

Do not claim production Airflow experience if you only read about it. Do not say cron is bad; it is fine for a single simple job. Do not say the orchestrator does the heavy computation. It schedules work that runs elsewhere.

## Likely interview questions

- **Why Airflow instead of cron?** It knows dependencies, retries failures, alerts, keeps run history and supports backfills.
- **What does idempotent mean and why does it matter?** Running twice gives the same final state, which matters because retries and backfills run tasks more than once.
- **What is a backfill?** Running the pipeline for past dates, safe when tasks take the logical date and are idempotent.

## See also

- [Idempotency and idempotency keys](#/kb/prod-idempotency)
- [Retries with backoff](#/kb/prod-retry-backoff)
- [Checkpointing and resuming a batch](#/kb/prod-checkpointing)
