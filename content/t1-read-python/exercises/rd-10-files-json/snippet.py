import csv
import io
import json

raw = "user,clicks,country\nana,12,PT\nbo,x,US\ncy,7,PT\n"
rows = list(csv.DictReader(io.StringIO(raw)))
print(rows[0])

totals = {}
for row in rows:
    try:
        clicks = int(row["clicks"])
    except ValueError:
        continue
    totals[row["country"]] = totals.get(row["country"], 0) + clicks

text = json.dumps(totals, sort_keys=True)
print(text)
back = json.loads(text)
print(back["PT"], type(back["PT"]).__name__)
