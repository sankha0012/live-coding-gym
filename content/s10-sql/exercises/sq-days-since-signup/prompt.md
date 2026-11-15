For customers who signed up on or after '2026-07-01', return how many whole days passed between signup_date and the fixed date '2026-11-01'. Never use the current date. Columns: customer_id, days. Sort by customer_id.

*julianday gives a number of days. CAST to INTEGER for whole days.*

Tables:

```
customers(customer_id, name, city, signup_date 'YYYY-MM-DD')
```
