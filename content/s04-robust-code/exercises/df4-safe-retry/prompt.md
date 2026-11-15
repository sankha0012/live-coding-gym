Your pipeline calls a payment service to charge a customer for a delivery. The call sometimes times out. Your retry helper retries timeouts three times with backoff. A teammate says: "If the first request actually went through and only the response was lost, we will charge the customer up to four times."

How do you make the retry safe? Explain what you change on the client and on the server, where the key comes from, and one thing that can still go wrong.
