**Why this matters.** Counting events per local day goes wrong near midnight, because one instant sits on different calendar days in different zones. Confusing "relabel" with "convert" puts events on the wrong day.

**How we get there.**
1. Reproduce. Take a UTC timestamp at 02:30 and count it for `America/Sao_Paulo`, three hours behind UTC. It belongs to the previous local day, but the buggy code keeps the same date.
2. Locate it. `ts.replace(tzinfo=tz)` only attaches a label to the same wall-clock time. It does not move the instant, so 02:30 UTC becomes 02:30 in Sao Paulo, a different moment.
3. Fix it in two parts. A naive timestamp is defined as UTC, so first label it with `replace(tzinfo=timezone.utc)`. Then convert with `ts.astimezone(tz)`.
4. Take the date from the converted value, as before. The rest stays.

**Check it.** Aware timestamps skip the labelling and are only converted. `ZoneInfo` also handles daylight saving, unlike a fixed offset. Cost is linear.

**Next time.** For a bug near midnight, test just before and after local midnight, and ask whether each call relabels or converts.
