Count per restaurant in a CTE first, then use both RANK() and DENSE_RANK() with OVER (ORDER BY orders DESC). RANK leaves gaps after ties.
