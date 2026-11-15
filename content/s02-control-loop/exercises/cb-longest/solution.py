def LongestWord(sen):
    best = ""
    for word in sen.split():
        clean = "".join(ch for ch in word if ch.isalnum())
        if len(clean) > len(best):   # strictly longer keeps the first on ties
            best = clean
    return best

print(LongestWord(input()))
