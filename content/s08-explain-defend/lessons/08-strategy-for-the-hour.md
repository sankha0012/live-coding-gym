# Strategy for the hour

## The problem it solves

A live round is about one hour. Most people lose it in one of two ways. They code for 50 minutes and have nothing left to explain. Or they type a prompt in the first minute, paste the answer, and cannot say what it does. The interviewer judges the code, the prompt you wrote, and how well you explain both. So you need a plan for the clock before you start.

## The time split

| Minutes | Phase | What you do |
|---|---|---|
| 5 | Clarify | Read the prompt twice. Ask about inputs, outputs and edge cases. |
| 25 | Code | Write the simplest correct version, then add the edge cases. |
| 10 | Prompt and AI use | Use the assistant on purpose, in view of the interviewer. |
| 20 | Explain | Walk through the code, the tests and what you would do next. |

These are targets, not laws. The point is that explaining gets a third of the hour. If you reach minute 40 and nothing runs, stop adding features and make what you have run.

The app's mock round is shorter: you get 35 minutes to code up to two Python exercises, and the follow-up questions about your code come after that. Scale the split down: about 3 minutes to clarify each exercise, the rest to prompt, code and review. Finishing after the 35 minutes costs you the in-time points.

You can use the assistant inside the 25 coding minutes too. The 10-minute block is the time you reserve for the prompt and for reading what comes back.

## Clarify (5 minutes)

Do not start typing. Say the contract out loud: "The input is a list of dicts, the output is a dict. Is that right?" Then run through the failure modes: missing values, NaN, empty input, duplicates, a dependency that fails, ordering and ties. Pick the ones that matter for this data. Write each agreed rule as a one-line comment at the top of the file. These comments become your tests later.

## Use the assistant visibly

Follow the same four steps every time.

1. **Prompt first.** Write a prompt that states the function name, the input, the output, and each edge case you just agreed. Say that you want a plain function with no extra dependencies. A prompt with the edge cases in it shows that you direct the tool.
2. **Read the output.** Read it slowly, line by line, before you run it. Say what each block does. If you cannot explain a line, ask the assistant to simplify it or remove it.
3. **Run the tests.** Write two or three small asserts yourself: the happy path, an empty input, a bad value. Run them. A failing assert is useful, because now you can show how you debug.
4. **Edit.** Change the code by hand. Even one small edit, such as renaming a variable or fixing a boundary, shows that the code is yours.

## When you are stuck

- **Shrink the problem.** Solve it for one row, or for an input of three items, and run it.
- **Say what you know.** "I know the output must be sorted, and I am not sure about ties." Saying this out loud is better than silence, and the interviewer often answers.
- **Print.** Add a print of the value that surprises you. Then remove it.
- **Ask the assistant a narrow question.** "Why does this line fail on an empty list?" is better than "fix it". Read the answer before you paste it.
- **Time-box it.** If you are stuck for more than five minutes, say so and pick the simpler version of the problem. A working simple version beats a broken complete one.

## Checklist to pin next to the screen

- Said the input and output contract out loud
- Named three or four failure modes
- Prompt includes function name, types and edge cases
- Read the generated code before running it
- Wrote my own asserts and ran them
- Edited at least one thing by hand
- Seeded any randomness; no wall clock; no network
- Left 20 minutes to explain
- Can say what I would add next

## Three traps people hit

1. **Pasting without reading.** If the interviewer asks "what does this line do?" and you do not know, the round is over. Read before you run.
2. **A one-line prompt.** "Write a function to clean this data" tells the interviewer nothing about your thinking. Include the rules.
3. **Spending the explain time on coding.** Stop coding at about minute 40, even if the code is not perfect. Use the rest to explain, test and name the limits.

## Say it like this

"I will use about five minutes to clarify, then write the code, then use the assistant for the parts that are routine. I always write the prompt with the edge cases in it, read what comes back, and run my own tests before I trust it. If I get stuck, I shrink the problem to one example and say what I am unsure about. I keep the last twenty minutes to explain the code, the tests, and what I would do next with more time."
