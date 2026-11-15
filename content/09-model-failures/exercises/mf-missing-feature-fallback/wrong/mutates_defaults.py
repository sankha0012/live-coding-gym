def fill_features(row, defaults):
    out=defaults; f=[]
    for k in list(defaults):
        if row.get(k) is None: f.append(k)
    out.update({k:v for k,v in row.items() if v is not None})
    return out, sorted(f)
