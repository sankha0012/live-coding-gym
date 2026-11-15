import string

def LongestWord(sen):
    best = ""
    for word in sen.split():
        clean = word.strip(string.punctuation)
        if len(clean) > len(best):
            best = clean
    return best

print(LongestWord(input()))
