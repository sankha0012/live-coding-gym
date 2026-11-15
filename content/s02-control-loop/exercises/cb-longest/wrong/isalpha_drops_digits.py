def LongestWord(sen):
    best = ""
    for word in sen.split():
        clean = "".join(ch for ch in word if ch.isalpha())
        if len(clean) > len(best):
            best = clean
    return best

print(LongestWord(input()))
