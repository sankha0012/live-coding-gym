Keep a dict of free couriers. min(free, key=lambda c: (math.dist(...), c)) then delete the chosen one.
