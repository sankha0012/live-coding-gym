class ConfigError(Exception):
    def __init__(self, problems):
        self.problems = sorted(problems)
        super().__init__("; ".join(self.problems))


def parse_config(raw):
    problems = []
    name = raw.get("name", "").strip()
    if not name:
        problems.append("name: missing")
    try:
        port = int(raw.get("port", 8080))
    except ValueError:
        port = 8080
    debug = str(raw.get("debug", "false")).strip().lower() in ("true", "1")
    try:
        timeout_s = float(raw.get("timeout_s", 5.0))
    except ValueError:
        timeout_s = 5.0
    tags = [t.strip() for t in raw.get("tags", "").split(",") if t.strip()]
    if problems:
        raise ConfigError(problems)
    return {"name": name, "port": port, "debug": debug, "timeout_s": timeout_s, "tags": tags}
