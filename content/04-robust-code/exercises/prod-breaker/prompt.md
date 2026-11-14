Complete CircuitBreaker. call(fn, fallback): if the breaker is open and fewer than `cooldown` seconds have passed since it opened, return fallback without calling fn. Otherwise call fn: on success reset the failure count, close the breaker and return the result; on an exception count the failure and return fallback. Open the breaker when failures reach max_failures, or when the single trial call after a cooldown fails. Time comes from clock().

*Stop hammering a dependency that's down; recover automatically.*
