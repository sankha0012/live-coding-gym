---
title: "Explaining code: structure and phrases"
summary: Six fixed steps for a one-minute explanation of any code, with phrases to say out loud.
tags: [interview, explaining, phrases]
---
1. **What it does**: one sentence with input, output and purpose.
2. **How it works**: the main idea, naming the data structure or algorithm.
3. **Complexity**: time and space, and say what n is.
4. **Trade-offs**: what you chose and what you gave up.
5. **Risks**: where it can break (empty input, nulls, ties, duplicates, a failing dependency).
6. **Next step**: the test, log, metric or alert you would add.

- Start from the purpose. Do not read the code line by line.
- Always name one risk before you are asked.
- The whole answer takes about one minute.

<!-- more -->

## Details

The template in one breath:

"It takes [input] and returns [output]. The idea is [data structure or algorithm]. It runs in [time] and uses [space], where n is [what]. I chose [choice] over [alternative] because [reason]. The main risks are [two risks], and with more time I would add [test, log or alert]."

Each step is a good place for the interviewer to interrupt. That is fine. Answer, then continue with the next step.

**Complexity.** "O(n)" alone is not an answer. Say "O(n) in the number of events". If two sizes matter, name both, as in O(n + m). If you are not sure, say what you know: "The sort dominates, so it is O(n log n). I believe the rest is linear."

**Trade-offs.** The most common one is memory for time: a set or dict makes each lookup O(1) and costs O(n) memory. Another is simple and readable against fast.

**Thinking-aloud phrases** for while you work:

- "Let me check I understood the problem."
- "Before coding, I will write the steps as comments."
- "I will test with a small example first."
- "Here is an edge case: what if the list is empty?"
- "If I had more time, I would..."
- "For the business, this means that..."

**Code from an assistant.** Say so, then show that you own it: "I asked the assistant for a first version, then I checked it against these edge cases and simplified the loop." If you cannot explain a line, rewrite it in a simpler way before you present it.

## Common mistakes

- Reading the code aloud: "here I define a dictionary, here I loop". The interviewer can read.
- Saying only that it works, with no risk named.
- Giving a complexity without saying what n is, or forgetting space.
- Claiming that you wrote by hand what an assistant wrote.
- Using long sentences. One idea per sentence is safer, above all in a second language.

## See also

- [The six-step live-coding routine](#/kb/iv-routine-six-steps)
- [Big-O of common Python operations](#/kb/py-complexity)
- [Verifying AI-written code](#/kb/ai-verifying-ai-code)
