# The control loop

## The problem it solves

Assistants make it easy to produce a lot of code you did not think about. In an interview, and in real work, the person who understands the solution wins. The control loop is a short routine that keeps you in charge: you decide the design, the assistant types, and nothing enters your file unread.

The assistant here is like autocomplete with a chat box. You are not expected to hand-code everything from scratch. You are expected to understand every line and to be able to change it.

## The loop

1. **Plan in comments.** Before any prompt, write the steps as comments in the file.
2. **Ask for one small piece.** One function, or one step of the plan.
3. **Read** every line of the answer.
4. **Run** it on a normal input and an edge input.
5. **Explain** it to yourself, line by line, out loud if you can.
6. **Change one thing by hand.** A rename, a boundary, a condition, a message.
7. **Repeat** with the next comment in the plan.

## Step 1: the plan as comments

Take the task: "Given text with words, print the three most frequent words, ties broken alphabetically."

```python
# 1. read all of stdin as text
# 2. split into lowercase words
# 3. count each word
# 4. sort by (-count, word) and take the first 3
# 5. print one word per line
```

The plan costs a minute and is the part that makes you the engineer. Each comment is a possible prompt, and each comment is a place to check the answer later. It also gives you something to say out loud in an interview: "I'll parse, count, sort, print."

## Step 2: one small ask

Ask for the first unfinished piece, not the whole program:

```text
Write a function count_words(text) that returns a dict mapping each
lowercase word to how many times it appears. Words are separated by whitespace.
```

The assistant answers with something like:

```python
def count_words(text):
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts
```

## Steps 3 to 5: read, run, explain

- **Read.** `text.lower().split()` makes a list of lowercase words. `counts.get(word, 0) + 1` is the counting idiom. The function returns the dict.
- **Run** a normal case and an edge case:

```python
print(count_words("a b a"))   # {'a': 2, 'b': 1}
print(count_words(""))        # {}
```

- **Explain.** "For each word I add one to its count; a new word starts from zero."

## Step 6: one small change by hand

Say the task also wants punctuation ignored. Do not ask the assistant for a rewrite. Edit one line yourself:

```python
    for word in text.lower().replace(",", " ").split():
```

This is small, and typing it proves you read the loop. In a real session you may prefer a better fix (`str.strip` with punctuation per word, or a regex), and the choice is yours.

## What to do when the answer is wrong

- If it fails your test, say what you ran, what you expected and what you got.
- If it is too big, throw it away and ask for a smaller piece.
- If you do not understand it, ask to have a single line explained, not for a new version.

## Common mistakes

- Skipping the plan and asking for "the whole solution".
- Pasting the answer in, then reading it later "if there is time".
- Running only the example from the task statement.
- Asking the assistant to make a change you could type in ten seconds.

## Related

- [Verifying AI-written code](#/kb/ai-verifying-ai-code)
- [The six-step routine](#/kb/iv-routine-six-steps)
- [Prompt anatomy](#/kb/ai-prompt-anatomy)
