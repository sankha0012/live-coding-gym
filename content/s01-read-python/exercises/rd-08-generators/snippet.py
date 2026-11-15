def batches(items, size):
    for start in range(0, len(items), size):
        print("making batch at", start)
        yield items[start:start + size]


ids = [10, 11, 12, 13, 14, 15, 16]
gen = batches(ids, 3)
print("created")
first = next(gen)
print("first:", first)
for batch in gen:
    print("batch:", batch, "sum:", sum(batch))
print(list(gen))
