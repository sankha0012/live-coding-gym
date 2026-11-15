from collections import deque

queue = deque()
ARRIVALS_PER_TICK = 5
SERVED_PER_TICK = 3
next_id = 0

for tick in range(1, 11):
    for _ in range(ARRIVALS_PER_TICK):
        queue.append((next_id, tick))
        next_id += 1
    for _ in range(min(SERVED_PER_TICK, len(queue))):
        queue.popleft()
    if tick % 5 == 0:
        oldest_id, arrived = queue[0]
        print(f"tick {tick}: depth={len(queue)} oldest waited {tick - arrived} ticks")

print(f"accepted={next_id} dropped=0")
