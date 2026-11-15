Start the loop at the stored index. Update the results and the index only after handler returns, so a crash leaves the checkpoint pointing at the failed item.
