def trim_history(messages, budget):
    cost=lambda m: len(m[1].split())
    head,rest,used=[],messages,0
    if messages and messages[0][0]=="system":
        head,rest,used=[messages[0]],messages[1:],cost(messages[0])
    tail=[]
    for m in reversed(rest):
        if used+cost(m)>budget: continue
        tail.append(m); used+=cost(m)
    return head+tail[::-1]
