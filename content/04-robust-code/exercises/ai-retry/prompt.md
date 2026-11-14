Write call_with_retry(fn, max_tries=3, base=1.0, sleep=None). Call fn(); if it raises, wait base * 2**attempt seconds (attempt = 0, 1, ...) using sleep(seconds) and try again. After max_tries failures, re-raise the last error. Don't sleep after the final failure.

*Calling a flaky model API or tool.*
