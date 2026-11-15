from dataclasses import dataclass
@dataclass(frozen=True)
class Version:
    major: int
    minor: int
    patch: int
    def __lt__(self, o): return str(self) < str(o)
    def __gt__(self, o): return str(self) > str(o)
def sort_versions(versions):
    return sorted(versions)
