import json
def extract_json(text):
    try: return json.loads(text)
    except ValueError: pass
    s,e=text.find("{"),text.rfind("}")
    if s==-1 or e<=s: return None
    try: return json.loads(text[s:e+1])
    except ValueError: return None
