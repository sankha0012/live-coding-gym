**Why this matters.** Grouping items by some property is one of the most common data tasks. The pattern is a dict whose values are lists, and the awkward part is creating each list the first time we need it.

**How we get there.**
1. Start with an empty dict. Its keys will be word lengths and its values the lists of words.
2. Walk the words once, in input order. Order matters, because each list must keep the order the words came in.
3. For each word, ask for the list at key `len(w)`. If it does not exist yet we need a fresh one: `out.setdefault(len(w), [])` returns the existing list or inserts an empty one.
4. Append the word to that list: `out.setdefault(len(w), []).append(w)`. Appending keeps duplicates, since we never check for repeats.
5. Return the dict.

**Check it.** An empty list gives `{}`, and `""` simply lands under key `0`. One pass, so time and space are linear.

**Watch out.** Assigning `out[len(w)] = [w]` overwrites the group each time, so only the last word of each length survives.
