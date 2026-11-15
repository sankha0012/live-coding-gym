**Why this matters.** Dispatch systems assign each incoming order to the closest available courier. The trap is state: once a courier takes an order, they are gone for the next one, and distance ties must resolve the same way every time.

**How we get there.**
1. Copy the couriers into a working dict, `free = dict(couriers)`, so we can remove entries without touching the caller's data.
2. Walk the orders in arrival order, since the rule is greedy: earlier orders choose first.
3. If `free` is empty, this order gets `None` and we move on.
4. Otherwise pick the nearest courier with `min(free, key=lambda c: (math.dist((ox, oy), free[c]), c))`. The key is a tuple, so equal distances fall back to the smaller id.
5. Record the choice in `result[oid]` and `del free[best]`, so nobody gets two orders.

**Check it.** Zero couriers gives `None` for every order. Each order scans all free couriers, so the cost is O(n * m).

**Watch out.** Forgetting to remove the chosen courier, or leaving the id out of the key, gives repeated couriers, or lets ties go to whichever courier was inserted first instead of the smaller id.
