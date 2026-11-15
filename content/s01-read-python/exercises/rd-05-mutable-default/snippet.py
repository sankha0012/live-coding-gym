def log_event(name, history=[]):
    history.append(name)
    return history


def log_event_safe(name, history=None):
    if history is None:
        history = []
    history.append(name)
    return history


first = log_event("start")
second = log_event("stop")
print(first)
print(second)
print(first is second)

third = log_event("retry", [])
print(third)

a = log_event_safe("start")
b = log_event_safe("stop")
print(a, b)
