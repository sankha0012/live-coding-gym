The classic bug is forgetting to flush the last run; looping to len(s) handles it. I build a list and join once, so it's O(n).
