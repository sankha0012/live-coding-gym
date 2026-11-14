Loop over the keys, parse each inside try/except ValueError, and append to a problems list instead of raising. Raise one ConfigError at the end. Do not use bool(text) for the flag.
