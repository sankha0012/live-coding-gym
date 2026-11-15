import re

def LongestWord(sen):
    best = ""
    for word in re.findall(r"[A-Za-z0-9]+", sen):
        if len(word) > len(best):
            best = word
    return best

print(LongestWord(input()))
