def trim_history(messages, budget):
    cost=lambda m: len(m[1].split())
    if not messages: return []
    head,rest=[messages[0]],messages[1:]; used=cost(messages[0])
    tail=[]
    for m in reversed(rest):
        if used+cost(m)>budget: break
        tail.append(m); used+=cost(m)
    return head+tail[::-1]
