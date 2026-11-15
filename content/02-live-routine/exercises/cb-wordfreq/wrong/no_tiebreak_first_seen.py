from collections import Counter

def TopWord(sen):
    clean = "".join(ch.lower() if ch.isalnum() or ch == " " else " " for ch in sen)
    return Counter(clean.split()).most_common(1)[0][0]

print(TopWord(input()))
