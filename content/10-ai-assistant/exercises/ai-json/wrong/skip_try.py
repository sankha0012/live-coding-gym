import json
def extract_json(text):
    s,e=text.find("{"),text.rfind("}")
    if s==-1 or e<=s: return None
    return json.loads(text[s:e+1])
