def trim_history(messages, budget):
    cost=lambda m: len(m[1].split())
    head,rest,used=[],messages,0
    if messages and messages[0][0]=="system" and cost(messages[0])<=budget:
        head,rest,used=[messages[0]],messages[1:],cost(messages[0])
    elif messages and messages[0][0]=="system":
        rest=messages[1:]
    tail=[]
    for m in reversed(rest):
        if used+cost(m)>budget: break
        tail.append(m); used+=cost(m)
    return head+tail[::-1]
