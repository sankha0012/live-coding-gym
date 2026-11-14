def title_case(s: str) -> str:
    return " ".join(w[:1].upper() + w[1:].lower() for w in s.split())
