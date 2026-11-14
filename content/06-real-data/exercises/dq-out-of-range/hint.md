One SELECT per rule with its own WHERE, joined by UNION ALL. A comparison with NULL is never true, so NULL rows drop out on their own.
