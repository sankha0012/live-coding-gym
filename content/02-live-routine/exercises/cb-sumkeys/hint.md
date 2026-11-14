s.split(',') gives 'a:1' pieces; piece.split(':') gives key and value; int(value). Use d[k] = d.get(k, 0) + v, then sorted(d).
