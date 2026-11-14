# After the round

## The problem it solves

A mock round teaches you only if you look at it afterwards. Without a debrief you repeat the same mistakes and you cannot tell if you are improving. The debrief is short: one page, written within an hour of the round while you still remember it. It turns a bad round into a drill list.

## One-page debrief template

Copy this into a note and fill it in after every mock.

```
Date: ____    Mock score: ____    In time: yes / no

1. What went well (2 or 3 things)
   -
   -

2. What to drill (topics, with the exercise or step to open)
   -
   -

3. Three mistakes to avoid next time
   a.
   b.
   c.

4. The question I could not answer well
   Question:
   A better answer in 3 sentences:

5. Prompt review
   My prompt was: (paste it)
   What was missing: (edge cases? types? output format?)

6. Next mock: date ____    One thing I will do differently: ____
```

Be specific. "Be more careful" is useless. "I forgot to handle an empty list and found it only when the interviewer asked" is a mistake you can fix.

## How to fill each part

**What went well.** Name behaviours, not feelings. "I clarified the contract before coding" or "I wrote my own asserts" are things you can repeat.

**What to drill.** Look at what cost you points. Did a hidden test fail on NaN? Open the robust code step. Did a SQL join double count rows? Open the SQL step and do two more exercises on joins. Write the exercise name, so the next session starts without thinking.

**Three mistakes.** Keep it to three. Common ones: not reading generated code, no edge-case tests, running out of time before explaining. Put them at the top of your pinned checklist for the next round.

**The unanswered question.** Write the question, then write a better answer in three sentences. Say it out loud once. Then add it to your flashcards if it is a fact, or practise it if it is an explanation.

**Prompt review.** The interviewer judges your prompt, so judge it yourself. Check that it named the function, the input and output types, and the edge cases. If it did not, rewrite it now.

## Use the app's mock score history

The app saves each finished mock with a total score from 0 to 100. A mock is one Python and one SQL exercise. The total mixes three things: the share of hidden tests that passed across both exercises (50 percent), the AI reviewer's marks (40 percent), and whether you finished within 45 minutes (10 percent). The reviewer marks your code, the prompt you wrote, and your answers to follow-up questions about the code. The readiness number on the journey page is the average of your last three mocks, and it only appears after three.

Use the history like this:

- **Look at the trend, not one score.** One bad round can be a hard pair of exercises. Three in a row tell you something.
- **Split the score.** Low test pass rate means you need more code practice and more edge cases. Low review marks means you need to practise writing clean code, writing better prompts, and explaining out loud. Out of time means you need to rehearse the time split.
- **Match the debrief to the score.** If the score went up but your list of mistakes did not change, the exercises were easy. Raise the difficulty.
- **Remember the limit.** The AI reviewer gives an opinion on communication. It is a useful signal, not the truth.

## Three traps people hit

1. **Skipping the debrief when the score is good.** A good score can hide a lucky pair of exercises. Fill the template anyway.
2. **Writing a long list.** Ten items means none get fixed. Keep three mistakes and two drills.
3. **Drilling what you already like.** People repeat the topics they are good at. Drill what the debrief says cost points.

## Say it like this

"After each practice round I write a one-page debrief. I note what went well, what to drill, and the three mistakes I want to avoid next time. I also review my own prompt, because it is part of what gets judged. I track my mock scores over time and look at the average of the last three, split into tests, explanation and time, so I know whether to practise code, speaking, or pacing."
