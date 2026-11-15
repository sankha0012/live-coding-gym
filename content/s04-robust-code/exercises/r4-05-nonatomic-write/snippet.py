import json
old = json.dumps({"version": 1, "weights": [0.1, 0.2]})
new = {"version": 2, "weights": [0.1, 0.2, 0.3, 0.4]}
disk = {}
def write_chunks(path, text, crash_after=None):
    disk[path] = ""  # open(path, "w") truncates the old content immediately
    for i in range(0, len(text), 10):
        if crash_after is not None and i >= crash_after: raise OSError("disk full")
        disk[path] += text[i:i + 10]

def save(path, payload, atomic, crash_after=None):
    target = path + ".tmp" if atomic else path
    write_chunks(target, json.dumps(payload), crash_after)
    if atomic:
        disk[path] = disk.pop(target)  # stands in for os.replace(tmp, path)

def try_load(path):
    try:
        return json.loads(disk[path])["version"]
    except json.JSONDecodeError:
        return "corrupt"
for atomic in (False, True):
    disk["model.json"] = old
    try:
        save("model.json", new, atomic, crash_after=20)
    except OSError as exc:
        print(f"atomic={atomic} save failed:", exc)
    print(f"atomic={atomic} after crash, readers see:", try_load("model.json"))
save("model.json", new, atomic=True)
print("atomic after success, readers see:", try_load("model.json"))
