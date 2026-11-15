Change: tags are case-insensitive. Make `parse_config` return every item of `tags` in lower case.

For example, `parse_config({"name": "x", "tags": " API, Web ,,Db "})["tags"]` must be `["api", "web", "db"]`. Order and duplicates are kept as before, and nothing else changes (empty items are still dropped, the default is still `[]`).

Do this by hand in your own passing solution. It should take one or two lines.
