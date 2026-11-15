Write `feature_row(keys, fallback)`. It returns a list of feature values, one per entry of `keys`, in the same order as `keys` (duplicates included, so the list has the same length as `keys`). An entity that is not in the feature store gets the value `fallback`. A stored `0.0` must stay `0.0`.

Use the `featurestore` helper to read the values. Documentation is available below the task, consult it. Check what it returns for ids it does not know.
