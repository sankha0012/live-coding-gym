In Postgres or Databricks I'd use DATE_TRUNC('month', created_at); this is SQLite, so strftime.
