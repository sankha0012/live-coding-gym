---
title: Stack patterns (brackets, undo)
summary: A list used as a stack (append, pop, [-1]) handles nesting, matching pairs and undo history.
tags: [algorithms, lists, stack]
---
```python
stack = []
stack.append("a")      # push
stack.append("b")
stack[-1]              # 'b'    peek at the top
stack.pop()            # 'b'    last in, first out
not stack              # False  empty check
out = []               # cancel neighbours that are equal
for ch in "abbaca":
    if out and out[-1] == ch: out.pop()
    else: out.append(ch)
"".join(out)           # 'ca'
```

- Use a stack when the newest open item must be handled first: nesting, matching, undo, backtracking.
- `append`, `pop()` and `[-1]` are all O(1). A full pass is O(n) time and O(n) space.
- Always check `if stack` before `pop()` or `[-1]`.

<!-- more -->

## Details

**Matching pairs.** The recipe for brackets, tags or any open and close tokens:

1. Keep a dict from each closer to its opener, for example `pairs = {")": "(", "]": "["}`.
2. On an opener, push it.
3. On a closer, the stack must be non-empty and its top must be the matching opener. Pop it. If not, the input is invalid.
4. At the end the stack must be empty. Anything left is an opener that was never closed.

Steps 3 and 4 are the two checks people forget.

**Undo.** Push the old state before each change. Undo pops it back:

```python
states = [""]                      # stack of versions
states.append(states[-1] + "ab")   # each edit pushes a new version
states.append(states[-1] + "cd")
if len(states) > 1:
    states.pop()                   # undo
states[-1]                         # 'ab'
```

For redo, keep a second stack. Undo moves a state onto it, and a new edit clears it.

**Depth-first search.** A stack replaces recursion: push the start, then loop `while stack:`, pop one item and push its neighbours.

**Last unresolved item.** For "next bigger value" questions, keep a stack of indexes that still wait for an answer. Each new value resolves the waiting indexes it beats.

## Common mistakes

- Calling `pop()` on an empty list, which raises `IndexError`. A closer with no opener hits this.
- Returning `True` after the loop without checking that the stack is empty.
- Using `pop(0)`. That takes from the front, is O(n), and makes a queue. Use `deque.popleft()` for queues.
- Storing only values when you need positions later. Push `(index, value)` or the index.

## See also

- [Lists: append, extend, insert, pop, in, copy](#/kb/py-lists)
- [deque and OrderedDict](#/kb/py-collections-deque)
- [Grids and matrices](#/kb/algo-matrix)
