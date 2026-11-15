**Why this matters.** A validator is a list of rules, and each rule can be quietly dropped. The tests must give every rule its own failing example.

**How we get there.**
1. Start with one valid address, `"ana@ifood.com"`, and check it with `is True`. That also rejects a function that returns something merely truthy.
2. Test the `@` count: no `@` and two `@` both fail. A version that accepts one or more `@` passes the first and fails the second.
3. Test the empty local part, `"@ifood.com"`.
4. Test the domain dot rule from three sides: no dot at all, a leading dot, a trailing dot. A check on only the start misses the trailing dot.
5. Test spaces in the local part, in the domain, and at both ends, since a version that forgets the space rule passes everything else.

**Check it.** In each invalid case break only that one rule and keep the rest valid, so a failure points at the rule. Each call is constant work apart from scanning the string.

**Watch out.** Mixing two broken rules in one example lets a version that checks only one of them still return `False`, and you never see the missing check.
