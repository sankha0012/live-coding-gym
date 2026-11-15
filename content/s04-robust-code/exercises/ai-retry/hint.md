for attempt in range(max_tries): try: return fn() except Exception: if attempt == max_tries - 1: raise; sleep(base * 2 ** attempt)
