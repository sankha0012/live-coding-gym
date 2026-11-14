class ConfigError(Exception):
    def __init__(self, problems):
        self.problems = sorted(problems)
        super().__init__("; ".join(self.problems))


def parse_config(raw):
    if "name" not in raw:
        raise ConfigError(["name: missing"])
    if not raw["name"].strip():
        raise ConfigError(["name: invalid"])
    out = {"name": raw["name"].strip()}
    try:
        out["port"] = int(raw.get("port", 8080))
        if not 1 <= out["port"] <= 65535:
            raise ValueError
    except ValueError:
        raise ConfigError(["port: invalid"])
    out["debug"] = str(raw.get("debug", "false")).strip().lower() in ("true", "1")
    out["timeout_s"] = float(raw.get("timeout_s", 5.0))
    out["tags"] = [t.strip() for t in raw.get("tags", "").split(",") if t.strip()]
    return out
