**Why this matters.** "Late" sounds obvious, but the boundary is where the money is. An order delivered exactly on the promised minute kept its promise, and a rate that counts it as late punishes good service.

**How we get there.**
1. Reproduce. Delivered in 30 and 45 minutes against a promise of 30 should give 0.5, but the starter prints 1.0.
2. Locate it. The comparison `>=` counts the on-time order as late. The spec says strictly greater, so we change it to `>`.
3. Run the empty case in our heads. If there are no delivered orders, `len(d)` is zero and the division crashes.
4. Guard before dividing: `if not d: return 0.0`. 
5. The rate is `len(late) / len(d)`.

**Check it.** Delivered exactly on time is not late, and a list with only cancelled orders returns 0.0 instead of an error.

**Watch out.** Boundary bugs hide because the typical case still works. When you see a comparison, test the value that sits exactly on the line, and test the empty input before every division.
