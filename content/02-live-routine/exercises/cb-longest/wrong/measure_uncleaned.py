def LongestWord(sen):
    best = max(sen.split(), key=len) if sen.split() else ""
    return "".join(ch for ch in best if ch.isalnum())

print(LongestWord(input()))
