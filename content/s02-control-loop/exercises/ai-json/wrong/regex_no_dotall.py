import json,re
def extract_json(text):
    m=re.search(r"\{.*\}",text)
    if not m: return None
    try: return json.loads(m.group(0))
    except ValueError: return None
