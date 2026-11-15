# Wrong types and parsing

## What it is

Data from CSV files, JSON APIs and forms arrives as text. Prices come as `"1,200.00"`, dates as `"01/03/2026"`, flags as `"False"`. Parsing means turning that text into the type the rest of the code expects, and deciding what happens when a value cannot be converted. The pandas details are in [dtypes and datetimes](#/kb/pd-dtypes-datetime).

## How it breaks in production

- **A bad row poisons the column.** One `"n/a"` makes the whole column text, and sums raise errors or concatenate strings.
- **Ambiguous dates.** `"01/03/2026"` is 3 January for pandas by default and 1 March for a Brazilian user. Nothing fails, the numbers are just wrong.
- **Truthy text.** `bool("False")` is `True`, because any non-empty string is true.
- **Silent coercion.** `errors="coerce"` turns failures into `NaN`. That is useful, but if you never count the failures, a broken upstream feed looks like a quiet day.
- **Lost zeros.** An id like `"007"` read as an integer becomes 7 and no longer joins.

## The defence in code

```python
import pandas as pd

raw = pd.DataFrame({
    "price": ["12.50", "1,200.00", "n/a", "7", ""],
    "when": ["2026-03-01", "01/03/2026", "2026-03-02", "bad", None],
})

def parse_price(s):
    return pd.to_numeric(s.str.replace(",", "", regex=False), errors="coerce")

price = parse_price(raw["price"])
when = pd.to_datetime(raw["when"], format="%Y-%m-%d", errors="coerce")

failed = raw["price"].notna() & price.isna()
print(price.tolist())                       # [12.5, 1200.0, nan, 7.0, nan]
print(raw.loc[failed, "price"].tolist())    # ['n/a', '']
print(when.isna().sum())                    # 3
print(pd.to_datetime("01/03/2026"), pd.to_datetime("01/03/2026", dayfirst=True))
print(bool("False"))                        # True
```

I strip the thousands separator before converting, because `to_numeric` rejects `"1,200.00"`. I give the date an explicit `format`, so `"01/03/2026"` is rejected instead of guessed. Then I count what failed. The empty string and `"n/a"` become `NaN`, and the last line shows why flags need an explicit mapping such as `{"True": True, "False": False}`. For ids, read the column as text with `dtype={"id": str}`.

## What to say in the interview

"I parse at the boundary with an explicit format and an explicit type, never rely on guessing. I use coercion so one bad cell does not crash the job, but I count the coerced rows and fail or alert if the share is above a threshold. Dates get a format, ids stay strings, and booleans get a mapping, because `bool('False')` is true."
