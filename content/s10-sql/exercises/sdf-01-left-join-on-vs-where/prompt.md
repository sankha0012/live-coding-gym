You wrote a report of every customer in Curitiba with the number of their delivered orders, and customers with zero delivered orders must appear with 0. Your query is `customers c LEFT JOIN orders o ON o.customer_id = c.customer_id AND o.status = 'delivered'`, grouped by customer. The interviewer asks: "Why is the status condition in the ON clause? My teammate would put it in WHERE, it reads the same."

Explain the difference, say what the report would look like with the condition in WHERE, and how you would check that your version keeps every customer.
