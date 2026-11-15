scores = [0.91, 0.35, 0.78, 0.62, 0.05, 0.88]
labels = [1, 0, 1, 1, 0, 1]

top_three = sorted(scores, reverse=True)[:3]
last_two = scores[-2:]
every_other = scores[::2]
positives = [s for s, y in zip(scores, labels) if y == 1]
flags = [s > 0.5 for s in scores]

print(top_three)
print(last_two)
print(every_other)
print(positives)
print(flags)
print(sum(flags) / len(flags))
