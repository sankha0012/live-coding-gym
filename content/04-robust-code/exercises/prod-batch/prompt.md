Write predict_batch(rows, model, fallback). Call model(row) for each row. If it raises, or returns None, NaN or infinity, use the fallback value with status 'fallback'; otherwise status 'ok'. Return (results, fallback_rate) where results is a list of {'id', 'pred', 'status'} in input order. One bad row must not break the batch.

*Partial failure isolation in batch inference.*
