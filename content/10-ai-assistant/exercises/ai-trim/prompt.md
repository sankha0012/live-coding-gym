Write trim_history(messages, budget). messages is a list of (role, text); a message costs one token per word. Always keep the first message if its role is 'system'. Then keep the most recent messages, going backwards, and stop at the first one that doesn't fit. Return them in the original order.

*Context window management for a chat agent.*
