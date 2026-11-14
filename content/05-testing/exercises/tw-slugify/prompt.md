`slugify(s)` turns a title into a URL-friendly slug.

- It lowercases the text.
- It splits on any whitespace (spaces, tabs, newlines) and joins the words with a single `-`.
- Repeated, leading and trailing whitespace never produce extra dashes.
- An empty string, or a string with only whitespace, returns `""`.

Write pytest tests in the editor. They must pass on the correct implementation and fail on every buggy one. The function is imported with: from solution import slugify
