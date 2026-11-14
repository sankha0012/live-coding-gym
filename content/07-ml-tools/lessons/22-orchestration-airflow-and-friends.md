# Orchestration: Airflow and friends

## What problem it solves

An ML system is a chain of jobs: pull data, validate it, build features, train, evaluate, publish. Each job must run in order, on a schedule, and survive failures. With a cron job per step you get a mess. Step two may start before step one finishes. A failure at night is found by a customer in the morning. Re-running last Tuesday means editing scripts by hand.

An orchestrator describes the jobs and their dependencies as a graph and then runs it for you. It handles the schedule, retries, alerts, history and re-runs.

## Where it sits in an ML pipeline

It sits above the code. The tasks themselves do the real work: SQL, pandas, training, calls to other services. The orchestrator decides when each task runs, in what order, and what happens when one fails. Typical uses are the daily feature build, the weekly retraining job and the nightly batch scoring job.

Key words:

- **DAG**: directed acyclic graph. Tasks are nodes, dependencies are arrows, and there are no loops.
- **Schedule**: when a run starts, for example every day at 03:00.
- **Retries**: run a failed task again, usually with a delay between attempts.
- **Backfill**: run the DAG for past dates, for example after a bug fix or when you add a new pipeline.
- **Idempotent task**: running it twice for the same date gives the same final result and no duplicates.

## A minimal real example

The first snippet runs here. It shows idempotency, which is the property that makes retries and backfills safe. The task takes the run date as input and replaces that day's output instead of appending to it.

```python
import pandas as pd

store = {}   # stands in for a table partitioned by date


def build_daily_features(run_date: str, orders: pd.DataFrame) -> None:
    day = orders[orders["date"] == run_date]
    result = day.groupby("city")["amount"].sum().reset_index()
    store[run_date] = result          # overwrite the partition, never append


orders = pd.DataFrame({
    "date": ["2026-01-01", "2026-01-01", "2026-01-02"],
    "city": ["sp", "sp", "rj"],
    "amount": [10.0, 5.0, 7.0],
})
build_daily_features("2026-01-01", orders)
build_daily_features("2026-01-01", orders)    # retry or backfill: same result
print(store["2026-01-01"])
```

The second snippet is illustrative, not run here. Airflow is not installed in this project. It shows the general shape of an Airflow DAG in the TaskFlow style; check the docs for the version you use. In Airflow 3 the same decorators are imported from `airflow.sdk`.

```python
from datetime import datetime, timedelta
from airflow.decorators import dag, task


@dag(schedule="@daily", start_date=datetime(2026, 1, 1), catchup=False,
     default_args={"retries": 2, "retry_delay": timedelta(minutes=5)})
def daily_features():
    @task
    def extract(ds=None):
        ...

    @task
    def build(data):
        ...

    build(extract())


daily_features()
```

Two things to notice. `retries` and `retry_delay` give you automatic retries. `catchup` controls whether Airflow creates runs for every missed past date. Both ideas matter in an interview.

## Airflow, cron, Prefect, Dagster

- **cron**: one line, runs a command at a time. No dependencies, no retries, no history, no UI. Fine for one small independent job.
- **Airflow**: the long-standing standard. Many integrations, mature scheduling, large community. It is heavy to run and its model is task-centred.
- **Prefect**: Python-first, workflows are ordinary functions with decorators. Lighter to start.
- **Dagster**: models data assets, the tables and files the pipeline produces, not only tasks. Good lineage view.

Pick based on the team and what already exists. There is no universal winner.

## The traps

- Tasks that append without a key. A retry doubles the data.
- Tasks that read "now" instead of the run date. A backfill then gives wrong data. Pass the logical date in.
- Passing large data between tasks through the orchestrator. Pass a path or a table name instead.
- Hidden dependencies, such as a task that reads a table another task writes without a declared link.

## What to say in an interview

Say: "I make tasks idempotent and parameterised by the run date, so retries and backfills are safe. I use an orchestrator when there are dependencies, retries, alerting and history to manage."

Say honestly which tools you have used. Do NOT claim production Airflow experience if you only read about it. Do NOT say cron is bad; it is fine for a single simple job. Do NOT say the orchestrator does the heavy computation. It schedules work that runs elsewhere.

## Three likely questions

**1. Why Airflow instead of cron?**
Cron only starts a command at a time. Airflow knows dependencies between tasks, retries failures, sends alerts, keeps run history and supports backfills. For a pipeline of several dependent steps that need to be re-runnable, that matters.

**2. What does idempotent mean and why does it matter?**
Running the task twice for the same input gives the same final state. It matters because retries and backfills run tasks more than once. I get this by overwriting a date partition or using an upsert on a key, not by appending blindly.

**3. What is a backfill?**
Running the pipeline for past dates, for example after fixing a bug or adding a new feature table. It works safely when tasks take the logical date as a parameter and are idempotent.
