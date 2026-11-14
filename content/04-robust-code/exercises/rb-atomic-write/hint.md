Put the temp file in the same directory so os.replace is a single rename on one filesystem. Wrap the write in try/except and delete the temp file before re-raising.
