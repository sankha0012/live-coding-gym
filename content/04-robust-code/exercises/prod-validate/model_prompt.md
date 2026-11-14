Write a Python 3.11 function validate(row, schema), standard library only.
- schema maps field -> (type, min, max, default); type is "float" or "int".
- For each schema field: if missing, None or NaN, use the default and record "missing:<field>".
  If it can't be converted to the type, use the default and record "bad_type:<field>".
  If outside [min, max], clip it and record "clipped:<field>".
- Record "extra:<field>" for fields not in the schema.
- Don't modify the input dict. Return (clean_row, sorted(issues)) so the output is deterministic.
Keep it short and readable. Then write 3 asserts: a clean row, a row with every problem, and a NaN value.
