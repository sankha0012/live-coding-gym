The dict in the signature is created once, so it survives between calls. Check the cache before you recurse, and pass it down.
