Keep a set of seen ids to skip repeats, and a dict of the best event per entity. Compare timestamps, not arrival order, and decide what >= versus > does for ties.
