# The control loop

An assistant can produce fifty lines in five seconds. The risk is not that the code is slow to write, it is that you end up owning code you never read. The control loop keeps you in charge: you design, the assistant types, and nothing enters your file unread.

## The loop

1. **Plan in comments.** Write the steps of the solution as comments before you prompt anything.
2. **Ask for one small piece.** One function, or one step of the plan.
3. **Read** every line of the answer.
4. **Run** it on a normal input and an edge input.
5. **Explain** it in your own words, out loud.
6. **Change one thing by hand.** A condition, a name, a boundary.
7. **Repeat** with the next comment.

## An example

The task: print the three most frequent words in a text, ties broken alphabetically. The plan comes first:

```python
# 1. split the text into lowercase words
# 2. count each word
# 3. sort by (-count, word) and keep the first 3
```

Ask for step 2 only, not the whole task: "Write count_words(text) returning a dict from lowercase word to count." A typical answer:

```python
def count_words(text):
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts

print(count_words("b a b A"))   # {'b': 2, 'a': 2}
print(count_words(""))          # {}
```

Read it: `split()` with no argument splits on any whitespace, `.get(word, 0)` returns 0 for a new word, and the function returns the dict. Run it: the normal case and the empty case both behave. Explain it: "each word adds one to its own counter."

Then change something by hand. Step 3 is yours to type:

```python
def top3(counts):
    return sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:3]

print(top3({"b": 2, "a": 2, "c": 1, "d": 5}))   # [('d', 5), ('a', 2), ('b', 2)]
```

The sort key is the tie rule written as code: negative count puts bigger counts first, and the word breaks ties alphabetically.

## Why the order matters

The plan makes you the designer, and each comment is a prompt you can check against. Running before accepting catches wrong code while it is still small. The explanation is what you will be asked for in the round, and the hand change proves you can edit the code without the assistant.

If an answer is wrong, report the input you ran, the output you expected and the output you got. If it is too big, throw it away and ask for a smaller piece.

Related: [The six-step routine](#/kb/iv-routine-six-steps), [Verifying AI-written code](#/kb/ai-verifying-ai-code).
