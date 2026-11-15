import math


class ConfigError(Exception):
    def __init__(self, problems):
        self.problems = sorted(problems)
        super().__init__("; ".join(self.problems))


def _name(s):
    s = s.strip()
    if not s:
        raise ValueError(s)
    return s


def _port(s):
    v = int(s)
    if not 1 <= v <= 65535:
        raise ValueError(s)
    return v


def _bool(s):
    v = s.strip().lower()
    if v in ("true", "1"):
        return True
    if v in ("false", "0"):
        return False
    raise ValueError(s)


def _timeout(s):
    v = float(s)
    if not math.isfinite(v) or v <= 0:
        raise ValueError(s)
    return v


def _tags(s):
    return [t.strip().lower() for t in s.split(",") if t.strip()]


# key -> (parser, default); a default of None means required
_FIELDS = {
    "name": (_name, None),
    "port": (_port, 8080),
    "debug": (_bool, False),
    "timeout_s": (_timeout, 5.0),
    "tags": (_tags, []),
}


def parse_config(raw):
    out, problems = {}, []
    for key, (parse, default) in _FIELDS.items():
        if key not in raw:
            if default is None:
                problems.append(f"{key}: missing")
            else:
                out[key] = list(default) if isinstance(default, list) else default
            continue
        try:
            out[key] = parse(raw[key])
        except (ValueError, TypeError):
            problems.append(f"{key}: invalid")
    if problems:
        raise ConfigError(problems)
    return out
