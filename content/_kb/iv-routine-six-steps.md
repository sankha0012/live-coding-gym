---
title: The six-step live-coding routine
summary: "Clarify, Example, Plan, Code, Test, Improve: the order to follow and say out loud in a live round."
tags: [interview, routine, checklist]
---
1. **Clarify** (2 to 3 min): restate the task, ask about input, empty input, ties, output, limits.
2. **Example** (1 min): a tiny input and the answer you expect, worked by hand.
3. **Plan** (2 min): the steps as comments, before any code.
4. **Code**: small runnable steps. Run every line or two.
5. **Test**: the tiny example, then one edge case. Say the expected value first.
6. **Improve**: complexity, trade-offs, what you would add with more time.

- Say each step out loud. The method is what interviewers score, not typing speed.
- Stuck for about 3 minutes: say so, go back to the tiny example, then ask for a hint.

<!-- more -->

## Details

**Clarify.** Restate the task in one sentence. Then ask up to five specific questions: the input type and size, what to do for empty or tiny input, how ties and duplicates behave, the type and order of the output, and the limits on time and memory. Write the answers as comments, for example `# ties: alphabetical` and `# empty: return []`. If the interviewer says "your choice", pick the simple option and say it.

**Example.** Use three to five items, small enough to check by hand. This example becomes your first test.

**Plan.** Write numbered comments such as `# 1. filter  # 2. group  # 3. sort`. Each comment later becomes a few lines of code. Name the data structure you will use.

**Code.** Fill in one comment at a time and run often. If you forget a method name, say the idea and move on: "I do not remember the exact name. The idea is to group and sum. I will write it like this and check."

**Test.** Say the expected value before you run. Use `assert` or `print`. Pick the edge case most likely to break the code: empty input, one item, a tie.

**Improve.** State the complexity and say what n is. Name one trade-off and one risk. For data tasks, say what the result means for the business.

**When stuck.** Say it, solve the tiny example by hand, try a simpler version of the task, or write the slow correct version first. A hint taken well is a good signal.

## Common mistakes

- Starting to code at once and solving the wrong problem.
- Asking "any edge cases?" in place of a specific question that has a one-word answer.
- Asking about ties and then not using the answer in the code.
- Testing only the happy path, or checking the output by eye.
- Going silent, or deleting everything and starting again, when one line is wrong.

## See also

- [Explaining code: structure and phrases](#/kb/iv-explaining-code)
- [The Coderbyte format](#/kb/iv-coderbyte-format)
- [What to test: behaviours, edges, failure paths](#/kb/test-what-to-test)
- [Big-O of common Python operations](#/kb/py-complexity)
