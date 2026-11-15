A request arrives with some features missing. Write `fill_features(row: dict, defaults: dict) -> tuple[dict, list[str]]`.

`defaults` maps each feature name to its fallback value. A feature is missing when its key is absent from `row` or its value is `None`. Fill each missing feature from `defaults`. A value of `0`, `0.0`, `False` or `""` is a real value, not missing. Keys in `row` that are not in `defaults` are kept unchanged. Return `(filled_row, filled_names)` where `filled_names` is the sorted list of features that were filled. Do not modify `row`.
