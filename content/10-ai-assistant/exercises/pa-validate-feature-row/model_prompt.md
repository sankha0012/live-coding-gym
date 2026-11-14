Write a Python function `validate_row(row: dict, schema: dict) -> list[str]` for a model-serving service.

Inputs: `row` maps feature names to values. `schema` maps each feature name to `{"type": "int" | "float" | "str", "required": bool, "min": number (optional), "max": number (optional)}`.

Output: a list of error strings, one per problem, in sorted feature order. An empty list means the row is valid. The function must never raise on a bad row.

Rules and edge cases:
- A missing required feature is an error. A missing optional feature is fine.
- `None` and NaN count as missing.
- Wrong type is an error. `bool` must not pass as `int`. An int is acceptable for a float feature.
- A value outside min/max is an error. The bounds are inclusive.
- Unknown features in the row are reported as errors, not silently ignored.
- Do not mutate the inputs. No global state, no randomness, deterministic output order.

Please also write pytest tests for: a valid row, a missing required field, NaN, a bool for an int, out-of-range at the exact bounds, an unknown feature and an empty row. Keep it to standard library only. After the code, explain in a few sentences the time complexity and one case the validator does not cover.
