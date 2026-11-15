import pandas as pd

events = pd.DataFrame({
    "user": ["ana", "bob", "ana", "bob"],
    "updated_at": ["2026-03-05", "2026-03-02", "2026-03-01", "2026-03-04"],
    "plan": ["pro", "free", "free", "pro"],
})

latest = events.drop_duplicates(subset="user", keep="last")
print(latest.sort_values("user")[["user", "plan"]].to_string(index=False))

fixed = (
    events.sort_values("updated_at")
    .drop_duplicates(subset="user", keep="last")
)
print(fixed.sort_values("user")[["user", "plan"]].to_string(index=False))
