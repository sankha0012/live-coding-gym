**Why this matters.** Balanced brackets are the first thing a parser or JSON validator checks. Counting is not enough: `([)]` has equal numbers of each kind but is still wrong, because order matters.
**How we get there.**
1. The last bracket opened must be the first one closed. That last-in, first-out shape is a stack; a plain list with `append` and `pop` is one.
2. Walk the string. Openers go on the stack; other characters are ignored.
3. For a closing bracket, a dict `pairs` maps it to its partner, for example `")"` to `"("`. The stack must not be empty, and the popped value must equal that partner. Otherwise we return `"false"`.
4. After the loop, anything left was never closed, so the answer is `"true"` only if the stack is empty.
**Check it.** An empty string, or one with no brackets, returns `"true"`. A lone `)` fails: the stack is empty. One pass gives O(n) time, and the stack can hold up to n characters.
**Watch out.** Forgetting the `not stack` check crashes on input that starts with a closing bracket, and forgetting the final emptiness check accepts `((`.
