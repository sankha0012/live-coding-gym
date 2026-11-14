class ConfigError(Exception):
    def __init__(self, problems):
        self.problems = sorted(problems)
        super().__init__("; ".join(self.problems))


def parse_config(raw):
    problems, out = [], {}
    if not raw.get("name", "").strip():
        problems.append("name: missing")
    else:
        out["name"] = raw["name"].strip()
    try:
        out["port"] = int(raw.get("port", 8080))
        if not 1 <= out["port"] <= 65535:
            raise ValueError
    except ValueError:
        problems.append("port: invalid")
    out["debug"] = bool(raw.get("debug", False))
    try:
        out["timeout_s"] = float(raw.get("timeout_s", 5.0))
        if out["timeout_s"] <= 0:
            raise ValueError
    except ValueError:
        problems.append("timeout_s: invalid")
    out["tags"] = [t.strip() for t in raw.get("tags", "").split(",") if t.strip()]
    if problems:
        raise ConfigError(problems)
    return out
