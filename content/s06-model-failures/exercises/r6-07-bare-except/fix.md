The bare `except: pass` hides the failed rows, so the status says ok although rows 2 and 4 failed. Change the first loop so it only catches the two expected errors, remembers the ids of the failed rows, and the status line prints `partial` whenever any row failed (and `ok` only when none did).

The output must be exactly:

```
{1: 2.5, 3: 2.0, 5: 5.0}
status: partial
done: 3 failed: [(2, 'ZeroDivisionError'), (4, 'KeyError')]
```
