A feature that is almost a copy of the label is a leakage suspect: it probably uses information that does not exist at prediction time.

Write `leaky_features(features, label, threshold=0.95)` where `features` is a DataFrame of numeric columns and `label` is a Series with the same index.

- Return the sorted list of column names whose absolute Pearson correlation with `label` is strictly above `threshold`. A strong negative correlation counts too.
- A column whose correlation is undefined (for example a constant column) is not flagged.
- Return `[]` when no column is flagged, or when `features` has no columns.
- Do not modify the inputs.
