def fill_features(row, defaults):
    out=dict(row); f=[]
    for k,d in defaults.items():
        if row.get(k) in (None,""):
            out[k]=d; f.append(k)
    return out, sorted(f)
