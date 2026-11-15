**Why this matters.** Checking that brackets are balanced is what every parser and JSON validator does first. The trap is that counting is not enough: `([)]` has equal numbers of each kind but is still wrong, because order matters.
**How we get there.**
1. The last bracket opened must be the first one closed. That "last in, first out" shape is a stack, and a plain list with `append` and `pop` is one.
2. Walk the string. Every opening character goes on the stack; characters that are not brackets are ignored.
3. For a closing bracket, a dict `pairs` maps it to its partner, for example `")"` to `"("`. The stack must not be empty, and the popped value must equal that partner. Otherwise we return `"false"` right away.
4. After the loop, anything left on the stack was never closed, so the answer is `"true"` only if the stack is empty.
**Check it.** An empty string, or one with no brackets, returns `"true"`. A lone `)` fails because the stack is empty when we need it. One pass gives O(n) time, and the stack can hold up to n characters.
**Watch out.** Forgetting the `not stack` check crashes on input that starts with a closing bracket, and forgetting the final emptiness check accepts `((`.
