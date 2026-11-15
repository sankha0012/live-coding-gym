Write predict_batch(rows, model, fallback) in Python, standard library only.
- rows is a list of dicts with an "id". Call model(row) for each row.
- If model raises any Exception, or returns None, NaN or +/-inf, use fallback and status "fallback"; otherwise status "ok".
- A prediction of 0.0 is valid. Keep input order.
- Return (results, fallback_rate) where results are dicts {"id", "pred", "status"}; fallback_rate is 0.0 for an empty batch.
Then write asserts for: a normal row, a row where the model raises, a NaN prediction, a 0.0 prediction, and an empty batch.
