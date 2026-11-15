Your query passes. Now edit it by hand, without asking the assistant: keep only the cuisines that have at least 100 delivered orders. Same columns, same sort.

Expected: 6 rows instead of 8. The two tiny cuisines, korean and thai (1 delivered order each), disappear; arabic, healthy, burger, brazilian, pizza and japanese remain in the same order. Think about where the condition goes: it is on an aggregate, so it cannot live in WHERE.
