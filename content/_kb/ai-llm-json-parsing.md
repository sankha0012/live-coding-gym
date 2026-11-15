---
title: Parsing JSON from an LLM reply
summary: Find the JSON object inside the reply text, parse it, validate the keys, and return an error instead of crashing.
tags: [ai, json, parsing]
---
```python
import json

def parse_reply(text, required):
    start, end = text.find("{"), text.rfind("}")
    if start == -1 or end <= start:
        return None, "no JSON object found"
    try:
        data = json.loads(text[start:end + 1])      # skips code fences and chatter
    except json.JSONDecodeError as e:
        return None, f"invalid JSON: {e.msg}"
    missing = sorted(k for k in required if k not in data)
    if missing:
        return None, f"missing keys: {missing}"
    return data, None
```

- Use it whenever code consumes a model's answer: labels, extracted fields, tool arguments.
- Key rule: a model reply is untrusted input. Extract, parse, validate, and never let it raise into the caller.
- Say: "I return `(data, error)` so the caller can retry with the error message or fall back."

<!-- more -->

## Details

Models often wrap JSON in a Markdown code fence or add a sentence before and after. Taking the text from the first `{` to the last `}` handles both.

```python
reply = 'Sure, here it is:\n{"label": "spam", "score": 0.9}\nHope this helps.'
parse_reply(reply, ["label", "score"])           # ({'label': 'spam', 'score': 0.9}, None)
parse_reply('{"label": "spam",}', ["label"])     # (None, 'invalid JSON: Expecting property name enclosed in double quotes')
parse_reply('{"label": "spam"}', ["label", "score"])   # (None, "missing keys: ['score']")
parse_reply("I cannot answer that.", ["label"])  # (None, 'no JSON object found')
```

Parsing is only the first check. Then validate the content like any other input:

- **Types.** `"score": "0.9"` is a string. Check with `isinstance`, and remember `bool` is an `int`.
- **Allowed values.** A label must be in your set. Models invent new ones.
- **Ranges.** A probability must be between 0 and 1, and finite.

On failure the usual policy is a bounded retry: send the error text back to the model once or twice, then use a fallback value and count the failure.

To reduce failures at the source, ask for "only a JSON object with keys ...", give one example, and use the provider's structured-output mode when there is one. Still keep the parser.

## Common mistakes

- Calling `json.loads` on the raw reply with no `try`.
- Using `eval` on model output. It runs arbitrary code.
- Assuming a parsed reply is valid: missing keys, wrong types and invented labels all parse fine.
- A greedy first-to-last brace match when the reply holds two objects. Use `json.JSONDecoder().raw_decode` from the first `{` in that case.
- Forgetting that `json.loads` accepts `NaN` and `Infinity`, which then flow into your numbers.
- Retrying without a limit.

## See also

- [JSON: dumps, loads, sort_keys](#/kb/py-json)
- [Input validation and data contracts](#/kb/prod-input-validation)
- [Retries with backoff](#/kb/prod-retry-backoff)
- [Fallbacks and fallback chains](#/kb/prod-fallbacks)
