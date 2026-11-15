You built a token bucket rate limiter for an API. A reviewer notices that your class receives a `clock` function in the constructor, and asks: "Why not just call `time.time()` inside `allow()`? It is shorter, and the result is the same in production."

Answer the reviewer. Give one test you could write with an injected clock that would be hard or flaky otherwise, and explain what could go wrong in production if the code read the real clock directly.
