# What the interviewer sees

You cannot see the interviewer's notes, but you can reason about what they have in front of them: the shared editor, the recording, the prompts you wrote, and your voice. Most of what is scored is visible in those four things, so make each of them tell a good story.

## The four things

**The editor.** Is there a plan in comments at the top? Does the code grow in small steps, or does a large block appear at once? Are the names clear? Is the final `print(...)` line still intact?

**The recording.** Assume it can show tab switches and pastes. A large paste with no spoken context looks like code you did not write. A paste preceded by "I asked for the parsing function, here it is, I am reading it" looks like a person using a tool.

**The prompts.** They are reviewed. Small, specific prompts with types and an example show that you understand the problem. Vague or huge prompts show that you are hoping.

**Your voice.** It carries the reasoning the code cannot: why this data structure, what you expect before you run, which edge case worries you.

## Signals that score well

- You state the expected result before you run: "I expect `[0, 1]` for this input."
- You run after every small step.
- You name a risk before being asked: "an empty list would divide by zero here."
- You change something by hand, even a small edit.
- You explain a line in one clear sentence.

## Signals that score badly

- Long silences, or typing in a second window with no narration.
- Accepting an answer without reading it, then being surprised by its behaviour.
- Saying "the assistant did it" when asked why a line exists.
- Testing only the example from the statement.

## Quick self-check

You are asked: "Why `sorted(..., key=lambda kv: (-kv[1], kv[0]))`?" A weak answer is "the assistant wrote it". A strong one is: "I need higher counts first and alphabetical order for ties, so I sort by the tuple of negative count and word." Verify the claim:

```python
items = [("b", 2), ("a", 2), ("d", 5)]
print(sorted(items, key=lambda kv: (-kv[1], kv[0])))   # [('d', 5), ('a', 2), ('b', 2)]
```

Being able to run that check in ten seconds is also a signal.

## Practical habit

Before you hand over the session, scroll through your own file and ask: could I explain every line? If not, simplify the line or ask the assistant to explain it now. The interviewer will do the same scroll.

Related: [Explaining code](#/kb/iv-explaining-code), [The six-step routine](#/kb/iv-routine-six-steps).
